# Identify Terminology

## Purpose

Systematically identify technical terms, jargon, and specialized vocabulary in academic papers. Determine which terms need explanation, how to gloss them effectively, and which can be used without explanation.

**Use this skill when:** Processing any academic text that will be explained to a reader (summaries, glossaries, teaching materials).

---

## Dependencies

- Uses `understand-academic-text` for field recognition and context
- Complements register settings for determining gloss depth

---

## Core Principles

### 1. Not All Unfamiliar Words Are Technical Terms

Distinguish between:
- **Technical jargon:** Field-specific terminology with precise meaning
  - "Phoneme," "gradient descent," "hegemony"
- **General academic vocabulary:** Used across disciplines
  - "Hypothesis," "methodology," "analysis"
- **Common words used precisely:** Everyday words with special meaning in context
  - "Training" (ML), "shift" (linguistics), "discipline" (Foucault)

### 2. Term Importance Varies

Not all technical terms need equal treatment:
- **Core concepts:** Central to the paper's argument → Always gloss
- **Methodological terms:** Important for understanding approach → Gloss if novel
- **Background terms:** Assumed knowledge → Gloss selectively
- **Passing references:** Mentioned but not central → Can skip

### 3. Glossing Strategy Depends on Register

How you handle terms depends on target audience:
- **None (accessible):** Explain concept, term as secondary
- **Selective (learning):** Term first + inline gloss
- **Heavy (expert):** Term only, minimal glossing

---

## Term Identification Checklist

### Phase 1: Scan for Technical Vocabulary
- [ ] Read through paper marking potentially technical terms
- [ ] Note where terms are introduced (often defined in context)
- [ ] Check for abbreviations and acronyms
- [ ] Identify terms that recur multiple times (likely important)
- [ ] Flag terms that seem field-specific

### Phase 2: Categorize Terms by Type
- [ ] Domain-specific terminology (unique to this field)
- [ ] Cross-domain terms (used in multiple fields)
- [ ] Method/technique names
- [ ] Statistical or analytical terms
- [ ] Theoretical concepts
- [ ] Proper nouns (named theories, tests, models)

### Phase 3: Assess Importance
- [ ] Which terms are central to main argument?
- [ ] Which are methodological (needed to understand how)?
- [ ] Which are background (context but not essential)?
- [ ] Which are mentioned only briefly?

### Phase 4: Check for Existing Definitions
- [ ] Does paper define the term itself?
- [ ] Is it explained in context?
- [ ] Does it reference a source for definition?
- [ ] Is meaning clear from usage pattern?

### Phase 5: Determine Glossing Strategy
- [ ] Which terms MUST be glossed (core concepts)?
- [ ] Which SHOULD be glossed (helpful but not critical)?
- [ ] Which CAN skip glossing (obvious from context)?
- [ ] For each term: What's the clearest 5-20 word gloss?

---

## Term Types and Recognition Patterns

### Domain-Specific Technical Terms

**Linguistics:**
- Phonetics: "alveolar," "fricative," "VOT," "formant"
- Syntax: "constituent," "c-command," "movement"
- Sociolinguistics: "variable," "style-shifting," "prestige"

**Recognition patterns:**
- Often have specialized morphology (suffixes like -eme, -ic, -ation)
- Defined in field-specific dictionaries or textbooks
- Used consistently with precise meaning across papers

**ML/AI:**
- Architecture: "transformer," "attention," "embedding," "encoder"
- Training: "gradient descent," "backpropagation," "optimizer"
- Evaluation: "perplexity," "BLEU," "F1 score"

**Recognition patterns:**
- Often borrowed from mathematics or computer science
- May be metaphorical (attention, memory, layers)
- Frequently abbreviated (CNN, RNN, LSTM)

**Critical Theory/Humanities:**
- Foucault: "genealogy," "episteme," "biopolitics," "panopticism"
- Derrida: "différance," "logocentrism," "trace"
- General: "hegemony," "discourse," "subjectivity"

**Recognition patterns:**
- Often repurposed common words with technical meaning
- May be non-English (untranslated French/German concepts)
- Typically associated with specific theorists

### Methodological Terms

**Quantitative methods:**
- "Regression," "p-value," "significance," "correlation"
- "Sample size," "confidence interval," "null hypothesis"

**Qualitative methods:**
- "Ethnography," "grounded theory," "thick description"
- "Coding," "themes," "saturation"

**Computational methods:**
- "Parsing," "tokenization," "annotation"
- "Corpus," "algorithm," "model"

**Recognition patterns:**
- Describe HOW research was conducted
- Often found in Methods section
- May be standard across multiple fields

### Abbreviations and Acronyms

**Types:**
- **Initialisms:** "NLP" (Natural Language Processing), "IMRaD"
- **Acronyms:** "BERT" (Bidirectional Encoder Representations), "ReLU"
- **Standard abbreviations:** "et al.," "cf.," "i.e."

**Recognition patterns:**
- All caps (usually)
- Often defined parenthetically on first use
- May become more familiar than full form (CNN vs Convolutional Neural Network)

### Borrowed or Cross-Domain Terms

**Terms used differently across fields:**
- "Network": Neural network (AI), social network (sociology), network analysis (graph theory)
- "Model": Statistical model, theoretical model, computational model
- "Embedding": Word embedding (NLP), tissue embedding (biology)

**Recognition patterns:**
- Need field-specific gloss
- Context disambiguates meaning
- Risk of confusion if reader knows term from different field

---

## Glossing Decision Matrix

For each identified term, use this matrix:

### Core Concept Terms → ALWAYS GLOSS

**Criteria:**
- Central to paper's main argument
- Used repeatedly throughout
- Understanding it is crucial for understanding paper
- Novel or uncommon term

**Example from ML paper:**
"Self-attention" in Transformer paper → Always gloss

**Example from linguistics:**
"Code-switching" in sociolinguistics paper → Always gloss

**Example from theory:**
"Panopticon" in Foucault → Always gloss

### Methodological Terms → GLOSS IF NOVEL

**Criteria:**
- Standard method might need explanation for non-experts
- Novel method ALWAYS needs explanation
- Commonly used method can skip gloss for expert audience

**Example - Novel:**
"Forced alignment" (automatic speech-to-text matching) → Gloss

**Example - Standard:**
"T-test" → Gloss for general audience, skip for stats-literate

### Background Terms → SELECTIVE GLOSS

**Criteria:**
- Provides context but not central to argument
- Common in the field
- May be defined earlier in paper

**Example:**
"Corpus" mentioned in linguistics paper → Quick gloss first time, then use freely

### Passing References → SKIP OR MINIMAL

**Criteria:**
- Mentioned once or twice
- Not important for main argument
- Fully defined in cited source

**Example:**
Brief reference to "GPT-2" in paper primarily about something else → Can skip detailed gloss

---

## Crafting Effective Glosses

### Gloss Length Guidelines

**5-10 words (short gloss):**
For simple concepts with clear analogues

**Example:**
- "Phoneme (distinct sound unit in a language)"
- "Backpropagation (method for updating neural network weights)"

**10-20 words (standard gloss):**
For most technical terms requiring some explanation

**Example:**
- "Attention mechanism (learned weights that allow model to focus on relevant parts of input when making predictions)"
- "Code-switching (alternating between two or more languages within a single conversation or utterance)"

**20-30 words (long gloss):**
For complex concepts, but use sparingly

**Example:**
- "Hegemony (when one group's cultural worldview becomes so dominant that it feels natural and inevitable rather than constructed or imposed through force)"

**30+ words:**
Too long for inline gloss—consider footnote or separate glossary entry

### Gloss Quality Criteria

✅ **Clear and accessible:** Uses simpler language than term itself
✅ **Accurate:** Doesn't oversimplify to point of distortion
✅ **Contextual:** Relevant to how term is used in THIS paper
✅ **Concise:** No unnecessary words
✅ **Standalone:** Comprehensible without reading full paper

### Gloss Strategies by Term Type

**For concrete terms:**
Use analogy or example
- "Corpus (large collection of texts, like a library of thousands of documents)"

**For abstract terms:**
Use function or purpose
- "Regularization (technique to prevent model from memorizing training data)"

**For processes:**
Use step-by-step mini-description
- "Gradient descent (iteratively adjusting model parameters to reduce error)"

**For comparative terms:**
Use contrast
- "Supervised learning (training with labeled examples) vs unsupervised (finding patterns without labels)"

---

## Handling Special Cases

### Newly Coined Terms (Neologisms)

**Example:** "Différance" (Derrida)

**Strategy:**
- Note it's coined by author/theorist
- Explain why existing term wasn't sufficient
- Provide closest approximation

**Gloss:** "Différance (Derrida's neologism combining 'difference' and 'deferral'—the idea that meaning is never fully present but always depends on absent terms and temporal delay)"

### Non-English Terms

**Example:** "Bildung" (German)

**Strategy:**
- Keep original term (shows respect for concept)
- Provide English approximation
- Note cultural/conceptual nuance if important

**Gloss:** "Bildung (German concept of self-cultivation through education—implies both knowledge acquisition and character development)"

### Terms With Multiple Meanings

**Example:** "Training" in ML vs "training" in education

**Strategy:**
- Specify which meaning for this context
- Distinguish from common usage if needed

**Gloss:** "Training (in machine learning: the process of adjusting a model's parameters using data, distinct from human learning)"

### Acronyms Becoming Terms

**Example:** "BERT" vs "Bidirectional Encoder Representations from Transformers"

**Strategy:**
- Full form on first use
- Acronym subsequently
- Can gloss acronym if very common

**First use:** "BERT (Bidirectional Encoder Representations from Transformers—a pre-trained language model)"

**Later:** "BERT" (no gloss needed)

### Theoretical Frameworks

**Example:** "Foucauldian analysis"

**Strategy:**
- Name the theorist
- Brief description of approach
- How it's being used here

**Gloss:** "Foucauldian analysis (using Michel Foucault's approach to examine power relations and knowledge production in social practices)"

---

## Context-Dependent Glossing

The same term may need different glosses depending on context:

### Example: "Embedding"

**In NLP context:**
"Embedding (representation of words as vectors in high-dimensional space)"

**In biology context:**
"Embedding (process of preserving tissue samples in solid medium for sectioning)"

**In mathematics context:**
"Embedding (mapping from one mathematical structure into another)"

### Example: "Model"

**In ML context:**
"Model (learned function mapping inputs to outputs)"

**In statistics context:**
"Model (mathematical representation of relationships between variables)"

**In theory context:**
"Model (conceptual framework for understanding phenomena)"

---

## Register-Specific Strategies

### None Register (Accessible First)

**Pattern:** Explanation first, term in parentheses

**Example:**
"The researchers looked at hissing sounds made with the tongue near the teeth (called alveolar fricatives in linguistics)"

**When to use:**
- Complete newcomers to field
- Partner-shareable content
- Prioritizing understanding over vocabulary building

### Selective Register (Learning Mode)

**Pattern:** Term first, gloss in parentheses

**Example:**
"The researchers analyzed alveolar fricatives (hissing sounds like 's' or 'z' made with tongue near teeth)"

**When to use:**
- Learning new subfield
- Building vocabulary through exposure
- Returning to field after break

### Heavy Register (Expert Mode)

**Pattern:** Term only, no gloss unless truly ambiguous

**Example:**
"The researchers analyzed alveolar fricatives using spectrographic analysis"

**When to use:**
- Expert audience
- Literature reviews
- Rapid reading of familiar material

---

## Examples: Full Terminology Processing

### Example 1: ML Paper (Transformer Architecture)

**Terms identified:**
- Encoder, decoder, attention, multi-head attention
- Positional encoding, layer normalization
- Query, key, value (in attention context)
- BLEU score, perplexity

**Glossing decisions:**

**Core concepts (always gloss):**
- "Self-attention (mechanism where each position attends to all positions to compute representations)"
- "Multi-head attention (parallel attention calculations from different learned perspectives)"
- "Positional encoding (added information about word position since model has no inherent sequence order)"

**Methodological (gloss if novel):**
- "Layer normalization (technique to stabilize training by normalizing layer outputs)"
- "BLEU score (metric for translation quality based on n-gram overlap)"

**Background (selective):**
- "Encoder (component that processes input sequence)"—might skip if standard architecture
- "Perplexity"—skip for expert audience, gloss for general

### Example 2: Sociolinguistics Paper (Variation Study)

**Terms identified:**
- Variable, variant, style-shifting
- Vernacular, prestige variety
- Sociolinguistic interview, apparent time
- F1, F2 (formant frequencies)

**Glossing decisions:**

**Core concepts:**
- "Sociolinguistic variable (linguistic feature that varies systematically across speakers or contexts)"
- "Style-shifting (changing speech patterns based on formality or situation)"
- "Apparent time (method of inferring language change by comparing age groups)"

**Methodological:**
- "Sociolinguistic interview (recorded conversation designed to capture natural speech across formality levels)"
- "F1 and F2 (first and second formant frequencies—acoustic measurements of vowel quality)"

**Background:**
- "Vernacular (everyday, casual speech form)"—quick gloss
- "Prestige variety (socially favored language variety)"—quick gloss

### Example 3: Critical Theory (Foucault)

**Terms identified:**
- Genealogy, episteme, discourse
- Panopticon, surveillance, discipline
- Power/knowledge, biopower
- Normalization, subjectivation

**Glossing decisions:**

**Core concepts:**
- "Genealogy (tracing how power relations historically shaped what counts as truth or knowledge)"
- "Panopticon (Bentham's prison design where guard tower sees all cells but prisoners can't see guard—induces self-surveillance)"
- "Discourse (system of language and practices that construct what can be known or said about a topic)"

**Theoretical:**
- "Power/knowledge (Foucault's concept that power and knowledge are inseparable—what counts as truth is shaped by power relations)"
- "Normalization (process by which certain behaviors/identities become 'normal' and others deviant)"

**Background:**
- "Biopower (power over populations as biological entities)"—gloss if central, skip if passing reference

---

## Common Pitfalls

❌ **Over-glossing:** Not every technical term needs explanation
- If paper defines it, don't re-define
- If it's standard background, skip for expert audience

❌ **Under-glossing:** Skipping terms reader needs
- Don't assume too much background
- Core concepts always need glossing

❌ **Circular glosses:** Using term to define itself
- "Hegemony is hegemonic dominance" ❌
- "Hegemony is cultural dominance that feels natural" ✅

❌ **Too technical glosses:** Using equally complex language
- "Phoneme is a phonological unit" ❌
- "Phoneme is a distinct sound unit" ✅

❌ **Too vague glosses:** Losing precision
- "Attention is when model pays attention" ❌
- "Attention is learned weighting of input elements" ✅

---

## Integration with Other Skills

This skill enables:

- **Register application:** Identifies what to gloss based on register
- **Summaries:** Ensures technical content is accessible
- **Glossary creation:** Systematic term extraction
- **Teaching materials:** Makes papers pedagogically useful

**Combined with understand-academic-text:** Identifies terms in context of paper structure

**Combined with extract-arguments:** Distinguishes core conceptual terms from background

---

## Self-Check: Terminology Work Quality

After processing terminology:

✅ **Coverage:** Did I identify all important technical terms?
✅ **Categorization:** Do I know which are core, methodological, background?
✅ **Glosses written:** Do I have clear, concise explanations?
✅ **Register-appropriate:** Are glosses right depth for target audience?
✅ **Accuracy:** Do glosses correctly represent concepts?
✅ **Clarity:** Could target reader understand glosses?

---

## Notes for Implementation

When using this skill:

1. **First pass: Flag everything** - Over-identify, then prune
2. **Second pass: Categorize** - Core vs background
3. **Third pass: Write glosses** - Test clarity by reading aloud
4. **Check register** - Adjust gloss style to audience
5. **Note uncertainties** - If unsure about a term's importance, include it

Remember: The goal is to make technical content accessible WITHOUT oversimplifying. Good glossing builds vocabulary while maintaining precision.
