# Explanation Depth: Balanced (default)

Standard academic detail level. Assume reader knows the field but not this specific paper. Explain specialized methods briefly, state significance without extensive unpacking.

**Philosophy**: Reader is somewhat familiar with the area but not an active expert on this specific topic. Give enough context to follow the argument without over-explaining standard practice.

## Core rules

1. **Brief methodology explanation**: Explain specialized methods in one sentence; skip justification of standard practices.
   - "They used mixed-effects regression to account for the nested data structure (multiple trials per subject)."
   - Not: a paragraph explaining why mixed-effects is appropriate.

2. **State significance, don't belabor it**: One sentence on why a finding matters is enough.
   - "This suggests active language change in progress — younger speakers are leading the shift."

3. **Acknowledge limitations without extensive discussion**: Note major scope constraints briefly.

4. **Statistical results with minimal interpretation**: Report numbers + one-phrase interpretation.
   - "Results showed p < 0.05, with a medium-large effect size (d = 0.7), suggesting a substantial and reliable difference."

5. **Assume field vocabulary is known**: Gloss only genuinely specialized sub-field terms, not general field vocabulary.

## Contrast with adjacent settings

**vs. Hand-Holding**: Skip analogies unless the concept is genuinely opaque. Don't explain why researchers used ANOVA.

**vs. Assume-Knowledge**: Do interpret results briefly. Don't just report "p < 0.001" — add "suggesting..." in one phrase.

## Example

**ML (Balanced)**: "The transformer employs multi-head self-attention (parallel attention mechanisms) with positional encoding to process all tokens simultaneously rather than sequentially. On WMT'14 EN-DE, it achieves 28.4 BLEU — 2.1 points above previous state-of-the-art — while also reducing training time substantially. The primary gains come from improved parallelization and better long-range dependency modeling."

**Sociolinguistics (Balanced)**: "Data from 40 sociolinguistic interviews following Labovian methodology. Analysis reveals significant age stratification: younger speakers show more /æ/-tensing in pre-nasal environments (p < 0.001, d = 1.2), suggesting active change in progress. Patterns align with Stage 3 Northern Cities Vowel Shift as documented in Detroit, though Chicago shows more advanced /ɑ/-backing."

## Watch for

- Balanced is the DEFAULT depth for most alcanzai synthesis
- Enough context to understand the work; not so much that the notes become textbooks
