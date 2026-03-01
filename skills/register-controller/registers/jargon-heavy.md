# Jargon Density: Heavy

Technical terminology as standard language. No glossing. Assume reader knows field vocabulary cold.

**Philosophy**: Efficiency. The technical terms are more precise and faster to read than plain alternatives. Reader is actively working in this area.

## Core rules

1. **No glossing**: Write for the expert reader. If they need it glossed, they're using the wrong register.

2. **Abbreviations after first mention**: Expand once ("Recurrent Neural Networks (RNNs)"), then use the abbreviation throughout.

3. **Assume methodological knowledge**: No explanation of standard techniques.
   - Write: "Results: p < 0.05, d = 0.7, 95% CI [0.4, 1.0]"
   - Not: "...meaning there's less than a 5% chance..." etc.

4. **Field conventions assumed**: IPA notation, Greek symbols, standard test names, theoretical framework citations — all without explanation.

## Rare exceptions for glossing

Gloss even in Heavy when:
- Novel/emerging terminology (< 5 years old, not yet standard)
- Ambiguous abbreviations (same acronym means different things across subfields)
- Cross-disciplinary borrowing ("Drawing on Bourdieu's habitus (embodied dispositions)...")

**Rule of thumb**: If 80%+ of field experts know the term cold, no gloss needed.

## Examples

**ML (Heavy)**: "Transformer: 12-layer enc-dec, 8 heads/layer, d_model=768. Adam optimizer (lr=1e-4, β₁=0.9, β₂=0.98), 100k steps. WMT'14 EN-DE: 28.4 BLEU (+2.1 vs SOTA). 60% latency reduction vs. RNN baselines."

**Linguistics (Heavy)**: "/æ/-tensing in pre-nasal environments: t=8.4, p<0.001, d=1.2. F1 lowering averages 85 Hz (SD=32). Age stratification significant F(2,52)=18.7, p<0.001, η²=0.28. Consistent with Stage 3 NCVS."

## Watch for

- Maximum information density, minimum explanatory overhead
- Expert should extract key findings in 30 seconds of skimming
- Heavy jargon is for working in the field, not learning it
