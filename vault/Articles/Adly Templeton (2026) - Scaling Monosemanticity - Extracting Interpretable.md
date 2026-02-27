---
title: "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet"
authors: ["Adly Templeton*,"]
url: "https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html"
type: "article"
status: "unread"
added: "2026-02-27"
tags:
  - sparse-autoencoders
  - monosemantic-features
  - mechanistic-interpretability
  - feature-steering
  - dictionary-learning
  - superposition-hypothesis
  - code-error-detection
  - multilingual-features
  - safety-relevant-features
  - scaling-laws
  - transformer-activations
  - machine-learning
---
# Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet

**Adly Templeton*,**


**Source:** [Web](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)

> [!quote] Memorable Quote
> "We find a diversity of highly abstract features. They both respond to and behaviorally cause abstract behaviors."

## Quick Refresh

Researchers demonstrated that sparse autoencoders (SAEs—neural networks that compress activations into sparse feature representations) can successfully extract interpretable features from Claude 3 Sonnet, Anthropic's large language model, scaling up from prior work on tiny models. They trained SAEs with up to 34 million features on the model's middle-layer activations and found highly abstract, monosemantic (single-concept) features that respond to famous people, geographic locations, code error patterns, and other complex concepts. These features are remarkably sophisticated—multilingual, multimodal, and capable of controlling model behavior—and some are potentially safety-relevant, including features related to deception, bias, and security vulnerabilities.

## Why You Cared

You were concerned about mechanistic interpretability of large language models and whether dictionary learning techniques could actually scale to production-grade systems. This paper provides concrete evidence that the method works and produces genuinely useful feature decompositions, not just toy examples. The safety-relevant findings—features tracking deception, bias, and dangerous content—directly connect interpretability to AI alignment work you care about. Additionally, the systematic relationship between concept frequency and dictionary size gives you a practical framework for thinking about how large an SAE needs to be to capture specific phenomena.

## Key Concepts

`#sparse-autoencoders` `#monosemantic-features` `#mechanistic-interpretability` `#feature-steering` `#dictionary-learning` `#superposition-hypothesis` `#code-error-detection` `#multilingual-features` `#safety-relevant-features` `#scaling-laws` `#transformer-activations` `#machine-learning`

## Related Papers

*Papers referenced in this article will appear here.*

## Source Text

[[Adly Templeton (2026) - Scaling Monosemanticity - Extracting Interpretable - Source]]
