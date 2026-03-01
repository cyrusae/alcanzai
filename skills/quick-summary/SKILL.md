---
name: quick-summary
description: Generate accessible quick summaries of academic papers. Use when creating coffee-chat style synthesis notes with four structured sections — summary, why-you-cared, key concepts, and memorable quote.
---

# Quick Summary

Generate exactly four sections using XML tags. Apply register settings from register-controller to all sections.

## Output format

```xml
<summary>
3-4 sentence overview
</summary>

<why_you_cared>
3-4 sentences explaining relevance
</why_you_cared>

<key_concepts>
concept-1, concept-2, concept-3, concept-4, concept-5, general-field
</key_concepts>

<memorable_quote>
"Exact quote from the paper."
</memorable_quote>
```

## Section 1: Summary

**Goal**: Help someone remember "oh right, THAT paper" after reading it months ago.

- What they did (method/approach)
- What they found (main result)
- Core contribution (what's new)

**Tone**: Coffee chat, not conference talk. "This paper looks at..." not "The authors demonstrate..."

**Expand acronyms on first use**: "RNNs (Recurrent Neural Networks)". After that, use freely.

Length: 3-4 sentences. Not fewer, not more.

## Section 2: Why You Cared

**Goal**: Explain why *this person* saved *this paper*. Personal relevance, not generic importance.

Frame as talking to future self: "You were researching X, and this paper..."

- What problem it helps solve
- What gap it fills
- Concrete value ("you'll cite this when...", "you can apply this method to...")

**Avoid**: "This is an important paper in the field." — too generic.

More casual than the summary. Use "you" throughout.

## Section 3: Key Concepts

5-8 specific concept tags + 2-5 general field tags. Lowercase, hyphenated.

- Specific: topics/methods central to THIS paper
- General: broader disciplines for cross-paper search

Format: `attention-mechanism` not `Attention Mechanism` or `attention_mechanism`

Do not include: generic terms ("research", "analysis"), author names, venue names.

## Section 4: Memorable Quote

One standout sentence from the paper itself — exact wording, verbatim.

**Find it in**: Introduction (stating contribution), Conclusion (summarizing findings), Results/Discussion (key insight).

**Good quote**: Makes a clear claim, 10-30 words, memorable, stands alone without context.

**Never use**:
- The paper title
- "In this paper we..." boilerplate
- Figure captions or section headers
- Quotes about future work

If no perfect quote exists: conclusion sentence summarizing the contribution.

Always include quotation marks in output.

## Common pitfalls

- Summary too technical → aim for coffee chat, not abstract
- Why_you_cared too generic → make it specific to research context
- Tags too broad → "machine-learning" alone isn't useful; get specific
- Title used as quote → find a real sentence from the body
- Missing XML tags → parser requires exact format
