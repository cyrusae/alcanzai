---
title: "Back Attention: Understanding and Enhancing Multi-Hop Reasoning in Large Language Models"
authors: ["Yu, Zeping", "Belinkov, Yonatan", "Ananiadou, Sophia", "Elhage, Nelson", "Nanda, Neel", "Olsson, Catherine", "Henighan, Tom", "Joseph, Nicholas", "Mann, Ben", "Askell, Amanda", "Bai, Yuntao", "Chen, Anna", "Conerly, Tom", "Fu, Yao", "Peng, Hao", "Sabharwal, Ashish", "Clark, Peter", "Khot, Tushar", "Geva, Mor", "Bastings, Jasmijn", "Filippova, Katja", "Globerson, Amir", "Geva, Mor", "Khashabi, Daniel", "Segal, Elad", "Khot, Tushar", "Roth, Dan", "Berant, Jonathan", "Gu, Jia-Chen", "Xu, Hao-Xiang", "Ma, Jun-Yu", "Lu, Pan", "Ling, Zhen-Hua", "Chang, Kai-Wei", "Peng, Nanyun", "Hanna, Michael", "Liu, Ollie", "Variengien, Alexandre", "Meng, Kevin", "Bau, David", "Andonian, Alex", "Belinkov, Yonatan", "Ai Meta", "Ai Meta", "Olah, Chris", "Sakarvadia, Mansi", "Ajith, Aswathy", "Khan, Arham", "Grzenda, Daniel", "Hudson, Nathaniel", "Bauer, André", "Chard, Kyle", "Foster, Ian", "Vig, Jesse", "Gehrmann, Sebastian", "Belinkov, Yonatan", "Qian, Sharon", "Nevo, Daniel", "Singer, Yaron", "Shieber, Stuart", "Wei, Jason", "Wang, Xuezhi", "Schuurmans, Dale", "Bosma, Maarten", "Xia, Fei", "Chi, Ed", "Quoc, V", "Le, Denny", "Zhou", "Yao, Shunyu", "Yu, Dian", "Zhao, Jeffrey", "Shafran, Izhak", "Griffiths, Tom", "Cao, Yuan", "Narasimhan, Karthik", "Yu, Zeping", "Ananiadou, Sophia", "Yu, Zeping", "Ananiadou, Sophia"]
year: 2025
venue: "Transformer Circuits Thread"
arxiv: "2502.10835"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - logit-flow
  - back-attention
  - multi-hop-reasoning
  - transformer-interpretability
  - attention-mechanisms
  - relation-extraction
  - entity-retrieval
  - latent-reasoning
  - knowledge-attribution
  - large-language-models
---

# Back Attention: Understanding and Enhancing Multi-Hop Reasoning in Large Language Models

**Yu, Zeping et al.** • 2025

> [!quote] Memorable Quote
> "In two-hop false cases, when the features at r1 positions, which are related to e2, are extracted at layer 28, they only activate the 'e2 features & r2 → e3' parameters in layers 28–31. Although this process does enhance the probability of e3, it amplifies the probability of e2 even more."

## Quick Refresh

This paper investigates how large language models perform latent multi-hop reasoning—internally retrieving and integrating knowledge across multiple steps without generating intermediate reasoning. The authors introduce logit flow, an interpretability method that traces how logit values propagate across layers toward final predictions, identifying four distinct stages in single-hop knowledge prediction: entity subject enrichment, entity attribute extraction, relation subject enrichment, and relation attribute extraction. For two-hop reasoning, they find failures often stem from the relation attribute extraction stage, where competing logits for intermediate entities outweigh the correct final answer. They propose back attention, a mechanism enabling lower transformer layers to access higher-layer hidden states, which improves accuracy across four LLMs and five reasoning datasets while adding only 0.002% parameters.

## Why You Cared

You were interested in understanding how transformer models perform multi-step reasoning internally, and this paper directly connects interpretability findings to practical improvements. The logit flow method provides neuron-level information flow analysis—more granular than layer-level approaches—that helps you diagnose failure modes in your own reasoning tasks. Back attention can be added to existing models during fine-tuning without retraining, making it immediately applicable to your work. The paper's identification of a specific bottleneck (conflicting logits at relation attribute extraction) explains why two-hop accuracy remains low even when individual steps work, giving you a diagnostic framework for similar failures in other multi-step reasoning scenarios.

## Key Concepts

`#logit-flow` `#back-attention` `#multi-hop-reasoning` `#transformer-interpretability` `#attention-mechanisms` `#relation-extraction` `#entity-retrieval` `#latent-reasoning` `#knowledge-attribution` `#large-language-models`

## Cites (Key Papers)

- [[Biran E., Gottesman D., Yang S., Geva M. & Globerson A. (2024) - Hopping too late: Exploring the limitations of large languag...]]
- [[Bricken T., Templeton A., Batson J., Chen B., Jermyn A., Conerly T., Turner N., Anil C., Denison C. & Askell A. (2023) - Towards monosemanticity: Decomposing language models with di...]]
- [[Brown B., Juravsky J., Ehrlich R., Clark R., Quoc V., Le C., Ré A. & Mirhoseini (2024) - Large language monkeys: Scaling inference compute with repea...]]
- [[Tom B Brown (2020) - Language models are few-shot learners]]
- [[Chen Z., Deng Y., Yuan H., Ji K. & Gu Q. (2024) - Self-play fine-tuning converts weak language models to stron...]]
- [[Creswell A., Shanahan M. & Higgins I. (2022) - Selection-inference: Exploiting large language models for in...]]
- [[Cunningham H., Ewart A., Riggs L., Huben R. & Sharkey L. (2023) - Sparse autoencoders find highly interpretable features in la...]]
- [[Dar G., Geva M., Gupta A. & Berant J. (2022) - Analyzing transformers in embedding space]]
- [[Dubey A., Jauhri A., Pandey A., Kadian A., Al-Dahle A., Letman A., Mathur A., Schelten A., Yang A. & Fan A. (2024) - The llama 3 herd of models]]
- [[Elhage N., Hume T., Olsson C., Schiefer N., Henighan T., Kravec S., Hatfield-Dodds Z., Lasenby R., Drain D. & Chen C. (2022) - Toy models of superposition]]

*(52 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Transformer Circuits Thread
**arXiv:** [2502.10835](https://arxiv.org/abs/2502.10835)
**PDF:** [[arxiv_2502.10835.pdf]]

## Abstract

We investigate how large language models perform latent multi-hop reasoning in prompts like "Wolfgang Amadeus Mozart's mother's spouse is". To analyze this process, we introduce logit flow, an interpretability method that traces how logits propagate across layers and positions toward the final prediction. Using logit flow, we identify four distinct stages in single-hop knowledge prediction: (A) entity subject enrichment, (B) entity attribute extraction, (C) relation subject enrichment, and (D) relation attribute extraction. Extending this analysis to multi-hop reasoning, we find that failures often stem from the relation attribute extraction stage, where conflicting logits reduce prediction accuracy. To address this, we propose back attention, a novel mechanism that enables lower layers to leverage higher-layer hidden states from different positions during attention computation. With back attention, a 1-layer transformer achieves the performance of a 2layer transformer. Applied to four LLMs, back attention improves accuracy on five reasoning datasets, demonstrating its effectiveness in enhancing latent multi-hop reasoning ability.

## Full Citation List

1. Biran E., Gottesman D., Yang S. et al. (2024). Hopping too late: Exploring the limitations of large language models on multi-hop queries.
2. Bricken T., Templeton A., Batson J. et al. (2023). Towards monosemanticity: Decomposing language models with dictionary learning.
3. Brown B., Juravsky J., Ehrlich R. et al. (2024). Large language monkeys: Scaling inference compute with repeated sampling.
4. Tom B Brown (2020). Language models are few-shot learners.
5. Chen Z., Deng Y., Yuan H. et al. (2024). Self-play fine-tuning converts weak language models to strong language models.
6. Creswell A., Shanahan M. & Higgins I. (2022). Selection-inference: Exploiting large language models for interpretable logical reasoning.
7. Cunningham H., Ewart A., Riggs L. et al. (2023). Sparse autoencoders find highly interpretable features in language models.
8. Dar G., Geva M., Gupta A. et al. (2022). Analyzing transformers in embedding space.
9. Dubey A., Jauhri A., Pandey A. et al. (2024). The llama 3 herd of models.
10. Elhage N., Hume T., Olsson C. et al. (2022). Toy models of superposition.
11. Elhage N., Nanda N., Olsson C. et al. (2021). A mathematical framework for transformer circuits. Transformer Circuits Thread, Vol. 1(1), pp. 12.
12. Jaden Fiotto-Kaufman Alexander RLoftus Eric Todd Jannik Brinkmann Caden Juang Koyena Pal Can Rager Aaron Mueller Samuel Marks arXiv:2407.14561 Arnab Sen Sharma, et al. 2024. Nnsight and ndif: Democratizing access to foundation model internals arXiv preprint
13. Fu Y., Peng H., Sabharwal A. et al. (2022). Complexity-based prompting for multi-step reasoning.
14. Gao L., Dupré La Tour T., Tillman H. et al. (2024). Scaling and evaluating sparse autoencoders.
15. Geva M., Bastings J., Filippova K. et al. (2023). Dissecting recall of factual associations in auto-regressive language models.
16. Geva M., Caciularu A., Wang K. R. et al. (2022). Transformer feed-forward layers build predictions by promoting concepts in the vocabulary space.
17. Geva M., Khashabi D., Segal E. et al. (2021). Did aristotle use a laptop? a question answering benchmark with implicit reasoning strategies. Transactions of the Association for Computational Linguistics, Vol. 9, pp. 346-361.
18. Geva M., Schuster R., Berant J. et al. (2020). Transformer feed-forward layers are keyvalue memories.
19. Gould R., Ong E., Ogden G. et al. (2023). Successor heads: Recurring, interpretable attention heads in the wild.
20. Gu J., Xu H., Ma J. et al. (2024). Model editing harms general abilities of large language models: Regularization to the rescue.
21. Gupta A., Rao A. & Anumanchipalli G. (2024). Model editing at scale leads to gradual and catastrophic forgetting.
22. Hanna M., Liu O. & Variengien A. (2024). How does gpt-2 compute greater-than?: Interpreting mathematical abilities in a pre-trained language model.
23. Hao S., Gu Y., Ma H. et al. (2023). Reasoning with language model is planning with world arXiv preprint.
24. Huang J., Chen X., Mishra S. et al. (2023). Large language models cannot self-correct reasoning yet.
25. Albert Q Jiang A., Sablayrolles A., Mensch C. et al. (2023). Mistral 7b.
26. Ju T., Chen Y., Yuan X. et al. (2024). vestigating multi-hop factual shortcuts in knowledge editing of large language models.
27. Katz S. & Belinkov Y. (2023). Visit: Visualizing and interpreting the semantic information flow of transformers.
28. 2024a. Understanding and patching compositional reasoning in llms Zhaoyi Li Gangwei Jiang Hong Xie Linqi Song Defu Lian Ying Wei arXiv:2402.14328 arXiv preprint
29. 2024b. Chain of thought empowers transformers to solve inherently serial problems Zhiyuan Li Hong Liu Denny Zhou Tengyu Ma arXiv:2402.12875 arXiv preprint
30. Vineet Hunter Lightman Yura Kosaraju Harri Burda Bowen Edwards Teddy Baker Jan Lee John Leike Schulman arXiv:2305.20050 Ilya Sutskever, and Karl Cobbe. 2023. Let's verify step by step arXiv preprint
31. Loshchilov (2017). Decoupled weight decay regularization.
32. Luo L., Liu Y., Liu R. et al. (2024). Improve mathematical reasoning in language models by automated process supervision.
33. Meng K., Bau D., Andonian A. et al. (2022). Locating and editing factual associations in gpt.
34. Ai Meta (2024). Introducing meta llama 3: The most capable openly available llm to date. Meta AI.
35. Ai Meta (2024). Llama 3.2: Revolutionizing edge ai and vision with open, customizable models.
36. Nostalgebraist (2020). Interpreting gpt: the logit lens.
37. Olah C. (2022). Mechanistic interpretability, variables, and the importance of interpretable bases.
38. Olsson C., Elhage N., Nanda N. et al. (2022). -context learning and induction heads.
39. Openai (2024). Learning to reason with llms.
40. Patel A., Bhattamishra S. & Goyal N. (2021). Are nlp models really able to solve simple math word problems? arXiv preprint.
41. Qi Z., Ma M., Xu J. et al. (2024). Mutual reasoning makes smaller llms stronger problem-solvers.
42. Roy S. & Roth D. (2016). Solving general arithmetic word problems.
43. Sakarvadia M., Ajith A., Khan A. et al. (2023). Memory injections: Correcting multi-hop reasoning failures during inference in transformer-based language models.
44. Scherlis A., Sachan K., Adam S Jermyn J. et al. (2022). Polysemanticity and capacity in neural networks.
45. Shum K., Diao S. & Zhang T. (2023). Automatic prompt augmentation and selection with chain-of-thought from labeled data.
46. Snell C., Lee J., Xu K. et al. (2024). Scaling llm test-time compute optimally can be more effective than scaling model parameters.
47. Stolfo A., Belinkov Y. & Sachan M. (2023). A mechanistic interpretation of arithmetic reasoning in language models using causal mediation analysis.
48. Templeton A. (2024). Scaling monosemanticity: Extracting interpretable features from claude 3 sonnet.
49. Hugo Touvron Thibaut Lavril Gautier Izacard Xavier Martinet Marie-Anne Lachaux Timothée Lacroix Baptiste Rozière Naman Goyal Eric Hambro arXiv:2302.13971 Faisal Azhar, et al. 2023a. Llama: Open and efficient foundation language models arXiv preprint
50. Hugo Touvron Louis Martin Kevin Stone Peter Albert Amjad Almahairi Yasmine Babaei Nikolay Bashlykov Soumya Batra Prajjwal Bhargava arXiv:2307.09288 Shruti Bhosale, et al. 2023b. Llama 2: Open foundation and fine-tuned chat models arXiv preprint
51. Vig J., Gehrmann S., Belinkov Y. et al. (2020). Investigating gender bias in language models using causal mediation analysis. Advances in neural information processing systems, Vol. 33, pp. 12388-12401.
52. Wang K., Variengien A., Conmy A. et al. (2022). terpretability in the wild: a circuit for indirect object identification in gpt-2 small.
53. Wang X., Wei J., Schuurmans D. et al. (2022). Self-consistency improves chain of thought reasoning in language models.
54. Wang X. & Zhou D. (2024). Chain-ofthought reasoning without prompting.
55. Wei J., Wang X., Schuurmans D. et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems, Vol. 35, pp. 24824-24837.
56. Wu Z., Geiger A., Arora A. et al. (2024). A library for understanding and improving pytorch models via interventions.
57. Yang S., Gribovskaya E., Kassner N. et al. (2024). Do large language models latently perform multi-hop reasoning? arXiv preprint.
58. Yao S., Yu D., Zhao J. et al. (2024). Tree of thoughts: Deliberate problem solving with large language models. Advances in Neural Information Processing Systems, pp. 36.
59. 2024a. Interpreting arithmetic mechanism in large language models through comparative neuron analysis Zeping Yu Sophia Ananiadou Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing the 2024 Conference on Empirical Methods in Natural Language Processing
60. 2024b. Neuronlevel knowledge attribution in large language models Zeping Yu Sophia Ananiadou Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing the 2024 Conference on Empirical Methods in Natural Language Processing
61. Zhang F. & Nanda N. (2023). Towards best practices of activation patching in language models: Metrics and methods.
62. Zhou D., Schärli N., Hou L. et al. (2022). Least-to-most prompting enables complex reasoning in large language models.
