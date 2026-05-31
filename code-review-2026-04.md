# Code Review — 2026-04-22

**Reviewer:** Claude (Opus 4.7), autonomous session
**Corpus:** `paper_library/*.py` + top-level config (docker-compose.yml, grobid.yaml, env.example, pyproject.toml)
**Commit reviewed:** `4bfa473` on branch `claude`
**Purpose:** Adversarial pass to surface bugs, design smells, and operational gaps before v0.2.6 implementation work begins. Findings triaged for downstream action.

---

## Severity Legend

| Severity | Meaning | Action |
|---|---|---|
| **H — definite bug** | Code is wrong; a test would catch it | File an issue, suggest fix |
| **M — almost-certainly-wrong** | 90%+ confidence, want human concurrence | File an issue, flag for review |
| **L — worth reconsidering** | Legit design case exists, but alternative has merit | Stays in this doc, no issue |
| **nit** | Style, naming, minor polish | Stays in this doc, no issue |

## Axes Surveyed

1. **Correctness** — silent failures, off-by-ones, misused APIs
2. **Error handling** — what happens at each boundary; which failures are user-visible
3. **Design coherence** — coupling, abstraction fit, pattern consistency
4. **Operational** — timeouts, retries, idempotence, resource leaks, logging, cost
5. **Interface contracts** — Pydantic constraints, public/private boundaries, doc drift
6. **Security** — credentials, URL/XML/HTML trust, path traversal
7. **Dead code / cruft**
8. **Performance** — only where obvious + material

---

## Executive Summary

**Overall health:** Solid. No architectural rot, no abandoned subsystems, no security disasters. The pipeline does what it says. Most findings are edge-case handling (what happens when the happy path breaks?) rather than "the code is wrong."

**Corpus:** 14 Python modules (~4,700 lines) + docker-compose.yml + grobid.yaml + env.example + pyproject.toml.

**Severity distribution:**
- **1 H (definite bug, ships broken output):** mojibake bullet character in article byline
- **~16 M (almost-certainly-wrong, will file):** data-loss pair in state persistence, silent wrong-data fallbacks (year, date, source type), filename timestamping breaks dedup, HEAD+GET redundancy, acronym destruction in titles, version drift, corrupt-cache startup crash, ToS-violating fake email, HTTP-not-HTTPS arXiv API, author-name parsing fragility, strict-required-fields overrejection, stub-metadata magic defaults
- **~15 L (worth reconsidering, doc-only):** mostly design/refactoring opportunities and dead code
- **~12 nits:** style, version strings, leftover imports (most covered by a single ruff pass)

**Load-bearing finding** — the interaction between M4 (non-atomic state write) and M5 (corrupt state → silent empty reset) is a **data-loss pair**. Either bug alone is survivable; together they let an interrupted batch write destroy the entire processed-papers record without visible error, causing hundreds of dollars of silent re-ingestion on the next run. Top priority fix.

**Top three findings (so you don't have to open the doc for the headline):**

1. **H35** — `markdown_writer.py:237` contains `â€¢` (literal mojibake bytes) instead of `•` (bullet). Every article note with a published_date renders with broken mojibake in the byline. One-character fix + regression test.
2. **M4 + M5 pair** — `state.py` can silently lose the entire processing-state record if a write is interrupted and the next load encounters corrupt JSON. Reset to empty state with only a `WARNING` log. Fix: atomic write + backup-on-corrupt.
3. **M17 + M21 + M1** — three independent "silent fall back to wrong value instead of None or raise" bugs. Pattern: errors are recovered by lying. Papers get tagged with today's date, unknown sources vanish from dedup tracking, years default to current-year.

**Good news (things I went looking for and didn't find):**

- No credential logging / API key leaking paths
- No obvious SQL/command injection surfaces (no SQL; no shell-out to user-provided strings)
- No path-traversal surface (all filenames go through sanitization before vault writes)
- XML parsing uses `lxml` with `fromstring` (not `parse`) and no XXE surfaces I could find — external entity expansion is off by default in lxml
- No catastrophic coupling; modules have clear seams at network/disk boundaries
- No dead subsystems (one dead class `WaybackArchiveHelper`, one unused convenience function)

---

## File-by-File Findings

### `paper_library/__init__.py` (39 lines) — clean

Nothing to flag. `__version__ = "0.2.5"` matches current ship state. Exports are minimal and appropriate.

---

### `paper_library/models.py` (248 lines)

**M1 — Silent no-op in `ProcessingState.mark_processed`** (lines 229–237)

```python
def mark_processed(self, identifier: str, source: str) -> None:
    if source == "arxiv":
        ...
    elif source == "doi":
        ...
    elif source == "web":
        ...
    # else: silently does nothing, no raise, no log
    self.last_updated = datetime.now()
```

If `source` is anything other than `"arxiv"/"doi"/"web"` (e.g., typo, new source type added to the fetcher but not the state layer), the call succeeds silently but the identifier is never recorded. Future runs will re-process the same paper. `orchestrator._get_source_type()` can return `"unknown"` for some inputs — those land here and vanish.

**Fix:** raise `ValueError(f"Unknown source: {source}")` or at minimum `logger.warning(...)` when no branch matches.

**L2 — Stale `Synthesis.model_used` default** (line 180): default is `"claude-haiku-20250514"` (the old `claude-3-5-haiku` ID), but the actual shipping model is `"claude-haiku-4-5"` (see `synthesis_generator.MODEL`). The real usage path sets this explicitly, so it only affects tests / hand-constructed Synthesis objects. Cosmetic but worth a one-line fix.

**L3 — Asymmetric inheritance:** `PaperMetadata` extends `BibliographicEntry` but `ArticleMetadata` doesn't. Design intent is clear (articles have `url`, not `doi`; no bibliography), but it undermines the stated design goal of "consistent metadata extraction" in the BibliographicEntry docstring. Not a bug; consider noting in the model's docstring why they diverge.

**nit:** `ProcessingState` has no `unmark_processed` / reset methods. `--force` at the orchestrator level bypasses the dedup check but doesn't clean up state. Irrelevant for current use; would matter if an "undo last ingest" feature is ever wanted.

---

### `paper_library/state.py` (173 lines)

**M4 — Non-atomic state write** (line 125)

```python
self.state_file.write_text(json.dumps(data, indent=2))
```

`Path.write_text` truncates and writes in one step. If the process is killed mid-write (rare but possible — Ctrl-C, OOM, container stop mid-batch), the file can end up empty or half-written. Every subsequent run starts from empty state because `_load_state` silently falls back on parse failure (see M5 below). Combined, these two bugs are a **data-loss pair**.

**Fix:** write to `state_file.with_suffix(".tmp")`, then `os.replace()` to the real name. Standard atomic-write idiom.

**M5 — Corrupt state file silently reverts to empty state** (lines 91–95)

```python
except Exception as e:
    logger.warning("could_not_load_state_file", error=str(e))
    logger.info("starting_with_empty_state")
    self._state = ProcessingState()
```

On any JSON parse failure, the code starts fresh. A user with a 500-paper state file that becomes corrupt for any reason (see M4 for how) gets silently reset — subsequent `alcanzai batch` runs will reprocess every paper. The cost: silently burning hundreds of dollars in API calls while the vault fills with duplicate notes.

**Fix:** backup the corrupt file to `state_file.with_suffix(".corrupt.<timestamp>")` before starting empty, and log at `ERROR` (not `WARNING`).

**L6 — `StateManager.load()` is hardcoded to `config.processing_state_file`** (line 61): the classmethod takes no args. Makes it harder to write tests or to use alternate state files. Minor coupling issue.

**L7 — `mark_processed`/`mark_failed` save on every call** (lines 145–153): every single paper triggers a full-state JSON write. For a 39-paper batch that's 39 writes of increasingly large JSON. Not a performance problem at current scale but worth noting if batches grow.

**L8 — No concurrency guard:** two simultaneous `alcanzai ingest` processes race; last-writer-wins, loses intermediate changes. Single-user CLI usage, so low risk. File-locking (fcntl on Linux/macOS) would close it.

---

### `paper_library/skills_manager.py` (193 lines)

**M9 — Corrupt `skills/skill_ids.json` crashes startup** (lines 61–64)

```python
def _load_cached_ids(self) -> None:
    if SKILL_IDS_FILE.exists():
        with open(SKILL_IDS_FILE) as f:
            self._skill_ids = json.load(f)
```

No try/except. If the cache file is corrupt (interrupted write, disk issue, manual mis-edit), `SkillsManager.__init__()` raises `json.JSONDecodeError` and the entire CLI dies — every command, not just synthesis. An `alcanzai validate` run can't even tell the user what went wrong.

**Fix:** wrap in try/except, log warning, start with empty `_skill_ids`. Skills will be re-uploaded on first use, which is the correct degradation path.

**L10 — Cache never verifies skill exists server-side:** if a skill is deleted/expired on Anthropic's side, the cached ID becomes stale. Next synthesis call fails with an API error, not a clear message. Could add `/skills/{id}` GET check on startup, but it's a cost/latency tradeoff. File as a known-gap note.

**L11 — Upload and cache-save not atomic:** `upload_skill` does `self.client.beta.skills.create(...)` then `self._save_cached_ids()`. If the save fails (disk full, permission error), we've paid for an upload that isn't recorded. Next run re-uploads. Minor cost exposure.

**nit:** `SKILL_NAMES` list (line 31) can drift from actual contents of `skills/` directory. No test verifies the two stay in sync. Consider deriving from `skills_dir.iterdir()` at module load.

---

### `paper_library/arxiv_fetcher.py` (396 lines)

**M12 — arXiv API uses plain HTTP** (line 49)

```python
API_BASE = "http://export.arxiv.org/api/query"
```

arXiv supports HTTPS. Using plain HTTP allows passive-MITM attackers to see what the user is researching and (more seriously) to silently modify paper metadata mid-flight. No real attacker scenario for a homelab user, but it's a free security improvement — change to `https://`.

Note `PDF_BASE = "https://arxiv.org/pdf"` is already HTTPS; only the API URL is HTTP. Inconsistent.

**M13 — Author name parsing breaks on compound surnames / honorifics / suffixes** (lines 271–306)

```python
# arXiv names are typically "Firstname Lastname"
name_parts = name.split()
if len(name_parts) >= 2:
    surname = name_parts[-1]
    forenames = " ".join(name_parts[:-1])
    formatted = f"{surname}, {forenames}"
```

Breaks on:
- `"Ludwig van Beethoven"` → `"Beethoven, Ludwig van"` ✓ (works)
- `"John Smith Jr."` → `"Jr., John Smith"` ✗ (treats "Jr." as surname)
- `"Dr. Jane Doe"` → `"Doe, Dr. Jane"` ✗ (leaves honorific in forenames)
- Names with particles like `"van der Waals"` → `"Waals, van der"` (debatable — depends on linguistic convention)

The arXiv test corpus has names like "Kaiser, Łukasz" that work, but even "Geoffrey E Hinton" would yield "Hinton, Geoffrey E" (marginal). Fix is non-trivial (requires a real name-parsing library like `nameparser`), but at least document the known-failure modes.

**Fix:** adopt `python-nameparser`, or normalize against a curated suffix list (`Jr.`, `Sr.`, `III`, etc.).

**M14 — Cached PDF not verified** (lines 354–357)

```python
if pdf_path.exists():
    logger.info("pdf_already_exists", filename=pdf_filename)
    return pdf_path
```

If a previous download was interrupted mid-write (process killed, OOM during `iter_content` loop), the partial file stays on disk. Next run skips re-download, passes the corrupt PDF to GROBID, which then fails or extracts garbage.

**Fix:** verify the file starts with `%PDF` magic bytes (cheap check) and/or has a plausible size before trusting the cache.

**L15 — `fetch_arxiv_paper` module-level convenience function (lines 383–395):** not called from anywhere in the codebase (orchestrator uses the `ArxivFetcher` class directly). Probably just legacy. Candidate for deletion.

**nit:** `raise ArxivError(...)` sometimes uses `from e`, sometimes doesn't. Minor exception-chaining inconsistency.

---

### `paper_library/doi_fetcher.py` (334 lines)

**M16 — Unpaywall called with placeholder email when none configured** (lines 265–283)

```python
def _fetch_unpaywall(self, doi: str) -> Optional[str]:
    email = self.email or "research@example.com"
    ...
```

Unpaywall's [API terms](https://unpaywall.org/products/api) require a real email address for identification and rate-limiting. `"research@example.com"` is obviously fake; Unpaywall could rate-limit or ban it (it's almost certainly been used by other tools too). This is both an ethical issue (abusing the polite-pool contract) and an operational risk (getting banned).

**Fix:** if `self.email` is None, either skip Unpaywall entirely and go straight to Semantic Scholar, or raise a config error. Do not send `example.com`.

**M17 — Silent year fallback to current year** (line 243)

```python
return PaperMetadata(
    ...
    year=year or datetime.now().year,
    ...
)
```

If year extraction from Crossref's `published-print` / `published-online` / `issued` all fail, the paper is tagged with the **current calendar year**. A 1987 paper with missing Crossref date fields becomes "2026 paper" in the vault, with filename `Author et al (2026) - Title` and YAML `year: 2026`. Silently wrong, hard to detect later, breaks dedup-by-year.

**Fix:** return `year=None` and let downstream code (markdown writer, filename) handle missing year explicitly. Or raise `DoiFetchError("could not determine year")`.

**L18 — User-Agent version drift** (line 54): `"User-Agent": "alcanzai/1.0"` hardcoded. Actual version is `0.2.5`. Use `from paper_library import __version__`.

**L19 — `_find_oa_pdf_url` dead in module but used in tests:** defined at line 258, but `fetch()` inlines the same logic directly. Tests import and use it. Either call it from `fetch()` to deduplicate, or inline it in tests and delete.

**L20 — DOI filename collision theoretical:** `safe_doi = re.sub(r"[^\w.-]", "_", doi)[:60]`. DOIs ≥60 chars with a long common prefix could collide. Vanishingly unlikely in practice; worth a note.

---

### `paper_library/web_fetcher.py` (880 lines)

**M21 — `_handle_pdf_from_url` sets `published_date=datetime.now()`** (line 322)

```python
metadata = ArticleMetadata(
    title="PDF from URL",
    authors=["Unknown"],
    url=url,
    published_date=datetime.now(),  # <-- silent fallback to today
    ...
)
```

Same class of bug as M17: a PDF found at a URL gets tagged as published today. When the orchestrator's `_process_article` / GROBID path takes over, the true date is extracted from PDF metadata and overwrites this. But if GROBID extraction fails silently or the PDF goes through the `doi_only` / `article` path, today's date lands in the note.

**Fix:** pass `published_date=None`. Pydantic accepts it (field is Optional).

**M22 — Filename timestamping prevents PDF dedup across `--force`** (lines 793–818)

```python
def _generate_pdf_filename_from_url(self, url: str) -> str:
    ...
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"web_{domain}_{slug}_{timestamp}.pdf"
```

Every `--force` reprocess of the same URL creates a new PDF file with a unique timestamp. The old PDF isn't deleted. Over time, `vault/PDFs/` accumulates near-duplicates. Also, the source note and paper note on second-run will point to the new filename, orphaning the old one.

**Fix:** drop the timestamp. If uniqueness is really needed for edge cases, hash the URL. Most straightforward fix: `web_{domain}_{slug}.pdf` — same URL → same filename → same file is overwritten (or skipped if the cache-verify check from M14 is added here too).

**M23 — Redundant HEAD + GET on every web fetch** (lines 232–266)

```python
head_response = requests.head(url, ...)
content_type = head_response.headers.get('content-type', 'text/html').lower()
if 'application/pdf' in content_type:
    get_response = requests.get(url, ...)  # ← second request
    ...
else:
    get_response = requests.get(url, ...)  # ← second request, different path
```

Every HTML fetch is 2 roundtrips (HEAD + GET). Every PDF fetch is also 2 roundtrips (HEAD + GET). This doubles latency and request count for no benefit — the content-type header is available on the GET response too.

Also: **if HEAD returns one content-type but GET returns another** (server redirects, type sniffing, etc.), the code treats the response as what HEAD said. Possible misparse.

**Fix:** single GET with `stream=True`, check `response.headers['content-type']`, read body only if needed.

**L24 — Mozilla-impersonating User-Agent** (line 100):
```python
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
```
Pretending to be Chrome on Windows is a gray-area ToS thing. For a personal tool it's probably fine, but a real UA like `"alcanzai/0.2.5 (+https://github.com/cyrusae/alcanzai)"` is more honest and arguably no worse at bypassing scraper blocks (the blocks that matter tend to check cookies/JS, not UA).

**L25 — `common_containers` selector too loose** (line 667): `{'class': 'content'}` matches literally any element with class="content", which on some sites is the sidebar or footer. Consider more specific selectors or requiring the match to also be a `<main>` / `<div>` with minimum text length.

**L26 — `WaybackArchiveHelper` is dead code** (lines 834–879): declared but never imported or used anywhere in the codebase. Either integrate (original v0.2 plan per the class docstring) or delete.

**L27 — UNSUPPORTED_HOSTS uses `endswith` with www-stripping** (line 181): `hostname.endswith('x.com')` blocks anything ending in `x.com` — including e.g. `mx.com` (a bank, not Twitter). Narrow false-positive surface but possible. Consider exact hostname match against a set.

---

### `paper_library/grobid_processor.py` (932 lines)

**M28 — Acronym destruction in title case-fixing** (lines 319–325)

```python
if title.isupper() or sum(1 for c in title if c.isupper()) > len([c for c in title if c.isalpha()]) * 0.5:
    title = title.title()
```

Titles like `"NLP Benchmarks: A Study of BERT, GPT, and LLaMA"` trigger the >50%-uppercase branch (counted by alpha char, not word) because the acronyms push the ratio past 50%. `.title()` then mangles: `"Nlp Benchmarks: A Study Of Bert, Gpt, And Llama"`. Observably worse than leaving it.

**Fix:** only apply title case if `title.isupper()` is true (no mixed-case words). Alternatively, apply only to words that are fully uppercase AND longer than some threshold (to protect acronyms of reasonable length). A real fix needs some domain-aware acronym protection.

**M29 — Strict required-fields check rejects valid papers** (lines 227–230)

```python
if not title or not authors or not year:
    raise GrobidError(
        "Could not extract required fields (title, authors, year) from GROBID output"
    )
```

Some legitimate PDFs don't have a publication year in their metadata — preprints without a date header, working papers, institutional technical reports. GROBID can't extract what isn't there. Failing hard means these papers can never be ingested; a softer approach (warn + use year=None or a detected-from-filename fallback) would handle more real documents.

**Fix:** relax the check. Require title + at least one author. Year can be None with a warning logged.

**L30 — `_calculate_garbage_score` is 175 lines of magic-number heuristics with no unit tests** (lines 582–757): already noted in the test audit. Worth breaking out to its own module with independent testing. Current structure is hard to modify safely.

**L31 — Trusted-venue keyword substring matching** (lines 742–747): `any(keyword in citation.venue.lower() for keyword in trusted_venue_keywords)` — `"linguistics"` in `"Unreliable Linguistics Newsletter"` would match. Real false-positive surface in humanities venues. Consider exact-word matching or a curated allowlist.

**L32 — Three `import re` inside functions** (lines 299, 607, 833): re is already used throughout; should be imported once at module top. `ruff` would flag this with `isort`/`PLC0415`.

**nit:** garbage threshold `60` is a magic number inlined at the filter site (line 914). Make it a class constant.

---

### `paper_library/citation_context.py` (320 lines)

**L33 — `_extract_char_context` fabricates sentence terminator** (lines 215–216)

```python
if not context.endswith(('.', '!', '?')):
    context += '.'
```

If the extracted context doesn't end at a sentence boundary (e.g., citation appears mid-phrase, or at end of truncated text), the code **appends a fake period**. This produces misleading output — the synthesis model sees `"The model in [3]."` when the real text was `"The model in [3], processed at..."`. Low harm but factually incorrect.

**Fix:** either truncate to the previous real sentence boundary, or leave the context as-is without fabrication. Honest is better than tidy.

**L34 — Bibliography marker list** (lines 227–233): hardcoded six patterns. Doesn't cover "Works Consulted", "Literatur" (German papers), or unusual formatting like double-spaced or numbered section headers. Also the 50%-of-text threshold is hardcoded. Both already noted in the test audit (B6).

**nit:** `dataclasses.field` imported but unused (line 17). Ruff F401.

**Overall this file is clean and well-designed.** The numeric-citation logic with `\b` word boundary to prevent `[30]` matching `[3]` is a nice detail.

---

### `paper_library/markdown_writer.py` (701 lines)

**H35 — Mojibake in article byline** (line 237) — **DEFINITE BUG**

```python
sections.append(f" â€¢ {metadata.published_date.strftime('%Y-%m-%d')}")
```

The characters `â€¢` are the classic mojibake pattern: the real bullet character `•` (U+2022, UTF-8 bytes `E2 80 A2`) got interpreted as three Windows-1252 characters (`â`, `€`, `•`) and then saved as those three code points in the source file. Running this code literally outputs `â€¢` in article notes, not a bullet.

**Verify:** grep `vault/Articles/` for any recently-generated articles; look for `â€¢` in bylines of articles that had `published_date` set.

**Fix:** change `" â€¢ "` to `" • "`. One-character fix, but should be committed with a regression test that asserts the rendered byline contains the real bullet character.

**L36 — YAML title escaping is minimal** (line 298): only handles `"` → `\"`. Titles containing `:`, leading `-`, leading `!`, or newlines aren't escaped. YAML is finicky; these could produce malformed frontmatter that Obsidian's parser rejects silently.

**Fix:** use a real YAML serializer (`yaml.safe_dump`) instead of hand-rolled string concatenation. Test audit B2 already flagged this as a coverage gap.

**L37 — `_format_citation_full` raw-text regex hacks** (lines 571–577): specific-case regex to fix `"JimmyLei Ba"` → `"Jimmy Lei Ba"` and `"ar Xiv"` → `"arXiv"`. These are targeted fixes for known-bad GROBID outputs. Unclear whether they cover all concatenation cases; might want a more general "insert space before consecutive capitals after a capital" rule. Low priority cleanup.

**F541** (line 155): `sections.append(f"")` — empty f-string. Ruff fix.

**nit:** `type: "paper"` / `type: "article"` in YAML frontmatter are stringly-typed. Pydantic enum would prevent drift.

---

### `paper_library/batch_process.py` (100 lines)

**M38 — Duplicated shebang** (lines 1–2)

```python
#!/usr/bin/env python3
#!/usr/bin/env python3
```

Harmless but obviously a copy-paste accident. Delete line 2.

**L39 — Functionally redundant with `cli.py batch`** (entire file): `batch_process.batch_process()` and `cli.batch()` do the same thing — read identifiers from a file, process them. The CLI version uses Click (structured output, consistent logging); this one uses `print()`. Two code paths for the same feature, drifted in style.

**Fix:** pick one. My lean: delete `batch_process.py`; the CLI version is the canonical entry. If there's a reason the standalone file exists (legacy scripts in some automation?), document it. The test `tests/test_pipeline.py` *doesn't* depend on it, so deletion is low-risk.

**Ruff F541** (lines 66, 78, 85): three unnecessary f-strings. Auto-fixable.

**L40 — Still using `print()`** (throughout): violates the v0.2.5 convention of structlog everywhere (per `discussions/ab - telemetry.md`). Related to L39 — if the file is deleted, this goes away too.

---

### `paper_library/cli.py` (148 lines)

Mostly clean; Click handles a lot of correctness for free.

**L41 — `validate` command creates the vault directory** (lines 131–134)

```python
if config.vault_path.exists():
    click.secho(f"✓ Vault directory exists: {config.vault_path}", fg="green")
else:
    click.secho(f"  Creating vault directory at {config.vault_path}", fg="yellow")
    config.vault_path.mkdir(parents=True, exist_ok=True)
    click.secho(f"✓ Vault directory created", fg="green")
```

`validate` is named as a *check*, but this branch **creates state as a side effect**. If the user runs `alcanzai validate` against a mistyped `VAULT_PATH` (say, `/Users/watc/GitHere/alcanzai/vault` instead of `/Users/watcher/...`), the tool silently creates an empty vault at the wrong path and reports success. No way to distinguish "valid" from "valid because I made it so."

**Fix:** `validate` should only *check*. Add a separate `alcanzai init` command (or a `validate --create` flag) for the create-if-missing behavior.

**F401** (line 12): `pathlib.Path` imported unused. Auto-fixable.

**F541** (lines 87, 134): two f-strings without placeholders. Auto-fixable.

**nit:** `stats` command outputs `failed` count only if non-zero, hiding the failed-list entirely. `alcanzai stats --verbose` with the failed list would be useful for debugging.

---

### `paper_library/orchestrator.py` (already reviewed during telemetry pass)

Most issues already flagged:
- F401 unused imports (`Optional, Union`)
- Stub `PaperMetadata` magic values for local PDFs (`title="[Title will be extracted from PDF]"`, `year=2024`) — see M42 below
- Mixed span-attribute-setting pattern (covered by audit B4)

**M42 — Stub-metadata magic defaults** (lines 257–265, 281–287)

```python
metadata = PaperMetadata(
    title="[Title will be extracted from PDF]",
    authors=["Unknown"],
    year=2024,  # ← hardcoded, will drift
    ...
)
```

Local-PDF and PDF-from-URL paths construct a PaperMetadata with placeholder values, expecting GROBID to overwrite them via `_merge_metadata()`. Problems:
1. `year=2024` is a hardcoded literal. This year's paper will be tagged 2024 if GROBID can't extract a year (see M29 — the strict check would prevent the stub from surviving, but if that's relaxed, this lands in the vault).
2. The magic strings `"[Title will be extracted from PDF]"` and `"Unknown"` could accidentally survive if `_merge_metadata` has a bug or GROBID returns None-equivalents that happen to be truthy in the merge.
3. `datetime.now().year` would at least be self-correcting; better would be None, with the merge logic guaranteeing replacement.

**Fix:** either make title/authors/year Optional on PaperMetadata (breaking change) and pass None here, or at least use `datetime.now().year` instead of `2024`.

---

### `paper_library/telemetry.py`, `token_utils.py`, `synthesis_generator.py`

All reviewed during the telemetry reacquaint session; findings already captured in issues #6 and #7. Not repeated here.

---

### `docker-compose.yml` + `grobid.yaml` + `env.example` + `pyproject.toml`

Reviewed. Nothing H/M; all reasonable for their purpose. Notes:

- **docker-compose.yml:** memory limit 8G may be high for modest homelab nodes; could note in README. CouchDB block is commented-out aspirational config; fine.
- **grobid.yaml:** All-wapiti forcing + `modelPreload: false` is the correct workaround for Apple Silicon; design rationale is captured in comments. Clean.
- **env.example:** two `# TODO:` comments inside the file ("Self-host GROBID properly", "Sync vault") — stale project notes in user-facing env template. Move to `docs/` or a TODO list. **nit.**
- **pyproject.toml:** `version = "0.1.0"` in `[project]` (line 3) is **out of sync with `paper_library/__init__.py` which says `0.2.5`**. Pip-installable metadata will report the wrong version.

**M43 — `pyproject.toml` version drift** (line 3): should be `"0.2.5"` to match `__version__`. Both places need to update in lockstep for each release. Consider sourcing from a single place (e.g., `setuptools-scm` from git tags, or a single VERSION file imported by both).

---

## Cross-Cutting Observations

### 1. The "silent data lie" pattern

The same anti-pattern recurs across modules: **on error, silently fall back to a wrong value instead of raising or returning None.** Specific instances:

| Where | What falls back | To what |
|---|---|---|
| `doi_fetcher._parse_crossref` (M17) | missing year | `datetime.now().year` |
| `web_fetcher._handle_pdf_from_url` (M21) | missing publication date | `datetime.now()` |
| `models.ProcessingState.mark_processed` (M1) | unknown source | no-op (identifier vanishes) |
| `state._load_state` (M5) | corrupt JSON | empty state |
| `arxiv_fetcher._download_pdf` (M14) | corrupt cached PDF | treated as valid |

All five are variations on the same judgment call: **"if we don't know, assume X"**. The right answer in every case is either **raise** (orchestrator-level recovery) or **return None and let the caller decide** (explicit opt-in to fallback behavior). Never silently fabricate.

This is worth addressing as a **principle** rather than issue-by-issue — maybe a one-paragraph "Error handling policy" section in a future CONTRIBUTING.md.

### 2. Non-atomic file writes

Both persistent-state writes (state.py M4, implicitly skills_manager M9 failure mode) use `Path.write_text(...)` which truncates-then-writes non-atomically. Standard fix is tmp-file + `os.replace`. Consider a shared `atomic_write(path, content)` helper in `paper_library/_io.py` or similar.

### 3. Version string is stored in four places

| Where | Value |
|---|---|
| `paper_library/__init__.py` `__version__` | `"0.2.5"` |
| `pyproject.toml` `[project].version` | `"0.1.0"` |
| `doi_fetcher.HEADERS` User-Agent | `"alcanzai/1.0"` |
| commit message for the telemetry ship | "v0.2.5" |

Three different values. Classic DRY violation. Candidate fixes:
- **Most rigorous:** `setuptools-scm` driving version from git tags; both Python and package metadata read from there
- **Simplest:** keep `__init__.py` as source of truth; `pyproject.toml` uses `dynamic = ["version"]` with a setuptools plugin; User-Agent imports `from paper_library import __version__`
- **CI check:** a test that asserts all three match

Either way: fix to one value before v0.3.0.

### 4. Name parsing lives in at least three places

- `arxiv_fetcher._extract_authors` — splits on whitespace, last word = surname
- `grobid_processor._extract_authors` — uses TEI `<forename>/<surname>` elements (correct by construction)
- `markdown_writer._format_authors_short` + `_format_citation_wikilink` + `_format_citation_full` — all interpret "Lastname, Firstname" from earlier modules

Inconsistent parsing rules for the same information. Consolidating into a `paper_library/names.py` module with a single `Person`/`AuthorName` type would:
- Make the "Lastname, Firstname" contract explicit
- Give one place to fix the known-failure cases (van, Jr., Dr., Łukasz)
- Enable `python-nameparser` integration at a single seam

### 5. Magic numbers and hardcoded thresholds

Scattered constants that a humanities-collection ingest might want to tune:

| Constant | Where | Current |
|---|---|---|
| Garbage citation threshold | `grobid_processor._extract_citations` | `60` |
| Context sentences | `CitationContextExtractor(context_sentences=2)` | `2` |
| Min web article length | `WebFetcher.MIN_CONTENT_LENGTH` | `500` |
| Max web article length | `WebFetcher.MAX_CONTENT_LENGTH` | `500_000` |
| Bibliography-detection text-position cutoff | `citation_context._remove_bibliography` | `0.5` (first half ignored) |
| Local-PDF stub year | `orchestrator._fetch_paper` | `2024` |
| Title case >50% uppercase trigger | `grobid_processor._clean_title` | `0.5` |

Some are already `Config` fields (`SYNTHESIS_TOKEN_BUDGET`) — that pattern scales.

### 6. `print()` vs `structlog` inconsistency

The v0.2.5 commit message said "All print() calls replaced with structlog across orchestrator, fetchers, grobid_processor, synthesis_generator, skills_manager, citation_context, markdown_writer, state." But `batch_process.py` still uses `print()` throughout. Either batch_process was missed in the sweep, or (more likely) the file is effectively abandoned in favor of `cli.py batch` and was not worth converting. Either way: L39 covers deletion.

### 7. Dead code / legacy

- `arxiv_fetcher.fetch_arxiv_paper` (convenience function, unused)
- `doi_fetcher._find_oa_pdf_url` (defined, inlined in caller)
- `web_fetcher.WaybackArchiveHelper` (declared, never imported)
- `batch_process.py` (redundant with `cli.batch`)
- `tests/legacy/` (already scheduled for deletion per test audit A1)

Total ~150 lines of dead code. A single "cleanup" PR removing all of it would be low-risk and satisfying.

### 8. Ruff findings

14 items, 13 auto-fixable. Listing here because they're a one-commit cleanup:

| Code | File | Count |
|---|---|---|
| F401 unused imports | arxiv_fetcher, doi_fetcher, citation_context, cli, orchestrator | 6 |
| F541 f-string no placeholders | batch_process, cli, markdown_writer, web_fetcher | 7 |
| E402 import not at top | web_fetcher | 1 |

Single `ruff check --fix paper_library/` handles all 13 auto-fixable. The E402 is intentional (BeautifulSoup try/except import), but can be restructured or `# noqa`-marked.

---

## Recommended Action Queue

Each item below maps to **one small GitHub issue** per your preference. Filed under a new epic `[EPIC] Code review 2026-04 followups`. H and M both file; L stays in this doc.

Items are grouped by severity, then ordered within each group by causal dependency and blast radius.

### H-priority (1 issue)

#### R1. Fix mojibake bullet in article byline — **H35**
- **File:** `paper_library/markdown_writer.py:237`
- **Change:** `" â€¢ "` → `" • "` (three characters → one)
- **Test:** assert that `article_to_markdown()` output contains `U+2022` (•) when `published_date` is set
- **Blast radius:** every article note with a published_date is affected; existing notes may need regeneration
- **Commit message:** `Fix mojibake bullet in article byline`

### M-priority (~16 issues, roughly ordered by blast radius)

#### R2. Atomic state write + backup-on-corrupt — **M4 + M5 combined**
- **Files:** `paper_library/state.py:125` (save), `paper_library/state.py:91-95` (load)
- **Changes:**
  - `save()`: write to `state_file.with_suffix(".tmp")`, then `os.replace()` to the real name
  - `_load_state()`: on JSONDecodeError, copy corrupt file to `state_file.with_suffix(f".corrupt.{int(time.time())}")` before starting empty; log at `ERROR` not `WARNING`
- **Why combined:** these are the data-loss pair; landing them separately leaves the second half of the bug in place
- **Test:** unit test that kills mid-write and verifies state is still parseable after; unit test that a corrupt state file is backed up and then empty state is loaded
- **Commit message:** `Atomic state writes and corrupt-state backup`

#### R3. Remove current-year fallback for DOI year — **M17**
- **File:** `paper_library/doi_fetcher.py:243`
- **Change:** `year=year or datetime.now().year` → `year=year` (`PaperMetadata.year` is currently required, so also relax that — see R4)
- **Depends on:** R4 (relaxing required-year on PaperMetadata)
- **Commit message:** `Stop silently tagging missing-year DOIs with current year`

#### R4. Relax strict required-field check in GROBID — **M29**
- **File:** `paper_library/grobid_processor.py:227-230`
- **Change:** require title + authors; allow year=None with `logger.warning("missing_year_in_grobid_metadata", ...)`. Also update `PaperMetadata` to make `year` Optional (breaking change for existing tests — update in same PR).
- **Enables:** R3 (DOI year fallback removal)
- **Commit message:** `Relax GROBID required-fields: year is optional with warning`

#### R5. Remove current-date fallback for PDF-from-URL — **M21**
- **File:** `paper_library/web_fetcher.py:322`
- **Change:** `published_date=datetime.now()` → `published_date=None`
- **Test:** assert that `_handle_pdf_from_url` returns `metadata.published_date is None` when no date is provided
- **Commit message:** `Stop defaulting PDF-from-URL published_date to now()`

#### R6. Stabilize PDF-from-URL filenames — **M22**
- **File:** `paper_library/web_fetcher.py:793-818`
- **Change:** drop the `_{timestamp}` suffix; filename becomes `web_{domain}_{slug}.pdf`; repeat downloads overwrite or skip based on whether the cached file is valid (see R7)
- **Edge case to handle:** existing orphan PDFs in `vault/PDFs/` from old runs. Document in the commit that users may want to clean `vault/PDFs/web_*` before upgrading.
- **Commit message:** `Remove timestamp from PDF-from-URL filenames to enable dedup`

#### R7. Verify cached PDFs before trusting them — **M14**
- **Files:** `paper_library/arxiv_fetcher.py:354-357` (primary); same pattern applies to `doi_fetcher._download_pdf` and `web_fetcher._handle_pdf_from_url`
- **Change:** before returning a cached PDF, verify `pdf_path.read_bytes()[:4] == b"%PDF"` and `pdf_path.stat().st_size > MIN_PDF_SIZE` (say 1KB). On mismatch, delete the file and re-download.
- **Commit message:** `Verify cached PDFs before returning — catches interrupted downloads`

#### R8. Raise on unknown source in mark_processed — **M1**
- **File:** `paper_library/models.py:229-237`
- **Change:** add `else: raise ValueError(f"Unknown source: {source}. Expected one of 'arxiv', 'doi', 'web'.")`
- **Impact check before filing:** grep for callers with possible unknown `source` values; `orchestrator._get_source_type` returns `"unknown"` in a fallthrough path — this issue needs to either handle that or raise a clearer error upstream
- **Commit message:** `Raise on unknown source in ProcessingState.mark_processed`

#### R9. Fix Unpaywall email — **M16**
- **File:** `paper_library/doi_fetcher.py:267`
- **Change:** remove `"research@example.com"` fallback. If `self.email` is None, skip Unpaywall and log a warning; proceed directly to Semantic Scholar. Rationale comment in code.
- **Commit message:** `Don't call Unpaywall with fake email — skip if unconfigured`

#### R10. Use HTTPS for arXiv API — **M12**
- **File:** `paper_library/arxiv_fetcher.py:49`
- **Change:** `API_BASE = "http://export.arxiv.org/api/query"` → `"https://export.arxiv.org/api/query"`
- **Commit message:** `Use HTTPS for arXiv API`

#### R11. Unify version string across the project — **M43**
- **Files:** `pyproject.toml:3`, `paper_library/__init__.py:17`, `paper_library/doi_fetcher.py:54`
- **Change:** pick one source of truth. Easiest: set `pyproject.toml` to `"0.2.5"`, import `__version__` into the User-Agent. Long-term: consider `setuptools-scm` — track as a future issue if not this PR.
- **Test:** a simple import-time assertion that all three values match, or a CI check.
- **Commit message:** `Unify version string across __init__, pyproject, User-Agent`

#### R12. Fix corrupt-skills-cache startup crash — **M9**
- **File:** `paper_library/skills_manager.py:61-64`
- **Change:** wrap `json.load(f)` in try/except. On failure, log warning and start with empty `_skill_ids`; skills will re-upload on first use.
- **Commit message:** `Tolerate corrupt skills_ids.json — fall back to empty cache with warning`

#### R13. Eliminate HEAD+GET doubling — **M23**
- **File:** `paper_library/web_fetcher.py:232-280`
- **Change:** single GET with `stream=True`, check `response.headers['content-type']`, read full body only if HTML and within size limits
- **Test:** mock that HEAD is not called for a successful fetch
- **Commit message:** `Single GET instead of HEAD+GET for web fetches`

#### R14. Protect acronyms in title case-fixing — **M28**
- **File:** `paper_library/grobid_processor.py:319-325`
- **Change:** only apply `.title()` if `title.isupper()` is true (no mixed-case words). Delete the `>50%` branch — it's too aggressive for modern CS/ML paper titles.
- **Test:** assert that `"Deep Learning with BERT"` survives unchanged; `"DEEP LEARNING WITH BERT"` becomes `"Deep Learning With Bert"` (bert-lowercasing is a separate, harder problem).
- **Commit message:** `Stop title()-ing titles with mixed case — protects acronyms`

#### R15. Replace stub-metadata magic values — **M42**
- **File:** `paper_library/orchestrator.py:257-265, 281-287`
- **Change:** `year=2024` → `year=datetime.now().year` (minimum improvement); better: make PaperMetadata fields Optional so local-PDF path can pass None and require GROBID to populate them — landed together with R4
- **Commit message:** `Replace hardcoded stub year in local-PDF and PDF-from-URL paths`

#### R16. Name-parsing polish in arxiv_fetcher — **M13**
- **File:** `paper_library/arxiv_fetcher.py:271-306`
- **Change:** at minimum, normalize honorifics (Dr., Mr., Mrs., Ms., Prof.) and suffixes (Jr., Sr., III, II, IV) before deciding the surname. Longer-term: adopt `python-nameparser` at the `paper_library/names.py` seam (Cross-cutting #4).
- **Tests:** verify `"John Smith Jr."`, `"Dr. Jane Doe"`, `"Ludwig van Beethoven"` all produce sensible output
- **Commit message:** `Handle name suffixes and honorifics in arXiv author parsing`

#### R17. Scope-tighten `alcanzai validate` — **L41** *(promoted to M because of silent-wrong-path risk)*
- **File:** `paper_library/cli.py:131-134`
- **Change:** `validate` reports pass/fail without creating directories. Add `alcanzai init` for the create-if-missing side of things, or a `--create` flag on validate.
- **Commit message:** `alcanzai validate no longer silently creates the vault`

### The one-shot cleanup issue

#### R18. Ruff auto-fixes + dead code removal — **bundled nits + L15/L19/L26/L39**
- **Files:** 8 modules across `paper_library/`, plus dead code
- **Changes:**
  1. `ruff check --fix paper_library/` (13 auto-fixable items)
  2. Hand-fix E402 in web_fetcher.py:45 (restructure BeautifulSoup import)
  3. Delete `arxiv_fetcher.fetch_arxiv_paper` (L15)
  4. Delete `web_fetcher.WaybackArchiveHelper` (L26)
  5. Either delete `doi_fetcher._find_oa_pdf_url` (L19) or use it inside `fetch()` to deduplicate
  6. Delete `paper_library/batch_process.py` (L39) — CLI subsumes it; verify no external automation depends on it first
- **Commit message:** `Clean up: ruff fixes, dead code removal, consolidate batch entry`

### L-items that stay in this doc (not filed)

L2 (stale model_used default), L3 (ArticleMetadata inheritance), L6 (StateManager coupling), L7 (per-call saves), L8 (no concurrency guard), L10 (skill cache freshness), L11 (skill upload atomicity), L18 (done via R11), L20 (DOI filename collision), L24 (Mozilla UA), L25 (common_containers too loose), L27 (UNSUPPORTED_HOSTS endswith), L30 (garbage score module), L31 (venue substring), L32 (done via R18), L33 (fabricated period), L34 (bibliography markers), L36 (YAML escaping → covered by test audit B2), L37 (citation raw-text regex), L40 (done via R18), and all nits.

These are worth reconsidering but don't meet the filing threshold. If any become load-bearing for a specific future change, promote to M and file at that time.

---

## Open Questions

Items that need a human judgment before Gemini can act.

1. **`batch_process.py`: keep or delete?** (R18 / L39) The file is redundant with `cli.py batch`. Delete-path is my lean — but before doing so, please confirm no external automation (shell scripts, cron jobs, shortcuts in your notes) depends on `python batch_process.py papers.txt`. If anything does, just fix it in place (convert to structlog, fix ruff nits).

2. **YAML frontmatter: invest in `yaml.safe_dump` or keep hand-rolled?** (L36 + test audit B2) Moving to `yaml.safe_dump` for all frontmatter generation is safer but produces slightly different whitespace/quoting than the current hand-rolled version. Obsidian parses both fine, but existing notes would "diff noisy" against newly-generated ones. Worth doing, but picks an opportunity.

3. **Name parsing: invest in `python-nameparser`?** (Cross-cutting #4, M13, R16) The library is mature (~5M downloads/year) and handles the edge cases I flagged. Adds one dependency for meaningful correctness improvement. Worth doing before the humanities-collection batch (19th-century authors with titles and suffixes will exercise this hard).

4. **Version management strategy?** (Cross-cutting #3, M43, R11) Three options:
   - Quick fix: single source (`__init__.__version__`), static assertion test
   - Medium: `pyproject.toml` `dynamic = ["version"]` with a setuptools plugin reading from `__init__.py`
   - Rigorous: `setuptools-scm` driving version from git tags
   
   My lean: **quick fix for R11, defer the bigger decision** until there's a reason (CI/CD release automation).

5. **Error handling policy document?** (Cross-cutting #1) Several findings cluster around "silently lie vs raise/None". Would be worth writing down the policy ("prefer None over fake values; raise at orchestrator boundaries; log at ERROR when falling back") so future contributors (human or agent) have a reference. Could live in CONTRIBUTING.md or a short `docs/error-handling.md`.

6. **Tune-able magic numbers: move to Config?** (Cross-cutting #5) Seven constants are currently inline. Some (`SYNTHESIS_TOKEN_BUDGET`) are already configurable. A question of taste: how many should users (humanities collection has different citation patterns, for instance) be able to tune without editing code?

7. **Do I file R4 (relax GROBID year requirement) and R15 (stub metadata) together, or separately?** They share a PaperMetadata schema change (year: int → year: Optional[int]). Combining reduces churn, but ties two concerns together and increases PR size. My lean: combine.

---

## Metadata

- **Review duration:** ~1 session
- **Code base state at review:** commit `4bfa473` (after test-audit landed)
- **Findings filed as issues:** R1–R18 (1 H + 16 M + 1 cleanup = 18 issues, under epic `[EPIC] Code review 2026-04 followups`)
- **Next action:** a human (or exomonad session) picks R items off in whatever order is most convenient. Each is sized for one PR with a pre-written commit message. Dependencies noted inline (R3 depends on R4, R15 ties to R4).

**Suggested shape for a follow-up fix session:**

> Open `docs/code-review-2026-04.md`. Tackle R1 first (mojibake, one-line fix + regression test). Then R2 (state atomicity — the data-loss pair). Then pick from R3–R17 based on blast-radius / your mood. R4+R15 should land together. R18 (ruff + dead code) is a low-risk first PR for an unfamiliar contributor to get their feet wet.
