# Detailed Summary

## Purpose

Generate comprehensive, section-by-section breakdown of academic papers for deep understanding. Produces structured analysis of each major section with connections between them.

**Use this skill when:** You need to deeply understand a paper's methodology, follow the argument step-by-step, or create detailed reading notes to share or reference.

---

## Dependencies

- Uses `understand-academic-text` for structure recognition
- Uses `extract-arguments` for per-section analysis
- Uses `identify-terminology` for term extraction
- Uses register settings for explanation depth and jargon handling

---

## Three-Pass Architecture

This is a **multi-step process** designed for caching efficiency and systematic coverage:

**Pass 1:** Extract Structure (identify sections)
**Pass 2:** Summarize Each Section (detailed breakdown)
**Pass 3:** Synthesize Connections (how sections relate)

Each pass builds on the previous, with results cached for efficiency.

---

## Pass 1: Extract Structure

### Purpose
Map the paper's organization before detailed analysis.

### Process Checklist

- [ ] Read through entire paper to identify major sections
- [ ] Note page ranges for each section
- [ ] Determine purpose of each section
- [ ] Identify subsections within major sections
- [ ] Distinguish main content from appendices/references
- [ ] Flag any non-standard organization

### Output Format

Generate JSON structure:

```json
{
  "paper_structure": {
    "total_pages": 12,
    "organization_type": "IMRaD",
    "sections": [
      {
        "title": "Introduction",
        "pages": "1-3",
        "purpose": "Motivate problem, review prior work, state contribution",
        "subsections": [
          "Background on attention mechanisms",
          "Limitations of RNNs",
          "Our contribution"
        ],
        "estimated_importance": "high"
      },
      {
        "title": "Model Architecture",
        "pages": "3-6",
        "purpose": "Describe Transformer architecture in detail",
        "subsections": [
          "Encoder structure",
          "Decoder structure",
          "Attention mechanisms",
          "Positional encodings"
        ],
        "estimated_importance": "high"
      },
      {
        "title": "Experiments",
        "pages": "6-9",
        "purpose": "Present translation tasks and results",
        "subsections": [
          "Datasets (WMT 2014)",
          "Training details",
          "Results and comparisons"
        ],
        "estimated_importance": "medium"
      },
      {
        "title": "Analysis",
        "pages": "9-11",
        "purpose": "Interpret results and visualize attention",
        "subsections": [
          "Attention visualization",
          "Model variations (ablation study)"
        ],
        "estimated_importance": "medium"
      },
      {
        "title": "Conclusion",
        "pages": "11-12",
        "purpose": "Summarize contribution and future work",
        "subsections": [],
        "estimated_importance": "high"
      }
    ]
  }
}
```

### Section Purpose Categories

**STEM/IMRaD papers:**
- Introduction: Context + contribution
- Methods: How research was conducted
- Results: Findings presented
- Discussion: Interpretation + implications

**Humanities papers:**
- Introduction: Argument + framework
- Background: Context + prior scholarship
- Analysis (multiple sections): Close reading + interpretation
- Conclusion: Synthesis + implications

**Social science:**
- Introduction: Research question
- Literature review: Prior work
- Theory: Conceptual framework
- Methods: Data collection + analysis approach
- Findings: Results
- Discussion: Interpretation + implications

### Estimating Importance

**High importance sections:**
- Introduction (sets up everything)
- Main findings/analysis (core contribution)
- Conclusion (synthesizes contribution)

**Medium importance:**
- Methods (important for understanding but not the contribution)
- Background/literature review (context but not novel)

**Lower importance:**
- Appendices (supplementary details)
- Acknowledgments (not content)

### Special Cases

**Non-standard organization:**
- Note deviations from expected structure
- Example: "Theoretical paper with no empirical results section"
- Adjust expectations accordingly

**Very long papers (>30 pages):**
- May need to group related sections
- Focus on major divisions (Introduction, Part I, Part II, Conclusion)
- Note chapter-level organization

**Very short papers (<5 pages):**
- Sections may be implicit rather than explicit
- Identify functional sections even without headers

---

## Pass 2: Summarize Each Section

### Purpose
Create detailed breakdown of each major section identified in Pass 1.

### Process Checklist (Per Section)

- [ ] Read section completely
- [ ] Identify 2-3 key points
- [ ] Extract technical terms introduced
- [ ] Note claims vs evidence vs speculation
- [ ] Identify connections to other sections
- [ ] Find notable quotes or claims
- [ ] Assess how this advances the overall argument

### Output Format (Per Section)

Generate XML for each section:

```xml
<section id="intro" importance="high">
  <title>Introduction</title>
  <pages>1-3</pages>
  
  <purpose>
  This section motivates the study of self-attention mechanisms by reviewing 
  limitations of RNN-based sequence models and stating the paper's contribution.
  </purpose>
  
  <key_points>
    <point priority="1">
    RNNs are inherently sequential, preventing parallelization during training, 
    which limits their applicability to very long sequences.
    </point>
    <point priority="2">
    Prior work on attention mechanisms used them in conjunction with RNNs, 
    not as standalone components.
    </point>
    <point priority="3">
    This paper proposes the Transformer, an architecture relying entirely on 
    attention mechanisms without any recurrence, achieving SOTA results on 
    translation tasks while being more parallelizable.
    </point>
  </key_points>
  
  <technical_terms>
    <term>
      <name>self-attention</name>
      <definition>Mechanism where each position in a sequence attends to all 
      positions to compute representations</definition>
      <importance>core</importance>
    </term>
    <term>
      <name>RNN (Recurrent Neural Network)</name>
      <definition>Neural network architecture that processes sequences sequentially, 
      maintaining hidden state</definition>
      <importance>background</importance>
    </term>
    <term>
      <name>SOTA (State of the Art)</name>
      <definition>Best currently known performance on a benchmark</definition>
      <importance>background</importance>
    </term>
  </technical_terms>
  
  <argument_type>Empirical + Methodological</argument_type>
  
  <evidence_presented>
    <evidence>Citation to prior RNN work showing sequential bottleneck</evidence>
    <evidence>Benchmark results table (previewed, detailed later)</evidence>
  </evidence_presented>
  
  <connections>
    <backward>Builds on prior attention mechanism work (Bahdanau et al. 2015)</backward>
    <forward>Sets up architecture description in Section 2</forward>
    <forward>Motivates experimental design in Section 3</forward>
  </connections>
  
  <notable_claims>
    <claim type="thesis">
    "The Transformer is the first transduction model relying entirely on 
    self-attention to compute representations."
    </claim>
    <claim type="performance">
    "Our model achieves 28.4 BLEU on WMT 2014 English-German translation."
    </claim>
  </notable_claims>
  
  <methodology_notes>
  N/A - Introduction section
  </methodology_notes>
  
  <interpretation>
  The introduction establishes that sequential processing is a bottleneck in 
  current models and positions self-attention as the solution. Strong motivation 
  through both theoretical argument (parallelization) and empirical promise 
  (SOTA results).
  </interpretation>
</section>
```

### Key Points Guidelines

**Priority ranking:**
1. Most important/novel point
2. Supporting or context point
3. Additional detail or implication

**Quality criteria:**
- Each point should be 1-3 sentences
- State claims explicitly (what does this section argue?)
- Include specific details (numbers, examples, comparisons)
- Use accessible language with technical terms glossed

**Example of good key point:**
> The Transformer uses multi-head attention (parallel attention calculations from different learned perspectives), allowing the model to attend to information from different representation subspaces—for instance, one head might focus on syntactic dependencies while another focuses on semantic relationships.

**Example of weak key point:**
> The model uses attention mechanisms which are important.
(Too vague, no specifics, doesn't explain why important)

### Technical Terms Extraction

**Importance levels:**
- **Core:** Central to this paper's contribution
- **Methodological:** Important for understanding approach
- **Background:** Context or prior work
- **Passing:** Mentioned briefly, not central

**When to include a term:**
- Introduced for the first time in THIS section
- Central to understanding the section
- Technical enough to benefit from definition

**When to skip:**
- Already defined in previous section
- Obvious from context
- Not technical (general academic vocabulary)

### Evidence vs Claims vs Interpretation

**Distinguish carefully:**

**Claims** (what author asserts):
- "Self-attention allows complete parallelization"
- "Transformers outperform RNNs on translation"

**Evidence** (what supports claims):
- "Training time reduced from 3 days to 12 hours"
- "BLEU score: 28.4 vs 26.0 baseline"

**Interpretation** (what evidence means):
- "This speed improvement makes training on larger datasets feasible"
- "The performance gain suggests attention captures dependencies RNNs miss"

### Connections Tracking

**Backward connections:**
- What prior sections does this build on?
- What concepts/findings are referenced?

**Forward connections:**
- What does this set up for later?
- What questions does this raise that later sections answer?

**Example:**
> Methods section sets up statistical tests used in Results. Results section provides data that Discussion interprets. Discussion references both Methods (for caveats) and Introduction (for theoretical implications).

---

## Pass 3: Synthesize Connections

### Purpose
Show how sections build on each other and construct the overall argument.

### Process Checklist

- [ ] Review all section summaries from Pass 2
- [ ] Identify narrative arc (how does argument progress?)
- [ ] Note which sections are most critical
- [ ] Find thematic connections across sections
- [ ] Assess argument strength and coherence
- [ ] Highlight any gaps or weaknesses

### Output Format

```xml
<synthesis>
  <narrative_arc>
  The paper follows a classical empirical pattern: Introduction motivates the 
  problem (RNN sequential bottleneck) and proposes solution (self-attention). 
  Architecture section provides technical implementation details. Experiments 
  validate that the approach works empirically. Analysis section interprets 
  why it works (attention heads specialize). Conclusion synthesizes contribution 
  and suggests future directions.
  </narrative_arc>
  
  <critical_path>
  The argument's critical path runs through:
  1. Introduction's theoretical motivation (parallelization)
  2. Architecture's technical feasibility (how self-attention works)
  3. Experiments' empirical validation (SOTA results)
  
  Without any one of these, the argument fails. Analysis is valuable but 
  supplementary—the core claim would stand even without attention visualization.
  </critical_path>
  
  <section_importance_ranking>
    <section rank="1">Introduction - sets up entire argument</section>
    <section rank="2">Architecture - technical core of contribution</section>
    <section rank="3">Experiments - empirical validation</section>
    <section rank="4">Analysis - interpretability insight</section>
    <section rank="5">Conclusion - synthesis (no new info)</section>
  </section_importance_ranking>
  
  <thematic_connections>
    <theme name="parallelization">
    Introduced in Introduction as motivation, implemented in Architecture 
    via self-attention, validated in Experiments via training time comparisons, 
    explained in Analysis via attention visualization.
    </theme>
    <theme name="performance-interpretability-tradeoff">
    Architecture achieves high performance but Analysis reveals model still 
    learns interpretable patterns (attention heads specialize), challenging 
    assumption that high performance requires opacity.
    </theme>
  </thematic_connections>
  
  <argument_strength>
  Strong argument with solid empirical validation. The theoretical motivation 
  (parallelization) is clearly stated, implementation is thoroughly described, 
  and results convincingly demonstrate superiority over baselines. Ablation 
  studies strengthen claims by showing each component matters.
  
  Minor weakness: Limited exploration of failure cases or limitations. Paper 
  briefly mentions very long sequences might benefit from local attention but 
  doesn't deeply investigate this.
  </argument_strength>
  
  <key_insights_across_sections>
    <insight>
    Self-attention alone is sufficient—no recurrence needed (Introduction claim 
    + Architecture implementation + Experiments validation)
    </insight>
    <insight>
    Attention heads learn specialized roles without explicit supervision (Analysis 
    discovery, not anticipated in Introduction)
    </insight>
    <insight>
    Parallelization enables practical training on large datasets (Methods 
    efficiency + Experiments speed comparisons)
    </insight>
  </key_insights_across_sections>
  
  <reading_strategy_recommendation>
  For deep understanding: Read Introduction → Architecture (focus on attention 
  mechanism) → Experiments (focus on results) → Analysis (interpretability).
  
  For quick understanding: Read Introduction + Conclusion, skim Architecture 
  diagrams, check Experiments tables.
  
  For methodology: Deep read Architecture + Experiments sections, skim others.
  </reading_strategy_recommendation>
</synthesis>
```

### Narrative Arc Patterns

**STEM empirical papers:**
Problem → Solution → Implementation → Validation → Interpretation

**Humanities papers:**
Question → Framework → Analysis → Evidence → Synthesis

**Theoretical papers:**
Critique of prior work → New framework → Implications → Applications

### Critical Path Identification

**Ask:** If I removed Section X, would the argument still work?

**Critical sections:**
- Cannot be removed without argument collapsing
- Contain essential claims or evidence
- Usually: Introduction, main analysis, conclusion

**Supporting sections:**
- Strengthen argument but not essential
- Provide additional validation or context
- Examples: Ablation studies, additional experiments

### Thematic Connection Mapping

**Identify themes that span sections:**
- Track how a concept evolves through the paper
- Note where theme is introduced vs developed vs concluded
- Show interdependencies

**Example:**
> "Interpretability theme: Mentioned as open question in Introduction, partially addressed by attention visualization in Analysis, suggested as future work in Conclusion"

---

## Complete Output Structure

Final deliverable combines all three passes:

```json
{
  "detailed_summary": {
    "metadata": {
      "paper_title": "...",
      "total_pages": 12,
      "organization_type": "IMRaD",
      "processing_date": "2024-01-10"
    },
    
    "structure": { /* Pass 1 JSON */ },
    
    "section_summaries": [
      /* Pass 2 XML for each section */
    ],
    
    "synthesis": { /* Pass 3 XML */ }
  }
}
```

---

## Caching Strategy

This three-pass design enables efficient caching:

### Pass 1 (Extract Structure)
**Input:** Full paper text (~20k tokens) + skill (~2k tokens)
**Output:** Structure JSON (~1k tokens)
**Cache:** Structure JSON for Passes 2 & 3

### Pass 2 (Summarize Sections)
**Per section:**
**Input:** Skill (~2k) + Structure (~1k, cached) + Section text (~4k)
**Output:** Section summary (~1k)
**Cache:** All section summaries for Pass 3

### Pass 3 (Synthesize)
**Input:** Skill (~2k) + Structure (~1k, cached) + All summaries (~5k, cached)
**Output:** Synthesis (~1k)
**Total cached:** ~6k tokens reused in Pass 3

**Cost savings:** ~60% reduction vs sending full paper multiple times

---

## Register Integration

### Jargon Density
- **None:** Explain technical terms in key points
- **Selective:** Gloss terms in technical_terms section, use freely in key points
- **Heavy:** Assume knowledge, minimal glossing

### Sentence Structure
- **Conversational:** Natural flow in key points and interpretation
- **Mixed:** Balance formal and accessible
- **Formal:** Academic register throughout

### Explanation Depth
- **Hand-holding:** More context in purpose and interpretation sections
- **Balanced:** Standard detail level
- **Assume-knowledge:** Minimal context, focus on novel content

---

## Domain Adaptations

### STEM Papers
- Emphasize methodology details in Methods section
- Include specific metrics and statistical tests in Results
- Note experimental design choices

### Humanities Papers
- Track argument development through analysis sections
- Note textual evidence and close reading strategies
- Identify theoretical framework application

### Social Science Papers
- Document research design decisions
- Note sampling and data collection procedures
- Track how findings connect to theory

---

## Quality Checks

After completing all three passes:

✅ **Completeness:** Every major section summarized?
✅ **Clarity:** Could someone understand the paper from this?
✅ **Connections:** Are relationships between sections clear?
✅ **Balance:** Appropriate detail for each section's importance?
✅ **Accuracy:** Faithful to paper's actual content?
✅ **Usefulness:** Would this help you deeply understand the paper?

---

## Common Pitfalls

❌ **Too much detail:** Section summaries shouldn't be as long as sections themselves
❌ **Missing connections:** Sections analyzed in isolation without showing relationships
❌ **Repeating content:** Key points shouldn't just copy abstract or conclusion
❌ **Ignoring structure:** Not using Pass 1 structure to guide Pass 2
❌ **Weak synthesis:** Pass 3 should go beyond listing sections to show how they work together

---

## Use Cases

**When to use detailed summary:**
- Learning a new subfield (need deep understanding)
- Preparing to implement a method (need technical details)
- Writing literature review (need comprehensive notes)
- Teaching/explaining paper to others (need structured breakdown)
- Paper is complex/dense (quick summary insufficient)

**When quick summary suffices:**
- Familiar territory (just need reminder)
- Skimming for relevance (deciding whether to read deeply)
- Building bibliography (need tags and main point)
- Paper is short/straightforward (no need for section breakdown)

---

## Notes for Implementation

- Process sections in order (easier to track connections)
- Use structure from Pass 1 as scaffolding for Pass 2
- Cache aggressively (structure + sections for synthesis)
- Adjust detail level based on section importance
- Make connections explicit (don't assume reader sees them)
- Include enough specifics to be useful (numbers, examples, quotes)

Remember: This is for DEEP understanding. Take time to analyze each section thoroughly. The three-pass structure prevents overwhelm while ensuring comprehensive coverage.
