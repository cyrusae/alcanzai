---
title: "Physics of Language Models: Part 3.3, Knowledge Capacity Scaling Laws"
authors: ["Allen-Zhu, Zeyuan", "Li, Yuanzhi", "Clark, Ian", "De, Gourab", "Mann, Anmol", "Ibrahim M Alabdulmohsin, Behnam", "Neyshabur, Xiaohua", "Zhai", "Allen-Zhu, Zeyuan", "Li, Yuanzhi", "Liang, Yingyu", "Allen-Zhu, Zeyuan", "Li, Yuanzhi", "Song, Zhao", "Black, Sid", "Biderman, Stella", "Hallahan, Eric", "Anthony, Quentin", "Gao, Leo", "Golding, Laurence", "He, Horace", "Leahy, Connor", "Mcdonell, Kyle", "Phang, Jason", "Pieler, Michael", "Usvsn Sai Prashanth, Shivanshu", "Purohit, Laria", "Reynolds, Jonathan", "Tow, Ben", "Wang, Samuel", "Weinbach", "Fedus, William", "Zoph, Barret", "Shazeer, Noam", "Edward, J", "Hu, Phillip", "Wallis, Zeyuan", "Allen-Zhu, Yuanzhi", "Li, Shean", "Wang, Lu", "Wang, Weizhu", "Chen", "Kwiatkowski, Tom", "Palomaki, Jennimaria", "Redfield, Olivia", "Collins, Michael", "Parikh, Ankur", "Alberti, Chris", "Epstein, Danielle", "Polosukhin, Illia", "Devlin, Jacob", "Lee, Kenton", "Li, Yuanzhi", "Liang, Yingyu", "Radford, Alec", "Wu, Jeffrey", "Child, Rewon", "Luan, David", "Amodei, Dario", "Sutskever, Ilya", "Shazeer, Noam", "Mirhoseini, Azalia", "Maziarz, Krzysztof", "Davis, Andy", "Le, Quoc", "Hinton, Geoffrey", "Dean, Jeff"]
year: 2024
venue: "Advances in neural information processing systems"
arxiv: "2404.05405"
type: "paper"
status: "unread"
added: "2026-01-09"
tags:
  - knowledge-capacity
  - scaling-laws
  - bit-complexity
  - transformer-architecture
  - language-model-training
  - quantization
  - sparse-models
  - factual-knowledge
  - information-theory
  - training-exposure
---
# Physics of Language Models: Part 3.3, Knowledge Capacity Scaling Laws

**Allen-Zhu, Zeyuan et al.** • 2024

> [!quote] Memorable Quote
> "a 7B model can store 14B bits of knowledge, surpassing the English Wikipedia and textbooks combined based on our estimation."

## Quick Refresh

This paper establishes a precise scaling law for how much factual knowledge language models can store: exactly 2 bits per parameter when trained sufficiently (1000 exposures to each fact). The authors measure knowledge capacity by training GPT-2, LLaMA, and Mistral models on synthetic datasets of (name, attribute, value) tuples—like "USA, capital, Washington D.C."—and use information-theoretic lower bounds to quantify learned knowledge rather than relying on loss or benchmark scores. They test how training duration, model architecture, quantization, sparsity (MoE), and data quality affect this ratio, finding that a 7B model could theoretically store 14 billion bits of knowledge, exceeding English Wikipedia combined.

## Why You Cared

Understanding the exact knowledge storage capacity of language models matters because it directly impacts scaling decisions: how large must a model be to contain human knowledge? Rather than hand-wavy comparisons ("GPT-4 is 10x better than GPT-3.5"), this paper offers a principled quantitative framework using information theory. The finding that knowledge capacity scales linearly with model parameters—not exponentially or sub-linearly—is a strong constraint on model design. Plus, the practical insights (e.g., that GPT-2 architecture rivals LLaMA for knowledge storage, or that domain-tagging data dramatically helps) give practitioners concrete levers to optimize training.

## Key Concepts

`#knowledge-capacity` `#scaling-laws` `#bit-complexity` `#transformer-architecture` `#language-model-training` `#quantization` `#sparse-models` `#factual-knowledge` `#information-theory` `#training-exposure`

## Cites (Key Papers)

- [[Q N +jD+D = [T L ] Let Q N +jD+1 T L -1], . . . , [T L -D + 1] for every j = 0, ...]]
- [[Q N +kd+1 = • • • = Q NLet +kd+n K = [d C ]]]
- [[Recall that each Q i is independently and uniformly generated at random from Q i...]]
- [[N ) as follows: Let n 1 be the Q 1 -th name from N 0 ; for i > 1, let n i be the...]]
- [[let a be the a ′ -th attribute in A. Construct D a = (w 1 , . . . , w D ) as fol...]]
- [[Ibrahim M Alabdulmohsin B., Neyshabur X. & Zhai (2022) - Revisiting neural scaling laws in language and vision]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 1, Context-Free Grammar]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 3.1, Knowledge Storage and ...]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 3.2, Knowledge Manipulation]]
- [[Allen-Zhu Z., Li Y. & Liang Y. (2019) - Learning and generalization in overparameterized neural netw...]]

*(29 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Advances in neural information processing systems
**arXiv:** [2404.05405](https://arxiv.org/abs/2404.05405)
**PDF:** [[arxiv_2404.05405.pdf]]

## Abstract

Scaling laws describe the relationship between the size of language models and their capabilities. Unlike prior studies that evaluate a model's capability via loss or benchmarks, we estimate the number of knowledge bits a model stores. We focus on factual knowledge represented as tuples, such as (USA, capital, Washington D.C.) from a Wikipedia page. Through multiple controlled datasets, we establish that language models can and only can store 2 bits of knowledge per parameter, even when quantized to int8, and such knowledge can be flexibly extracted for downstream applications. Consequently, a 7B model can store 14B bits of knowledge, surpassing the English Wikipedia and textbooks combined based on our estimation.

More broadly, we present 12 results on how (1) training duration, (2) model architecture, (3) quantization, (4) sparsity constraints such as MoE, and (5) data signal-to-noise ratio affect a model's knowledge storage capacity. Notable insights include:

• The GPT-2 architecture, with rotary embedding, matches or even surpasses LLaMA/Mistral architectures in knowledge storage, particularly over shorter training durations. This arises because LLaMA/Mistral uses GatedMLP, which is less stable and harder to train. • Prepending training data with domain names (e.g., wikipedia.org) significantly increases a model's knowledge capacity. Language models can autonomously identify and prioritize domains rich in knowledge, optimizing their storage capacity.

## Full Citation List

1. Q N +j D+D = [T L ] Let Q N +j D+1 T L -1], . . . , [T L -D + 1] for every j = 0, . . . , K -1
2. Q N +kd+1 = • • • = Q NLet +kd+n K = [d C ]
3. Recall that each Q i is independently and uniformly generated at random from Q i . We now present an alternative method for generating the training dataset
4. N ) as follows: Let n 1 be the Q 1 -th name from N 0 ; for i > 1, let n i be the Q i -th name from N 0 \ {n 1 NConstruct
5. let a be the a ′ -th attribute in A. Construct D a = (w 1 , . . . , w D ) as follows: Let w 1 be the Q N +(a ′ -1)D+1 -th element in T L ; for i > 1, let w i be the Q N +(a ′ -1)D+i -th element in T L \ {w 1
6. Ibrahim M Alabdulmohsin B., Neyshabur X. & Zhai (2022). Revisiting neural scaling laws in language and vision.
7. Allen Z. & Li Y. (2023). Physics of Language Models: Part 1, Context-Free Grammar.
8. Allen Z. & Li Y. (2023). Physics of Language Models: Part 3.1, Knowledge Storage and Extraction.
9. Allen Z. & Li Y. (2023). Physics of Language Models: Part 3.2, Knowledge Manipulation.
10. Allen-Zhu Z., Li Y. & Liang Y. (2019). Learning and generalization in overparameterized neural networks, going beyond two layers.
11. Allen-Zhu Z., Li Y. & Song Z. (2019). A convergence theory for deep learning via overparameterization.
12. Black S., Biderman S., Hallahan E. et al. (2022). GPT-NeoX-20B: An open-source autoregressive language model.
13. Bubeck S., Chandrasekaran V., Eldan R. et al. (2023). Sparks of artificial general intelligence: Early experiments with gpt-4.
14. Fedus W., Zoph B. & Shazeer N. (2022). Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity.
15. Frantar E., Saleh Ashkboos T., Hoefler D. et al. (2022). GPTQ: Accurate post-training compression for generative pretrained transformers.
16. Golovneva O., Allen-Zhu Z., Weston J. et al. (2024). Reverse training to nurse the reversal curse.
17. Gunasekar S., Zhang Y., Aneja J. et al. (2023). Textbooks are all you need.
18. Henighan T., Kaplan J., Katz M. et al. (2020). Scaling laws for autoregressive generative modeling.
19. Hernandez D., Kaplan J., Henighan T. et al. (2021). Scaling laws for transfer.
20. Hestness J., Narang S., Ardalani N. et al. (2017). Deep learning scaling is predictable, empirically.
21. Hoffmann J., Borgeaud S., Mensch A. et al. (2022). Training computeoptimal large language models.
22. Edward J., Hu P., Wallis Z. et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models.
23. Hwang C., Cui W., Xiong Y. et al. (2022). Tutel: Adaptive mixture-of-experts at scale.
24. Albert Q Jiang A., Sablayrolles A., Mensch C. et al. (2023). Mistral 7b.
25. Joshi M., Choi E., Weld D. S. et al. (2017). Triviaqa: A large scale distantly supervised challenge dataset for reading comprehension.
26. Kaplan J., Mccandlish S., Henighan T. et al. (2020). Scaling laws for neural language models.
27. Kwiatkowski T., Palomaki J., Redfield O. et al. (2019). Natural questions: a benchmark for question answering research.
28. Li Y. & Liang Y. (2018). Learning overparameterized neural networks via stochastic gradient descent on structured data.
29. Li Y., Bubeck S., Eldan R. et al. (2023). Textbooks are all you need ii: phi-1.5 technical report.
30. Muennighoff N., Rush A. M., Barak B. et al. (2023). Aleksandra Piktus, Nouamane Tazi, Sampo Pyysalo, Thomas Wolf, and Colin Raffel. Scaling data-constrained language models.
31. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
32. Rosenfeld J. S. (2021). Scaling laws for deep learning.
33. Rosenfeld J. S., Rosenfeld A., Belinkov Y. et al. (2019). A constructive prediction of the generalization error across scales.
34. Shazeer N. (2020). Glu variants improve transformer.
35. Shazeer N., Mirhoseini A., Maziarz K. et al. (2016). Outrageously large neural networks: The sparsely-gated mixture-of-experts layer.
36. Su J., Lu Y., Pan S. et al. (2021). Roformer: Enhanced transformer with rotary position embedding.
37. Touvron H., Lavril T., Izacard G. et al. (2023). Open and efficient foundation language models.
38. Touvron H., Martin L., Stone K. et al. (2023). Llama 2: Open foundation and fine-tuned chat models.
39. Yu D., Kaur S., Gupta A. et al. (2023). Skillmix: A flexible and expandable family of evaluations for ai models.
