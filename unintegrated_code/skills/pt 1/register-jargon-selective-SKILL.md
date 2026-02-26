# Jargon Density: Selective

## Strategy
Keep technical terminology AND provide inline glosses for specialized terms. Use this for learning through exposure while maintaining accessibility.

**When to use:**
- Learning new subfield (user's DEFAULT mode)
- Building vocabulary through repeated exposure
- Returning to field after hiatus (burnout recovery, gap year)
- Want "just in case" glossaries
- Interdisciplinary reading where terminology overlaps

---

## Core Principle

**Term first, gloss second**

Think: "Technical term (accessible explanation)"

NOT: "Explanation (oh by the way, called technical term)"

---

## Format Pattern

```
technical-term (accessible explanation)
```

### Examples

**Phonetics:**
✅ "Alveolar fricatives (hissing sounds like 's' or 'z' made with tongue near teeth)"
❌ "Hissing sounds (alveolar fricatives)"

**Machine Learning:**
✅ "Gradient descent (iterative method to minimize error by adjusting parameters)"
❌ "Minimizing error through parameter adjustment (gradient descent)"

**Critical Theory:**
✅ "Hegemony (cultural dominance that feels natural rather than imposed)"
❌ "Cultural dominance (hegemony)"

---

## What to Gloss

### Always Gloss

**Field-specific terminology:**
- Not in general academic vocabulary
- Requires domain knowledge to understand
- Examples: "phoneme," "attention mechanism," "epistemic violence"

**Methods and techniques:**
- Research procedures
- Analytical approaches
- Examples: "forced alignment," "ablation study," "close reading"

**Abbreviations on first use:**
- Spell out + define
- Examples: "RNN (Recurrent Neural Network—processes sequences step-by-step)"
- After first use: just "RNN"

### Never Gloss

**General academic vocabulary:**
- Used across disciplines
- Examples: "hypothesis," "significant," "methodology," "analyze"

**Terms defined earlier:**
- Already glossed in this document/summary
- Use freely after first explanation

**Common abbreviations after first use:**
- First: "VOT (Voice Onset Time—delay between consonant release and vowel start)"
- Later: just "VOT"

### Sometimes Gloss (Use Judgment)

**Cross-disciplinary terms with multiple meanings:**
- "Embedding" (NLP vs neuroscience vs mathematics)
- "Network" (social, neural, graph theory)
- Disambiguate with context-specific gloss

**Background assumptions:**
- For undergrad audience: gloss "p-value"
- For expert audience: skip it
- Depends on target reader

---

## Gloss Length Guidelines

**Short gloss (5-10 words):**
For simple, concrete concepts

"Phoneme (distinct sound unit in a language)"
"Corpus (large collection of texts)"

**Standard gloss (10-20 words):**
For most technical terms

"Attention mechanism (learned weights allowing model to focus on relevant parts of input when making predictions)"
"Code-switching (alternating between two or more languages within single conversation)"

**Long gloss (20-30 words):**
For complex concepts, use sparingly

"Hegemony (when one group's cultural worldview becomes so dominant it feels natural and inevitable, rather than constructed or imposed through force)"

**Over 30 words:**
Too long for inline gloss—consider breaking into multiple sentences or separate explanation

---

## Crafting Quality Glosses

### Clarity First
Use simpler language than the term itself

✅ "Alveolar ridge (bumpy area behind upper teeth)"
❌ "Alveolar ridge (anterior coronal surface)"

### Accuracy Maintained
Don't oversimplify to the point of distortion

✅ "Transformer (neural network using self-attention instead of recurrence)"
❌ "Transformer (fancy AI thing)"

### Contextual
Relevant to how term is used in THIS paper

✅ "Embedding (in NLP: vector representation of words)"
❌ "Embedding (mathematical mapping)" [when discussing NLP]

### Concise
No unnecessary words

✅ "Gradient descent (iteratively adjust parameters to reduce error)"
❌ "Gradient descent (the process by which we iteratively make adjustments to the parameters in order to reduce the amount of error)"

### Standalone
Comprehensible without reading full paper

✅ "Panopticon (prison design with central guard tower observing all cells)"
❌ "Panopticon (see Bentham's description in Section 2)"

---

## Gloss Strategies by Term Type

### For Concrete Terms
Use analogy or example

"Corpus (large collection of texts, like a library of thousands of documents)"

### For Abstract Terms
Use function or purpose

"Regularization (technique to prevent model from memorizing training data too closely)"

### For Processes
Use step-by-step mini-description

"Backpropagation (calculating gradients by propagating errors backward through network layers)"

### For Comparative Terms
Use contrast

"Supervised learning (training with labeled examples) vs unsupervised (finding patterns without labels)"

### For Borrowed/Repurposed Terms
Note the specific meaning

"Training (in machine learning: adjusting model parameters using data—distinct from human learning)"

---

## First Use vs Subsequent Use

### First Occurrence
Full term + gloss

"The model uses self-attention (mechanism where each position attends to all positions to compute representations)"

### Subsequent Occurrences  
Term only, no re-gloss

"The self-attention mechanism allows..."
"Each attention head..."

### Exception: Complex Terms
Can provide brief reminder if many pages between uses

First: "VOT (Voice Onset Time—delay between consonant release and vowel start)"
Much later: "VOT (voice timing)" [brief reminder]

---

## Handling Special Cases

### Newly Coined Terms

Include origin + explanation

"Différance (Derrida's neologism combining 'difference' and 'deferral'—meaning is never fully present but always deferred)"

### Non-English Terms

Keep original + gloss with cultural context

"Bildung (German concept of self-cultivation through education—both knowledge and character development)"

### Acronyms as Terms

Full form + explanation

"BERT (Bidirectional Encoder Representations from Transformers—language model that processes text considering both left and right context)"

Then: Just "BERT"

### Multiple Meanings

Specify which sense

"Model (in ML: learned function mapping inputs to outputs—distinct from statistical or theoretical models)"

---

## Examples Across Domains

### Linguistics

"The researchers measured VOT (Voice Onset Time—delay between releasing a consonant and starting the vowel) for bilabial stops (consonants like 'p' and 'b' made with both lips). They found that speakers exhibited code-switching (alternating between languages mid-conversation) in casual but not formal contexts."

**What works:**
- Each term gets one clear gloss
- Glosses use accessible language
- After first use, terms flow naturally
- Technical precision maintained

### Machine Learning

"The Transformer uses multi-head attention (parallel attention calculations from different learned perspectives) with each head focusing on different aspects of input. The attention mechanism (learned weighting of input positions) allows the model to capture long-range dependencies without recurrence (sequential processing). Training uses gradient descent (iteratively adjusting parameters to minimize error)."

**What works:**
- Each concept glossed on first use
- Later references use terms freely
- Glosses explain function, not just definition
- Builds vocabulary systematically

### Critical Theory

"Foucault's genealogy (tracing how power relations shaped what counts as truth) reveals epistemic violence (harm from excluding certain ways of knowing) in colonial discourse. The panopticon (Bentham's prison design with central observation tower) exemplifies disciplinary power (control through surveillance and normalization) rather than sovereign power (rule through spectacular punishment and law)."

**What works:**
- Theoretical concepts made concrete
- Comparisons clarify distinctions
- Technical terms preserved for precision
- Accessible explanations enable understanding

---

## Quality Checks

When writing in Selective register, verify:

✅ **Term prominent:** Technical vocabulary comes first
✅ **Gloss clear:** Explanation actually helps
✅ **Appropriate length:** 5-20 words for most terms
✅ **Contextual:** Relevant to paper's usage
✅ **Builds vocabulary:** Reader learns terms through exposure
✅ **Accessible:** Non-experts can follow with glosses

---

## Common Pitfalls

❌ **Circular glosses:** Using term to define itself
- Bad: "Hegemony (hegemonic cultural dominance)"
- Good: "Hegemony (cultural dominance feeling natural not imposed)"

❌ **Too technical glosses:** Equally complex language
- Bad: "Phoneme (phonological segment in mental lexicon)"
- Good: "Phoneme (distinct sound unit in language)"

❌ **Too vague:** Losing precision
- Bad: "Attention (when model pays attention)"
- Good: "Attention (learned weighting of input elements)"

❌ **Excessive re-glossing:** Re-explaining every time
- Bad: Using full gloss on every occurrence
- Good: Gloss once, then use term freely

❌ **Missing core terms:** Skipping important jargon
- Bad: Assuming reader knows field-specific terms
- Good: Glossing anything requiring domain knowledge

---

## Benefits of Selective Register

✅ **Vocabulary building** through repeated exposure
✅ **Precision preserved** using exact technical terms
✅ **Accessibility maintained** via inline glosses
✅ **Portable notes** can share with partners or non-experts
✅ **Learning support** especially valuable during field transitions
✅ **Memory aid** glosses help recall during research breaks
✅ **Just-in-case coverage** over-gloss rather than under-gloss

---

## When to Use

**Ideal for:**
- Learning new subfields within domain
- Returning after hiatus (burnout, gap year)
- Building shareable notes
- Interdisciplinary reading
- Anyone valuing "just in case" glossaries
- DEFAULT mode for most reading

**Not ideal for:**
- Expert literature reviews (use Heavy)
- Complete beginners (use None)
- Speed-reading familiar material (Heavy)

---

## Integration with Output Tasks

### In Quick Summaries
Gloss 3-5 core terms in summary section
Expand acronyms on first use
Balance accessibility with precision

### In Detailed Summaries
Gloss new terms in each section summary
Build vocabulary progressively
Track which terms defined in which sections

### In Glossary Extraction
Use Selective glosses as starting point
Terms already identified
Definitions already drafted

---

## Notes for Implementation

- Default register for most use cases
- Expect moderate word count (not as long as None, not as short as Heavy)
- First-use glossing requires tracking what's been explained
- Balance: enough glosses to help, not so many they interrupt flow
- Quality over quantity: better to skip marginal terms than over-gloss

Remember: This register builds vocabulary through exposure. Each gloss is a mini-lesson. Over time, reader needs fewer glosses as terms become familiar.
