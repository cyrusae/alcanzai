# Architecture Conversation Distilled
## UX Flow → MVP Scope → Implementation Roadmap

---

## 1. Intended UX Flow

### The Reality You're Living
Your actual reading workflow is **mixed**:
- arXiv AI/LLM papers during research
- Blog posts from Transformer Circuits, LessWrong, Distill.pub while browsing
- Academic papers via DOI when referenced
- Clean PDFs you already have locally
- All of this happens in parallel browser tabs

### The MVP Experience You Want
**Clear Your Tabs Workflow:**

```bash
# Week 1: You have a pile of open tabs and scattered PDFs
# You want to: Process them all into one searchable, connected knowledge base

cat my_research.txt
https://arxiv.org/abs/2312.12345                              # Paper
https://transformer-circuits.pub/2023/monosemantic-features/  # Blog
10.1162/coli_a_00123                                          # DOI
https://www.lesswrong.com/posts/xyz                           # Article
https://arxiv.org/abs/2311.09876                              # Paper

# Run once:
./ingest.py --batch my_research.txt

# Output:
[1/5] arXiv 2312.12345 → Fetching... ✓ Synthesized → vault/Papers/
[2/5] Transformer Circuits → Fetching... ✓ Synthesized → vault/Articles/
[3/5] DOI 10.1162... → Resolving... ✓ Synthesized → vault/Papers/
[4/5] LessWrong → Fetching... ✓ Synthesized → vault/Articles/
[5/5] arXiv 2311.09876 → Fetching... ✓ Synthesized → vault/Papers/

All tabs processed! Check your Obsidian vault.
```

### What You Get in Obsidian

**Reading your paper:**
```markdown
# Neural Models of Syntax
**Smith, Jones & Chen** • 2023

> [!quote]
> "Transformers develop implicit syntactic knowledge without supervision"

## Quick Refresh
[3-4 sentence AI summary]

## Why You Cared
[2-3 sentences about relevance to your research]

## Key Concepts
#syntax #transformers #neural-networks #probing-tasks

## Cites (Key Papers)
- [[Vaswani et al (2017) - Attention Is All You Need]]
- [[Devlin et al (2019) - BERT]]

## Cited By
- [[Johnson et al (2024) - Syntax in Multilingual LLMs]]

## Details
venue, authors, year, DOI, PDF link, etc.

---
[Full abstract + optional detailed summary on demand]
```

**In Obsidian Graph View:**
- Click `[[Vaswani et al 2017]]` → jump to that paper
- Graph shows: "Who cites whom"
- Clusters show: Topic groups
- Backlinks show: Papers that cite this one

**Searching:**
- Type "syntax" → finds papers + articles with that tag
- Type "author:Smith" → all papers by that author
- Type "status:read" → only papers you've reviewed
- Query with Dataview: `TABLE authors, year WHERE tags contains "transformers"`

---

## 2. MVP Scope (What Needs to Work)

### Input Types in Priority Order

**Tier 1: Remote Content (Easy Wins)**
1. **arXiv ID** - `./ingest.py --arxiv 2312.12345`
   - Fetch PDF directly from arXiv
   - Extract metadata from arXiv API
   - Send to GROBID + Claude → synthesis

2. **DOI** - `./ingest.py --doi 10.1162/coli_a_00123`
   - Resolve DOI → metadata via CrossRef API
   - Fetch PDF via Unpaywall (free open access) or direct link
   - Send to GROBID + Claude → synthesis

3. **URL (Web Article)** - `./ingest.py --url https://transformer-circuits.pub/...`
   - Fetch HTML, extract metadata (OG tags, article tags)
   - Convert HTML → markdown
   - Send markdown to Claude → synthesis
   - Store in `vault/Articles/` instead of `vault/Papers/`

**Tier 2: Local Content (Medium Effort)**
4. **Clean PDF** - `./ingest.py --pdf paper.pdf`
   - Assume text layer exists (no OCR needed)
   - Send to GROBID for metadata + citations
   - Send full text to Claude → synthesis
   - Output to `vault/Papers/`

### What Gets Deferred to v0.2
- ❌ Scanned PDFs (need OCRmyPDF preprocessing)
- ❌ Annotated PDFs (need annotation extraction from tablet readers)
- ❌ Multi-page spreads (need image processing)
- ❌ Author pages (defer citation graph features)
- ❌ Detailed summaries on-demand (basic synthesis only)

### Processing Pipeline (Unified)

For **all** input types, the pipeline is:

```
Input (PDF or HTML or URL)
    ↓
[Fetch/Download]
    ↓
[Extract Metadata] → PaperMetadata or ArticleMetadata
    ↓
[Extract Citations] → list[Citation] (stored, not retrieved yet)
    ↓
[Generate Synthesis] → summary, why_you_cared, key_concepts, memorable_quote
    ↓
[Render Markdown] → YAML frontmatter + formatted content
    ↓
[Write to Vault] → vault/Papers/filename.md or vault/Articles/filename.md
    ↓
[Update State] → mark_processed(identifier, source)
```

### Obsidian Vault Structure

```
vault/
├── Papers/
│   ├── Smith et al (2023) - Neural Syntax.md        # From arXiv/DOI
│   ├── Vaswani et al (2017) - Attention.md          # From arXiv/DOI
│   └── Brown et al (2020) - GPT-3.md                # From local PDF
│
├── Articles/
│   ├── Anthropic (2023) - Monosemanticity.md        # From URL
│   ├── Christiano (2024) - RLHF.md                  # From URL
│   └── Olah (2023) - Circuits.md                    # From URL
│
├── PDFs/
│   ├── arxiv_2312.12345.pdf
│   ├── doi_10.1162_coli.pdf
│   └── paper_smith2023.pdf
│
├── Topics/                    # Manually created for organization
│   ├── Transformers.md
│   └── Mechanistic Interpretability.md
│
├── Authors/                   # Future: auto-generated
│   └── (deferred to Phase 2)
│
├── Sessions/                  # Your reading notes
│   └── Week 1 - LLM Syntax.md
│
├── _templates/
│   ├── paper.md              # Template for papers
│   └── article.md            # Template for articles
│
├── _meta/
│   ├── Library Overview.md
│   └── processing_state.json  # What's been processed
│
└── .obsidian/                # Obsidian config (git-ignored)
    └── plugins/              # Plugins enabled
```

### Output Format: Paper Note Example

```yaml
---
title: "Neural Models of Syntax"
authors: [Smith John, Jones Alice, Chen Wei]
year: 2023
venue: Computational Linguistics
volume: 49
issue: 2
pages: 123-145
doi: 10.1162/coli_a_00123
arxiv: 2312.12345
type: paper
status: read
added: 2024-01-06
tags:
  - neural-networks
  - syntax
  - transformers
  - dependency-parsing
---

# Neural Models of Syntax

**[[Smith, John]]** • [[Jones, Alice]] • [[Chen, Wei]]** • 2023

> [!quote] Memorable Quote
> "Transformers achieve state-of-the-art syntax parsing without explicit syntactic structure."

## Quick Refresh

This paper demonstrates that transformer-based language models develop implicit representations of syntactic structure through pre-training alone. The authors probe BERT and GPT-2 using syntactic tests and find they capture hierarchical dependencies better than RNN-based models.

Key contribution: Attention heads specialize for different syntactic relations without explicit training.

## Why You Cared

You were researching how LLMs handle syntax for your computational linguistics coursework. This bridges formal syntax theory with neural approaches—transformers aren't just "bag of words plus attention" but learn hierarchical structure.

## Key Concepts

`#hierarchical-structure` `#attention-specialization` `#emergent-syntax` `#bert` `#gpt2`

## Cites (Key Papers)

- [[Vaswani et al (2017) - Attention Is All You Need]] - Foundation for transformers
- [[Devlin et al (2019) - BERT]] - Model being analyzed
- [[Linzen et al (2016) - Assessing Syntactic Abilities]] - Probing methodology

[Full citation list in details section below]

## Cited By

- [[Johnson et al (2024) - Syntax in Multilingual LLMs]]
- [[Lee et al (2024) - Cross-lingual Syntax Transfer]]

## Details

**Published:** Computational Linguistics, Vol 49(2), pp 123-145  
**DOI:** [10.1162/coli_a_00123](https://doi.org/10.1162/coli_a_00123)  
**arXiv:** [2312.12345](https://arxiv.org/abs/2312.12345)  
**PDF:** [[smith2023-neural-syntax.pdf]]  

**Abstract:**
We investigate whether modern transformer language models develop implicit syntactic representations...

---

## Full Citation List

1. [[Vaswani et al (2017) - Attention Is All You Need]]
2. [[Devlin et al (2019) - BERT]]
... (auto-generated from GROBID output)
```

### Output Format: Article Note Example

```yaml
---
title: "Toy Models of Superposition"
authors: [Elhage Nelson, Hume Trenton]
publisher: Anthropic
url: https://transformer-circuits.pub/2022/toy_model/index.html
type: article
published: 2022-09-08
added: 2024-01-06
tags:
  - interpretability
  - superposition
  - circuits
---

# Toy Models of Superposition

**Source:** [Transformer Circuits Thread](https://transformer-circuits.pub/)  
**Authors:** [[Elhage, Nelson]] • [[Hume, Trenton]]  
**Published:** 2022-09-08

## Quick Refresh

[Claude-generated synthesis of article content]

## Key Concepts

`#superposition` `#polysemanticity` `#interpretability` `#neural-networks`

## Related Papers

- [[Olah et al (2020) - Zoom In]] - Related work
- [[Anthropic (2023) - Monosemanticity]] - Follow-up

## Original Content

[Full article converted to markdown]
```

---

## 3. What Needs to Be Coded (MVP Implementation Plan)

### Foundation Already Built ✅
These were delivered in previous session:
- `config.py` - Configuration management
- `models.py` - Pydantic data models
- `state.py` - State management (processing_state.json)
- `docker-compose.yml` - GROBID setup
- `env.example` - Environment template

### Code Missing for MVP (In Build Order)

#### Phase A: Infrastructure & Utilities (Enablers)

**1. grobid_processor.py** [BLOCKING]
```python
# Purpose: Parse GROBID XML response into PaperMetadata
# Input: PDF file path OR PDF bytes
# Output: PaperMetadata object with all extracted fields

class GrobidProcessor:
    def __init__(self, grobid_url: str)
    def process(self, pdf_path: Path) -> PaperMetadata
        # Sends PDF to GROBID, parses XML, extracts:
        # - title, authors, year, venue, volume, pages
        # - citations (list[Citation])
        # Handles errors gracefully (GROBID timeout, invalid PDF)

# Usage:
processor = GrobidProcessor(config.grobid_url)
metadata = processor.process(Path("paper.pdf"))
```

**2. synthesis_generator.py** [BLOCKING]
```python
# Purpose: Call Claude to generate synthesis
# Input: Paper metadata + extracted text
# Output: Synthesis object

class SynthesisGenerator:
    def __init__(self, api_key: str)
    def generate_quick_synthesis(self, 
        text: str, 
        metadata: PaperMetadata
    ) -> Synthesis
        # Calls Claude Haiku with:
        # - Paper text (or first N words for web content)
        # - Structured prompt for: summary, why_cared, concepts, quote
        # Returns Synthesis object

    def generate_detailed_summary(self, 
        text: str, 
        metadata: PaperMetadata
    ) -> str:
        # Deferred to v0.2, but method exists for later

# Usage:
generator = SynthesisGenerator(config.anthropic_api_key)
synthesis = generator.generate_quick_synthesis(full_text, metadata)
```

**3. markdown_writer.py** [BLOCKING]
```python
# Purpose: Convert PaperMetadata + Synthesis → markdown file
# Input: PaperMetadata, Synthesis, content type ("paper" or "article")
# Output: Markdown string ready to write to disk

class MarkdownWriter:
    @staticmethod
    def paper_to_markdown(
        metadata: PaperMetadata,
        synthesis: Synthesis
    ) -> str:
        # Generates markdown with:
        # - YAML frontmatter (all metadata fields)
        # - Title + author byline
        # - Memorable quote block
        # - Quick Refresh section
        # - Why You Cared section
        # - Key Concepts tags
        # - Citation links: [[Author, Year]] format
        # - Details section (abstract, DOI, arXiv, etc.)
        # - Full citation list (auto-generated from GROBID)

    @staticmethod
    def article_to_markdown(
        metadata: ArticleMetadata,
        synthesis: Synthesis,
        content: str  # HTML converted to markdown
    ) -> str:
        # Similar but for web articles:
        # - No citations section (web content doesn't extract those)
        # - No venue/volume/pages
        # - Original content section with full HTML→markdown conversion

# Usage:
markdown = MarkdownWriter.paper_to_markdown(metadata, synthesis)
# markdown is ready to write to file
```

#### Phase B: Fetchers (Source-specific)

**4. arxiv_fetcher.py** [BLOCKING]
```python
# Purpose: Given arXiv ID, fetch PDF + metadata
# Input: arXiv ID (e.g., "2312.12345")
# Output: Tuple[Path (to PDF), PaperMetadata (from arXiv API)]

class ArxivFetcher:
    def fetch(self, arxiv_id: str) -> Tuple[Path, PaperMetadata]:
        # 1. Hit arXiv API for metadata:
        #    - authors, title, year, abstract
        #    - https://api.arxiv.org/query?id_list=2312.12345
        # 2. Download PDF:
        #    - https://arxiv.org/pdf/2312.12345.pdf
        #    - Save to vault/PDFs/arxiv_2312.12345.pdf
        # 3. Return: (Path to PDF, PaperMetadata with arxiv_id set)

    def parse_arxiv_id(self, text: str) -> Optional[str]:
        # Helper: Extract arXiv ID from various formats:
        # - "2312.12345"
        # - "https://arxiv.org/abs/2312.12345"
        # - "arxiv:2312.12345"

# Usage:
fetcher = ArxivFetcher(vault_path=config.vault_path)
pdf_path, metadata = fetcher.fetch("2312.12345")
```

**5. doi_fetcher.py** [BLOCKING for MVP as decided]
```python
# Purpose: Given DOI, resolve to PDF + metadata
# Input: DOI (e.g., "10.1162/coli_a_00123")
# Output: Tuple[Path (to PDF), PaperMetadata (from CrossRef + Unpaywall)]

class DoiFetcher:
    def fetch(self, doi: str) -> Tuple[Path, PaperMetadata]:
        # 1. Query CrossRef API for metadata:
        #    - https://api.crossref.org/works/{doi}
        #    - Extract: authors, title, year, venue, volume, pages, abstract
        # 2. Find PDF URL via Unpaywall API:
        #    - https://api.unpaywall.org/v2/{doi}?email=user@example.com
        #    - Try: publisher PDF, repository, preprint
        # 3. Download PDF to vault/PDFs/doi_*.pdf
        # 4. Return: (Path, PaperMetadata with doi set)
        # 5. If no PDF found, raise PdfNotFound(doi)

    def parse_doi(self, text: str) -> Optional[str]:
        # Helper: Extract DOI from various formats

# Usage:
fetcher = DoiFetcher(vault_path=config.vault_path)
pdf_path, metadata = fetcher.fetch("10.1162/coli_a_00123")
```

**6. web_fetcher.py** [BLOCKING for MVP as decided]
```python
# Purpose: Given URL, fetch content + extract metadata
# Input: URL (e.g., "https://transformer-circuits.pub/...")
# Output: ArticleMetadata + markdown content

class WebFetcher:
    def fetch(self, url: str) -> Tuple[ArticleMetadata, str]:
        # 1. Fetch HTML:
        #    - requests.get(url)
        #    - Follow redirects
        # 2. Extract metadata from OG tags:
        #    - og:title → title
        #    - article:author → authors
        #    - article:published_time → date
        #    - og:description → abstract/summary
        # 3. Convert HTML → markdown:
        #    - Use markdownify library
        # 4. Return: (ArticleMetadata, markdown_content)

    def is_url(self, text: str) -> bool:
        # Check if string is a URL

    def detect_type(self, url: str) -> str:
        # "arxiv" vs "doi" vs "url"

# Usage:
fetcher = WebFetcher()
metadata, content = fetcher.fetch("https://transformer-circuits.pub/...")
```

**7. pdf_fetcher.py** [MEDIUM - for local PDFs]
```python
# Purpose: Load local PDF + extract basic metadata
# Input: Path to PDF file
# Output: Tuple[Path, FileMetadata (basic, no GROBID yet)]

class LocalPdfFetcher:
    def fetch(self, pdf_path: Path) -> Tuple[Path, PaperMetadata]:
        # 1. Verify PDF exists and is readable
        # 2. Extract basic metadata from PDF:
        #    - Use pypdf or pdfplumber
        #    - Get: title, author (if in PDF metadata)
        #    - If not present, use filename for title
        # 3. Return: (Path, PaperMetadata with minimal fields)
        # 4. GROBID processor will fill in the rest

# Usage:
fetcher = LocalPdfFetcher()
pdf_path, metadata = fetcher.fetch(Path("my_paper.pdf"))
```

#### Phase C: Orchestration

**8. orchestrator.py or main.py** [BLOCKING]
```python
# Purpose: Coordinate the entire pipeline
# Input: Identifier (arXiv ID, DOI, URL, or Path)
# Output: Paper note written to vault + state updated

class PaperProcessor:
    def __init__(self, config: Config, state_manager: StateManager):
        self.arxiv_fetcher = ArxivFetcher(config.vault_path)
        self.doi_fetcher = DoiFetcher(config.vault_path)
        self.web_fetcher = WebFetcher()
        self.pdf_fetcher = LocalPdfFetcher()
        self.grobid_processor = GrobidProcessor(config.grobid_url)
        self.synthesis_generator = SynthesisGenerator(config.anthropic_api_key)
        self.markdown_writer = MarkdownWriter()
        self.state = state_manager

    def process(self, identifier: str) -> bool:
        """
        Process a single paper/article from any source.
        
        Returns: True if successful, False if already processed
        """
        # 1. Check if already processed
        if self.state.is_processed(identifier):
            print(f"Already processed: {identifier}")
            return False

        try:
            # 2. Determine source type and fetch
            if self._is_arxiv(identifier):
                pdf_path, metadata = self.arxiv_fetcher.fetch(identifier)
                source = "arxiv"
            elif self._is_doi(identifier):
                pdf_path, metadata = self.doi_fetcher.fetch(identifier)
                source = "doi"
            elif self._is_url(identifier):
                metadata, content = self.web_fetcher.fetch(identifier)
                # For web: skip GROBID, go straight to synthesis
                synthesis = self.synthesis_generator.generate_quick_synthesis(
                    content, metadata
                )
                markdown = self.markdown_writer.article_to_markdown(
                    metadata, synthesis, content
                )
                source = "web"
            else:  # Local PDF
                pdf_path, metadata = self.pdf_fetcher.fetch(Path(identifier))
                source = "pdf"

            # 3. Process with GROBID (papers only, not web)
            if source != "web":
                grobid_metadata = self.grobid_processor.process(pdf_path)
                # Merge GROBID results with fetched metadata
                metadata = self._merge_metadata(metadata, grobid_metadata)

            # 4. Generate synthesis
            if source == "web":
                # Already done above
                pass
            else:
                # Extract text from PDF for synthesis
                text = extract_text_from_pdf(pdf_path)  # Use pdfplumber
                synthesis = self.synthesis_generator.generate_quick_synthesis(
                    text, metadata
                )

            # 5. Write to vault
            if source == "web":
                # Already have markdown
                pass
            else:
                markdown = self.markdown_writer.paper_to_markdown(
                    metadata, synthesis
                )

            # 6. Write to appropriate directory
            if metadata.type == "article":
                output_dir = config.articles_dir
            else:
                output_dir = config.papers_dir

            output_path = output_dir / f"{self._generate_filename(metadata)}.md"
            output_path.write_text(markdown)

            # 7. Update state
            if source == "arxiv":
                self.state.mark_processed(metadata.arxiv_id, "arxiv")
            elif source == "doi":
                self.state.mark_processed(metadata.doi, "doi")
            elif source == "web":
                self.state.mark_processed(metadata.url, "web")
            else:
                self.state.mark_processed(str(pdf_path), "pdf")

            print(f"✓ Processed {identifier} → {output_path}")
            return True

        except Exception as e:
            self.state.mark_failed(identifier, str(e))
            print(f"✗ Failed {identifier}: {e}")
            return False

    def process_batch(self, identifiers: List[str]) -> dict:
        """Process multiple papers, return stats."""
        results = {"success": 0, "failed": 0, "skipped": 0}
        for i, identifier in enumerate(identifiers, 1):
            try:
                if self.process(identifier):
                    results["success"] += 1
                else:
                    results["skipped"] += 1
            except Exception as e:
                results["failed"] += 1
        
        return results

# Usage:
config = Config()
state = StateManager.load()
processor = PaperProcessor(config, state)

# Single paper:
processor.process("2312.12345")

# Batch from file:
with open("urls.txt") as f:
    identifiers = [line.strip() for line in f]
results = processor.process_batch(identifiers)
print(f"Results: {results['success']} processed, {results['failed']} failed")
```

**9. cli.py** [NICE TO HAVE for v0.1.0]
```python
# Purpose: Command-line interface for the processor

import click

@click.group()
def cli():
    """Paper library processor - turn your tabs into a knowledge base"""
    pass

@cli.command()
@click.argument('identifier')
def process(identifier):
    """Process a single paper (arXiv ID, DOI, URL, or PDF path)"""
    config = Config()
    state = StateManager.load()
    processor = PaperProcessor(config, state)
    processor.process(identifier)

@cli.command()
@click.argument('file', type=click.File('r'))
def batch(file):
    """Process multiple papers from a file (one per line)"""
    config = Config()
    state = StateManager.load()
    processor = PaperProcessor(config, state)
    
    identifiers = [line.strip() for line in file if line.strip()]
    results = processor.process_batch(identifiers)
    
    print(f"\nResults:")
    print(f"  ✓ Processed: {results['success']}")
    print(f"  ⊘ Skipped: {results['skipped']}")
    print(f"  ✗ Failed: {results['failed']}")

@cli.command()
def stats():
    """Show processing statistics"""
    state = StateManager.load()
    stats = state.get_stats()
    
    print(f"Processing Statistics:")
    print(f"  Papers (arXiv): {stats['arxiv']}")
    print(f"  Papers (DOI): {stats['doi']}")
    print(f"  Articles (Web): {stats['web']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Total processed: {stats['total']}")

if __name__ == '__main__':
    cli()

# Usage:
# python cli.py process 2312.12345
# python cli.py batch my_tabs.txt
# python cli.py stats
```

#### Phase D: Helpers (Non-blocking but useful)

**10. text_extraction.py** [SUPPORTING]
```python
# Purpose: Extract text from PDFs for synthesis
# Input: PDF file path
# Output: Extracted text (first N words for web, all for papers)

def extract_text_from_pdf(pdf_path: Path, max_words: int = None) -> str:
    """Extract readable text from PDF"""
    # Use pdfplumber for better text extraction than pypdf
    # Return full text if max_words is None
    # Return first N words if max_words is set

def extract_text_from_markdown(markdown: str) -> str:
    """Extract text from markdown, skip frontmatter"""
    # Skip YAML frontmatter
    # Return clean text
```

**11. file_naming.py** [SUPPORTING]
```python
# Purpose: Generate consistent filenames for notes
# Input: PaperMetadata or ArticleMetadata
# Output: Filename string (no extension, no path)

def generate_paper_filename(metadata: PaperMetadata) -> str:
    """
    Generate: "Smith et al (2023) - Neural Syntax"
    From: authors=[Smith, Jones, Chen], year=2023, title="Neural Models..."
    """
    # Use first author's last name
    # Format: "Author1 et al (Year) - Title"
    # Slugify title to remove special chars
    # Limit to 80 chars

def generate_article_filename(metadata: ArticleMetadata) -> str:
    """Similar but for articles"""
```

---

## 4. Cross-Reference: What Was Built vs. What's Missing

### MVP Evaluation Summary

From the MVP_EVALUATION.md document created in parallel:

| Component | Built | Missing | Blocker |
|-----------|-------|---------|---------|
| Configuration | ✅ config.py | — | No |
| Data Models | ✅ models.py | — | No |
| State Management | ✅ state.py | — | No |
| **GROBID Processing** | ✅ Docker | ❌ Code | **YES** |
| **arXiv Fetcher** | ❌ | ❌ | **YES** |
| **DOI Fetcher** | ❌ | ❌ | **YES** |
| **Web Fetcher** | ❌ | ❌ | **YES** |
| **Synthesis Generator** | ❌ | ❌ | **YES** |
| **Markdown Writer** | ❌ | ❌ | **YES** |
| **Orchestrator** | ❌ | ❌ | **YES** |
| Markdown Output Format | ✅ (Designed) | ❌ (Template) | **Partial** |

### Architecture Conversation Added These Clarifications

From the highlights reel, the previous Claude conversation evolved:

**Starting Point:** Just arXiv papers + database

**Evolved to:** Unified "Clear Your Tabs" system
- ✅ Decided: Include web content in MVP (not v0.2)
- ✅ Decided: Both papers and articles use same synthesis pipeline
- ✅ Decided: Articles stored separately (vault/Articles/) but same search/graph
- ✅ Decided: Obsidian handles both seamlessly

**Templates Designed:**
- ✅ Paper note format (with citations, frontmatter, sections)
- ✅ Article note format (similar structure, different fields)
- ✅ Vault directory layout

---

## 5. Build Order Recommendation

### Sprint 1: Core MVP (1-2 weeks)
**Goal: Process your first 5 papers end-to-end**

Priority order (fixes blockers first):

1. **grobid_processor.py** [~2 hours]
   - Parse GROBID XML
   - Extract to PaperMetadata
   - Error handling for timeouts

2. **synthesis_generator.py** [~2 hours]
   - Claude integration
   - Prompt engineering for quick synthesis
   - Cost tracking

3. **markdown_writer.py** [~2 hours]
   - Render paper template
   - Render article template
   - File writing + error handling

4. **arxiv_fetcher.py** [~1.5 hours]
   - arXiv API integration
   - PDF download
   - Metadata extraction

5. **orchestrator.py** [~2 hours]
   - Tie all pieces together
   - State management integration
   - Error handling

6. **Test with 3 of your arXiv papers manually**

### Sprint 2: Full Input Support (v0.1.0)
**Goal: "Clear your tabs" works for mixed content**

7. **doi_fetcher.py** [~2 hours]
   - CrossRef + Unpaywall APIs
   - PDF resolution

8. **web_fetcher.py** [~1.5 hours]
   - HTML fetch + metadata extraction
   - HTML → markdown conversion

9. **cli.py** [~1.5 hours]
   - Command-line interface
   - Batch processing

10. **Test with batch of your mixed tabs**

### Sprint 3: Polish & Deploy (v0.1.0 final)

11. **Error handling & retry logic** [~2 hours]
12. **Logging** [~1 hour]
13. **Documentation** [~2 hours]
14. **Test on all ~24 your arXiv papers**
15. **Measure token costs, quality**

### Total Estimate
- **Sprint 1:** ~9.5 hours (get first paper working)
- **Sprint 2:** ~5 hours (add web support)
- **Sprint 3:** ~5 hours (polish & deploy)
- **Total MVP:** ~19.5 hours of development

---

## 6. Key Decisions Made (From Architecture Conversation)

These were decided during the architecture conversation and locked into project.json:

1. ✅ **Output: Obsidian** (not Notion, not SQLite)
   - Graph view for citations
   - Fast search
   - Local-first
   - Mobile sync via Livesync

2. ✅ **MVP Input: arXiv + DOI + Web + Clean PDFs**
   - Covers 90% of actual use
   - Relatively easy to implement
   - Defer OCR to v0.2

3. ✅ **Metadata: YAML frontmatter + JSON state**
   - No database for MVP
   - Human-readable
   - Git-friendly

4. ✅ **Synthesis: Two-tier (quick + detailed)**
   - MVP: Quick summary only
   - v0.2: Detailed on-demand

5. ✅ **Citations: Extract and store, defer retrieval**
   - MVP: Parse citations, store in note
   - v0.2: Build citation index, author pages

6. ✅ **Processing: Stateless + deduplication tracking**
   - Can re-run safely
   - Tracks by DOI/arXiv/URL

---

## 7. Open Questions from Architecture Conversation

These need clarification before coding:

### 1. **Filename Generation**
Current design: "Author et al (Year) - Title"
- Example: `Smith et al (2023) - Neural Syntax.md`

**Question:** What if:
- Author has 2 people? (Smith & Jones vs Smith, Jones & Chen)
- Title is very long? (currently would truncate to 80 chars)
- Multiple papers by same author in same year? (Smith et al 2023a/b/c)

**Recommendation:** Use decision from conversation:
> "Use full author list for citation disambiguation (Smith, Jones & Chen 2023 vs Smith, Lee & Park 2023)"

So filenames should be similar: `Smith, Jones & Chen (2023) - Title.md`

### 2. **Citation Wikilink Format**
Current design in template: `[[Vaswani et al (2017) - Attention Is All You Need]]`

**Question:** Should citations link to:
- Notes that exist in vault (if paper is already processed)?
- Or just be dangling links (created when needed)?

**Recommendation:** Start with dangling links. Obsidian shows them as "future notes" and will help you discover gaps in your library.

### 3. **PDF Storage**
Current design: `vault/PDFs/` with generated names

**Question:** Should PDFs be:
- Embedded in note frontmatter (`[[smith2023.pdf]]`)?
- Stored in separate directory with link?
- Organized by source (arxiv_2312.12345.pdf vs doi_10.1162_coli.pdf)?

**Recommendation:** Separate directory organized by source type. Link via frontmatter. Obsidian can embed via `![[pdf]]` syntax.

---

## Summary

**The MVP you wanted:**
- One command to clear your tabs (mixed sources)
- All papers + articles searchable in Obsidian
- With AI-generated summaries + citation network

**What was built:**
- Foundation layer: config, models, state, Docker

**What needs to be coded:**
- 11 Python modules (~19.5 hours total)
- 9.5 hours blocking (core pipeline)
- 5 hours for full feature set
- 5 hours polish

**Start with:** grobid_processor.py → synthesis_generator.py → markdown_writer.py → arxiv_fetcher.py → orchestrator.py. Test end-to-end with one arXiv paper.

