# Quick Summary

## Purpose

Generate accessible, coffee-chat style summaries of academic papers for personal knowledge management. Produces four structured outputs: summary, relevance explanation, key concepts, and memorable quote.

**Use this skill when:** You need a quick, skimmable reminder of what a paper is about and why it matters to you.

---

## Dependencies

- Uses `understand-academic-text` for paper structure comprehension
- Uses `extract-arguments` to identify main contribution
- Uses `identify-terminology` for selective jargon handling
- Uses register settings for tone and explanation depth

---

## Output Format

Generate exactly four sections using XML tags:

```xml
<summary>
3-4 sentence overview in accessible language
</summary>

<why_you_cared>
3-4 sentences explaining relevance and importance
</why_you_cared>

<key_concepts>
concept-1, concept-2, concept-3, concept-4, concept-5, general-field
</key_concepts>

<memorable_quote>
"Exact quote from the paper (not title, not abstract)"
</memorable_quote>
```

---

## Section 1: Summary

### Purpose
Provide a 3-4 sentence overview that helps someone remember "oh right, THAT paper."

### Audience
- Someone who read the paper months ago
- Someone who heard about it from someone else
- Your future self skimming notes

### Tone and Style
**Think: Coffee chat explanation**
- "This paper looks at..." not "The authors demonstrate..."
- Plain, accessible language
- Use jargon where necessary, but explain it
- Short sentences, natural flow

### Content Requirements

**Must include:**
- [ ] What they actually did (research approach)
- [ ] What they found (main results or argument)
- [ ] Core contribution (what's new or different)
- [ ] Context if needed (why this matters)

**Expand acronyms on first use:**
- "RNNs (Recurrent Neural Networks)"
- "NLP (Natural Language Processing)"
- "IMRaD (Introduction, Methods, Results, and Discussion)"

**After first expansion, use freely:**
- "The RNN model struggled with long sequences..."

### Length Guidelines
- **Minimum:** 3 sentences (too short loses key details)
- **Target:** 3-4 sentences (sweet spot)
- **Maximum:** 5 sentences (getting too long for "quick" summary)

### Quality Checks

✅ **Accessible:** Could your partner (smart non-expert) understand this?
✅ **Specific:** Does it distinguish THIS paper from similar work?
✅ **Complete:** Does it answer "what + how + so what"?
✅ **Memorable:** Would this jog your memory in 6 months?

### Examples

**Good summary (STEM):**
> This paper introduces the Transformer architecture, which relies entirely on attention mechanisms without recurrence or convolution. The model achieves state-of-the-art results on machine translation tasks (28.4 BLEU on English-German) while being more parallelizable than RNNs (Recurrent Neural Networks). Key innovation: multi-head attention allows the model to focus on different aspects of input simultaneously, and positional encodings provide sequence order information the model otherwise lacks.

**Why it's good:**
- ✅ Plain language ("relies on" vs "utilizes")
- ✅ Specific numbers (28.4 BLEU)
- ✅ Explains innovation clearly
- ✅ Expands RNN acronym
- ✅ 3 sentences, flows naturally

**Good summary (Humanities):**
> Foucault traces how power shifted from sovereign spectacle (public executions) to disciplinary surveillance (prisons, schools, hospitals) in the 18th-19th centuries. The panopticon—Bentham's prison design where a central tower observes all cells but prisoners can't see the guard—becomes his paradigm for modern power: visibility induces self-discipline. The key insight is that power works through normalization (making certain behaviors seem natural) rather than prohibition, making it more pervasive and harder to resist.

**Why it's good:**
- ✅ Historical context clear
- ✅ Explains panopticon concretely
- ✅ Defines normalization inline
- ✅ Shows stakes ("harder to resist")
- ✅ Accessible despite complex theory

**Bad summary (too technical):**
> The paper demonstrates that self-attention-based transduction models without recurrent or convolutional components achieve SOTA performance on seq2seq tasks via parallelizable multi-head attention mechanisms with learned positional embeddings.

**Why it's bad:**
- ❌ Jargon overload (SOTA, seq2seq, transduction)
- ❌ Single run-on sentence
- ❌ No expansion of terms
- ❌ Would confuse future self

**Bad summary (too vague):**
> This paper is about a new kind of neural network model. The authors test their model on some tasks and it works pretty well. Their approach is different from previous methods.

**Why it's bad:**
- ❌ No specifics (what model? what tasks?)
- ❌ Vague language ("pretty well" = how well?)
- ❌ Doesn't distinguish from any other ML paper
- ❌ Wouldn't help you remember

---

## Section 2: Why You Cared

### Purpose
Explain relevance to YOUR research/interests in 3-4 sentences. The "so what?" that made you save this paper.

### Frame as Future-Self Reminder
**Pattern:** "You were researching X, and this paper..."
- "You were exploring how LLMs handle syntax..."
- "You needed background on sociolinguistic variation..."
- "You wanted to understand Foucault's concept of power..."

### Content Requirements

**Must address:**
- [ ] What problem this helps you solve
- [ ] What gap in knowledge it fills
- [ ] How it connects to your research questions
- [ ] What specific insight you found valuable

**Avoid:**
- ❌ Generic importance ("This is an important paper in the field")
- ❌ Pure summary repetition (restate summary differently)
- ❌ Vague value statements ("This could be useful")

### Tone
**More casual than the summary:**
- Use "you" (talking to future self)
- "This bridges X and Y" not "This paper serves as a bridge"
- "You'll want to cite this when..." not "Researchers may cite"

### Domain-Specific Context

**For STEM/ML papers:**
- Focus on methodology you can use
- Benchmarks you can compare to
- Techniques you might apply

**Example:**
> You were researching how LLMs handle syntax without explicit linguistic supervision. This paper shows transformers develop implicit syntactic structure through pre-training alone—the attention heads specialize for different syntactic relations (subject-verb, dependency parsing) without being told to. This means you don't need hand-crafted features for syntax tasks; the model learns them. You'll want to cite this when arguing that language models develop structured representations.

**For Humanities/Theory:**
- Focus on conceptual framework value
- Arguments that support/challenge your thesis
- Interpretive strategies you can apply

**Example:**
> You were trying to understand how power operates in institutional settings for your thesis on educational surveillance. Foucault's panopticon gives you the conceptual framework: power works through visibility that induces self-regulation, not just through explicit rules. This helps you analyze classroom monitoring technologies—students behave differently when they know they could be watched, even if they're not being watched constantly. The normalization concept explains why students come to see surveillance as natural rather than oppressive.

**For Social Science:**
- Methodology for your data collection
- Findings relevant to your questions
- Theoretical framework you're using

**Example:**
> You were designing your sociolinguistic study on code-switching in bilingual communities. This paper's methodology—sociolinguistic interviews across different formality levels—is exactly what you need for capturing natural speech variation. The finding that code-switching serves identity negotiation (not just language deficiency) challenges deficit models you've seen in education literature. You'll adapt their interview protocol for your study.

### Quality Checks

✅ **Personal:** Speaks to YOUR specific interests/needs
✅ **Specific:** Names concrete value, not abstract importance
✅ **Actionable:** Clear how you'll use this (cite it, apply method, build on finding)
✅ **Contextual:** Shows how it fits your broader research

---

## Section 3: Key Concepts

### Purpose
Generate 5-8 searchable tags for future retrieval and connections.

### Two-Tier Structure

**Tier 1: Specific concepts (5-8 tags)**
- Topics or methods central to THIS paper
- Technical terminology
- Novel contributions

**Tier 2: General fields (2-5 tags)**
- Broader disciplines or areas
- For high-level filtering
- Connecting across subfields

### Format
Lowercase, hyphenated, no spaces
- ✅ `attention-mechanism`
- ✅ `sociolinguistic-variation`
- ✅ `foucauldian-analysis`
- ❌ `Attention Mechanism`
- ❌ `attention_mechanism`

### Content Selection

**Include:**
- Core theoretical concepts introduced
- Methods or techniques used
- Phenomena being studied
- Key findings (if tag-worthy)

**Avoid:**
- Generic terms that apply to everything ("research", "analysis")
- Author names as tags (these are in metadata)
- Venue names (also in metadata)

### Examples

**ML Paper (Transformer):**
```xml
<key_concepts>
transformers, attention-mechanism, self-attention, multi-head-attention, 
positional-encoding, neural-machine-translation, sequence-to-sequence, 
natural-language-processing, deep-learning
</key_concepts>
```

**Breakdown:**
- Specific (7): transformers, attention-mechanism, self-attention, multi-head-attention, positional-encoding, neural-machine-translation, sequence-to-sequence
- General (2): natural-language-processing, deep-learning

**Sociolinguistics Paper:**
```xml
<key_concepts>
code-switching, bilingualism, sociolinguistic-variation, identity-negotiation, 
language-attitudes, interview-methodology, qualitative-methods, 
sociolinguistics, applied-linguistics
</key_concepts>
```

**Breakdown:**
- Specific (6): code-switching, bilingualism, sociolinguistic-variation, identity-negotiation, language-attitudes, interview-methodology
- General (3): qualitative-methods, sociolinguistics, applied-linguistics

**Theory Paper (Foucault):**
```xml
<key_concepts>
panopticon, surveillance, disciplinary-power, normalization, biopower,
foucauldian-analysis, critical-theory, philosophy, social-theory
</key_concepts>
```

**Breakdown:**
- Specific (5): panopticon, surveillance, disciplinary-power, normalization, biopower
- General (4): foucauldian-analysis, critical-theory, philosophy, social-theory

### Quality Checks

✅ **Searchable:** Would you actually search for these?
✅ **Distinctive:** Differentiate this from similar papers?
✅ **Balanced:** Mix of specific + general?
✅ **Accurate:** Actually present in the paper?

---

## Section 4: Memorable Quote

### Purpose
Extract ONE standout sentence that captures a key insight, claim, or finding.

### Selection Criteria

**Look for quotes that:**
- Capture the main insight or contribution
- Are memorable/quotable (you'd actually cite this)
- Represent the paper's argument well
- Make sense with minimal context

**Where to find good quotes:**
- Introduction (stating contribution)
- Conclusion (summarizing findings)
- Key results section (stating main finding)
- Discussion (implications or insights)

### What NOT to Use

❌ **The paper title**
- "Attention Is All You Need" ← This is the title, not a quote

❌ **Abstract boilerplate**
- "In this paper we propose..." ← Generic framing

❌ **Author bio or acknowledgments**
- "We thank the reviewers..." ← Not about content

❌ **Figure captions or section headers**
- "Figure 1: Model architecture" ← Not from prose

❌ **Citations to other work**
- "As Smith (2020) showed..." ← Citing others, not their claim

### Quality Standards

**Good quotes:**
- Make a clear claim or statement
- Are 10-30 words (not too short, not too long)
- Use the paper's exact wording (verbatim)
- Include quotation marks in your output

### Examples

**Strong quotes:**

✅ "The Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output."
- **Why:** Novel contribution stated clearly

✅ "Transformers achieve state-of-the-art syntax parsing without explicit syntactic structure."
- **Why:** Surprising key finding

✅ "Power operates through normalization, making certain behaviors seem natural rather than imposed."
- **Why:** Core theoretical insight

✅ "Code-switching serves as identity negotiation, not language deficiency."
- **Why:** Challenges common assumptions

**Weak quotes:**

❌ "This paper presents a new approach."
- **Why:** Too generic, no specific insight

❌ "Future work will explore these questions further."
- **Why:** Looking forward, not capturing THIS paper

❌ "As shown in Table 2, accuracy improved."
- **Why:** Referencing a table, not standalone insight

### If No Perfect Quote Exists

**Acceptable fallbacks (in order of preference):**
1. A sentence from the conclusion summarizing the contribution
2. A sentence from the introduction stating the main claim
3. The most impactful sentence from results/discussion

**Never:**
- Make up a quote
- Use the title as the quote
- Leave the field blank

### Format
Always include quotation marks in your output:
```xml
<memorable_quote>
"Your exact quote from the paper here."
</memorable_quote>
```

---

## Integration with Dependencies

### Use understand-academic-text for:
- Identifying paper structure (where to find key info)
- Locating introduction/conclusion for quotes
- Understanding context

### Use extract-arguments for:
- Identifying main claim (goes in summary)
- Finding supporting evidence (informs summary)
- Understanding contribution (goes in why_you_cared)

### Use identify-terminology for:
- Determining what jargon to gloss (summary)
- Extracting key concepts (tags)
- Maintaining accessibility

### Apply register settings:
- **Jargon density:** Affects how much you gloss in summary/why_you_cared
- **Sentence structure:** Affects tone (conversational default for quick summary)
- **Explanation depth:** Affects how much context you provide

---

## Process Checklist

Use this workflow for each paper:

### Preparation
- [ ] Read paper using `understand-academic-text` approach
- [ ] Identify main argument using `extract-arguments`
- [ ] Flag technical terms using `identify-terminology`
- [ ] Check register settings for target audience

### Drafting
- [ ] Write 3-4 sentence summary (plain language, specific)
- [ ] Write 3-4 sentence why_you_cared (personal relevance)
- [ ] Generate 5-8 specific tags + 2-5 general tags
- [ ] Select one memorable quote (exact wording)

### Quality Check
- [ ] Summary: Accessible + specific + complete?
- [ ] Why_you_cared: Personal + actionable?
- [ ] Key concepts: Searchable + balanced?
- [ ] Quote: Memorable + representative?
- [ ] All sections use correct XML tags?

### Output
- [ ] Format with proper XML tags
- [ ] Verify quote has quotation marks
- [ ] Check no sections are blank
- [ ] Return complete structured output

---

## Common Pitfalls

❌ **Summary too technical:** Remember coffee chat tone, not academic abstract
❌ **Why_you_cared too generic:** Make it specific to user's research interests
❌ **Tags too broad:** "Machine learning" alone isn't useful—get specific
❌ **Using title as quote:** Find a real sentence from the paper
❌ **Missing XML tags:** Parser expects exact format
❌ **Not expanding acronyms:** First use must spell out

---

## Adaptation Notes

### For Different Domains

**STEM papers:**
- Summary: Focus on methodology + results
- Why_you_cared: Emphasize applicability of methods
- Tags: Include techniques, metrics, datasets

**Humanities papers:**
- Summary: Focus on argument + theoretical framework
- Why_you_cared: Emphasize conceptual value
- Tags: Include theorists, concepts, close reading subjects

**Social science papers:**
- Summary: Focus on research question + findings
- Why_you_cared: Emphasize methodology + implications
- Tags: Include methods, populations, social factors

### For Different Paper Types

**Empirical papers:** Focus on findings and methods
**Theoretical papers:** Focus on concepts and arguments
**Review papers:** Focus on synthesis and gaps identified
**Methodological papers:** Focus on technique and applications

---

## Self-Check

After generating synthesis:

✅ Would I understand this without reading the full paper?
✅ Would this help me remember the paper in 6 months?
✅ Is the relevance clear and specific?
✅ Are tags actually searchable/useful?
✅ Would I actually quote that sentence?

If any answer is no, revise that section.

---

## Notes for Implementation

- This skill produces structured output for parsing
- Register settings affect ALL sections (tone, jargon, depth)
- Domain context informs "why_you_cared" framing
- Quality over speed: Take time to find the right quote
- When uncertain, err toward more accessible language

Remember: This is for YOUR future self. Make it actually useful for skimming and remembering, not just technically complete.
