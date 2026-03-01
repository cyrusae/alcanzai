# Explanation Depth: Balanced

## Strategy
Provide standard academic detail. Explain methodology clearly, note significance where relevant, but assume reader has general field literacy. The default level of explanation.

**Philosophy**: Strike a balance between efficiency and clarity. Explain enough to understand the work, skip explanations of standard practices. Reader knows the field but may need refreshers on specific techniques.

---

## When to Use This Register

✅ **Use Balanced Depth when:**
- Working within your field but not on this specific topic
- Creating standard literature review notes
- Unsure which depth to use (safest default)
- Want notes that work across different reading contexts
- Need to balance comprehension and efficiency

❌ **Don't use Balanced Depth when:**
- Learning entirely new field (use Hand-Holding)
- Need maximum efficiency for active research (use Assume-Knowledge)
- Creating notes for non-experts (use Hand-Holding)

---

## Core Principles

### 1. Explain Novel or Non-Standard Methods
Standard methods get brief mention, novel approaches get explanation.

**Balanced**:
"The researchers used sociolinguistic interviews following Labovian methodology. Each interview included careful speech, reading passage, word list, and minimal pairs. Coding was done by two independent coders with 92% agreement."

**More explanation (Hand-Holding)**:
"Sociolinguistic interviews are designed to capture natural speech while minimizing observer effects. The Labovian protocol starts with casual conversation, then progressively shifts to more formal contexts..."

**Less explanation (Assume-Knowledge)**:
"Data from 40 sociolinguistic interviews, Labovian protocol, standard coding procedures."

### 2. Note Significance Without Extended Discussion
Point out what matters, but don't extensively develop implications.

**Balanced**:
"This finding challenges the view that transformers are merely pattern matchers, suggesting they learn hierarchical structure. This has implications for theories of language acquisition."

**More (Hand-Holding)**:
"This finding fundamentally challenges the dominant view in the field. Before this paper, most researchers assumed transformers were sophisticated pattern matchers without genuine syntactic understanding. If BERT learns hierarchical structure from data alone, it suggests..."

**Less (Assume-Knowledge)**:
"Results challenge pattern-matching view, support emergent hierarchy."

### 3. Provide Context for Technical Choices
Brief rationale for methodological decisions, not extensive justification.

**Balanced**:
"They chose mixed-effects regression to account for nested data structure (multiple trials per subject). The maximal random effects structure was justified by likelihood ratio test (χ² = 45.2, p < 0.001)."

**More (Hand-Holding)**:
"Mixed-effects regression is appropriate here because the data are nested—multiple trials from each subject, and subjects aren't independent. Regular regression would treat each trial as independent, but trials from the same person are correlated..."

**Less (Assume-Knowledge)**:
"Mixed-effects model with maximal random effects structure (LRT: χ² = 45.2, p < 0.001)."

### 4. Standard Results Reporting
State findings with appropriate statistical detail, brief interpretation.

**Balanced**:
"Younger speakers showed significantly more /æ/-tensing than older speakers (β = 12 Hz/decade, SE = 2.1, p < 0.001). This pattern suggests active change in progress rather than stable variation."

**More (Hand-Holding)**:
"The age effect shows younger speakers averaging 12 Hz more tensing per decade (β = 12, SE = 2.1, p < 0.001). The p-value well below 0.05 indicates this isn't random variation. The pattern suggests active language change happening in real time—if it were stable variation, we wouldn't see such clear age stratification."

**Less (Assume-Knowledge)**:
"Significant age effect (β = 12 Hz/decade, p < 0.001); change in progress."

### 5. Brief Methodological Summary
Cover the essentials without extensive detail.

**Balanced**:
"The model consists of 12 encoder layers with 8 attention heads per layer and 768-dimensional embeddings. Trained on WMT'14 EN-DE for 100k steps using Adam optimizer. Achieved 28.4 BLEU, outperforming previous SOTA by 2.1 points."

---

## Examples Across Domains

### Linguistics/Phonetics
**Balanced**:
"The study analyzes /æ/-tensing in pre-nasal environments among 40 Chicago speakers. Acoustic measurements of F1 and F2 formants reveal significant age stratification (p < 0.001), with younger speakers exhibiting more tensing.

Data were collected through sociolinguistic interviews and coded for phonological environment, word class, and social factors. Multivariate regression controls for these variables while isolating the age effect. The pattern aligns with Stage 3 NCVS progression documented in Detroit (Gordon 2001) and Buffalo (Labov et al. 2006), though Chicago shows more advanced /ɑ/-backing."

### Machine Learning
**Balanced**:
"The transformer architecture processes tokens in parallel using multi-head self-attention rather than sequential processing. This enables both faster training and better capture of long-range dependencies.

The model consists of 12-layer encoder-decoder architecture with 8 attention heads per layer. Positional encodings preserve word order information. Trained on WMT 2014 EN-DE for 100k steps, the model achieves 28.4 BLEU, surpassing previous state-of-the-art by 2+ points. The improvement comes primarily from parallel processing efficiency and better handling of long-distance relationships."

### Sociolinguistics
**Balanced**:
"The corpus comprises 40 sociolinguistic interviews conducted with working-class Philadelphia speakers. Interviews followed Labovian protocol across four style contexts (casual conversation, reading passage, word list, minimal pairs). Eight phonological variables were coded by two independent coders with 92% agreement.

Analysis reveals active change in progress. Younger speakers lead across all innovative features, with significant age differences (p < 0.01 for all variables). This pattern indicates generational change rather than age grading. The findings align with previous Philadelphia studies but show accelerated change in apparent time."

### Statistics
**Balanced**:
"Mixed-effects logistic regression was employed with random intercepts for subject and item. Fixed effects included condition, trial number, and previous accuracy. Model comparison via likelihood ratio test supported maximal random effects structure (χ² = 45.2, df = 3, p < 0.001).

Results show significant main effect of condition (β = 0.82, SE = 0.15, p < 0.001), with treatment group outperforming controls. The effect persists when controlling for potential confounds, suggesting causal relationship. Effect size (OR = 2.4, 95% CI [1.8, 3.2]) indicates substantial practical significance."

---

## What to Explain vs. What to Assume

### Always Explain:
- **Novel or non-standard methods**: Anything unusual needs brief justification
- **Key findings and their direction**: What was found and whether it's positive/negative
- **Statistical significance**: Report p-values, effect sizes, confidence intervals
- **Major implications**: Why findings matter (one sentence typically sufficient)

### Can Assume:
- **Standard methodologies**: Sociolinguistic interviews, ANOVA, regression, etc.
- **Common field practices**: Standard coding procedures, typical statistical thresholds
- **Basic concepts**: What p-values mean, what hierarchical structure is
- **Standard notation**: Readers know β, SE, F, χ², etc.

### The Test:
Would a peer in your field understand this without looking things up? If yes, Balanced is appropriate.

---

## Integration with Jargon Density

### With None Jargon
Accessible terminology + standard academic detail.

"The model processes all words simultaneously (parallel processing) rather than one at a time. This is faster for training and better at understanding relationships between distant words. The model has 12 layers, with each layer refining the understanding. Trained on a large translation dataset, it achieved 28.4 BLEU (standard translation quality metric), beating previous best by about 2 points."

### With Selective Jargon
Technical vocabulary + balanced explanation.

"The transformer employs multi-head self-attention (parallel attention mechanisms) to process all tokens simultaneously. This differs from RNNs by enabling parallel computation and direct connections between distant positions. The 12-layer architecture with 8 heads per layer achieves 28.4 BLEU on WMT'14 EN-DE, outperforming previous SOTA by 2.1 points through improved parallelization and long-range dependency modeling."

### With Heavy Jargon
Expert terminology + standard academic detail.

"12-layer encoder-decoder with 8 attention heads per layer, 768-dimensional embeddings. Trained on WMT'14 EN-DE for 100k steps with Adam (lr=1e-4, β₁=0.9, β₂=0.98). Achieves 28.4 BLEU, +2.1 over previous SOTA. Improvements primarily from parallel processing efficiency and long-range dependency modeling. Inference latency reduced 60% vs. RNN baselines."

---

## Quality Checklist

Before finalizing synthesis in Balanced Depth, verify:

- [ ] Standard methods mentioned but not extensively explained
- [ ] Novel approaches get brief justification
- [ ] Key findings clearly stated with statistical support
- [ ] One-sentence significance noted where relevant
- [ ] No extended methodological justifications (save for Hand-Holding)
- [ ] No assumption that reader knows non-standard techniques (that's Assume-Knowledge)
- [ ] Appropriate for peer in your field to read and understand
- [ ] Balances efficiency with clarity
- [ ] Could serve as literature review notes

---

## Common Pitfalls

❌ **Over-explaining standard practices**: "ANOVA compares multiple groups..."
**Fix**: Just state "ANOVA shows..." and move on

❌ **Under-explaining novel methods**: "They used novel clustering approach"
**Fix**: One sentence on what makes it novel: "Novel clustering approach that accounts for temporal dependencies..."

❌ **No interpretation**: Just reporting stats without saying what they mean
**Fix**: Add brief interpretation: "...suggesting active change rather than stable variation"

❌ **Too much detail on methodology**: Extensive parameter choices
**Fix**: Key parameters only, defer full detail to methods section if needed

❌ **Inconsistent depth**: Some sections Hand-Holding, others Assume-Knowledge
**Fix**: Maintain steady Balanced level throughout

---

## Examples of Good Balanced Flow

### Results section:

"Acoustic analysis reveals significant /æ/-tensing in pre-nasal environments (t = 8.4, p < 0.001, d = 1.2). F1 lowering averages 85 Hz in tensed versus lax tokens. ANOVA shows main effects for phonological environment (F(3,156) = 42.1, p < 0.001) and speaker age (F(2,52) = 18.7, p < 0.001), with significant interaction (F(6,156) = 3.8, p = 0.002).

Regression analysis (R² = 0.71) identifies following-nasal as strongest predictor (β = -78, SE = 8.2). Social factors show age grading—younger speakers exhibit more tensing (β = 12 per decade, SE = 2.1)—and style stratification, with careful speech showing reduced tensing.

These patterns align with NCVS Stage 3 documented in Detroit and Buffalo, though Chicago demonstrates more advanced /ɑ/-backing. This suggests regional variation in the chain shift trajectory, with Chicago leading the change."

**What works**:
- Standard statistical reporting (assumes reader knows ANOVA, regression)
- Key findings clearly stated
- Brief interpretation ("suggests regional variation")
- Comparison to previous work
- No extended explanations of methods
- Efficient but clear
- Appropriate for field peer to quickly grasp

---

## Notes for Implementation

- **Default register for**: Most academic synthesis tasks
- **Word count**: Moderate (more than Assume-Knowledge, less than Hand-Holding)
- **Versatility**: Works across widest range of contexts
- **Safest choice**: When unsure which depth to use

**Remember**: Balanced Depth is the workhorse. It provides enough detail to understand the work without extensive tutorial. Use Hand-Holding when learning, Assume-Knowledge when scanning—but Balanced handles most situations effectively.

This is the "standard literature review note" register.
