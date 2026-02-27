---
title: "Sparse Crosscoders for Cross-Layer Features and Model Diffing"
authors: ["Jack Lindsey*,"]
url: "https://transformer-circuits.pub/2024/crosscoders/index.html"
type: "article"
status: "unread"
added: "2026-02-26"
tags:
  - sparse-autoencoders
  - crosscoders
  - transcoders
  - superposition
  - dictionary-learning
  - residual-stream
  - feature-interpretation
  - model-diffing
  - circuit-analysis
  - mechanistic-interpretability
---
# Sparse Crosscoders for Cross-Layer Features and Model Diffing

**Jack Lindsey*,**


**Source:** [Web](https://transformer-circuits.pub/2024/crosscoders/index.html)

> [!quote] Memorable Quote
> "If features are jointly represented by multiple layers, where some of their activity can be understood as being in parallel, it is natural to apply dictionary learning to them jointly."

## Quick Refresh

This paper introduces sparse crosscoders, a generalization of sparse autoencoders that read from and write to multiple layers of neural networks simultaneously. Where standard SAEs (Sparse Autoencoders) operate on single layers and transcoders predict one layer from the previous one, crosscoders extract shared features that span across layers and even across entirely different models. The authors demonstrate that crosscoders identify redundant structure across layers more efficiently than training separate per-layer SAEs, and show two key applications: simplifying circuit analysis by tracking persistent features across the residual stream, and enabling "model diffing" to compare feature representations between different model versions or architectures.

## Why You Cared

You care about interpretability of neural networks and mechanistic understanding of how they process information. Crosscoders offer a promising method for simplifying the complexity of circuit analysis by consolidating duplicate features that persist across layers—a problem that per-layer SAE analysis struggles with. The model diffing application is particularly relevant if you are interested in comparing how different training runs, finetuned versions, or scaled models learn similar or different internal representations. This gives you concrete tools to audit what changes (and what stays the same) when a model is modified.

## Key Concepts

`#sparse-autoencoders` `#crosscoders` `#transcoders` `#superposition` `#dictionary-learning` `#residual-stream` `#feature-interpretation` `#model-diffing` `#circuit-analysis` `#mechanistic-interpretability`

## Related Papers

*Papers referenced in this article will appear here.*

## Source Text

[[Jack Lindsey (2026) - Sparse Crosscoders for Cross-Layer Features and Model - Source]]
