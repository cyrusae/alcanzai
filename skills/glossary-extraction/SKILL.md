---
name: glossary-extraction
description: Extract and define technical terms from academic papers as a structured glossary. Use when building a searchable vocabulary list from scholarly text, with definitions calibrated to the specified register.
---

# Glossary Extraction

Extract technical terms and produce structured glossary entries. Apply register settings for definition style.

## Output format

```xml
<glossary>

## [TERM]
**Definition**: [1-3 sentence definition in register-appropriate language]
**Example**: "[Sentence from the paper using this term, or constructed example]"
**Related**: [2-4 related terms from this paper or field, comma-separated]

---

</glossary>
```

## Term selection

**Include**:
- Technical terms specific to this field or paper
- Abbreviations/acronyms (define under the full term, cross-reference the acronym)
- Novel terms introduced or redefined by this paper
- Terms the paper uses as key concepts

**Exclude**:
- General academic vocabulary (hypothesis, methodology, correlation, framework)
- Terms already universally known to the paper's intended audience
- Author names, paper titles, venue names

## Definition depth by register

**None jargon**: Plain language first, technical term as appositive. "The process of [plain description]—what the field calls [term]—involves..."

**Selective jargon**: Technical definition using field vocabulary, with one-phrase gloss for the most specialized parts.

**Heavy jargon**: Full technical definition, no plain language scaffolding. Assume field knowledge.

**Hand-holding depth**: Include "Why this matters" — connect the term to its role in the paper's argument.

**Balanced depth**: Definition + one example. Skip the "why this matters" unless the term is central to the thesis.

**Assume-knowledge depth**: Compact definition only. One sentence max.

## Acronym handling

Define under the full term. Add a cross-reference entry:

```
## RNN → See Recurrent Neural Network
```

## Quality checks

- Definitions accurate to how the paper uses the term (not just dictionary definition)
- Example sentences are actual quotes from the paper where possible
- Related terms form a network (cross-references should be consistent)
- No circular definitions ("X is the process of doing X-ing")
