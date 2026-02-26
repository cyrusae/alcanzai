# Explanation Depth: Hand-Holding

## Strategy
Assume reader is intelligent but new to the field. Explain methodology choices, connect concepts to familiar ideas, provide context for why things matter.

**Philosophy**: The reader can follow complex arguments, but needs scaffolding to understand field-specific conventions, implicit assumptions, and why researchers made certain choices.

---

## When to Use This Register

✅ **Use Hand-Holding Depth when:**
- Learning a new field or subfield
- Returning to research after significant gap
- Creating notes to share with intelligent non-experts
- Want to understand *why* researchers did what they did, not just *what* they did
- Building foundational understanding before diving deep

❌ **Don't use Hand-Holding Depth when:**
- Already familiar with field conventions
- Need efficient scanning (use Balanced or Assume-Knowledge)
- Time/token constraints matter more than learning
- Creating reference notes for active research

---

## Core Principles

### 1. Explain Methodological Choices
Don't just state what was done—explain why it was done this way.

**Hand-Holding**:
"They used sociolinguistic interviews rather than surveys because interviews capture natural speech patterns. Surveys would give them self-reported data (what people think they say), but interviews reveal actual usage (what people really say)."

**Not Hand-Holding**:
"The data come from 40 sociolinguistic interviews."

### 2. Connect to Familiar Concepts
Bridge from known to unknown using analogies and comparisons.

**Hand-Holding**:
"Multi-head attention is like having multiple spotlights scanning a sentence simultaneously. Each 'head' focuses on different relationships—one might track subject-verb agreement while another tracks long-distance dependencies. The model learns which relationships to focus on through training."

**Not Hand-Holding**:
"The model employs multi-head self-attention with 8 heads per layer."

### 3. Explain Field Conventions
Make implicit assumptions explicit.

**Hand-Holding**:
"They report p-values (probability that results are due to chance) below 0.05. In most fields, p < 0.05 is the standard threshold for 'statistically significant'—meaning we're confident enough to say this pattern is real, not random."

**Not Hand-Holding**:
"Results showed p < 0.05 across all conditions."

### 4. Provide Context for Why Things Matter
Explain significance and implications, not just findings.

**Hand-Holding**:
"This finding challenges the dominant view in the field. Before this paper, most researchers assumed transformers were just sophisticated pattern matchers. But if BERT actually learns hierarchical structure without explicit syntax training, it suggests language models can discover linguistic principles from data alone—which has implications for how we think about language acquisition in humans too."

**Not Hand-Holding**:
"The findings suggest BERT learns hierarchical structure despite lack of explicit supervision."

### 5. Unpack Technical Concepts Progressively
Break complex ideas into digestible steps.

**Hand-Holding**:
"The encoding works in layers. First, the model converts words to vectors (lists of numbers representing meaning). Then each layer transforms these vectors, with early layers capturing simple patterns (like which words appear together) and later layers capturing complex relationships (like who did what to whom). By the final layer, each word's vector contains information about its role in the sentence."

**Not Hand-Holding**:
"The 12-layer encoder progressively transforms token embeddings to capture increasingly abstract linguistic features."

---

## Examples Across Domains

### Linguistics/Phonetics
**Hand-Holding**:
"The researchers measured vowel formants—essentially the acoustic fingerprint of how a vowel sounds. The first formant (F1) relates to tongue height: higher tongue position produces lower F1 values. The second formant (F2) relates to frontness: fronter vowels have higher F2.

When they measured the 'a' sound in 'cat' before 'n' or 'm', they found younger speakers had lower F1 values than older speakers. This means younger speakers' tongues are higher when saying this vowel—the sound is tenser. They measured 40 speakers across different age groups, and the pattern held up statistically (p < 0.001), meaning it's not just random variation.

Why does this matter? It shows active language change happening in real time. The vowel shift isn't complete yet—you can see it progressing across generations."

### Machine Learning  
**Hand-Holding**:
"Previous models like RNNs processed sentences word by word, left to right. This is slow because you can't parallelize it—you have to finish word 1 before starting word 2. It also struggles with long-range dependencies because information from early words gets diluted as it passes through many time steps.

The transformer solves both problems by processing all words simultaneously. The attention mechanism lets each word 'look at' every other word to figure out which ones are relevant. For example, in 'The cat that chased the mouse escaped,' the word 'escaped' needs to connect back to 'cat' (not 'mouse'). Attention learns these relationships automatically.

The result: faster training (all words processed in parallel) and better long-range understanding (direct connections between distant words). On translation tasks, this achieved 28.4 BLEU—about 2 points better than previous best, which is a substantial improvement in this benchmark."

### Sociolinguistics
**Hand-Holding**:
"Sociolinguistic interviews are designed to sound like natural conversation, but they're actually carefully structured to elicit different speech styles. The interviewer might start with casual topics ('Tell me about growing up here'), then shift to more formal tasks like reading a word list. This matters because people adjust their speech based on context—more casual in relaxed conversation, more careful when reading aloud.

By comparing the same person across these contexts, researchers can see which features are stable (appear in all styles) versus which are variable (appear in casual speech but disappear in careful speech). Variable features often indicate social meaning—they're markers of identity or group membership rather than fundamental pronunciation differences.

In this study, they tracked 8 different pronunciation features across 4 speaking contexts, then used multivariate analysis to separate social factors (age, gender) from contextual ones (casual vs. formal). This lets them identify which social groups are leading linguistic changes."

### Statistics
**Hand-Holding**:
"They used mixed-effects regression, which is appropriate when you have nested data—in this case, multiple trials per subject and multiple subjects per item. Regular regression would treat each trial as independent, but trials from the same person are correlated (some people are just faster/more accurate overall).

Mixed effects accounts for this by including 'random intercepts' for subject and item. This means the model estimates a baseline for each subject ('Alice tends to be 10% more accurate than average') and each item ('Question 5 tends to be harder than average'), then looks for effects above and beyond these baselines.

The model comparison (likelihood ratio test, χ² = 45.2, p < 0.001) shows that including these random effects significantly improves the fit—the data are better explained when we account for individual differences. The fixed effect for condition (β = 0.82, p < 0.001) represents the treatment effect after controlling for these individual differences."

---

## What to Explain vs. What to Assume

### Always Explain:
- **Why researchers made methodological choices**: "They used X instead of Y because..."
- **Field-specific conventions**: "In this field, p < 0.05 is considered..."
- **Technical terminology on first use**: Even if glossed in jargon register, explain *why* it matters
- **Statistical significance and effect sizes**: What the numbers actually mean
- **Connections between findings and implications**: "This matters because..."

### Can Assume:
- **Basic academic literacy**: Reader knows what a hypothesis is, what research means
- **General intelligence**: Don't over-explain obvious logical connections
- **Reading comprehension**: Don't repeat the same explanation multiple times

### The Test:
Would a smart undergraduate in a different field understand this without additional research? If not, add more explanation.

---

## Integration with Jargon Density

### With None Jargon
Maximum accessibility—every concept explained from first principles.

"The model processes all words at once instead of one by one. This parallel approach is faster because modern computers can do many calculations simultaneously (like how your phone can run multiple apps at once). It also helps the model understand long-distance relationships in sentences—when a word early in the sentence affects a word much later, the model can connect them directly instead of passing information step by step."

### With Selective Jargon
Technical terms + explanations of methodology and significance.

"The transformer employs multi-head self-attention (parallel attention mechanisms that focus on different aspects of word relationships). This differs from RNNs because it processes all tokens simultaneously rather than sequentially. The parallel processing matters for two reasons: it's much faster to train (you can process entire sentences at once), and it captures long-range dependencies better (direct connections between distant words rather than passing information through many intermediate steps)."

### With Heavy Jargon
Expert terminology but still explains *why* choices matter.

"The architecture employs 12-layer encoder with 8 attention heads per layer. This design choice enables capturing both local syntactic patterns (early layers) and long-range semantic dependencies (later layers). Trained on WMT'14 EN-DE for 100k steps, achieving 28.4 BLEU—2.1 points above previous SOTA. The improvement comes primarily from better handling of long-range dependencies and more efficient parallelization during training."

---

## Quality Checklist

Before finalizing synthesis in Hand-Holding Depth, verify:

- [ ] Methodological choices explained (why, not just what)
- [ ] At least one analogy or comparison to familiar concept per section
- [ ] Field conventions made explicit (don't assume reader knows norms)
- [ ] Statistical results explained (what p < 0.05 means, not just reported)
- [ ] Connections drawn between findings and implications
- [ ] Technical concepts unpacked progressively (step by step)
- [ ] "Why this matters" appears at least once
- [ ] Smart undergraduate from different field could follow the logic
- [ ] Not condescending—assumes intelligence, just not prior knowledge

---

## Common Pitfalls

❌ **Over-explaining basics**: "A hypothesis is a testable prediction..."
**Fix**: Assume general academic literacy, explain field-specific things

❌ **Just reporting without explaining**: "They used ANOVA" with no context
**Fix**: "They used ANOVA (comparing multiple groups at once) because..."

❌ **Condescending tone**: "As you may know..." or "Obviously..."
**Fix**: Explain matter-of-factly without suggesting reader should already know

❌ **Skipping the "why this matters"**: All description, no significance
**Fix**: Connect findings to broader questions or implications

❌ **Too many analogies**: Every concept gets a metaphor
**Fix**: Use analogies for genuinely complex ideas, not obvious ones

---

## Examples of Good Hand-Holding Flow

### Methodology section:

"The researchers chose sociolinguistic interviews over surveys for a specific reason: surveys tell you what people *think* they say, but interviews reveal what people *actually* say. When you ask someone 'Do you pronounce 'caught' and 'cot' the same?', many people can't accurately self-report—they genuinely don't know, or they report what they think is 'correct' rather than what they actually do.

The interview protocol follows Labov's methodology, designed to capture natural speech while minimizing the observer's paradox (the problem that people change how they talk when they know they're being recorded). The interviewer starts with casual topics and gradually shifts to more formal tasks—reading a word list, then reading minimal pairs. This progression lets the researchers see which features are stable across contexts versus which ones shift based on formality.

Each interview was then coded for 8 phonological variables. 'Coding' here means listening to the recording and marking each instance of the sound in question—for example, every time the speaker says a word with 'a' before 'n' (like 'can', 'hand', 'stand'). Two trained coders did this independently to ensure reliability, then any disagreements were resolved by a third coder."

**What works**:
- Explains *why* methodology was chosen
- Unpacks field conventions (observer's paradox, coding)
- Provides context for each step
- Connects methodology to research goals
- No jargon left unexplained
- Assumes intelligence but not prior knowledge

---

## Notes for Implementation

- **Default register for**: Learning new fields, gap-year refresh, partner-shareable notes
- **Word count**: Longest (explanations add substantial length)
- **Cognitive load**: Higher during writing, lower during reading
- **Best paired with**: None or Selective jargon, Conversational or Mixed structure

**Remember**: Hand-Holding builds understanding, not just knowledge. The goal is for reader to finish not just knowing *what* was found, but understanding *why* it was done this way and *why* it matters. This takes more words but creates deeper comprehension.

This is the "teach me this field" register.
