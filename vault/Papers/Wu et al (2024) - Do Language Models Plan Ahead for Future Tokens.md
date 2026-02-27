---
title: "Do Language Models Plan Ahead for Future Tokens?"
authors: ["Wu, Wilson", "Morris, John X", "Levine, Lionel", "Barthel, Maik", "Sauppe, Sebastian", "Stephen C Levinson, Antje S", "Meyer", "Bau, David", "Zhu, Jun-Yan", "Strobelt, Hendrik", "Lapedriza, Agata", "Zhou, Bolei", "Torralba, Antonio", "Beck, Amir", "Biderman, Stella", "Schoelkopf, Hailey", "Anthony, Quentin", "Bradley, Herbie", "Kyle, O'", "Brien, Eric", "Hallahan, Mohammad", "Aflah Khan, Shivanshu", "Purohit", "Usvsn Sai Prashanth, Edward", "Raff, Aviya", "Skowron, Lintang", "Sutawika, Oskar", "Van, Der", "Wal", "Bisk, Yonatan", "Zellers, Rowan", "Le Bras, Ronan", "Gao, Jianfeng", "Choi, Yejin", "Huettig, Falk", "Nguyen, Tri", "Rosenberg, Mir", "Song, Xia", "Gao, Jianfeng", "Tiwary, Saurabh", "Majumder, Rangan", "Deng, Li", "Olah, Chris", "Cammarata, Nick", "Schubert, Ludwig", "Goh, Gabriel", "Petrov, Michael", "Carter, Shan", "Pal, Koyena", "Sun, Jiuding", "Yuan, Andrew", "Wallace, Byron", "Bau, David", "Paperno, Denis", "Kruszewski, Germán", "Lazaridou, Angeliki", "Pham, Ngoc Quan", "Bernardi, Raffaella", "Pezzelle, Sandro", "Baroni, Marco", "Boleda, Gemma", "Fernández, Raquel", "Shen, Zuowei", "Yang, Haizhao", "Zhang, Shijun", "Stern, Mitchell", "Shazeer, Noam M", "Uszkoreit, Jakob", "Vaswani, Ashish", "Shazeer, Noam", "Parmar, Niki", "Uszkoreit, Jakob", "Jones, Llion", "Gomez, Aidan N", "Kaiser, Ł Ukasz", "Polosukhin, Illia"]
year: 2024
venue: "Frontiers in psychology"
doi: "10.3389/fpsyg.2016.01858"
arxiv: "2404.00859"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - pre-caching
  - breadcrumbs-hypothesis
  - myopic-training
  - off-diagonal-gradients
  - transformer-inference
  - future-token-prediction
  - gradient-descent-theory
  - mechanistic-interpretability
  - model-scaling
  - language-modeling
---

# Do Language Models Plan Ahead for Future Tokens?

**Wu, Wilson et al.** • 2024

> [!quote] Memorable Quote
> "Breadcrumbs: The features that most benefit the present inference task are the same as those that are most useful to the future."

## Quick Refresh

This paper investigates whether transformers deliberately prepare information for future tokens during inference, or whether future-token predictivity is an incidental byproduct of optimizing for the current step. The authors introduce "myopic training"—a scheme that blocks gradients from flowing backward to past timesteps—to disentangle two competing hypotheses: pre-caching (deliberate future computation) versus breadcrumbs (current features naturally aligning with future needs). In a synthetic task where pre-caching is necessary, transformers clearly learn to pre-cache; in natural language modeling with GPT-2, the myopia gap is small (0.12 cross-entropy), suggesting breadcrumbs dominate, though larger models show increasing pre-caching behavior.

## Why You Cared

You care about understanding what transformers actually compute at each forward pass and whether their internal representations genuinely reflect planning or are simpler artifacts of greedy optimization. This paper directly addresses that by creating a clever experimental setup that can isolate pre-caching from simpler explanations. The findings matter for model interpretability, for thinking about efficiency gains from optimizing training objectives differently, and for understanding how planning-like behavior emerges with scale.

## Key Concepts

`#pre-caching` `#breadcrumbs-hypothesis` `#myopic-training` `#off-diagonal-gradients` `#transformer-inference` `#future-token-prediction` `#gradient-descent-theory` `#mechanistic-interpretability` `#model-scaling` `#language-modeling`

## Cites (Key Papers)

- [[Barthel M., Sauppe S., Stephen C Levinson A. & Meyer (2016) - The timing of utterance planning in task-oriented dialogue: ...]]
- [[Bau D., Zhu J., Strobelt H., Lapedriza A., Zhou B. & Torralba A. (2020) - Understanding the role of individual units in a deep neural ...]]
- [[Beck A. (2017) - First-Order Methods in Optimization]]
- [[Belinkov Y. (2019) - Probing classifiers: Promises, shortcomings, and advances, 2...]]
- [[Belrose N., Furman Z., Smith L., Halawi D., Ostrovsky I., Mckinney L., Biderman S. & Steinhardt J. (2023) - Eliciting latent predictions from transformers with the tune...]]
- [[Biderman S., Schoelkopf H., Anthony Q., Bradley H., Kyle O., Brien E., Hallahan M., Aflah Khan S., Purohit, Usvsn Sai Prashanth E., Raff A., Skowron L., Sutawika O., Van D. & Wal (2023) - Pythia: a suite for analyzing large language models across t...]]
- [[Bisk Y., Zellers R., Le Bras R., Gao J. & Choi Y. (2020) - Piqa: Reasoning about physical commonsense in natural langua...]]
- [[Cai T., Li Y., Geng Z., Peng H., Lee J. D., Chen D., Dao T. & Medusa (2024) - Simple llm inference acceleration framework with multiple de...]]
- [[Gao L., Biderman S., Black S., Golding L., Hoppe T., Foster C., Phang J., He H., Thite A., Nabeshima N., Presser S. & Leahy C. (2020) - The Pile: An 800gb dataset of diverse text for language mode...]]
- [[Hernandez E., Arnab S., Sharma T., Haklay K., Meng M., Wattenberg J., Andreas Y., Belinkov D. & Bau (2024) - Linearity of relation decoding in transformer language model...]]

*(24 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Frontiers in psychology
**DOI:** [10.3389/fpsyg.2016.01858](https://doi.org/10.3389/fpsyg.2016.01858)
**arXiv:** [2404.00859](https://arxiv.org/abs/2404.00859)
**PDF:** [[arxiv_2404.00859.pdf]]

## Abstract

Do transformers "think ahead" during inference at a given position? It is known transformers prepare information in the hidden states of the forward pass at time step t that is then used in future forward passes t + τ. We posit two explanations for this phenomenon: pre-caching, in which off-diagonal gradient terms present during training result in the model computing features at t irrelevant to the present inference task but useful for the future, and breadcrumbs, in which features most relevant to time step t are already the same as those that would most benefit inference at time t + τ. We test these hypotheses by training language models without propagating gradients to past timesteps, a scheme we formalize as myopic training. In a constructed synthetic data setting, we find clear evidence for pre-caching. In the autoregressive language modeling setting, our experiments are more suggestive of the breadcrumbs hypothesis, though pre-caching increases with model scale.

## Full Citation List

1. Barthel M., Sauppe S., Stephen C Levinson A. et al. (2016). The timing of utterance planning in task-oriented dialogue: Evidence from a novel list-completion paradigm. Frontiers in psychology, Vol. 7, pp. 1858. DOI: 10.3389/fpsyg.2016.01858
2. Bau D., Zhu J., Strobelt H. et al. (2020). Understanding the role of individual units in a deep neural network. Proceedings of the National Academy of Sciences, Vol. 117(48), pp. 30071-30078. DOI: 10.1073/pnas.1907375117
3. Beck A. (2017). First-Order Methods in Optimization. Society for Industrial and Applied Mathematics. DOI: 10.1137/1.9781611974997
4. Belinkov Y. (2019). Probing classifiers: Promises, shortcomings, and advances, 2021. Yonatan Belinkov and James Glass. Analysis methods in neural language processing: A survey.
5. Belrose N., Furman Z., Smith L. et al. (2023). Eliciting latent predictions from transformers with the tuned lens.
6. Biderman S., Schoelkopf H., Anthony Q. et al. (2023). Pythia: a suite for analyzing large language models across training and scaling.
7. Bisk Y., Zellers R., Le Bras R. et al. (2020). Piqa: Reasoning about physical commonsense in natural language. DOI: 10.1609/aaai.v34i05.6239
8. Cai T., Li Y., Geng Z. et al. (2024). Simple llm inference acceleration framework with multiple decoding heads.
9. Gao L., Biderman S., Black S. et al. (2020). The Pile: An 800gb dataset of diverse text for language modeling.
10. Hernandez E., Arnab S., Sharma T. et al. (2024). Linearity of relation decoding in transformer language models.
11. Hewitt J. & Liang P. (2019). Designing and interpreting probes with control tasks.
12. Huettig F. (2015). Four central questions about prediction in language processing. DOI: 10.1016/j.brainres.2015.02.014
13. Li K., Hopkins A. K., Bau D. et al. (2023). Emergent world representations: Exploring a sequence model trained on a synthetic task.
14. Meng K., Bau D., Andonian A. et al. (2023). Locating and editing factual associations in gpt.
15. Language and communication George AMiller 10.1037/11135-000 Mc Graw-Hill 1951 New York, NY, US
16. Nanda N., Chan L., Lieberum T. et al. (2023). Progress measures for grokking via mechanistic interpretability.
17. Nesterov Y. (2018). Lectures on Convex Optimization.
18. Nguyen T., Rosenberg M., Song X. et al. (2016). MS MARCO: A human generated machine reading comprehension dataset.
19. Olah C., Cammarata N., Schubert L. et al. (2020). Zoom in: An introduction to circuits. Distill. DOI: 10.23915/distill.00024.001
20. Pal K., Sun J., Yuan A. et al. (2023). Future lens: Anticipating subsequent tokens from a single hidden state. DOI: 10.18653/v1/2023.conll-1.37
21. Paperno D., Kruszewski G., Lazaridou A. et al. (2016). The LAMBADA dataset: Word prediction requiring a broad discourse context. DOI: 10.18653/v1/P16-1144
22. Pfau J., Merrill W. & Bowman S. R. (2024). Let's think dot by dot: Hidden computation in transformer language models.
23. Pimentel T., Valvoda J., Hall Maudslay R. et al. (2020). Information-theoretic probing for linguistic structure.
24. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
25. Jack W Rae A., Potapenko, Siddhant M. et al. (2019). Compressive transformers for long-range sequence modelling.
26. Shen R., Bubeck S., Eldan R. et al. (2023). Positional description matters for transformers arithmetic.
27. Shen Z., Yang H. & Zhang S. (2022). Optimal approximation rate of relu networks in terms of width and depth. Journal de Mathématiques Pures et Appliquées, Vol. 157, pp. 101-135. DOI: 10.1016/j.matpur.2021.07.009
28. Does string-based neural mt learn source syntax? Xing Shi Inkit Padhi Kevin Knight 10.18653/v1/D16-1159 01 2016
29. Stern M., Shazeer N. M. & Uszkoreit J. (2018). Blockwise parallel decoding for deep autoregressive models.
30. Vaswani A., Shazeer N., Parmar N. et al. (2017). Attention is all you need.
31. Welbl J., Liu N. F. & Gardner M. (2017). Crowdsourcing multiple choice science questions.
32. Xu Y., Zhao S., Song J. et al. (2020). A theory of usable information under computational constraints.
33. Zhang Y., Dai H., Toraman K. et al. (2018). kg 2 : Learning to reason science exam questions with contextual knowledge graph embeddings.
34. Zhong Z., Liu Z., Tegmark M. et al. (2023). The clock and the pizza: Two stories in mechanistic explanation of neural networks.
