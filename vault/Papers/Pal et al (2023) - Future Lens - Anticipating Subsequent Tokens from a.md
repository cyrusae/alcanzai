---
title: "Future Lens: Anticipating Subsequent Tokens from a Single Hidden State"
authors: ["Pal, Koyena", "Sun, Jiuding", "Yuan, Andrew", "Wallace, Byron C", "Bau, David", "Carlini, Nicholas", "Ippolito, Daphne", "Jagielski, Matthew", "Lee, Katherine", "Tramer, Florian", "Zhang, Chiyuan", "Carlini, Nicholas", "Liu, Chang", "Erlingsson, Úlfar", "Kos, Jernej", "Song, Dawn", "Carlini, Nicholas", "Tramer, Florian", "Wallace, Eric", "Jagielski, Matthew", "Herbert-Voss, Ariel", "Lee, Katherine", "Roberts, Adam", "Brown, Tom", "Song, Dawn", "Elman, Jeffrey L", "Feldman, Vitaly", "Zhang, Chiyuan", "Gao, Leo", "Biderman, Stella", "Black, Sid", "Golding, Laurence", "Hoppe, Travis", "Foster, Charles", "Phang, Jason", "He, Horace", "Thite, Anish", "Nabeshima, Noa", "Presser, Shawn", "Leahy, Connor", "Geva, Mor", "Schuster, Roei", "Berant, Jonathan", "Levy, Omer", "Haviv, Adi", "Cohen, Ido", "Gidron, Jacob", "Schuster, Roei", "Goldberg, Yoav", "Geva, Mor", "Michael, Jordan", "Kong, Jun", "Wang, Jin", "Yu, Liang-Chih", "Zhang, Xuejie", "Meng, Kevin", "Bau, David", "Schuster, Tal", "Fisch, Adam", "Gupta, Jai", "Dehghani, Mostafa", "Bahri, Dara", "Vinh, Q", "Tran, Yi", "Tay, Donald", "Metzler", "Su, Yixuan", "Cai, Deng", "Wang, Yan", "Vandyke, David", "Baker, Simon", "Li, Piji", "Collier, Nigel", "Vaswani, Ashish", "Shazeer, Noam", "Parmar, Niki", "Uszkoreit, Jakob", "Jones, Llion", "Gomez, Aidan N", "Kaiser, Łukasz", "Polosukhin, Illia", "Wei, Jason", "Tay, Yi", "Bommasani, Rishi", "Raffel, Colin", "Zoph, Barret", "Borgeaud, Sebastian", "Yogatama, Dani", "Bosma, Maarten", "Zhou, Denny", "Metzler, Donald", "Chi, Ed H", "Hashimoto, Tatsunori", "Vinyals, Oriol", "Liang, Percy", "Dean, Jeff", "Fedus, William", "Xin, Ji", "Tang, Raphael", "Yu, Yaoliang", "Lin, Jimmy"]
year: 2023
venue: "Cognitive Science"
doi: "10.1016/0364-0213(90)90002-E"
arxiv: "2311.04897"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - causal-intervention
  - hidden-state-analysis
  - multi-token-prediction
  - learned-prompts
  - transformer-interpretability
  - soft-prompt-optimization
  - logit-lens
  - probing-methods
  - language-model-internals
  - machine-learning
---

# Future Lens: Anticipating Subsequent Tokens from a Single Hidden State

**Pal, Koyena et al.** • 2023

> [!quote] Memorable Quote
> "We hence optimize this objective with the model frozen and only prefix left to be trained."

## Quick Refresh

This paper investigates whether individual hidden states in language models encode information about multiple future tokens, not just the immediate next token. The researchers tested this on GPT-J-6B using three methods: direct vocabulary prediction via linear models, causal interventions that transplant hidden states into new contexts, and learned soft prompts optimized to extract future token information. The learned prompt method achieved 48.4% accuracy in predicting tokens one step ahead and remained surprisingly accurate for tokens up to three steps ahead, peaking at middle layers rather than the final layer where next-token predictions peak.

## Why You Cared

You were interested in understanding what information is implicitly encoded at different layers of transformer models and whether we could decode that information in novel ways. This paper shows that future token predictions are not evenly distributed through the network—they concentrate at middle layers and can be extracted through learned prompts, suggesting that the "encoding" of upcoming text happens earlier than current theory predicts. The Future Lens visualization they present also provides a practical tool for inspecting what a model "knows" about future tokens at any given point, which could help with model interpretability and debugging.

## Key Concepts

`#causal-intervention` `#hidden-state-analysis` `#multi-token-prediction` `#learned-prompts` `#transformer-interpretability` `#soft-prompt-optimization` `#logit-lens` `#probing-methods` `#language-model-internals` `#machine-learning`

## Cites (Key Papers)

- [[Belrose N., Furman Z., Smith L., Halawi D., Ostrovsky I., Mckinney L., Biderman S. & Steinhardt J. (2023) - Eliciting latent predictions from transformers with the tune...]]
- [[Carlini N., Ippolito D., Jagielski M., Lee K., Tramer F. & Zhang C. (2023) - Quantifying memorization across neural language models]]
- [[Carlini N., Liu C., Erlingsson Ú., Kos J. & Song D. (2019) - The secret sharer: Evaluating and testing unintended memoriz...]]
- [[Ulfar Erlingsson, Alina Oprea, and Colin Raffel. 2021. Extracting training data ...]]
- [[Devlin J., Chang M., Lee K. & Toutanova K. (2018) - BERT: pre-training of deep bidirectional transformers for la...]]
- [[Yom Din A., Karidi T., Choshen L. & Geva M. (2023) - Jump to conclusions: Shortcutting transformers]]
- [[Elman J. L. (1990) - Finding structure in time]]
- [[Feldman V. & Zhang C. (2020) - What neural networks memorize and why: Discovering the long ...]]
- [[Gao L., Biderman S., Black S., Golding L., Hoppe T., Foster C., Phang J., He H., Thite A., Nabeshima N., Presser S. & Leahy C. (2020) - LM-debugger: An interactive tool for inspection and interven...]]
- [[Geva M., Schuster R., Berant J. & Levy O. (2021) - Transformer feed-forward layers are keyvalue memories]]

*(21 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Cognitive Science
**DOI:** [10.1016/0364-0213(90)90002-E](https://doi.org/10.1016/0364-0213(90)90002-E)
**arXiv:** [2311.04897](https://arxiv.org/abs/2311.04897)
**PDF:** [[arxiv_2311.04897.pdf]]

## Abstract

We conjecture that hidden state vectors corresponding to individual input tokens encode information sufficient to accurately predict several tokens ahead. More concretely, in this paper we ask: Given a hidden (internal) representation of a single token at position t in an input, can we reliably anticipate the tokens that will appear at positions ≥ t + 2? To test this, we measure linear approximation and causal intervention methods in GPT-J-6B to evaluate the degree to which individual hidden states in the network contain signal rich enough to predict future hidden states and, ultimately, token outputs. We find that, at some layers, we can approximate a model's output with more than 48% accuracy with respect to its prediction of subsequent tokens through a single hidden state. Finally we present a "Future Lens" visualization that uses these methods to create a new view of transformer states.

## Full Citation List

1. Belrose N., Furman Z., Smith L. et al. (2023). Eliciting latent predictions from transformers with the tuned lens.
2. Carlini N., Ippolito D., Jagielski M. et al. (2023). Quantifying memorization across neural language models.
3. Carlini N., Liu C., Erlingsson Ú. et al. (2019). The secret sharer: Evaluating and testing unintended memorization in neural networks.
4. Ulfar Erlingsson, Alina Oprea, and Colin Raffel. 2021. Extracting training data from large language models Nicholas Carlini Florian Tramer Eric Wallace Matthew Jagielski Ariel Herbert-Voss Katherine Lee Adam Roberts Tom Brown Dawn Song USENIX Security Symposium
5. Devlin J., Chang M., Lee K. et al. (2018). BERT: pre-training of deep bidirectional transformers for language understanding.
6. Yom Din A., Karidi T., Choshen L. et al. (2023). Jump to conclusions: Shortcutting transformers.
7. Elman J. L. (1990). Finding structure in time. Cognitive Science, Vol. 14(2), pp. 179-211. DOI: 10.1016/0364-0213(90)90002-E
8. Feldman V. & Zhang C. (2020). What neural networks memorize and why: Discovering the long tail via influence estimation.
9. Gao L., Biderman S., Black S. et al. (2020). LM-debugger: An interactive tool for inspection and intervention in transformer-based language models.
10. Geva M., Schuster R., Berant J. et al. (2021). Transformer feed-forward layers are keyvalue memories. DOI: 10.18653/v1/2021.emnlp-main.446
11. Gurnee W., Nanda N., Pauly M. et al. (2023). Finding neurons in a haystack: Case studies with sparse probing.
12. Haviv A., Cohen I., Gidron J. et al. (2023). Understanding transformer memorization recall through idioms.
13. Hernandez E., Arnab S., Sharma T. et al. (2023). Linearity of relation decoding in transformer language models.
14. Ippolito D., Tramèr F., Nasr M. et al. (2023). Preventing verbatim memorization in language models gives a false sense of privacy.
15. Michael J. (1997). Serial order: A parallel distributed processing approach.
16. Katz S. & Belinkov Y. (2023). Interpreting transformer's attention dynamic memory and visualizing the semantic information flow of gpt.
17. Kong J., Wang J., Yu L. et al. (2022). Accelerating inference for pretrained language models by unified multi-perspective early exiting.
18. Lehman E., Jain S., Pichotta K. et al. (2021). Does bert pretrained on clinical notes reveal sensitive data? arXiv preprint.
19. Xiang L., Li P. & Liang (2021). Prefix-tuning: Optimizing continuous prompts for generation.
20. Alex Andonian, and Yonatan Belinkov. 2022a. Locating and editing factual associations in GPT Kevin Meng David Bau Advances in Neural Information Processing Systems 36
21. Meng K., Arnab S., Sharma A. et al. (2022). Mass editing memory in a transformer.
22. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
23. Schuster T., Fisch A., Gupta J. et al. (2022). Confident adaptive language modeling.
24. Su Y., Cai D., Wang Y. et al. (2021). Nonautoregressive text generation with pre-trained language models. DOI: 10.18653/v1/2021.eacl-main.18
25. Sun J., Shaib C. & Wallace B. C. (2023). Evaluating the zero-shot robustness of instruction-tuned language models.
26. Vaswani A., Shazeer N., Parmar N. et al. (2017). Attention is all you need.
27. Wallace E., Feng S., Kandpal N. et al. (2019). Universal adversarial triggers for attacking and analyzing nlp.
28. Wang B. & Komatsuzaki A. (2021). Gpt-j-6b: A 6 billion parameter autoregressive language model.
29. Wei J., Tay Y., Bommasani R. et al. (2022). Emergent abilities of large language models. Transactions on Machine Learning Research.
30. Xiao Y., Wu L., Guo J. et al. (2023). A survey on non-autoregressive generation for neural machine translation and beyond.
31. Xin J., Tang R., Yu Y. et al. (2021). BERxiT: Early exiting for BERT with better fine-tuning and extension to regression. DOI: 10.18653/v1/2021.eacl-main.8
