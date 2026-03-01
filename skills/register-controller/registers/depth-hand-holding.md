# Explanation Depth: Hand-Holding

Assume reader is intelligent but new to the field. Explain methodology choices, connect to familiar concepts, provide context for why findings matter.

**Philosophy**: Reader can follow complex arguments but needs scaffolding for field conventions, implicit assumptions, and researcher decision-making.

## Core rules

1. **Explain why, not just what**: "They used sociolinguistic interviews rather than surveys because interviews capture what people actually say, not what they think they say."

2. **Connect to familiar concepts**: Bridge from known to unknown via analogies.
   - "Multi-head attention is like having multiple spotlights scanning a sentence. Each 'head' focuses on different relationships — one might track subject-verb agreement while another tracks long-distance dependencies."

3. **Make field conventions explicit**: Don't assume reader knows standard practices.
   - "They report p-values (probability that results are due to chance) below 0.05. In most fields, p < 0.05 is the standard threshold for 'statistically significant' — meaning we're confident enough to say the pattern is real."

4. **Explain significance**: Connect findings to broader implications.
   - "This challenges the dominant view. Before this paper, most researchers assumed transformers were just sophisticated pattern matchers. But if BERT learns hierarchical structure without explicit syntax training, it suggests language models can discover linguistic principles from data alone."

5. **Progressive unpacking**: Break complex ideas into digestible steps, building one on the previous.

## Example

**ML (Hand-Holding)**: "Previous models like RNNs processed sentences word by word, left to right. This is slow because you can't parallelize it — you have to finish word 1 before starting word 2. The transformer solves this by processing all words simultaneously. The attention mechanism lets each word 'look at' every other word to figure out which ones are relevant. For 'The cat that chased the mouse escaped,' 'escaped' needs to connect back to 'cat' (not 'mouse') — attention learns these relationships automatically."

## Watch for

- "Would a smart undergraduate from a different field understand this without looking things up?"
- Explain field conventions, not basic academic concepts (assume general academic literacy)
- Not condescending — assumes intelligence, just not prior knowledge
