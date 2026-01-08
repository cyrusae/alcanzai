# MVP Evaluation ↔ Architecture Conversation: Cross-Reference

## What These Two Documents Show

**MVP_EVALUATION.md** (from code review):
- What was actually delivered
- What's missing for the architecture to work
- Identified 7 blocking components
- Highlighted 3 decision points needing clarification

**ARCHITECTURE_DISTILLED.md** (from conversation highlights):
- What you actually want to build (the UX)
- How the conversation evolved to MVP v0.1.0 scope
- Complete specification of the 11 modules needed
- Build order and time estimates

**This document:** Shows how they align + what was settled

---

## 1. Alignment: Both Documents Identified Same Blockers

### The 5 Core Blocking Components

Both documents independently identified these exact modules as essential:

| Module | MVP Eval | Architecture | Rationale |
|--------|----------|--------------|-----------|
| grobid_processor.py | ✅ Blocked | ✅ Phase A | Without this, GROBID is just Docker setup—no code to use it |
| synthesis_generator.py | ✅ Blocked | ✅ Phase A | No way to call Claude—models exist but no integration |
| markdown_writer.py | ✅ Blocked | ✅ Phase A | Output format designed but not rendered to disk |
| arxiv_fetcher.py | ✅ Blocked | ✅ Phase B | arXiv is v0.1.0 requirement, needs API integration |
| orchestrator.py | ✅ Blocked | ✅ Phase C | No main entry point—everything is orphaned without this |

**Convergence:** Both reviews reached the same conclusion about what matters.

---

## 2. New Details from Architecture Conversation

The conversation added **context and scope** to what the MVP Eval didn't have:

### A. Scope Expansion: Web Content Included

**MVP Eval said:**
- Marked web content as "YES (in scope)" but noted uncertainty
- "Question: Should arxiv_fetcher.py assume papers are local files or fetch from arXiv API?"

**Architecture Conversation settled this:**
- ✅ Web content explicitly in v0.1.0 MVP
- ✅ "Clear your tabs" workflow requires this
- ✅ Actually easier than thought (web_fetcher.py is simple)
- ✅ Both papers and articles use same synthesis pipeline

**Impact:** This means web_fetcher.py is NOT optional—it's required for v0.1.0.

### B. Design Specification: Templates Provided

**MVP Eval said:**
- ❌ "No actual template showing what the output looks like"
- Marked as "BLOCKER? YES" for Obsidian format

**Architecture Conversation provided:**
- ✅ Complete paper template (with example content)
- ✅ Complete article template
- ✅ Vault structure diagram
- ✅ File naming convention: "Author et al (Year) - Title"
- ✅ Citation format: `[[Author et al (Year) - Title]]`

**Impact:** markdown_writer.py now has clear specifications to implement.

### C. Input Priority Clarified

**MVP Eval said:**
- "Question: Should arxiv_fetcher.py assume papers are local files or fetch from arXiv API?"
- Suggested "Both: If arXiv ID found locally, use that. Otherwise, fetch."

**Architecture Conversation decided:**
- ✅ Tier 1: arXiv ID (direct from API)
- ✅ Tier 1: DOI (via CrossRef + Unpaywall)
- ✅ Tier 1: URL (web articles)
- ✅ Tier 2: Clean PDF (local file upload)
- ❌ Deferred: Scanned PDFs (needs OCR, v0.2)

**Impact:** doi_fetcher.py is now confirmed as v0.1.0, not deferred.

### D. State Management Enhancement

**MVP Eval said:**
- ⚠️ "What about duplicate detection across sources? Paper exists in arXiv AND via DOI submission—current state.is_processed() would miss this!"

**Architecture Conversation implicitly addressed this:**
- Each source tracked separately: processed_arxiv_ids, processed_dois, processed_urls
- No version tracking mentioned yet
- Assumption: User won't intentionally process same paper from multiple sources

**Impact:** state.py is probably fine as-is, but may need version family tracking later.

---

## 3. Gaps That Still Remain

### A. Error Handling Strategy (Both Documents Avoid It)

**MVP Eval noted:**
- "No error handling: What happens if GROBID is down? Network fails? How do we retry?"

**Architecture Conversation assumed:**
- Happy path only in specifications
- No mention of: retry logic, timeout handling, partial failures

**Needs decision:**
- Should GROBID failure fall back to basic PDF metadata extraction?
- Should network failures queue for retry?
- Should partial processing (got metadata, synthesis failed) be stored?

**Recommendation:** Build Phase 1 without retry logic (fail loudly), add in Phase 3 when you've seen real failures.

### B. Logging Strategy (Neither Document Specifies)

**MVP Eval noted:**
- "No logging: Hard to debug what's happening in production"

**Architecture Conversation showed CLI output but not log structure:**
```bash
[1/5] arXiv 2312.12345 → Fetching... ✓ Synthesized
```

**Needs decision:**
- Should logs go to file, stdout, both?
- What verbosity levels? (DEBUG, INFO, ERROR)
- How to track costs per paper, per batch?

**Recommendation:** Simple stdout logging in v0.1.0, add file logging in v0.1.5.

### C. Testing Strategy (Neither Document Addresses)

**MVP Eval noted:**
- "No tests: No test fixtures, no test data, no example processing flows"

**Architecture Conversation is implementation-focused, not test-focused**

**Needs decision:**
- Should you test with real arXiv papers or mock fixtures?
- How to test GROBID without real server?
- How to test Claude integration without spending money?

**Recommendation:** 
- Use 2-3 real papers from your collection as integration tests
- Mock GROBID responses for unit tests
- Use Claude API directly (token cost is negligible for ~10 papers)

### D. Performance & Cost Tracking (Implied but Not Detailed)

**Architecture Conversation mentioned:**
- "Token cost not a concern - can err on side of sending full papers to Haiku"
- Synthesis object has `cost_usd: float` field

**Needs specification:**
- What should you send Claude? (Full text, abstract + intro, first N words?)
- How to measure token usage per paper?
- When to measure: per paper, per batch, total?

**Recommendation:**
- Start with full paper text to Claude (you said cost doesn't matter)
- Log tokens used per paper in metadata
- Measure after first batch to see pattern

---

## 4. Architecture Decisions Made in Conversation

These were settled and should be coded to spec:

### ✅ Decided: Obsidian YAML Frontmatter Format

```yaml
---
title: "..."
authors: [List, Of, Authors]
year: 2023
venue: "Journal Name"
volume: 49
issue: 2
pages: 123-145
doi: 10.1162/coli_a_00123
arxiv: 2312.12345
type: paper  # or "article"
status: read
added: 2024-01-06
tags:
  - tag1
  - tag2
---
```

**For articles:**
```yaml
---
title: "..."
authors: [Author List]
publisher: "Site Name"
url: https://example.com/article
type: article
published: 2024-01-06
added: 2024-01-06
tags:
  - tag1
---
```

### ✅ Decided: Citation Format in Notes

Wikilinks with full author list for disambiguation:
- `[[Vaswani et al (2017) - Attention Is All You Need]]`
- `[[Smith, Jones & Chen (2023) - Title]]`
- Not: `[[2017-Vaswani]]` (loses context)
- Not: `[[Vaswani]]` (ambiguous)

### ✅ Decided: File Naming Convention

"FirstAuthor et al (Year) - Title" format:
- arXiv paper: `Smith et al (2023) - Neural Syntax.md`
- Web article: `Olah (2023) - Circuits.md`
- Multi-author: `Smith, Jones & Chen (2023) - Title.md`

Slugified title (remove special chars, limit 80 chars total).

### ✅ Decided: Vault Organization

```
vault/
├── Papers/              # From arXiv, DOI, local PDFs
├── Articles/            # From URLs
├── PDFs/                # Original files
├── Topics/              # User-created
├── Sessions/            # User-created
├── Authors/             # Future
├── _templates/          # Templates
└── _meta/               # processing_state.json
```

### ✅ Decided: Note Sections (Standard for All Papers)

1. Title + author byline + year
2. Memorable quote (blockquote)
3. "Quick Refresh" (3-4 sentence synthesis)
4. "Why You Cared" (2-3 sentences about relevance)
5. Key Concepts (tag list)
6. Cites (links to cited papers)
7. Cited By (links to papers citing this)
8. Details (metadata section)
9. Abstract
10. Full Citation List

For articles, same structure minus citations (web content doesn't have bibliography).

---

## 5. Module Implementation Checklist

From Architecture Distilled, with notes from MVP Eval:

### Phase A: Core Infrastructure

- [ ] **grobid_processor.py**
  - Parse GROBID XML response → PaperMetadata
  - Error handling for: timeouts, invalid PDFs, network failures
  - Testing: Mock GROBID for unit tests, real server for integration

- [ ] **synthesis_generator.py**
  - Call Claude Haiku with paper text
  - Prompt for: summary, why_cared, key_concepts, memorable_quote
  - Track tokens used + cost per paper
  - Error handling: API timeouts, rate limits

- [ ] **markdown_writer.py**
  - Render paper template (with sections from decision above)
  - Render article template (without citation section)
  - File writing + path generation
  - Error handling: File already exists, permission issues

### Phase B: Fetchers

- [ ] **arxiv_fetcher.py**
  - Query arXiv API for metadata
  - Download PDF directly from arXiv
  - Save to vault/PDFs/arxiv_{id}.pdf
  - Error handling: Paper not found, invalid ID format

- [ ] **doi_fetcher.py**
  - Query CrossRef API for metadata
  - Use Unpaywall API to find PDF (free version)
  - Save to vault/PDFs/doi_{slug}.pdf
  - Error handling: DOI not found, PDF not available, invalid format

- [ ] **web_fetcher.py**
  - Fetch HTML content via requests
  - Extract metadata from OG tags (title, author, date)
  - Convert HTML → markdown via markdownify
  - Error handling: 404, timeout, blocked, invalid content

- [ ] **local_pdf_fetcher.py**
  - Load local PDF file
  - Extract basic metadata (title, page count)
  - Verify file exists and is readable
  - Error handling: File not found, invalid PDF, no read permission

### Phase C: Orchestration

- [ ] **orchestrator.py**
  - Detect input type (arXiv ID, DOI, URL, file path)
  - Route to appropriate fetcher
  - Coordinate: fetch → GROBID → synthesis → markdown → write → state
  - State management: Check for duplicates, mark processed/failed
  - Error handling: Catch at module level, mark_failed in state

- [ ] **cli.py**
  - `process <identifier>` - process single paper
  - `batch <file>` - process multiple papers
  - `stats` - show processing statistics
  - Pretty output formatting

### Phase D: Utilities

- [ ] **text_extraction.py**
  - Extract text from PDF via pdfplumber
  - Skip non-text elements
  - Return full text or first N words

- [ ] **file_naming.py**
  - Generate filename from PaperMetadata
  - Handle: author lists, special characters, long titles
  - Format: "Author et al (Year) - Title"

---

## 6. Build Sequencing Strategy

### Sequential Path (Safe, Recommended)

Build in this order, testing end-to-end after each phase:

1. **grobid_processor.py** (2h)
   - Test: Send one of your arXiv PDFs to GROBID locally
   - Verify: Can parse response into PaperMetadata object

2. **synthesis_generator.py** (2h)
   - Test: Call Claude with paper text from step 1
   - Verify: Gets back valid Synthesis object, check cost

3. **markdown_writer.py** (2h)
   - Test: Render markdown from metadata + synthesis in step 1-2
   - Verify: Matches template design, can write to file

4. **arxiv_fetcher.py** (1.5h)
   - Test: Fetch one arXiv paper (2312.12345)
   - Verify: Downloads PDF, extracts metadata

5. **orchestrator.py** (2h)
   - Test: End-to-end on one arXiv paper
   - Verify: Full pipeline works, note appears in vault

6. **Test on 3-5 of your papers** (1h)
   - Measure: Cost, speed, quality
   - Check: Obsidian reads notes correctly
   - Document: Any edge cases

Then move to Phase B (fetchers 2 & 3), then Phase C (CLI polish).

### Parallel Path (Risky, Could Save Time)

If you're confident:
- Someone: arxiv_fetcher.py in parallel
- Someone: grobid_processor.py in parallel
- Then: coordinate on synthesis_generator.py

**Not recommended for first module** because you'll debug integration issues.

---

## 7. Comparison Table: Conversation Evolution vs Code Reality

| Aspect | Early Conversation | Final Architecture | Code Status | Gap |
|--------|-------------------|-------------------|-------------|-----|
| Output interface | Notion vs Obsidian | Obsidian settled | ✅ Designed | Config ready |
| Input sources | arXiv + DOI | + Web + Clean PDF | ✅ Specified | Fetchers missing |
| Database | SQLite vs JSON | JSON + YAML | ✅ models.py | No GROBID integration |
| Metadata fields | List of 8 | Expanded in models | ✅ Complete | Writers missing |
| State tracking | Simple dict | Sets for fast lookup | ✅ state.py | No cross-source dedup |
| Synthesis tiers | Quick + detailed | Quick (detailed v0.2) | ✅ Decided | No generator yet |
| Citation handling | Extract + store | Extract, defer retrieval | ✅ Models | No linking logic |
| MVP input priority | Debated | arXiv + DOI + web + PDF | ✅ Decided | All fetchers missing |

---

## 8. Risk Assessment

### Low Risk (Should Work As Designed)
- ✅ Obsidian note generation (template is clear)
- ✅ Configuration loading (already built)
- ✅ State management (already built)
- ✅ GROBID integration (Docker is ready, just need parser)

### Medium Risk (Need Careful Implementation)
- ⚠️ CrossRef + Unpaywall integration (APIs sometimes finicky)
- ⚠️ Web content extraction (metadata varies by site)
- ⚠️ HTML → markdown conversion (edge cases with special content)
- ⚠️ Claude prompt engineering (getting consistent synthesis format)

### High Risk (Will Need Iteration)
- ⚠️ Deduplication across sources (haven't faced real duplicate yet)
- ⚠️ Error recovery (only theoretical at this point)
- ⚠️ Performance at scale (untested with 200+ papers)

**Mitigation:** Start with ~24 arXiv papers. Real issues will surface.

---

## 9. What to Do Next

### Immediate (This Chat)
1. ✅ Review ARCHITECTURE_DISTILLED.md (complete spec)
2. ✅ Review MVP_EVALUATION.md (what's built vs missing)
3. ✅ Review this document (alignment)
4. Decide: Start building Phase A immediately?

### Short-term (Next Chat or Session)
1. Create project directory structure:
   ```
   paper_library/
   ├── __init__.py
   ├── config.py          # (copy from previous)
   ├── models.py          # (copy from previous)
   ├── state.py           # (copy from previous)
   ├── grobid_processor.py
   ├── synthesis_generator.py
   ├── markdown_writer.py
   ├── arxiv_fetcher.py
   ├── orchestrator.py
   └── cli.py
   ```

2. Build grobid_processor.py first (simplest, most testable)
3. Test with one real arXiv PDF from your collection
4. Measure: GROBID response time, extracted metadata quality

### Medium-term (After First Sprint)
1. Add synthesis_generator.py, test cost
2. Add markdown_writer.py, generate first note
3. Test end-to-end with arxiv_fetcher.py
4. Measure: Token costs, processing time, note quality

### Timeline
- **MVP working:** 1-2 weeks at ~2 hours/day
- **Full v0.1.0:** 2-3 weeks at ~2 hours/day
- **Polish + deploy:** Week 4

---

## Summary

| Document | Shows | Complements |
|----------|-------|-----------|
| MVP Evaluation | What was built + what's missing | Shows the gap |
| Architecture Distilled | What you want + how to build it | Shows the plan |
| This document | How they align | Shows the bridge |

**Key convergence:** Both documents independently identified the exact same 5 blocking modules (GROBID processor, synthesis generator, markdown writer, arxiv fetcher, orchestrator). This is a strong signal they're correct.

**Key addition from conversation:** Web content in MVP was debated and settled. This adds web_fetcher.py as a required component, not optional.

**Ready to code:** All design decisions are locked. Specifications are clear. Can start building Phase A immediately.

