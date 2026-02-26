# Explanation Depth: Assume-Knowledge

## Strategy
Minimal explanation. Assume reader knows field conventions, standard methods, and why things matter. Focus on findings, methods, and results—skip pedagogical scaffolding.

**Philosophy**: Reader is actively working in this area. They don't need methods explained or significance spelled out. Maximize information density, minimize explanatory overhead.

---

## When to Use This Register

✅ **Use Assume-Knowledge Depth when:**
- Actively researching this specific topic
- Creating quick reference notes for ongoing work
- Need to scan many papers efficiently
- Reader knows the literature and conventions cold
- Time/token efficiency is critical

❌ **Don't use Assume-Knowledge Depth when:**
- Somewhat familiar but not expert in this area (use Balanced)
- Returning after gap (use Balanced or Hand-Holding)
- May share notes with less specialized readers
- Learning the specific methodology being used

---

## Core Principles

### 1. State Methods, Don't Explain Them
Report what was done, skip justification and explanation.

**Assume-Knowledge**:
"40 sociolinguistic interviews, Labovian protocol, dual coding (92% agreement)."

**More explanation (Balanced)**:
"Data collected through 40 sociolinguistic interviews following Labovian methodology. Two independent coders achieved 92% agreement."

**Much more (Hand-Holding)**:
"Sociolinguistic interviews following Labov's methodology—designed to capture natural speech across multiple style contexts. Two trained coders independently marked each token, achieving 92% agreement, indicating reliable coding."

### 2. Report Results Without Interpretation
State findings with full statistical detail, let reader interpret.

**Assume-Knowledge**:
"Significant age effect (β = 12 Hz/decade, SE = 2.1, t = 5.7, p < 0.001). Phonological environment: F(3,156) = 42.1, p < 0.001, η² = 0.45."

**More interpretation (Balanced)**:
"Younger speakers show significantly more tensing (β = 12 Hz/decade, p < 0.001), suggesting active change in progress. Phonological environment also significant (F = 42.1, p < 0.001), with pre-nasal contexts showing strongest effect."

**Much more (Hand-Holding)**:
"The age effect is substantial and highly significant (β = 12 Hz/decade, p < 0.001). This means younger speakers average 12 Hz more tensing per decade of age. The p-value well below 0.05 indicates this isn't random chance. This pattern suggests active language change happening in real time..."

### 3. Skip Standard Practice Justification
Standard methods need no explanation or justification.

**Assume-Knowledge**:
"Mixed-effects model, maximal random effects structure."

**More justification (Balanced)**:
"Mixed-effects regression to account for nested data structure. Maximal random effects structure justified by LRT (χ² = 45.2, p < 0.001)."

**Much more (Hand-Holding)**:
"Mixed-effects regression accounts for the nested data structure (multiple trials per subject). The maximal random effects structure includes random intercepts for both subject and item, justified by likelihood ratio test showing significantly better fit..."

### 4. Dense Technical Detail
Include all relevant parameters, results, and specifications efficiently.

**Assume-Knowledge**:
"12-layer encoder, 8 heads/layer, d_model=768, d_ff=3072. Adam: lr=1e-4, β₁=0.9, β₂=0.98, ε=1e-9. 100k steps, warmup=4k. WMT'14 EN-DE: 28.4 BLEU (+2.1 vs SOTA)."

**Less dense (Balanced)**:
"12-layer encoder with 8 attention heads per layer and 768-dimensional embeddings. Trained with Adam optimizer for 100k steps. Achieved 28.4 BLEU on WMT'14 EN-DE, outperforming previous SOTA by 2.1 points."

### 5. Assume Familiarity with Literature
Reference prior work by name only, no explanation.

**Assume-Knowledge**:
"Patterns align with Gordon (2001) Detroit findings, contra Labov et al. (2006) Buffalo trajectory."

**More context (Balanced)**:
"Patterns align with Stage 3 NCVS progression documented in Detroit (Gordon 2001), though Chicago shows more advanced /ɑ/-backing compared to Buffalo (Labov et al. 2006)."

---

## Examples Across Domains

### Linguistics/Phonetics
**Assume-Knowledge**:
"/æ/-tensing in pre-nasal environments: t = 8.4, p < 0.001, d = 1.2. F1 Δ = 85 Hz (SD = 32) tensed vs. lax. ANOVA: environment F(3,156) = 42.1, p < 0.001, η² = 0.45; age F(2,52) = 18.7, p < 0.001, η² = 0.28; interaction F(6,156) = 3.8, p = 0.002.

Regression (adj. R² = 0.71): following-nasal β = -78 (SE = 8.2), age β = 12/decade (SE = 2.1), style β = -15 (SE = 4.5). Consistent with Gordon (2001) Stage 3 NCVS, but more advanced /ɑ/-backing than Detroit/Buffalo."

### Machine Learning
**Assume-Knowledge**:
"Transformer: 12-layer enc-dec, 8 heads, d_model=768, d_ff=3072, d_k=d_v=64. Positional encoding: sinusoidal. Dropout p=0.1. Residual connections + layer norm.

Training: Adam (lr=1e-4, β₁=0.9, β₂=0.98, ε=1e-9), warmup 4k steps, 100k total. Label smoothing ε_ls=0.1. Batch size 25k tokens.

WMT'14 EN-DE: 28.4 BLEU (base), 41.0 (big). EN-FR: 41.8 BLEU, SOTA. Inference: 60% latency reduction vs. RNN. Training: 12hr on 8 P100s (base), 3.5d (big)."

### Sociolinguistics
**Assume-Knowledge**:
"N=40 sociolinguistic interviews, working-class Philadelphia. Labovian protocol, 4 style contexts. 8 phonological variables, dual coding (κ=0.89).

All variables show significant age effects (p < 0.01), females lead. Change in progress, not age grading (no style×age interaction). Accelerated relative to Labov (2001) baseline. Network density correlates with innovation adoption (r=0.67, p < 0.001)."

### Statistics
**Assume-Knowledge**:
"GLMM: logit link, random intercepts (subject, item). Fixed: condition, trial, prev_acc. Maximal RE structure (LRT: χ²=45.2, df=3, p < 0.001).

Main effect condition: β=0.82, SE=0.15, z=5.47, p < 0.001. OR=2.27 [1.70, 3.03]. Conditional R²=0.68. Treatment effect robust to confound controls. Sensitivity analysis: effect persists across alternative model specifications."

---

## What to Report vs. What to Skip

### Always Report:
- **Full statistical details**: All relevant parameters, test statistics, effect sizes
- **Methods specifications**: Exact procedures, parameters, sample sizes
- **Key findings**: Results with numerical precision
- **Comparisons to prior work**: Citations showing relationship to literature

### Can Skip:
- **Why methods were chosen**: Assume reader knows standard practices
- **What statistics mean**: No explanation of p-values, confidence intervals
- **Broader implications**: Just findings, not significance discussion
- **Standard definitions**: No glossing of field terminology
- **Methodological justification**: Assume reader understands rationale

### The Test:
Is this information necessary for someone actively researching this topic to evaluate/use the work? If no, skip it.

---

## Integration with Jargon Density

### With None Jargon
Accessible terminology + minimal explanation (unusual pairing).

"Model processes all words simultaneously (parallel processing). 12 layers, 8 attention heads per layer. Trained on translation task, achieved 28.4 BLEU. 2+ points better than previous best. Training took 12 hours on 8 GPUs."

### With Selective Jargon
Technical vocabulary + minimal explanation.

"Transformer employs multi-head self-attention (8 heads per layer) across 12 encoder-decoder layers. Trained on WMT'14 EN-DE for 100k steps, achieving 28.4 BLEU (+2.1 vs. SOTA). Parallel processing enables 60% inference latency reduction versus sequential models."

### With Heavy Jargon
Expert terminology + minimal explanation (most common pairing).

"12-layer enc-dec, 8 heads/layer, d_model=768. Adam optimizer, 100k steps. WMT'14 EN-DE: 28.4 BLEU, +2.1 SOTA. 60% latency reduction vs. RNN baselines. Primary gains from parallel computation and improved long-range dependency modeling."

---

## Quality Checklist

Before finalizing synthesis in Assume-Knowledge Depth, verify:

- [ ] Methods stated without explanation or justification
- [ ] Full statistical details included (all parameters, test stats, effect sizes)
- [ ] Results reported without interpretive commentary
- [ ] No explanation of standard practices or conventions
- [ ] Citations by name only (no context on what they showed)
- [ ] Maximum information density (no pedagogical scaffolding)
- [ ] Appropriate for expert actively working in this area
- [ ] Could serve as quick reference during active research
- [ ] All details needed to evaluate work are present

---

## Common Pitfalls

❌ **Adding interpretive commentary**: "This suggests..." or "This matters because..."
**Fix**: Just state findings, let reader interpret

❌ **Explaining standard methods**: "Mixed-effects accounts for nested structure..."
**Fix**: "Mixed-effects model" is sufficient

❌ **Incomplete statistical reporting**: Giving p-values without effect sizes
**Fix**: Include all relevant stats: β, SE, test statistic, p, CI, effect size

❌ **Conversational explanations**: "The interesting part is..."
**Fix**: Direct statement: "Main finding:"

❌ **Justifying methodological choices**: "They chose X because..."
**Fix**: "Methods: X" without justification

---

## Examples of Good Assume-Knowledge Flow

### Complete Results Section:

"**Methods:** N=40, ages 18-75 (M=42, SD=16). Sociolinguistic interviews, Labovian protocol. 8 phonological variables, 4 style contexts. Dual coding, κ=0.89. Acoustic analysis: Praat, F1/F2 extraction, normalization via Lobanov.

**Analysis:** Mixed ANOVA: 2 (gender) × 4 (age group) × 4 (style) × 8 (variable), repeated measures on style and variable. Post-hoc: Tukey HSD. Alpha = 0.05. Effect sizes: partial η².

**Results:** 
- Age: F(3,144) = 28.4, p < 0.001, η²_p = 0.37. Linear trend: F(1,36) = 68.2, p < 0.001.
- Gender: F(1,36) = 15.7, p < 0.001, η²_p = 0.30. Females lead across 7/8 variables.
- Style: F(3,108) = 42.1, p < 0.001, η²_p = 0.54. Casual > reading passage > word list.
- Age×Gender: F(3,144) = 4.2, p = 0.007. Gender difference strongest in youngest cohort.

Regression (8 separate models, one per variable):
- /æ/-tensing: age β = 12 Hz/decade (SE = 2.1), gender β = 35 Hz (SE = 8.4), style β = -15 Hz (SE = 4.5). R² = 0.71.
- /ɑ/-backing: age β = -45 Hz/decade (SE = 7.2), R² = 0.63.
- [Remaining 6 variables: see Table 2]

**Comparison:** Acceleration vs. Labov (2001): /æ/ 3.2×, /ɑ/ 2.8×. Pattern consistent with Gordon (2001) Detroit Stage 3, but more advanced than Buffalo (Labov et al. 2006). Network analysis: innovation adoption correlates with density (r = 0.67, p < 0.001), replicating Milroy & Milroy (1985)."

**What works**:
- Dense statistical reporting, no explanation
- Methods stated without justification
- Results presented efficiently with full detail
- Comparisons by citation only
- No interpretive commentary
- Maximum information per word
- Expert can quickly extract all relevant details

---

## Notes for Implementation

- **Default register for**: Active research on this specific topic
- **Word count**: Shortest (maximum density, no explanatory overhead)
- **Scanning efficiency**: Highest (expert can extract key info in seconds)
- **Best paired with**: Heavy jargon, Formal or Mixed structure

**Remember**: Assume-Knowledge is for working experts, not learners. If the reader needs to pause to look things up, you're using the wrong depth. This register assumes the paper is directly relevant to active work and the reader knows the context cold.

This is the "efficient scanning for active research" register.
