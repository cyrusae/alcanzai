  Current state (v0.2.0, just completed): The full ingestion pipeline is working cleanly across all input types: arXiv, DOI (Crossref +
  Unpaywall/Semantic Scholar for OA PDFs), HTML web articles, PDFs from direct URLs, and PDFs behind abstract/landing pages. GROBID extracts
  clean body text (handles 2-column academic PDF layouts correctly). Claude synthesis uses a native Skills API setup with a register system
  (jargon/structure/depth axes). Citation contexts — the sentences surrounding each in-text citation — are extracted and passed to the synthesis
   prompt. Output goes to an Obsidian vault with source notes linked separately. 148 unit tests passing. Tested against a batch of ~39 mixed
  papers and articles.

  What's intentionally deferred and needs design discussion: There's a cluster of interrelated features I've been calling the "Hard Mode batch"
  that I want to think through before implementing, because they're all entangled:

  - OCR (OCRmyPDF + Unpaper) for scanned PDFs and book scans — needed before I can ingest my humanities collection and older materials
  - Annotations — highlights/notes from Android tablet PDF readers (and eventually Kindle Scribe); these would enrich the synthesis but there's
  no standard format
  - Acquisition stack — *arr-style quality upgrades when you have a bad scan of something that exists in better form elsewhere; largely solved
  for arXiv papers already, matters most for humanities
  - Versioning — current deduplication is by identifier (arXiv ID, DOI, URL); preprint→published isn't tracked; need a merge/promotion path
  - Humanities validation — citation patterns differ (footnotes, very old citations), garbage detector and numeric [N] matching haven't been
  tested against real humanities PDFs

  These feel like they share a precondition: knowing whether a given PDF has a usable text layer, and whether you already have a "better"
  version of it, before deciding what to do. I want to think through the right sequencing and whether there's an architecture that handles the
  whole cluster coherently rather than bolting each piece on separately.

  Also on the horizon but lower priority: on-demand detailed section-by-section summaries (skill exists, just needs a trigger); OTel
  instrumentation for homelab deployment; eventually an "interventions from within the note" mechanism (e.g. setting a frontmatter flag in
  Obsidian to request a detailed summary).