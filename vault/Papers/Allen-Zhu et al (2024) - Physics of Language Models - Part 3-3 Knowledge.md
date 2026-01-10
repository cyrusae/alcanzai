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
  - language-models
  - transformer-architecture
  - quantization
  - model-efficiency
  - training-exposure
  - data-quality
  - sparse-models
  - synthetic-datasets
---
# Physics of Language Models: Part 3.3, Knowledge Capacity Scaling Laws

**Allen-Zhu, Zeyuan et al.** â€¢ 2024

> [!quote] Memorable Quote
> "Language models can autonomously identify and prioritize domains rich in knowledge, optimizing their storage capacity."

## Quick Refresh

This paper establishes that language models can store approximately 2 bits of knowledge per parameter when sufficiently trained, using synthetic datasets of (name, attribute, value) tuples converted to natural language. Through controlled experiments varying model size, architecture, training duration, quantization, and data quality, the authors show this 2-bit-per-parameter ratio holds consistently—meaning a 7B model could theoretically store 14B bits of knowledge, exceeding English Wikipedia. The work provides a principled framework for measuring knowledge capacity that sidesteps the ambiguities of benchmark-based comparisons.

## Why You Cared

You bookmarked this because it answers a fundamental but previously fuzzy question: *how much knowledge can a language model actually store, and how does that scale with size?* Rather than relying on noisy benchmark comparisons (which conflate architecture, data, and scale), the authors use a controlled synthetic setting to extract a clean constant—2 bits per parameter—that has real practical implications for model selection and training decisions. The paper also surfaces surprising findings (e.g., GPT-2 matches newer architectures for knowledge storage; data diversity matters more than repetition) that challenge conventional wisdom and offer a reusable experimental methodology for future architecture comparisons.

## Key Concepts

`#knowledge-capacity` `#scaling-laws` `#bit-complexity` `#language-models` `#transformer-architecture` `#quantization` `#model-efficiency` `#training-exposure` `#data-quality` `#sparse-models` `#synthetic-datasets`

## Cites (Key Papers)

- [[Ibrahim M Alabdulmohsin B., Neyshabur X. & Zhai (2022) - Revisiting neural scaling laws in language and vision]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 1, Context-Free Grammar]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 3.1, Knowledge Storage and ...]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 3.2, Knowledge Manipulation]]
- [[Allen-Zhu Z., Li Y. & Liang Y. (2019) - Learning and generalization in overparameterized neural netw...]]
- [[Allen-Zhu Z., Li Y. & Song Z. (2019) - A convergence theory for deep learning via overparameterizat...]]
- [[Black S., Biderman S., Hallahan E., Anthony Q., Gao L., Golding L., He H., Leahy C., Mcdonell K., Phang J., Pieler M., Usvsn Sai Prashanth S., Purohit L., Reynolds J., Tow B., Wang S. & Weinbach (2022) - GPT-NeoX-20B: An open-source autoregressive language model]]
- [[Bubeck S., Chandrasekaran V., Eldan R., Gehrke J., Horvitz E., Kamar E., Lee P., Tat Lee Y., Li Y. & Lundberg S. (2023) - Sparks of artificial general intelligence: Early experiments...]]
- [[Fedus W., Zoph B. & Shazeer N. (2022) - Switch transformers: Scaling to trillion parameter models wi...]]
- [[Frantar E., Saleh Ashkboos T., Hoefler D. & Alistarh (2022) - GPTQ: Accurate post-training compression for generative pret...]]

*(24 more citations below)*

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

1. Ibrahim M Alabdulmohsin B., Neyshabur X. & Zhai (2022). Revisiting neural scaling laws in language and vision.
2. Allen Z. & Li Y. (2023). Physics of Language Models: Part 1, Context-Free Grammar.
3. Allen Z. & Li Y. (2023). Physics of Language Models: Part 3.1, Knowledge Storage and Extraction.
4. Allen Z. & Li Y. (2023). Physics of Language Models: Part 3.2, Knowledge Manipulation.
5. Allen-Zhu Z., Li Y. & Liang Y. (2019). Learning and generalization in overparameterized neural networks, going beyond two layers. Advances in neural information processing systems, Vol. 32.
6. Allen-Zhu Z., Li Y. & Song Z. (2019). A convergence theory for deep learning via overparameterization.
7. Black S., Biderman S., Hallahan E. et al. (2022). GPT-NeoX-20B: An open-source autoregressive language model.
8. Bubeck S., Chandrasekaran V., Eldan R. et al. (2023). Sparks of artificial general intelligence: Early experiments with gpt-4.
9. Fedus W., Zoph B. & Shazeer N. (2022). Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. The Journal of Machine Learning Research, Vol. 23(1), pp. 5232-5270.
10. Frantar E., Saleh Ashkboos T., Hoefler D. et al. (2022). GPTQ: Accurate post-training compression for generative pretrained transformers.
11. Golovneva O., Allen-Zhu Z., Weston J. et al. (2024). Reverse training to nurse the reversal curse.
12. Gunasekar S., Zhang Y., Aneja J. et al. (2023). Textbooks are all you need.
13. Henighan T., Kaplan J., Katz M. et al. (2020). Scaling laws for autoregressive generative modeling.
14. Hernandez D., Kaplan J., Henighan T. et al. (2021). Scaling laws for transfer.
15. Hestness J., Narang S., Ardalani N. et al. (2017). Deep learning scaling is predictable, empirically.
16. Hoffmann J., Borgeaud S., Mensch A. et al. (2022). Training computeoptimal large language models.
17. Edward J., Hu P., Wallis Z. et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models.
18. Hwang C., Cui W., Xiong Y. et al. (2022). Tutel: Adaptive mixture-of-experts at scale.
19. Albert Q Jiang A., Sablayrolles A., Mensch C. et al. (2023). Mistral 7b.
20. Joshi M., Choi E., Weld D. S. et al. (2017). Triviaqa: A large scale distantly supervised challenge dataset for reading comprehension.
21. Kaplan J., Mccandlish S., Henighan T. et al. (2020). Scaling laws for neural language models.
22. Kwiatkowski T., Palomaki J., Redfield O. et al. (2019). Natural questions: a benchmark for question answering research. Transactions of the Association for Computational Linguistics, Vol. 7, pp. 453-466.
23. Li Y. & Liang Y. (2018). Learning overparameterized neural networks via stochastic gradient descent on structured data.
24. Li Y., Bubeck S., Eldan R. et al. (2023). Textbooks are all you need ii: phi-1.5 technical report.
25. Muennighoff N., Rush A. M., Barak B. et al. (2023). Aleksandra Piktus, Nouamane Tazi, Sampo Pyysalo, Thomas Wolf, and Colin Raffel. Scaling data-constrained language models.
26. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners. OpenAI blog, Vol. 1(8), pp. 9.
27. Rosenfeld J. S. (2021). Scaling laws for deep learning.
28. Rosenfeld J. S., Rosenfeld A., Belinkov Y. et al. (2019). A constructive prediction of the generalization error across scales.
29. Shazeer N. (2020). Glu variants improve transformer.
30. Shazeer N., Mirhoseini A., Maziarz K. et al. (2016). Outrageously large neural networks: The sparsely-gated mixture-of-experts layer.
31. Su J., Lu Y., Pan S. et al. (2021). Roformer: Enhanced transformer with rotary position embedding.
32. Touvron H., Lavril T., Izacard G. et al. (2023). Open and efficient foundation language models.
33. Touvron H., Martin L., Stone K. et al. (2023). Llama 2: Open foundation and fine-tuned chat models.
34. Yu D., Kaur S., Gupta A. et al. (2023). Skillmix: A flexible and expandable family of evaluations for ai models.
