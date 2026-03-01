# Jargon Density: Heavy

## Strategy
Use technical terminology as primary language with minimal glossing. Assume reader knows field conventions and standard terms.

**When to use:**
- Expert audience (active researchers in field)
- Literature reviews (efficient technical summaries)
- Rapid reading of familiar material
- Writing for publication or professional contexts
- Speed matters more than accessibility

---

## Core Principle

**Term only, no gloss**

Think: Direct technical communication

NOT: "Hand-holding with explanations"

---

## Format Pattern

```
technical-term [no parenthetical]
```

### Examples

**Phonetics:**
✅ "Analyzed F1/F2 formants for alveolar fricatives"
❌ "Analyzed formants (resonant frequencies of vocal tract)"

**Machine Learning:**
✅ "Transformer with 12 attention heads, 768-dimensional embeddings"
❌ "Transformer (attention-based architecture) with embeddings (vector representations)"

**Critical Theory:**
✅ "Foucauldian genealogy reveals epistemic ruptures"
❌ "Genealogy (historical analysis of power/knowledge)"

---

## When to Gloss (Rarely)

### Novel Methods/Concepts
Only if THIS paper introduces something new

"Applied novel regularization technique (L1 + L2 hybrid penalty on layer-specific activations)"
- Gloss because it's novel, not standard

### Genuine Ambiguity
Only when term could have multiple meanings in context

"Embedding (word-level, not sentence-level)"
- Disambiguates which type

### Paper-Specific Usage
When author uses term non-standardly

"Fine-tuning (here: only final two layers, not full network)"
- Clarifies departure from convention

### Never Gloss

**Standard field terminology:**
- Everyone in field knows these
- Examples: "regression," "p-value," "corpus," "hegemony"

**Methods from textbooks:**
- Established techniques
- Examples: "t-test," "forced alignment," "close reading"

**Common architectures/models:**
- Widely known in field
- Examples: "Transformer," "BERT," "RNN"

**Previously established concepts:**
- From prior influential work
- Examples: "Chomskyan syntax," "Foucauldian power," "Bayesian inference"

---

## Efficiency Markers

### Dense Technical Language

Use field-standard phrasing without explanation

**Good:**
"Applied Transformer encoder with positional encodings, trained via Adam optimizer (lr=1e-4, β₁=0.9, β₂=0.999) for 100k steps."

**Too verbose:**
"Used a Transformer architecture (attention-based model) with positional information added (positional encodings) and trained it using the Adam optimization algorithm (a variant of stochastic gradient descent) with specific hyperparameters."

### Abbreviations Without Expansion

Use standard abbreviations freely after field adoption

**Good:**
- "RNN struggled with long sequences, LSTM improved, Transformer solved"
- "Applied NLP techniques to sociolinguistic data"
- "Used IMRaD structure"

**Don't do:**
- "RNN (Recurrent Neural Network)"
- "NLP (Natural Language Processing)"
- First occurrence = use abbreviation directly

### Technical Precision

Prefer precise technical term over accessible synonym

**Good:**
- "Multivariate logistic regression"
- "Spectrotemporal analysis"
- "Dialectological variation"

**Avoid:**
- "Statistical method analyzing multiple factors"
- "Sound analysis over time"
- "Regional language differences"

---

## Examples by Domain

### Linguistics (Heavy)

"Examined /æ/-tensing in Philadelphia English via apparent time methodology. F1/F2 measurements showed significant correlation with social class (p<0.001). Style-shifting evident across formality levels, consistent with Labovian sociolinguistic theory."

**What makes this Heavy:**
- Phonetic notation (/æ/)
- Assumed knowledge of formants (F1/F2)
- Standard methods unnamed (how F1/F2 measured)
- Reference to theory without explanation
- Statistical notation without gloss

### Machine Learning (Heavy)

"Transformer architecture: 12-layer encoder, 768-dim embeddings, 12 attention heads. Training: Adam (lr=1e-4, warmup=4k steps, dropout=0.1). Evaluation: BLEU on WMT 2014 En→De. Results: 28.4 BLEU, outperforming RNN baseline (26.0)."

**What makes this Heavy:**
- Hyperparameters without explanation
- Standard metrics assumed (BLEU)
- Architecture details unglossed
- Notation conventions (→ for translation direction)

### Critical Theory (Heavy)

"Foucauldian genealogy traces disciplinary power's epistemic conditions. Panopticon instantiates surveillance-normalization nexus. Biopower operates through population-level interventions, distinct from sovereign juridical power."

**What makes this Heavy:**
- Theoretical vocabulary assumed
- Concepts from specific theorist (Foucault)
- Assumed knowledge of framework
- Dense conceptual relationships

---

## Handling Specialized Notation

### Mathematical/Statistical
Use standard notation without explanation

**Good:**
- "p < 0.05"
- "r² = 0.87"
- "F(2,47) = 12.3"
- "β = 0.42, SE = 0.08"

**Not:**
- "p-value (probability of result under null hypothesis) less than 0.05"

### Phonetic/Linguistic
Use IPA and standard conventions

**Good:**
- "/p/ vs /b/ differ in VOT"
- "Raised /æ/ before nasals"
- "C₁VC₂ syllable structure"

**Not:**
- "/p/ (voiceless bilabial stop) vs /b/ (voiced bilabial stop)"

### Technical Abbreviations
Use field-standard abbreviations freely

**Good:**
- "CNN outperformed RNN on CV tasks"
- "ANOVA revealed main effect of condition"
- "DOI: 10.1162/coli_a_00123"

**Not:**
- Expanding every acronym on first use

---

## When Heavy Register Fails

### Cross-Disciplinary Papers
If paper bridges multiple fields, may need selective glossing

**Problem:**
"Applied NLP transformers to sociolinguistic corpus"
- NLP people know "transformers"
- Sociolinguists know "corpus"
- Might not know each other's terms

**Solution:**
Brief disambiguation when fields collide, otherwise Heavy

### Novel Frameworks
If paper proposes entirely new approach, need more explanation

**Problem:**
Pure Heavy assumes shared baseline—new paradigms need establishment

**Solution:**
Use Heavy for established concepts, add explanation for novel contributions

### Genuinely Obscure Terms
Even experts might not know hyper-specialized terminology

**Problem:**
"Applied Sørensen-Dice coefficient for evaluation"
- Obscure metric even in ML

**Solution:**
Brief gloss: "Sørensen-Dice coefficient (F1 variant for overlapping sets)"

---

## Comparison Across Registers

### Same Content, Three Registers

**None (Accessible):**
"The researchers looked at how people in Philadelphia pronounce the vowel in words like 'cat' and 'bad.' They found that how you pronounce this sound correlates with social class—working-class speakers tend to raise the vowel (make it sound more like the vowel in 'key'), while middle-class speakers don't do this as much. Linguists call this /æ/-tensing, and it's a classic example of sociolinguistic variation."

**Selective (Learning):**
"The study examined /æ/-tensing (raising of the vowel in 'cat,' 'bad' to sound more like 'ee') in Philadelphia English. Acoustic analysis of F1/F2 formants (resonant frequencies indicating tongue position) showed correlation with social class. The phenomenon exemplifies sociolinguistic variation (systematic differences in language use across social groups)."

**Heavy (Expert):**
"Analyzed /æ/-tensing in Philadelphia English via F1/F2 measurements. Significant correlation with social class (p<0.001). Classic sociolinguistic variable showing style-shifting across formality registers."

---

## Quality Checks

When writing in Heavy register, verify:

✅ **Efficient:** Conveys maximum information in minimum words
✅ **Precise:** Uses exact technical terminology
✅ **Standard:** Follows field conventions for notation/abbreviation
✅ **Assumes knowledge:** Doesn't explain basics
✅ **Focused:** Emphasizes novel content, assumes baseline understanding
✅ **Professional:** Publication-quality technical communication

---

## Common Pitfalls

❌ **Over-explaining:** Glossing standard terms
- Bad: "Used p-values (probability of results under null hypothesis)"
- Good: "p < 0.05"

❌ **Avoiding technical terms:** Using vague synonyms
- Bad: "The model's learning method" instead of "gradient descent"
- Good: Direct technical terminology

❌ **Inconsistent abbreviation:** Mixing expanded and abbreviated forms
- Bad: "RNN (Recurrent Neural Network) vs CNN"
- Good: "RNN vs CNN" (both abbreviated)

❌ **Glossing for non-experts:** Imagining general audience
- Bad: "Attention mechanism (how model focuses on relevant input)"
- Good: "Attention mechanism" (no gloss)

---

## Benefits of Heavy Register

✅ **Efficiency:** Convey information quickly
✅ **Precision:** Exact technical language
✅ **Professionalism:** Publication-ready summaries
✅ **Respect for reader:** Assumes expertise
✅ **Density:** Maximum information per word
✅ **Speed:** Rapid scanning for experts

---

## When to Use

**Ideal for:**
- Literature reviews
- Expert consultations
- Professional writing
- Rapid scanning of familiar papers
- Technical documentation
- Grant writing
- Academic presentations

**Not ideal for:**
- Learning new subfield (use Selective)
- Teaching/explaining to others (use Selective or None)
- Interdisciplinary work (use Selective)
- Partner-shareable content (use None)
- Uncertain about reader expertise (default to Selective)

---

## Integration with Output Tasks

### In Quick Summaries
- Concise 2-3 sentence summaries
- Technical claims stated directly
- Assume reader knows context
- No expansion of acronyms after field-standard

### In Detailed Summaries
- Dense per-section breakdowns
- Standard methods mentioned without explanation
- Focus on novel contributions
- Hyperparameters listed without justification

### In Literature Reviews
- Comparative statements across papers
- Synthesis of technical findings
- Standard terminology throughout

---

## Notes for Implementation

- Most concise of three registers (~50% word count of None)
- Requires tracking field-standard vs novel terms
- When in doubt about whether to gloss, don't
- Assumes active researcher-level expertise
- Optimize for information density
- Respect reader's time and knowledge

Remember: Heavy register is not about being exclusionary—it's about efficient communication between experts who share extensive background knowledge. The brevity is a sign of respect for reader's expertise, not gatekeeping.
