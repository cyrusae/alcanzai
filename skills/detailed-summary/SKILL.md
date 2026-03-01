---
name: detailed-summary
description: Generate detailed section-by-section summaries of academic papers. Use when creating comprehensive notes that break down methods, results, and implications with more depth than a quick summary provides.
---

# Detailed Summary

Generate a structured section-by-section breakdown. Apply register settings from register-controller throughout.

## Output format

```xml
<detailed_summary>

## Paper: [Title]
**Authors**: [Authors] | **Year**: [Year] | **Venue**: [Venue if available]

---

## Problem and Contribution

[2-4 sentences: what gap/problem, what this paper contributes, why it matters]

---

## Methods

[3-6 sentences: study design, dataset/sample, analysis approach, key implementation details]

---

## Results

[3-6 sentences: primary findings with specifics, statistical detail appropriate to register, secondary findings if notable]

---

## Discussion and Implications

[2-4 sentences: what authors claim the findings mean, how it connects to prior work, limitations acknowledged]

---

## Key Concepts

[Same as quick-summary key_concepts: 5-8 specific + 2-5 general, comma-separated, lowercase hyphenated]

---

## Quick Grab

**Thesis**: [One sentence — main claim]
**Why this matters**: [One sentence — contribution to the field]
**Biggest limitation**: [One sentence — main scope constraint]
**Memorable quote**: "[Exact quote from paper]"

</detailed_summary>
```

## Section guidance

**Problem and Contribution**: State the gap in literature (what wasn't known/solved before), then the specific contribution. Avoid just restating the abstract.

**Methods**: Detail appropriate to register (hand-holding: explain why choices were made; assume-knowledge: just the specs). Always include: study design, sample/dataset size, analysis method.

**Results**: Lead with primary finding. Include quantitative results appropriate to register. Note direction and magnitude, not just significance.

**Discussion and Implications**: Distinguish what the data show (results) from what the authors infer (discussion). Include at least one acknowledged limitation.

**Quick Grab section**: Always present regardless of register. The thesis/limitation/quote should be scannable even when the main sections are dense.

## Handling different paper types

**Empirical**: Standard IMRaD structure maps directly to Methods/Results/Discussion sections.

**Theoretical**: Methods → "Argument structure and approach"; Results → "Core claims and supporting arguments".

**Review/Survey**: Methods → "Search/inclusion criteria and taxonomy"; Results → "Key patterns across reviewed literature"; Discussion → "Identified gaps and recommendations".

## Register interaction

Jargon and depth settings from register-controller have the most impact on Methods and Results sections. The Quick Grab section should always be readable regardless of register — make it accessible even in heavy/assume-knowledge mode.
