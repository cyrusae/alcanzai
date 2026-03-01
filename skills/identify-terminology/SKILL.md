---
name: identify-terminology
description: Identify and classify technical terminology in academic papers. Use when determining which terms need glossing, assessing domain and jargon density, and tracking acronyms for consistent handling.
---

# Identify Terminology

## Term classification

**Universal academic vocabulary** — no glossing needed in any register:
- hypothesis, methodology, corpus, analysis, paradigm, framework, empirical, theoretical

**Field-standard vocabulary** — gloss in none/selective registers, not in heavy:
- Terms all practitioners in this field know without explanation
- Examples: BERT, transformer (ML); p-value, ANOVA (stats); code-switching (linguistics)

**Specialized sub-field vocabulary** — gloss in all registers except assume-knowledge:
- Terms requiring specific coursework or deep specialization
- Examples: /æ/-tensing, F1/F2 formants (phonetics); epistemic violence, habitus (critical theory)

**Novel/paper-specific terms** — always gloss on first use:
- Terms introduced or redefined by this paper
- Examples: names of new models, new frameworks, new taxonomies

## Acronym tracking

First use: expand in full with brief explanation. Format: `ACRONYM (Full Name — what it means)`
Subsequent uses: acronym only.

Track which acronyms have been introduced. Don't re-expand.

## Domain detection

From title/abstract keywords, identify primary domain:
- **ML/AI**: neural, learning, model, transformer, attention, training, inference
- **NLP**: language, text, translation, parsing, NLU, generation
- **Computer vision**: image, visual, detection, segmentation, pixel
- **Linguistics**: phonology, syntax, morphology, pragmatics, corpus, sociolinguistics
- **Statistics**: regression, Bayesian, significance, variance, distribution
- **Critical theory**: power, discourse, hegemony, subjectivity, ideology

Domain affects which terms count as "field-standard" vs. "specialized."

## Jargon density assessment

Assess the paper's own register to calibrate synthesis:
- Papers that write "utilize" and avoid contractions throughout → likely higher-jargon audience
- Papers with accessible prose in introduction → broader audience intended
- Nature/Science papers → interdisciplinary, accessible style appropriate
- Workshop/conference papers → expert audience assumed
