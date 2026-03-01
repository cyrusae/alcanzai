# Glossary Extraction

## Purpose

Systematically extract and define technical terminology from academic papers to create a reference glossary. Produces structured term-definition pairs with usage context and importance ranking.

**Use this skill when:** You need a technical terminology reference, are learning a new field's vocabulary, or want to build a searchable glossary across multiple papers.

---

## Dependencies

- Uses `identify-terminology` for term recognition and categorization
- Uses `understand-academic-text` for contextual understanding
- Uses `extract-arguments` to assess term importance
- Uses register settings for definition style

---

## Output Format

Generate structured glossary as JSON:

```json
{
  "glossary": {
    "paper_info": {
      "title": "...",
      "authors": "...",
      "field": "..."
    },
    "terms": [
      {
        "term": "self-attention",
        "definition": "Mechanism where each position in a sequence attends to all positions to compute representations",
        "context": "Core architecture component in Transformer model",
        "importance": "core",
        "category": "methodology",
        "first_occurrence": "page 2",
        "synonyms": ["intra-attention"],
        "related_terms": ["multi-head attention", "attention mechanism"],
        "example_usage": "Self-attention allows the model to weigh the importance of different positions when encoding each position."
      }
    ]
  }
}
```

---

## Term Extraction Process

### Phase 1: Identification

**Systematic scanning checklist:**
- [ ] Read through paper marking all potentially technical terms
- [ ] Check abstract for key terminology
- [ ] Scan introduction for concepts being introduced
- [ ] Note methods section for technique/procedure terms
- [ ] Check for explicitly defined terms (parenthetical definitions)
- [ ] Track abbreviations and acronyms
- [ ] Identify field-specific jargon

**Term recognition patterns:**

**Explicit definitions:**
- "X is defined as..."
- "We call this X..."
- "X (definition in parentheses)"

**Implicit definitions:**
- Term used consistently with specific meaning
- Context makes meaning clear
- Contrasted with related concepts

**Field markers:**
- Capitalized terms (Transformer, BERT)
- Hyphenated compounds (self-attention, multi-head)
- Terms from specific theorists (Foucauldian, Chomskyan)
- Domain-specific morphology (-eme, -ization, -icity)

### Phase 2: Categorization

**Category types:**

**Core concepts (importance: core):**
- Central to paper's contribution
- Novel or redefined in this work
- Used extensively throughout

**Methodological terms (importance: methodological):**
- Research techniques or procedures
- Analytical approaches
- Tools or instruments

**Background terms (importance: background):**
- From prior work or general field knowledge
- Provides context but not novel
- Standard terminology

**Technical jargon (importance: specialized):**
- Field-specific but not central to THIS paper
- Mentioned in passing
- Assumed knowledge

### Phase 3: Definition Crafting

**Definition quality criteria:**

✅ **Clear:** Uses simpler language than term itself
✅ **Accurate:** Correctly represents the concept
✅ **Concise:** 10-30 words typically
✅ **Contextual:** Relevant to how term is used in THIS paper
✅ **Standalone:** Comprehensible without reading full paper

**Definition strategies:**

**For concrete terms:**
Use function or purpose
- "Corpus: Large collection of texts used for linguistic analysis"

**For abstract terms:**
Use explanation of concept
- "Hegemony: Cultural dominance that feels natural rather than imposed"

**For processes:**
Use step or mechanism description
- "Backpropagation: Method for computing gradients by propagating errors backward through network layers"

**For comparative terms:**
Use contrast or analogy
- "Supervised learning: Training with labeled examples, as opposed to unsupervised learning where model finds patterns in unlabeled data"

---

## Importance Assessment

### Core Terms (Must Include)

**Criteria:**
- Paper's main contribution involves this concept
- Term appears in title or abstract
- Used 10+ times throughout paper
- Understanding this is essential for understanding paper

**Examples:**
- "Self-attention" in Transformer paper
- "Code-switching" in bilingualism study
- "Panopticon" in Foucault analysis

**Treatment:**
- Longer, more detailed definitions
- Include multiple usage examples
- Note how paper uses/extends term

### Methodological Terms (Should Include)

**Criteria:**
- Describes how research was conducted
- Technical procedure or technique
- Novel method or standard method applied unusually

**Examples:**
- "Sociolinguistic interview"
- "Ablation study"
- "Forced alignment"

**Treatment:**
- Definition includes purpose or application
- Note when method is standard vs novel

### Background Terms (Selective)

**Criteria:**
- Provides context but not central
- Standard field terminology
- Mentioned but not deeply discussed

**Examples:**
- "RNN" in Transformer paper (for contrast)
- "Vernacular" in sociolinguistics study
- "Discourse" in theory paper (if not main focus)

**Treatment:**
- Brief, standard definition
- Can skip if extremely common in target field

### Specialized Jargon (Minimal)

**Criteria:**
- Very field-specific
- Mentioned once or twice
- Not essential for understanding contribution

**Examples:**
- Specific statistical test names used once
- Brief reference to concept from other work
- Technical detail in appendix

**Treatment:**
- Include only if reader likely to encounter term again
- Very brief definition or reference to source

---

## Context and Usage

### Context Field

**Purpose:** Explain where/why this term matters in the paper

**Good context examples:**
- "Core mechanism enabling parallelization in Transformer architecture"
- "Sociolinguistic variable studied across three communities"
- "Foucault's framework for analyzing institutional power"

**Bad context examples:**
- "Discussed in the paper" (too vague)
- "Important concept" (doesn't explain why)
- "See page 5" (reference without context)

### Example Usage

**Purpose:** Show term in actual use from the paper

**Selection criteria:**
- Illustrates typical usage
- Provides additional clarity
- 10-30 words ideally
- Complete sentence or clause

**Good examples:**
- "Multi-head attention allows the model to jointly attend to information from different representation subspaces."
- "Code-switching served identity negotiation functions, allowing speakers to signal group membership."

**Bad examples:**
- "We used self-attention" (too minimal)
- "As shown in Figure 3..." (reference without substance)

---

## Relationships and Connections

### Synonyms

**Include:**
- Alternative names for same concept
- Equivalent terms from different subfields
- Abbreviations

**Examples:**
- "Self-attention" / "intra-attention"
- "RNN" / "Recurrent Neural Network"
- "Power/knowledge" / "power-knowledge nexus"

### Related Terms

**Include:**
- Closely related concepts
- Terms used in conjunction
- Superordinate or subordinate terms

**Examples:**
For "self-attention":
- Related: "multi-head attention", "attention mechanism", "query-key-value"

For "code-switching":
- Related: "bilingualism", "translanguaging", "language alternation"

For "panopticon":
- Related: "surveillance", "disciplinary power", "normalization"

**Purpose:** Help reader navigate conceptual network

---

## Register-Specific Adaptations

### None Register (Accessible Definitions)

**Style:** Explanation-first, term-second pattern

**Example:**
```json
{
  "term": "alveolar fricative",
  "definition": "Hissing sound made with the tongue near the tooth ridge, like 's' or 'z' in English. Linguists call these alveolar fricatives because they're produced at the alveolar ridge (the bumpy area behind your upper teeth).",
  "importance": "methodological"
}
```

**Characteristics:**
- Longer definitions with more context
- Analogies to familiar concepts
- Step-by-step explanations for processes

### Selective Register (Learning Definitions)

**Style:** Term-first with clear gloss

**Example:**
```json
{
  "term": "alveolar fricative",
  "definition": "Consonant sound produced by directing air through a narrow channel at the alveolar ridge (bumpy area behind upper teeth), creating friction. Examples: /s/, /z/ in English.",
  "importance": "methodological"
}
```

**Characteristics:**
- Technical term prominent
- Clear, accessible explanation
- Concrete examples included
- Moderate length (15-25 words)

### Heavy Register (Expert Definitions)

**Style:** Concise, technical

**Example:**
```json
{
  "term": "alveolar fricative",
  "definition": "Fricative consonant articulated at the alveolar ridge (/s/, /z/ in English).",
  "importance": "methodological"
}
```

**Characteristics:**
- Minimal explanation
- Assumes background knowledge
- Standard field terminology
- Brief (5-15 words)

---

## Organization and Structure

### Alphabetical Ordering

**Primary sort:** Alphabetical by term
- Makes lookup easier
- Standard glossary convention

**Secondary sort:** By importance within letter
- Core terms first
- Background terms last

### Category Grouping (Alternative)

**Option:** Group by category instead of alphabetical

**Categories:**
- Core Concepts
- Methodological Terms
- Theoretical Frameworks
- Statistical/Analytical Methods
- Background/Context

**When to use:**
- Creating teaching materials
- Field-specific term banks
- Cross-paper glossaries

---

## Quality Checks

### Completeness
- [ ] All technical terms from abstract included?
- [ ] Methods section terminology covered?
- [ ] Novel contributions defined?
- [ ] Key theoretical concepts explained?

### Accuracy
- [ ] Definitions match paper's usage?
- [ ] No circular definitions?
- [ ] Technical details correct?
- [ ] Related terms accurately connected?

### Clarity
- [ ] Could target reader understand definitions?
- [ ] Are examples helpful?
- [ ] Is context clear?
- [ ] Are relationships between terms explained?

### Usefulness
- [ ] Would you reference this glossary while reading?
- [ ] Does it cover terms you'd look up?
- [ ] Are importance rankings helpful for prioritizing learning?

---

## Special Cases

### Newly Coined Terms

**Example:** "Différance" (Derrida)

**Handling:**
```json
{
  "term": "différance",
  "definition": "Neologism coined by Derrida combining French 'différence' (difference) and 'différer' (to defer). Refers to the concept that meaning is never fully present but always depends on absent terms and temporal delay.",
  "context": "Central concept in Derrida's deconstruction",
  "importance": "core",
  "category": "theoretical",
  "note": "Spelled with 'a' to distinguish from French 'différence'"
}
```

**Include:**
- Etymology or origin
- Why existing term was insufficient
- Pronunciation if non-obvious

### Non-English Terms

**Example:** "Bildung" (German)

**Handling:**
```json
{
  "term": "Bildung",
  "definition": "German concept referring to self-cultivation through education, encompassing both knowledge acquisition and character development. No direct English equivalent.",
  "context": "Central to 19th century German educational philosophy",
  "importance": "core",
  "language": "German",
  "approximate_translations": ["self-cultivation", "formation", "education"]
}
```

**Include:**
- Source language
- Cultural or conceptual nuances
- Why term is kept untranslated

### Abbreviations and Acronyms

**Example:** "BERT"

**Handling:**
```json
{
  "term": "BERT",
  "full_form": "Bidirectional Encoder Representations from Transformers",
  "definition": "Pre-trained language model that processes text bidirectionally (considering both left and right context) using transformer architecture.",
  "context": "Widely used for NLP tasks requiring contextual understanding",
  "importance": "background",
  "category": "model/architecture"
}
```

**Include:**
- Full expansion on first occurrence
- Whether to use abbreviation or full form subsequently

### Terms with Multiple Meanings

**Example:** "Model" (multiple senses in ML)

**Handling:**
```json
{
  "term": "model",
  "definition": "In machine learning context: learned function that maps inputs to outputs (e.g., 'the Transformer model'). Distinct from 'model' as theoretical framework or 'model' in statistical sense.",
  "context": "Used throughout to refer to neural network architectures",
  "importance": "core",
  "disambiguation": "Referring specifically to trained neural networks, not statistical or theoretical models"
}
```

**Include:**
- Context-specific meaning
- How this differs from other uses
- Disambiguation notes

---

## Integration with Other Skills

### With identify-terminology
- Use term identification checklist
- Apply categorization framework
- Follow glossing strategies

### With understand-academic-text
- Leverage section awareness for context
- Use structure to find definitions
- Track where terms are introduced

### With extract-arguments
- Assess which terms are central to argument
- Identify terms in claims vs background
- Prioritize terms critical to contribution

---

## Cross-Paper Glossary Extension

### Building a Field-Specific Glossary

**Approach:**
1. Extract glossary from each paper
2. Merge terms across papers
3. Track which papers use which terms
4. Note differences in usage

**Entry format for multi-paper glossary:**
```json
{
  "term": "attention mechanism",
  "consensus_definition": "Method for neural networks to focus on relevant parts of input",
  "papers_using": ["Transformer (Vaswani 2017)", "BERT (Devlin 2019)", ...],
  "usage_variations": {
    "Vaswani 2017": "Learned weighting of input positions",
    "Bahdanau 2015": "Alignment model for translation",
  },
  "evolution": "Introduced in Bahdanau 2015 for translation, generalized in Vaswani 2017, extended to pre-training in Devlin 2019"
}
```

**Benefits:**
- Track terminology evolution
- Understand different uses across subfields
- Build comprehensive field knowledge

---

## Use Cases

**Learning new field:**
- Extract glossary from foundational papers
- Build vocabulary systematically
- Track term relationships

**Teaching/explaining:**
- Create reference materials for students
- Provide accessible definitions
- Show conceptual networks

**Writing literature review:**
- Ensure consistent terminology usage
- Reference standard definitions
- Track how different authors use terms

**Cross-disciplinary work:**
- Map terminology differences across fields
- Create translation between vocabularies
- Identify shared vs distinct concepts

---

## Common Pitfalls

❌ **Including too many terms:** Not every technical word needs entry
❌ **Circular definitions:** Using term to define itself
❌ **Too vague:** Definition doesn't actually explain concept
❌ **Too technical:** Definition as complex as original term
❌ **Missing context:** Reader can't tell why term matters
❌ **No examples:** Abstract definition without usage illustration

---

## Process Checklist

### Preparation
- [ ] Read paper using understand-academic-text approach
- [ ] Flag all technical terms during reading
- [ ] Note where terms are defined or explained

### Extraction
- [ ] Identify 15-30 key terms (adjust by paper length)
- [ ] Categorize by importance
- [ ] Draft definitions for each
- [ ] Find usage examples
- [ ] Note relationships between terms

### Refinement
- [ ] Check definitions for clarity
- [ ] Verify accuracy against paper
- [ ] Add context for each term
- [ ] Ensure register consistency
- [ ] Test: Could target reader use this?

### Output
- [ ] Format as structured JSON
- [ ] Sort appropriately (alphabetical or categorical)
- [ ] Include all required fields
- [ ] Verify no terms missing

---

## Notes for Implementation

- Start with core terms (5-10), then expand to methodological and background
- Quality over quantity: 20 good entries better than 50 superficial ones
- Context is crucial: definitions alone aren't enough
- Examples ground abstract definitions
- Relationships help build conceptual understanding
- Register matters: match definitions to target audience

Remember: This glossary should be a reference you'd actually use. Make it clear, accurate, and genuinely helpful for understanding the field's vocabulary.
