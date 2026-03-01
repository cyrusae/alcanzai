---
title: "Values in the wild: Discovering and analyzing values in real-world language model interactions"
authors: ["Unknown"]
url: "https://www.anthropic.com/research/values-wild"
type: "article"
status: "unread"
added: "2026-02-27"
tags:
  - ai-alignment
  - value-expression
  - language-model-behavior
  - constitutional-ai
  - real-world-evaluation
  - contextualized-values
  - jailbreak-detection
  - value-mirroring
  - sycophancy
  - privacy-preserving-analysis
---
# Values in the wild: Discovering and analyzing values in real-world language model interactions

**Unknown**


**Source:** [Web](https://www.anthropic.com/research/values-wild)

> [!quote] Memorable Quote
> "If we want those judgments to be congruent with our own values (which is, after all, the central goal of AI alignment research) then we need to have ways of testing which values a model expresses in the real world."

## Quick Refresh

This paper describes a method for observing what values AI systems express during real-world conversations. Anthropic's Societal Impacts team analyzed 308,210 anonymized conversations with Claude (filtering to those involving subjective judgment) and built a hierarchical taxonomy of values—grouped into five top categories (Practical, Epistemic, Social, Protective, Personal) with dozens of specific values underneath. They found that Claude generally aligns with its training toward helpfulness, honesty, and harmlessness, but also discovered that expressed values shift contextually (romantic advice triggered emphasis on "healthy boundaries"; controversial history prompted "historical accuracy") and that Claude frequently mirrors user values while occasionally reframing or resisting them.

## Why You Cared

You care about AI alignment and want concrete evidence of whether training actually shapes real-world behavior. This paper is directly relevant because it moves beyond pre-deployment testing to monitor deployed models in production—a critical gap in current practice. The method they developed, using privacy-preserving data collection and language models to extract values, gives you a scalable framework for auditing your own systems, and the released dataset lets you run comparative analyses if you're working in a related space.

## Key Concepts

`#ai-alignment` `#value-expression` `#language-model-behavior` `#constitutional-ai` `#real-world-evaluation` `#contextualized-values` `#jailbreak-detection` `#value-mirroring` `#sycophancy` `#privacy-preserving-analysis`

## Related Papers

*Papers referenced in this article will appear here.*

## Source Text

[[Unknown (2026) - Values in the wild - Discovering and analyzing values in - Source]]
