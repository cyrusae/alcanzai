# Jargon Density: Heavy

## Strategy
Use technical terminology as standard language with minimal glossing. Assume reader knows field conventions and vocabulary.

**Philosophy**: Reader is actively working in the field or has deep familiarity. Efficiency matters. Use jargon freely without explanatory glosses—the technical terms are more precise and faster to read than plain language alternatives.

---

## When to Use This Register

✅ **Use Heavy Jargon when:**
- Actively working in the field, doing literature reviews
- Speed and efficiency are priorities
- Writing for expert audience (e.g., dissertation notes)
- Reader knows field vocabulary cold
- Creating quick reference notes for rapid scanning

❌ **Don't use Heavy Jargon when:**
- Returning to field after hiatus (use Selective for refresh)
- Reader needs to learn vocabulary (use Selective or None)
- Sharing notes with non-expert collaborators
- Interdisciplinary work where field-specific terms vary

---

## Core Principles

### 1. Technical Terminology as Default
Use precise jargon without explanation. Reader knows what these terms mean.

**Heavy**: "The study analyzes /æ/-tensing in pre-nasal environments using acoustic measurements of F1/F2 formants."

**Not Selective**: "The study analyzes /æ/-tensing (vowel becomes tighter and higher) in pre-nasal environments (before sounds like 'n' or 'm')..."
(Too slow for expert reader)

### 2. Abbreviations Without Expansion
Use standard field abbreviations freely after first mention.

**First mention**: "Recurrent Neural Networks (RNNs)"
**All subsequent**: "RNNs"

**Standard abbreviations** (after establishing in first section):
- VOT, F1/F2, ANOVA, RNN, BERT, GPT, fMRI, EEG, etc.
- Field-specific notation: /æ/-tensing, σ² (variance), β coefficients
- Methodology shortcuts: t-test, ANCOVA, multivariate regression

### 3. Assume Methodological Knowledge
No need to explain standard techniques or conventions.

**Heavy**: "Results: p < 0.05, d = 0.7, 95% CI [0.4, 1.0]"
(Reader knows what these mean)

**Not Heavy**: "Results showed p < 0.05 (statistically significant), with effect size d = 0.7 (medium-large) and 95% confidence intervals [0.4, 1.0] (range containing true effect)."
(Unnecessary for expert)

### 4. Field Conventions Assumed
Use standard notation, terminology, and framing from the field.

**Examples**:
- Linguistics: IPA notation, tree diagrams, feature matrices without legend
- ML: Architecture diagrams, loss curves, hyperparameter notation
- Statistics: Greek symbols, standard test names, assumption checks implied
- Critical theory: Theoretical frameworks cited by name, concepts used freely

---

## Examples Across Domains

### Linguistics/Phonetics
"Participants exhibited /æ/-tensing in pre-nasal environments (p < 0.001), consistent with Stage 3 NCVS progression. F1/F2 measurements show significant lowering of /ɑ/ (β = -120 Hz, SE = 25), with backing evident in apparent time. Social conditioning shows sharp age stratification and gender differentiation in line with curvilinear pattern."

### Machine Learning
"The transformer employs 12-layer encoder-decoder architecture with 8 attention heads per layer and 768-dimensional embeddings. Trained on 40GB corpus for 100k steps with Adam optimizer (lr = 1e-4, β₁ = 0.9, β₂ = 0.98). Achieved 28.4 BLEU on WMT'14 EN-DE, outperforming SOTA RNN baselines by 2+ BLEU. Inference latency reduced 60% vs sequential models."

### Sociolinguistics
"Corpus comprises 40 sociolinguistic interviews following Labovian protocol. Coding scheme tracks 8 phonological variables across 4 style contexts (careful speech, reading passage, word list, minimal pairs). Multivariate analysis controls for age, gender, SES, and network density. Results show vigorous change in progress with female speakers leading, consistent with linguistic market hypothesis."

### Statistics
"Employed mixed-effects logistic regression with random intercepts for subject and item. Fixed effects: condition (treatment/control), trial number, previous accuracy. Model comparison via likelihood ratio test favored maximal random effects structure (χ² = 45.2, df = 3, p < 0.001). Conditional R² = 0.68. Treatment effect: OR = 2.4, 95% CI [1.8, 3.2]."

### Critical Theory
"The text enacts epistemic violence through hegemonic discourse formations that naturalize power asymmetries. Foucauldian power/knowledge dynamics operate via disciplinary mechanisms that constitute subjectivity while foreclosing alterity. Deconstructive reading reveals constitutive outside and demonstrates how binary opposition structures the text's ontological commitments."

---

## When to Gloss (Rare Exceptions)

Even in Heavy Jargon, occasionally gloss if:

1. **Novel or emerging terminology** (< 5 years old, not yet standard)
   - "Using RLHF (Reinforcement Learning from Human Feedback), a technique introduced by Christiano et al. (2017)..."

2. **Ambiguous abbreviations** (same acronym used differently across subfields)
   - "We employ NMT (Neural Machine Translation, not Network Management Tools)..."

3. **Specialized sub-subfield terms** (even experts might not know)
   - "The model exhibits catastrophic forgetting (complete loss of previously learned patterns upon learning new tasks)..."

4. **Cross-disciplinary borrowing** (using terms from adjacent field)
   - "Drawing on Bourdieu's habitus (embodied dispositions), we analyze..."

**Rule of thumb**: If 80%+ of field experts know the term cold, no gloss needed.

---

## Integration with Output Tasks

### Quick Summaries
- Minimal glossing—assume vocabulary knowledge
- Dense information per sentence
- Standard abbreviations throughout
- Focus on results, contribution, novel findings

### Detailed Summaries
- Section-by-section technical breakdown
- Methodology details without explanation
- Results presented with full statistical notation
- Assume reader can interpret figures/tables

### Glossary Extraction
- Extract only truly specialized or novel terms
- Definitions assume field background
- Cross-reference related technical concepts
- Include standard notation and formulas

---

## Quality Checklist

Before finalizing synthesis in Heavy Jargon register, verify:

- [ ] Technical terminology used throughout without glossing
- [ ] Standard abbreviations used after first mention
- [ ] No explanation of common methodologies
- [ ] Field conventions and notation assumed
- [ ] Information density maximized (efficient reading)
- [ ] Results presented with full technical detail
- [ ] Reader can skim quickly for key findings
- [ ] No hand-holding or pedagogical asides

---

## Common Pitfalls

❌ **Occasional glossing**: Inconsistent switching between Heavy and Selective
**Fix**: Commit to Heavy—if glossing is needed, wrong register

❌ **Over-explanation**: Explaining why certain methods were chosen
**Fix**: State what was done; expert knows the why

❌ **Expanding every acronym**: Spelling out RNN, ANOVA, etc. every time
**Fix**: Expand once in first section, use abbreviation throughout

❌ **Accessible analogies**: "Think of attention like a spotlight..."
**Fix**: Reader doesn't need analogies; use technical description

❌ **Cautious phrasing**: "This might suggest..." when results are clear
**Fix**: Direct claims; reader can judge evidence themselves

---

## Examples of Good Heavy Jargon Flow

### Results section:

"Acoustic analysis reveals significant /æ/-tensing in pre-nasal contexts (t = 8.4, p < 0.001, d = 1.2). F1 lowering averages 85 Hz (SD = 32) in tensed vs. lax tokens. ANOVA shows main effects for phonological environment (F(3,156) = 42.1, p < 0.001, η² = 0.45) and speaker age (F(2,52) = 18.7, p < 0.001, η² = 0.28), with significant interaction (F(6,156) = 3.8, p = 0.002).

Regression model (adjusted R² = 0.71) identifies following-nasal as strongest predictor (β = -78, SE = 8.2, p < 0.001), controlling for word frequency and lexical class. Social factors show age grading (younger speakers exhibit more tensing, β = 12 per decade, SE = 2.1) and style stratification (careful speech shows less tensing, β = -15, SE = 4.5).

These patterns align with Stage 3 NCVS progression documented in Detroit (Gordon 2001) and Buffalo (Labov et al. 2006). Chicago data show more advanced backing of /ɑ/, suggesting regional variation in chain shift trajectory."

**What works**:
- Dense statistical reporting without explanation
- Technical linguistic terminology used freely
- Citations by name only (expert knows the papers)
- Efficient information delivery
- Expert can quickly extract key findings

---

## Efficiency Markers

Heavy Jargon should enable **rapid scanning**. Use:

- **Standard headings**: Methods, Results, Discussion (no creativity needed)
- **Statistical notation**: p < 0.05, β = 0.7, R² = 0.65 (no prose)
- **List format for complex info**: 
  - Model: 12-layer transformer
  - Training: 100k steps, Adam optimizer
  - Performance: 28.4 BLEU, +2.1 vs baseline
- **Tables/figures referenced**: "See Table 2" (not described in text)
- **Abbreviations liberally**: Once defined, use everywhere

---

## Notes for Implementation

- **Default register for**: Expert literature review, dissertation work, rapid reference
- **Word count**: Shortest register (high information density)
- **Tone**: Professional, technical, no pedagogical elements
- **Pacing**: Fast—reader can skim for key info

**Remember**: Heavy Jargon is optimized for speed and precision. An expert in the field should be able to extract key findings in 30 seconds of skimming. If they need to pause to understand terminology, you're not writing Heavy enough—or reader needs Selective instead.

This register is for **working in the field**, not learning the field.
