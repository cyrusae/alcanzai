# Jargon Density: None

## Strategy
Prioritize accessible explanations over technical terminology. Use plain language as primary, with technical terms introduced secondarily for vocabulary building.

**When to use:**
- Complete newcomers to the field
- Partner-shareable content (smart non-expert audience)
- Interdisciplinary readers unfamiliar with domain
- Neuropsych papers or other fields where user lacks background

---

## Core Principle

**Explanation first, term second**

Think: "Here's what this means (and experts call it X)"

NOT: "X means this"

---

## Format Pattern

```
[accessible explanation] (technical term: [additional detail if needed])
```

### Examples

**Phonetics:**
✅ "Hissing sounds made with your tongue near your teeth (alveolar fricatives like 's' and 'z')"
❌ "Alveolar fricatives (hissing sounds)"

**Machine Learning:**
✅ "The model learns by adjusting numbers to reduce errors (called gradient descent)"
❌ "Gradient descent (adjusting parameters to minimize loss)"

**Critical Theory:**
✅ "When one culture's way of thinking feels so normal that alternatives seem wrong (hegemony in Gramsci's terms)"
❌ "Hegemony (cultural dominance)"

---

## When to Include Technical Terms

### Always include (for vocabulary building):
- Core concepts central to the paper
- Terms user will encounter repeatedly
- Standard field terminology

**But make them secondary:**
- Put in parentheses after explanation
- Add "called X" or "known as X" framing
- Include brief extra context if helpful

### Can skip:
- Very specialized jargon used once
- Abbreviations for simple concepts
- Terms obvious from context

---

## Explanation Strategies

### Use Analogies
Connect unfamiliar concepts to familiar ones

**Good:**
"Like autocomplete but for entire sentences (language models predict next words)"

**Better than:**
"Language models (systems that predict next tokens in sequences)"

### Use Concrete Examples
Ground abstract concepts in specific instances

**Good:**
"Words like 'bank' have multiple meanings—the financial institution or the river's edge (polysemy: one word, multiple senses)"

**Better than:**
"Polysemy (when a single word has multiple related meanings)"

### Use Functional Descriptions
Explain what something DOES before what it IS

**Good:**
"Software that automatically matches spoken words to written text (called forced alignment)"

**Better than:**
"Forced alignment (automatic speech-to-text matching)"

### Build Up Complexity
Start simple, add detail

**Good:**
"The model looks at all the words at once (parallel processing), unlike older models that had to read one word at a time (sequential processing). This is why transformers train faster."

**Better than:**
"Transformers use parallel processing instead of sequential processing, enabling faster training."

---

## Length Considerations

Expect longer explanations than other registers:
- **Selective:** 15-20 words average
- **None:** 20-30 words average (more scaffolding needed)
- **Heavy:** 5-10 words average

Trade length for clarity—accessible explanations take more words.

---

## Tone

### Conversational and Patient
- "This is like..." not "Analogous to..."
- "They found that..." not "The study demonstrates..."
- "The cool part is..." not "Notably,"

### Explicit Connections
Don't assume reader makes conceptual leaps

**Good:**
"The model pays attention to different words when making predictions. This attention mechanism lets it focus on relevant parts—like how you might focus on the verb when understanding a sentence's tense."

**Too implicit:**
"Attention mechanisms enable selective focus on relevant input positions."

### Define By Showing
Use examples as definitions

**Good:**
"Languages vary in systematic ways. Spanish speakers might say 'no sé' where English speakers say 'I don't know'—both patterns are regular, just different (linguistic variation)."

**Too abstract:**
"Linguistic variation (systematic differences in language use across speakers or contexts)"

---

## Technical Term Introduction Patterns

### Pattern 1: Parenthetical Definition
`[explanation] (technical term)`

"The tiny delay between releasing your lips for 'p' and starting the vowel sound (Voice Onset Time, or VOT for short)"

### Pattern 2: "Called" Construction  
`[explanation] called [term]`

"This is called self-attention because each word attends to all other words, including itself"

### Pattern 3: "Known as" Construction
`[explanation] known as [term]`

"This pattern is known as code-switching in linguistics"

### Pattern 4: Appositive
`[explanation]—[term in context]`

"The model adjusts its internal numbers to reduce mistakes—a process researchers call gradient descent"

---

## Examples Across Domains

### Linguistics (Phonetics)

**Selective register:**
"Alveolar fricatives (hissing sounds like 's' or 'z' made with tongue near teeth)"

**None register:**
"Hissing sounds you make by pushing air through a narrow space created when your tongue is near the bumpy area behind your upper teeth. Think of the 's' in 'snake' or the 'z' in 'zebra.' Linguists call these alveolar fricatives because they're made at the alveolar ridge (that bumpy area)."

### Machine Learning

**Selective register:**
"Gradient descent (iterative method for minimizing error by adjusting parameters)"

**None register:**
"Imagine you're hiking down a mountain in thick fog and can only see a few feet ahead. You'd feel around with your foot to find which direction slopes downward, then take a step that way. Keep repeating until you reach the bottom. That's basically how gradient descent works—the model makes small adjustments to reduce errors, checking after each adjustment whether it's going in the right direction. 'Gradient' just means slope, and 'descent' means going downhill toward lower error."

### Critical Theory

**Selective register:**
"Hegemony (cultural dominance that feels natural rather than imposed)"

**None register:**
"Imagine growing up in a society where everyone assumes certain jobs are 'for men' and others 'for women.' Nobody enforces this with laws, but it feels so normal that alternatives seem weird or wrong. That's hegemony—when one group's worldview becomes so dominant it feels like just 'the way things are' rather than one possible choice among many. Gramsci called this cultural dominance without force."

---

## When Explanation Would Be Too Long

### Strategy 1: Break into pieces
Instead of one massive gloss, explain in steps across sentences

**Not this:**
"RNNs (Recurrent Neural Networks—neural networks that process sequences by maintaining a hidden state that gets updated at each step, allowing them to handle variable-length inputs like sentences, though they must process sequentially which prevents parallelization)"

**Do this:**
"Older models called RNNs process text one word at a time, keeping track of what they've seen so far in a kind of memory (the 'hidden state'). This works, but it's slow because they can't skip ahead—they have to read word 1 before word 2 before word 3, and so on. The 'recurrent' part means they loop back and update their memory at each step."

### Strategy 2: Defer details
Give functional explanation now, technical details later if needed

**Initial:**
"The model uses a technique called attention to focus on relevant words"

**Later if needed:**
"That attention mechanism works by calculating weights for each word based on how related it is to the current position"

### Strategy 3: Use footnote/aside pattern
Main explanation stays accessible, parenthetical adds precision

**Example:**
"They measured how the sound changes over time by looking at a visual graph of the sound wave (technically called a spectrogram, which shows frequency on the vertical axis and time on the horizontal)"

---

## Quality Checks

When writing in None register, verify:

✅ **Accessible:** Could someone with no field knowledge understand this?
✅ **Concrete:** Are there examples or analogies?
✅ **Patient:** Is the explanation unhurried?
✅ **Complete:** Does it actually explain the concept, not just name it?
✅ **Vocabulary-building:** Are technical terms still present (secondarily)?

---

## Common Pitfalls

❌ **Condescending tone:** Don't talk down
- Bad: "Simply put..." "Basically..."
- Good: Natural conversational tone

❌ **Explaining too much:** Not every word needs definition
- Bad: "Scientists (people who study things) use methods (ways of doing research)..."
- Good: Use normal words without over-glossing

❌ **Abandoning precision:** Accessible ≠ vague
- Bad: "It's kind of like magic how it works"
- Good: "It works by [concrete mechanism explained simply]"

❌ **No technical terms:** Defeats vocabulary-building purpose
- Bad: Only explanations, never introducing proper terminology
- Good: Explanations first, then technical terms for reference

---

## Integration with Other Registers

### Compared to Selective
- Selective: "Term (explanation)"
- None: "Explanation (term)"

### Compared to Heavy
- Heavy: "Technical term only"
- None: "Explanation (with term for reference)"

### Use Cases

**Choose None when:**
- Reader has no domain background
- Material is very specialized/technical
- Goal is accessibility over efficiency
- Sharing with non-expert audiences

**Choose Selective instead when:**
- Reader is learning the field
- Want balance of access + vocabulary building
- Some domain familiarity exists

**Choose Heavy instead when:**
- Reader is expert
- Efficiency matters more than accessibility
- Technical precision is priority

---

## Notes for Implementation

- Expect 1.5-2x word count vs Selective register
- Use more complete sentences, fewer parentheticals
- Analogies and examples are your friends
- Don't sacrifice accuracy for simplicity
- Technical terms should still appear (for learning)
- Patient explanations build understanding

Remember: The goal is genuine understanding, not dumbing down. Accessible explanations can be just as rigorous as technical ones—they just take more words and use more familiar concepts.
