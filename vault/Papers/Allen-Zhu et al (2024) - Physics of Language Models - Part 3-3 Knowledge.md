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
  - knowledge-capacity-scaling
  - bit-complexity
  - language-model-efficiency
  - transformer-architecture
  - quantization-effects
  - training-duration
  - model-parametrization
  - junk-data-robustness
  - knowledge-extraction
  - mixture-of-experts
---
# Physics of Language Models: Part 3.3, Knowledge Capacity Scaling Laws

**Allen-Zhu, Zeyuan et al.** • 2024

> [!quote] Memorable Quote
> "Larger models can store more knowledge, but does the total knowledge scale linearly with the model's size? What is the exact constant of this scaling?"

## Quick Refresh

This paper establishes that language models store factual knowledge at a constant rate of approximately 2 bits per parameter when trained sufficiently on knowledge-rich data. The authors measure this by training transformer models (GPT-2, LLaMA, Mistral) on synthetic datasets of (name, attribute, value) tuples and deriving a theoretical "bit complexity lower bound" that quantifies how much knowledge a model has learned. Key finding: a 7B parameter model can store ~14 billion bits of knowledge—exceeding English Wikipedia—and this ratio holds across different architectures, model sizes, and training regimes, though it degrades with insufficient training or noisy data.

## Why You Cared

Understanding how knowledge scales with model size is fundamental to predicting whether massive models are necessary or if smaller, well-trained models could suffice. Rather than relying on benchmark scores (which conflate architecture, data, and size), this paper provides a precise, theoretically grounded measurement framework. It reveals practical insights: GPT-2 rivals modern architectures for knowledge storage; gated MLPs underperform on moderately rare knowledge; int8 quantization doesn't hurt capacity; and junk data is devastating unless domains are explicitly marked. For practitioners choosing model sizes or data strategies, this is a principled alternative to traditional scaling law studies.

## Key Concepts

`#knowledge-capacity-scaling` `#bit-complexity` `#language-model-efficiency` `#transformer-architecture` `#quantization-effects` `#training-duration` `#model-parametrization` `#junk-data-robustness` `#knowledge-extraction` `#mixture-of-experts`

## Cites (Key Papers)

- [[k-D 10 -C 1-K5 -L1 -T4 0k N5 00 k-D 10 -C 1-K1 0-L1 -T4 0k N5 00 k-D 10 -C 1-K2 ...]]
- [[Ibrahim M Alabdulmohsin B., Neyshabur X. & Zhai (2022) - Revisiting neural scaling laws in language and vision]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 1, Context-Free Grammar]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 3.1, Knowledge Storage and ...]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 3.2, Knowledge Manipulation]]
- [[Allen-Zhu Z., Li Y. & Liang Y. (2019) - Learning and generalization in overparameterized neural netw...]]
- [[Allen-Zhu Z., Li Y. & Song Z. (2019) - A convergence theory for deep learning via overparameterizat...]]
- [[Black S., Biderman S., Hallahan E., Anthony Q., Gao L., Golding L., He H., Leahy C., Mcdonell K., Phang J., Pieler M., Usvsn Sai Prashanth S., Purohit L., Reynolds J., Tow B., Wang S. & Weinbach (2022) - GPT-NeoX-20B: An open-source autoregressive language model]]
- [[Bubeck S., Chandrasekaran V., Eldan R., Gehrke J., Horvitz E., Kamar E., Lee P., Tat Lee Y., Li Y. & Lundberg S. (2023) - Sparks of artificial general intelligence: Early experiments...]]
- [[Fedus W., Zoph B. & Shazeer N. (2022) - Switch transformers: Scaling to trillion parameter models wi...]]

*(25 more citations below)*

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

1. k-D 10 -C 1-K5 -L1 -T4 0k N5 00 k-D 10 -C 1-K1 0-L1 -T4 0k N5 00 k-D 10 -C 1-K2 0-L1 -T4 0k N2 00 k-D 10 -C 1-K 5 0-L1 -T4 0k N1 00 0k -D 10 -C 1-K1 -L4 -T4 0k N1 00 0k -D 10 -C 1-K2 -L4 -T4 0k N5 00 k-D 10 -C 1-K5 -L4 -T4 0k N5 00 k-D 10 -C 1-K1 0-L4 -T4 0k N5 00 k-D 10 -C 1-K2 0-L4 -T4 0k N2 00 k-D 10 -C 1-K5 0-L4 -T4 0k N1 00 0k -D 10 00 0-C1 -K 1-L4 -T4 0k N1 00 0k -D 10 00 0-C1 -K 2-L4 -T4 0k N5 00 k-D 10 00 0-C1 -K 5-L4 -T4 0k N5 00 k-D 10 00 0-C1 -K 10 -L4 -T4 0k N2 00 k-D 10 00 0-C1 -K 20 -L4 -T4 0k N1 00 k-D 10 00 0-C1 -K 50 -L4 -T4 0k
2. Ibrahim M Alabdulmohsin B., Neyshabur X. & Zhai (2022). Revisiting neural scaling laws in language and vision.
3. Allen Z. & Li Y. (2023). Physics of Language Models: Part 1, Context-Free Grammar.
4. Allen Z. & Li Y. (2023). Physics of Language Models: Part 3.1, Knowledge Storage and Extraction.
5. Allen Z. & Li Y. (2023). Physics of Language Models: Part 3.2, Knowledge Manipulation.
6. Allen-Zhu Z., Li Y. & Liang Y. (2019). Learning and generalization in overparameterized neural networks, going beyond two layers.
7. Allen-Zhu Z., Li Y. & Song Z. (2019). A convergence theory for deep learning via overparameterization.
8. Black S., Biderman S., Hallahan E. et al. (2022). GPT-NeoX-20B: An open-source autoregressive language model.
9. Bubeck S., Chandrasekaran V., Eldan R. et al. (2023). Sparks of artificial general intelligence: Early experiments with gpt-4.
10. Fedus W., Zoph B. & Shazeer N. (2022). Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity.
11. Frantar E., Saleh Ashkboos T., Hoefler D. et al. (2022). GPTQ: Accurate post-training compression for generative pretrained transformers.
12. Golovneva O., Allen-Zhu Z., Weston J. et al. (2024). Reverse training to nurse the reversal curse.
13. Gunasekar S., Zhang Y., Aneja J. et al. (2023). Textbooks are all you need.
14. Henighan T., Kaplan J., Katz M. et al. (2020). Scaling laws for autoregressive generative modeling.
15. Hernandez D., Kaplan J., Henighan T. et al. (2021). Scaling laws for transfer.
16. Hestness J., Narang S., Ardalani N. et al. (2017). Deep learning scaling is predictable, empirically.
17. Hoffmann J., Borgeaud S., Mensch A. et al. (2022). Training computeoptimal large language models.
18. Edward J., Hu P., Wallis Z. et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models.
19. Hwang C., Cui W., Xiong Y. et al. (2022). Tutel: Adaptive mixture-of-experts at scale.
20. Albert Q Jiang A., Sablayrolles A., Mensch C. et al. (2023). Mistral 7b.
21. Joshi M., Choi E., Weld D. S. et al. (2017). Triviaqa: A large scale distantly supervised challenge dataset for reading comprehension.
22. Kaplan J., Mccandlish S., Henighan T. et al. (2020). Scaling laws for neural language models.
23. Kwiatkowski T., Palomaki J., Redfield O. et al. (2019). Natural questions: a benchmark for question answering research.
24. Li Y. & Liang Y. (2018). Learning overparameterized neural networks via stochastic gradient descent on structured data.
25. Li Y., Bubeck S., Eldan R. et al. (2023). Textbooks are all you need ii: phi-1.5 technical report.
26. Muennighoff N., Rush A. M., Barak B. et al. (2023). Aleksandra Piktus, Nouamane Tazi, Sampo Pyysalo, Thomas Wolf, and Colin Raffel. Scaling data-constrained language models.
27. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
28. Rosenfeld J. S. (2021). Scaling laws for deep learning.
29. Rosenfeld J. S., Rosenfeld A., Belinkov Y. et al. (2019). A constructive prediction of the generalization error across scales.
30. Shazeer N. (2020). Glu variants improve transformer.
31. Shazeer N., Mirhoseini A., Maziarz K. et al. (2016). Outrageously large neural networks: The sparsely-gated mixture-of-experts layer.
32. Su J., Lu Y., Pan S. et al. (2021). Roformer: Enhanced transformer with rotary position embedding.
33. Touvron H., Lavril T., Izacard G. et al. (2023). Open and efficient foundation language models.
34. Touvron H., Martin L., Stone K. et al. (2023). Llama 2: Open foundation and fine-tuned chat models.
35. Yu D., Kaur S., Gupta A. et al. (2023). Skillmix: A flexible and expandable family of evaluations for ai models.
