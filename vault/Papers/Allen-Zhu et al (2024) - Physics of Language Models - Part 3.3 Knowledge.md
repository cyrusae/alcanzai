---
title: "Physics of Language Models: Part 3.3, Knowledge Capacity Scaling Laws"
authors: ["Allen-Zhu, Zeyuan", "Li, Yuanzhi", "Clark, Ian", "De, Gourab", "Mann, Anmol", "Ibrahim M Alabdulmohsin, Behnam", "Neyshabur, Xiaohua", "Zhai", "Allen-Zhu, Zeyuan", "Li, Yuanzhi", "Liang, Yingyu", "Allen-Zhu, Zeyuan", "Li, Yuanzhi", "Song, Zhao", "Black, Sid", "Biderman, Stella", "Hallahan, Eric", "Anthony, Quentin", "Gao, Leo", "Golding, Laurence", "He, Horace", "Leahy, Connor", "Mcdonell, Kyle", "Phang, Jason", "Pieler, Michael", "Usvsn Sai Prashanth, Shivanshu", "Purohit, Laria", "Reynolds, Jonathan", "Tow, Ben", "Wang, Samuel", "Weinbach", "Fedus, William", "Zoph, Barret", "Shazeer, Noam", "Edward, J", "Hu, Phillip", "Wallis, Zeyuan", "Allen-Zhu, Yuanzhi", "Li, Shean", "Wang, Lu", "Wang, Weizhu", "Chen", "Kwiatkowski, Tom", "Palomaki, Jennimaria", "Redfield, Olivia", "Collins, Michael", "Parikh, Ankur", "Alberti, Chris", "Epstein, Danielle", "Polosukhin, Illia", "Devlin, Jacob", "Lee, Kenton", "Li, Yuanzhi", "Liang, Yingyu", "Radford, Alec", "Wu, Jeffrey", "Child, Rewon", "Luan, David", "Amodei, Dario", "Sutskever, Ilya", "Shazeer, Noam", "Mirhoseini, Azalia", "Maziarz, Krzysztof", "Davis, Andy", "Le, Quoc", "Hinton, Geoffrey", "Dean, Jeff"]
year: 2024
venue: "Advances in neural information processing systems"
arxiv: "2404.05405"
type: "paper"
status: "unread"
added: "2026-01-08"
tags:
  - knowledge-capacity
  - scaling-laws
  - language-model-efficiency
  - bit-complexity
  - factual-knowledge-storage
  - model-architecture-comparison
  - training-exposures
  - quantization-effects
  - synthetic-datasets
  - mixture-of-experts
---
# Physics of Language Models: Part 3.3, Knowledge Capacity Scaling Laws

**Allen-Zhu, Zeyuan et al.** • 2024

> [!quote] Memorable Quote
> "Language models can autonomously identify and prioritize domains rich in knowledge, optimizing their storage capacity."

## Quick Refresh

This paper measures how much factual knowledge language models can store by training GPT-2, LLaMA, and Mistral on synthetic datasets of (name, attribute, value) tuples—like (USA, capital, Washington D.C.)—and tracking what gets learned. The key finding is that models consistently achieve a 2 bits-per-parameter storage capacity when trained sufficiently (1000 exposures to each fact), meaning a 7B model could store 14 billion bits of knowledge. The authors also show how training duration, architecture choices, quantization, and data quality affect this capacity through systematic controlled experiments.

## Why You Cared

Understanding scaling laws for knowledge storage directly addresses a fundamental question about LLM efficiency: how large does a model actually need to be to store human knowledge? This matters because it challenges assumptions about model size (e.g., does GPT-4 really need 1T parameters?), informs decisions about training data preparation, and provides a principled framework for comparing architectures that's cleaner than traditional benchmark comparisons. The synthetic evaluation setting avoids benchmark contamination issues and lets you isolate the effects of individual design choices—something real-world evaluation can't easily do.

## Key Concepts

`#knowledge-capacity` `#scaling-laws` `#language-model-efficiency` `#bit-complexity` `#factual-knowledge-storage` `#model-architecture-comparison` `#training-exposures` `#quantization-effects` `#synthetic-datasets` `#mixture-of-experts`

## Cites (Key Papers)

- [[N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=200000 N=100000 N=50000 N=20...]]
- [[25 bit / param N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=200000 N=1000...]]
- [[25 bit / param N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=200000 N=1000...]]
- [[25 bit / param N=1000000]]
- [[N=500000 N=200000 N=100000 N=50000 N=20000 N=10000 (c) Figure 1(a) quantized to ...]]
- [[25 bit / param N=20000000 N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=20...]]
- [[25 bit / param N=20000000 N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=20...]]
- [[k-D 10 -C 1-K5 -L1 -T4 0k N5 00 k-D 10 -C 1-K1 0-L1 -T4 0k N5 00 k-D 10 -C 1-K2 ...]]
- [[25 bit / param N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=200000 N=1000...]]
- [[25 bit / param N=1000000]]

*(42 more citations below)*

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

1. N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=200000 N=100000 N=50000 N=20000 N=10000 10 -6 16 -8 6-20 20 -1 6 35 a) 1000 exposures -memorizable knowledge accuracy
2. 25 bit / param N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=200000 N=100000 N=50000 N=20000 N=10000 (a) Same Figure 1 model size (#params
3. 25 bit / param N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=200000 N=100000 N=50000 N=20000 N=10000
4. 25 bit / param N=1000000
5. N=500000 N=200000 N=100000 N=50000 N=20000 N=10000 (c) Figure 1(a) quantized to 4bit
6. 25 bit / param N=20000000 N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=200000 N=100000 N=50000 (d) Same Figure 1(b) model size (#params
7. 25 bit / param N=20000000 N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=200000 N=100000 N=50000
8. k-D 10 -C 1-K5 -L1 -T4 0k N5 00 k-D 10 -C 1-K1 0-L1 -T4 0k N5 00 k-D 10 -C 1-K2 0-L1 -T4 0k N2 00 k-D 10 -C 1-K 5 0-L1 -T4 0k N1 00 0k -D 10 -C 1-K1 -L4 -T4 0k N1 00 0k -D 10 -C 1-K2 -L4 -T4 0k N5 00 k-D 10 -C 1-K5 -L4 -T4 0k N5 00 k-D 10 -C 1-K1 0-L4 -T4 0k N5 00 k-D 10 -C 1-K2 0-L4 -T4 0k N2 00 k-D 10 -C 1-K5 0-L4 -T4 0k N1 00 0k -D 10 00 0-C1 -K 1-L4 -T4 0k N1 00 0k -D 10 00 0-C1 -K 2-L4 -T4 0k N5 00 k-D 10 00 0-C1 -K 5-L4 -T4 0k N5 00 k-D 10 00 0-C1 -K 10 -L4 -T4 0k N2 00 k-D 10 00 0-C1 -K 20 -L4 -T4 0k N1 00 k-D 10 00 0-C1 -K 50 -L4 -T4 0k
9. 25 bit / param N=10000000 N=5000000 N=2000000 N=1000000 N=500000 N=200000 N=100000 N=50000 N=20000 N=10000 1000
10. 25 bit / param N=1000000
11. N=500000 N=200000 N=100000 N=50000
12. 25 bit / param N=1000000
13. N=500000 N=200000 N=100000 N=50000
14. Q N +j D+D = [T L ] Let Q N +j D+1 T L -1], . . . , [T L -D + 1] for every j = 0, . . . , K -1
15. Q N +kd+1 = • • • = Q NLet +kd+n K = [d C ]
16. Recall that each Q i is independently and uniformly generated at random from Q i . We now present an alternative method for generating the training dataset
17. N ) as follows: Let n 1 be the Q 1 -th name from N 0 ; for i > 1, let n i be the Q i -th name from N 0 \ {n 1 NConstruct
18. let a be the a ′ -th attribute in A. Construct D a = (w 1 , . . . , w D ) as follows: Let w 1 be the Q N +(a ′ -1)D+1 -th element in T L ; for i > 1, let w i be the Q N +(a ′ -1)D+i -th element in T L \ {w 1
19. Ibrahim M Alabdulmohsin B., Neyshabur X. & Zhai (2022). Revisiting neural scaling laws in language and vision.
20. Allen Z. & Li Y. (2023). Physics of Language Models: Part 1, Context-Free Grammar.
21. Allen Z. & Li Y. (2023). Physics of Language Models: Part 3.1, Knowledge Storage and Extraction.
22. Allen Z. & Li Y. (2023). Physics of Language Models: Part 3.2, Knowledge Manipulation.
23. Allen-Zhu Z., Li Y. & Liang Y. (2019). Learning and generalization in overparameterized neural networks, going beyond two layers.
24. Allen-Zhu Z., Li Y. & Song Z. (2019). A convergence theory for deep learning via overparameterization.
25. Black S., Biderman S., Hallahan E. et al. (2022). GPT-NeoX-20B: An open-source autoregressive language model.
26. Bubeck S., Chandrasekaran V., Eldan R. et al. (2023). Sparks of artificial general intelligence: Early experiments with gpt-4.
27. Fedus W., Zoph B. & Shazeer N. (2022). Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity.
28. Frantar E., Saleh Ashkboos T., Hoefler D. et al. (2022). GPTQ: Accurate post-training compression for generative pretrained transformers.
29. Golovneva O., Allen-Zhu Z., Weston J. et al. (2024). Reverse training to nurse the reversal curse.
30. Gunasekar S., Zhang Y., Aneja J. et al. (2023). Textbooks are all you need.
31. Henighan T., Kaplan J., Katz M. et al. (2020). Scaling laws for autoregressive generative modeling.
32. Hernandez D., Kaplan J., Henighan T. et al. (2021). Scaling laws for transfer.
33. Hestness J., Narang S., Ardalani N. et al. (2017). Deep learning scaling is predictable, empirically.
34. Hoffmann J., Borgeaud S., Mensch A. et al. (2022). Training computeoptimal large language models.
35. Edward J., Hu P., Wallis Z. et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models.
36. Hwang C., Cui W., Xiong Y. et al. (2022). Tutel: Adaptive mixture-of-experts at scale.
37. Albert Q Jiang A., Sablayrolles A., Mensch C. et al. (2023). Mistral 7b.
38. Joshi M., Choi E., Weld D. S. et al. (2017). Triviaqa: A large scale distantly supervised challenge dataset for reading comprehension.
39. Kaplan J., Mccandlish S., Henighan T. et al. (2020). Scaling laws for neural language models.
40. Kwiatkowski T., Palomaki J., Redfield O. et al. (2019). Natural questions: a benchmark for question answering research.
41. Li Y. & Liang Y. (2018). Learning overparameterized neural networks via stochastic gradient descent on structured data.
42. Li Y., Bubeck S., Eldan R. et al. (2023). Textbooks are all you need ii: phi-1.5 technical report.
43. Muennighoff N., Rush A. M., Barak B. et al. (2023). Aleksandra Piktus, Nouamane Tazi, Sampo Pyysalo, Thomas Wolf, and Colin Raffel. Scaling data-constrained language models.
44. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
45. Rosenfeld J. S. (2021). Scaling laws for deep learning.
46. Rosenfeld J. S., Rosenfeld A., Belinkov Y. et al. (2019). A constructive prediction of the generalization error across scales.
47. Shazeer N. (2020). Glu variants improve transformer.
48. Shazeer N., Mirhoseini A., Maziarz K. et al. (2016). Outrageously large neural networks: The sparsely-gated mixture-of-experts layer.
49. Su J., Lu Y., Pan S. et al. (2021). Roformer: Enhanced transformer with rotary position embedding.
50. Touvron H., Lavril T., Izacard G. et al. (2023). Open and efficient foundation language models.
51. Touvron H., Martin L., Stone K. et al. (2023). Llama 2: Open foundation and fine-tuned chat models.
52. Yu D., Kaur S., Gupta A. et al. (2023). Skillmix: A flexible and expandable family of evaluations for ai models.
