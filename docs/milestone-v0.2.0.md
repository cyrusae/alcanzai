# alcanzai v0.2.0 Milestone — "Full Pipeline"

**Tagged:** 2026-02-27
**Branch:** claude
**Test suite:** 148 unit tests passing, 26 integration tests available (require GROBID + API key)

---

## What This Version Is

v0.2.0 completes the core ingestion pipeline. Every planned input source works.
Every paper that can be automatically acquired (arXiv, OA via DOI, web article,
PDF URL, PDF behind a landing page) runs end-to-end to an Obsidian note with
AI synthesis and citation context. A batch of 39 mixed papers and articles runs
cleanly.

The remaining hard problems — scanned/annotated PDFs, humanities collections,
versioning, acquisition — are intentionally out of scope and are discussed below.

---

## What Shipped

### Input sources
- **arXiv** — ID in any format, PDF download, metadata from Atom API
- **DOI** — Crossref metadata + Unpaywall primary / Semantic Scholar fallback for OA PDF; `doi_only` path synthesizes from abstract when no PDF found
- **Web articles** — HTML with OG tag / JSON-LD / meta extraction; Distill/`d-article` support; markdownify conversion
- **PDF from URL** — detects `Content-Type: application/pdf`, downloads, routes through GROBID
- **PDF landing pages** — scans `<a>` tags with scoring (`.pdf` href = 3pts, `/pdf/` path = 2pts, link text match = 1pt); handles PhilArchive, SSRN, ACL Anthology style pages
- **Local PDF** — path passed directly

### Text quality
- **GROBID body text** replaces pdfplumber for synthesis and citation context. GROBID correctly reconstructs reading order from 2-column PDFs. pdfplumber remains as fallback for scanned PDFs (GROBID body < 1000 chars).
- Citation markers (`[N]`, `[1, 3, 5]`) are preserved in GROBID body text via `<ref>` element text content.

### Synthesis
- **Native Skills API** (`betas=["skills-2025-10-02"]`) with 7 skills: `understand-academic-text`, `extract-arguments`, `identify-terminology`, `register-controller`, `quick-summary`, `detailed-summary`, `glossary-extraction`
- **Register system** — 3 axes × 3 options: jargon (none/selective/heavy), structure (conversational/mixed/formal), depth (hand-holding/balanced/assume-knowledge)
- Skill IDs cached in `skills/skill_ids.json`; invalidate with `SkillsManager.invalidate_cache()`
- **Citation contexts** passed to synthesis prompt — up to 10k chars of how the paper uses its key sources, hard-capped to stay under the 200k token limit

### Citation context extraction
- Author-year styles: narrative (`Smith et al. (2023)`) and parenthetical (`(Smith et al., 2023)`) for 1, 2, and 3+ author cases
- Numeric style: `[N]`, `[1, 3, 5]` — matched by 1-based bibliography position, `\b` word boundary prevents `[30]` matching `[3]`
- Bibliography stripping before matching (detects References/Bibliography section in latter 50% of text)
- Output attached to `Citation.contexts[]` and rendered as blockquotes in the Cites section

### Vault output
- `vault/Papers/` — paper notes with YAML frontmatter, synthesis, citation context blockquotes, full citation list
- `vault/Articles/` — article notes
- `vault/Sources/` — raw web article markdown as linked notes (`[[filename - Source]]`); PDFs use `vault/PDFs/` as source of truth (no source note written)
- `vault/PDFs/` — downloaded PDFs (`arxiv_<id>.pdf`, `doi_<slug>.pdf`, `web_<slug>.pdf`)
- `vault/_meta/processing_state.json` — deduplication by arXiv ID, DOI, URL

### Infrastructure
- CLI: `alcanzai ingest`, `alcanzai batch`, `alcanzai stats`, `alcanzai validate`
- 148 unit tests; pytest marks for `integration` tests (require external services)
- Pre-commit hooks (ruff + black)
- Apple Silicon GROBID workaround: `grobid.yaml` forces all 19 models to `engine: wapiti`, avoids TF/AVX crash under QEMU

---

## Deferred Work

### Cluster 1: Hard Mode batch (intentionally out of scope)

OCR, humanities collection, annotation ingestion, acquisition stack, and
versioning are interrelated and need to be theorized together before
implementation. They share a precondition: you need to know whether a given PDF
has a usable text layer before deciding whether to OCR it, and you need to know
whether you already have a "better" version before deciding whether to acquire
another one.

The components:
- **OCR** — OCRmyPDF + Unpaper preprocessing before GROBID. The pipeline already handles clean-PDF → GROBID → body text; OCR just adds a step that adds a text layer to the PDF before sending it. The GROBID body text extraction path would then work normally.
- **Two-page spreads and book scans** — Unpaper deskew/dewarping before OCR. Needs testing with actual book scans.
- **Annotation ingestion** — Android tablet PDF readers (Xodo, etc.), future Kindle Scribe. Highlights/notes would enrich the `why_you_cared` section. No standard format; needs per-app investigation.
- **Acquisition stack** — `*arr`-style quality upgrades. When you have a bad scan, try to find a better version (OA PDF, publisher version). Largely solved for arXiv papers by existing DOI→Unpaywall chain; the humanities collection is where this matters.
- **Versioning** — Current deduplication is by identifier (arXiv ID, DOI, URL). Preprint → published version is not tracked; re-ingesting a published DOI for a paper already in the vault by arXiv ID will create a duplicate note. Needs a merge or promotion path.

### Cluster 2: Detailed summaries and note interventions

The `detailed-summary` skill and `generate_detailed_summary()` in
`synthesis_generator.py` are implemented but not wired to a user-facing trigger.

Agreed design principles:
- Detailed summary lives in a **linked note** (`vault/Papers/<filename> - Detail.md`) rather than being appended to the main note
- `alcanzai ingest --force` regenerates the quick note but does **not** touch the detail note
- The detail note gets its own frontmatter and could be independently versioned

**"Trigger from within the .md"** — the broader idea of triggering pipeline actions from inside an Obsidian note (regenerate synthesis, request detail, change register) is genuinely interesting but requires infrastructure that doesn't exist yet. Possible approaches:
- **File watcher daemon** (`alcanzai watch`) — polls vault for frontmatter flags like `detail_requested: true`, runs action, clears flag
- **Obsidian plugin** — calls `alcanzai` CLI directly from a button/command
- **Templater + shell** — Obsidian's Templater plugin can run shell commands; could be a bridge

This is probably v0.4 territory. For v0.3, a simple CLI flag (`alcanzai detail 1706.03762`) is sufficient.

### Cluster 3: Telemetry

OTel instrumentation for homelab container deployment. Currently using `print()`
statements throughout, which is acceptable for a local personal tool. The
structured data needed for OTel traces (step timing, token counts, cost, source
type, citation hit rates) is already being computed — it just needs to be
exported rather than printed.

Plan: implement when deploying to K3s. The print statements can stay; OTel would
be additive. No existing code needs to change — just add an `otel_exporter.py`
and wrap the orchestrator steps.

### Cluster 4: Knowledge graph (Phase 2)

Citation graph, author pages, cross-paper connections. The data model already
supports this (`BibliographicEntry` shared base, `Citation.contexts[]`). Blocked
on having enough papers in the vault to make the graph interesting.

---

## Known Gaps at v0.2.0

- **Deduplication for versions**: preprint + published DOI for same paper creates two notes. Not a problem for the current AI-centric batch (all arXiv); will surface when ingesting humanities DOIs.
- **Synthesis hasn't been tested against humanities collections**: different citation patterns (author-date vs footnote styles used in lit crit), very old citations, scanned materials. The garbage detector and citation pattern matcher were designed with this in mind but are unvalidated against real humanities PDFs.
- **Logging is print statements**: acceptable for v0.2, replace with OTel for homelab deployment.
- **`--force` creates orphaned source notes**: if you force-reprocess an article, a new `- Source.md` is written but the old one isn't deleted. Low priority.

---

## v0.3.0 Initial Scope

1. **Detailed summary trigger** — `alcanzai detail <id>` CLI command; writes `<filename> - Detail.md` to `vault/Papers/`; idempotent (won't overwrite if exists unless `--force`)
2. **OCR pipeline** — OCRmyPDF + Unpaper preprocessing; auto-detect scanned PDFs (check if GROBID body text < threshold after first pass); add `--ocr` flag to `ingest`
3. **OTel instrumentation** — additive; structured traces for homelab deployment

The Hard Mode batch cluster (annotations, acquisition, versioning, humanities
validation) probably warrants its own milestone design session before
implementation, given the interdependencies.
