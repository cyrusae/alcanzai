---
title: "The Reversal Curse: Llms Trained On \"A Is B\" Fail To Learn \"B Is A\""
authors: ["Berglund, Lukas", "Tong, Meg", "Kaufmann, Max", "Balesni, Mikita", "Stickland, Asa Cooper", "Korbak, Tomasz", "Evans, Owain", "Barrington, Daphne", "Bireta, Tamra J", "Fry, Sheena E", "Jalbert, Annie", "Neath, Ian", "Aimée, M", "Surprenant, Gerald", "Tehan, G Anne", "Tolan", "Brown, Tom", "Mann, Benjamin", "Ryder, Nick", "Subbiah, Melanie", "Kaplan, Jared D", "Dhariwal, Prafulla", "Neelakantan, Arvind", "Shyam, Pranav", "Sastry, Girish", "Askell, Amanda", "St, Helen", "John, Richard", "Guitard, Dominic", "Saint-Aubin, Jean", "Poirier, Marie", "Miller, Leonie M", "Tolan, Anne", "Hase, Peter", "Diab, Mona", "Celikyilmaz, Asli", "Li, Xian", "Kozareva, Zornitsa", "Stoyanov, Veselin", "Bansal, Mohit", "Iyer, Srinivasan", "Chen, Shu", "Lewandowsky, Stephan", "Lin, Stephanie", "Hilton, Jacob", "Evans, Owain", "Speer, Robyn", "Chin, Joshua", "Havasi, Catherine", "Thomas, John G", "Milner, Haley R", "Haberlandt, Karl F", "Timo Van Kerkoerle, Louise", "Pape, Milad", "Ekramnia, Xiaoxia", "Feng, Jordy", "Tasserie, Morgan", "Dupont, Xiaolian", "Li, Bechir", "Jarraya, Wim", "Vanduffel, Stanislas", "Dehaene", "Yao, Yunzhi", "Huang, Shaohan", "Dong, Li", "Wei, Furu", "Chen, Huajun", "Zhang, Ningyu"]
year: 2024
venue: "Memory & Cognition"
doi: "10.1101/2023.03.04.531109"
arxiv: "2309.12288"
type: "paper"
status: "unread"
added: "2026-01-09"
tags:
  - knowledge-retrieval
  - order-effects
  - logical-deduction
  - model-generalization
  - fact-learning
  - finetuning
  - auto-regressive-language-models
  - knowledge-representation
  - transformer-models
  - natural-language-processing
  - machine-learning
---
# The Reversal Curse: Llms Trained On "A Is B" Fail To Learn "B Is A"

**Berglund, Lukas et al.** â€¢ 2024

> [!quote] Memorable Quote
> "Sentences of the form '<name> is <description>' and '<description> is <name>' often co-occur in pretraining datasets; if the former appears in a dataset, the latter is intuitively more likely to appear. Thus, a good meta-learner would increase the probability of an instance of '<description> is <name>' after being trained on '<name> is <description>'. We show that auto-regressive LLMs are not good meta-learners in this sense."

## Quick Refresh

This paper demonstrates that large language models (LLMs) like GPT-3 and Llama suffer from a surprising failure called the "Reversal Curse": if a model is trained on a statement like "A is B," it fails to generalize to the reversed statement "B is A." For example, a model trained on "Valentina Tereshkova was the first woman to travel to space" cannot answer "Who was the first woman to travel to space?" The researchers show this through three experiments—finetuning on synthetic facts, testing real-world celebrity knowledge, and reversing instructions—and find the effect holds across model sizes and families, even with data augmentation and other attempted fixes.

## Why You Cared

This paper matters because it exposes a basic failure in how LLMs generalize that contradicts what we might expect from intelligent systems. Since symmetry is a fundamental logical property (if A=B then B=A), this shows LLMs don't perform simple logical deduction from training data, even though they can do it when information appears in-context. For anyone building or deploying LLMs, this reveals a concrete brittleness in knowledge representation—models may appear to know facts but only in the specific order they saw them during training. It also raises questions about the reliability of LLMs as knowledge bases and suggests the training paradigm itself has limitations we haven't solved.

## Key Concepts

`#knowledge-retrieval` `#order-effects` `#logical-deduction` `#model-generalization` `#fact-learning` `#finetuning` `#auto-regressive-language-models` `#knowledge-representation` `#transformer-models` `#natural-language-processing` `#machine-learning`

## Cites (Key Papers)

- [[Allen Z., Li Y., Berglund L., Stickland A. C., Balesni M., Kaufmann M., Tong M., Korbak T., Kokotajlo D. & Evans O. (2023) - Taken out of context: On measuring situational awareness in ...]]
- [[Bireta T. J., Fry S. E., Jalbert A., Neath I., Aimée M., Surprenant G., Tehan G. A. & Tolan (2010) - Backward recall and benchmark effects of working memory]]
- [[Brown T., Mann B., Ryder N., Subbiah M., Kaplan J. D., Dhariwal P., Neelakantan A., Shyam P., Sastry G. & Askell A. (2020) - Language models are few-shot learners]]
- [[St H. & John R. (2013) - Are forward and backward recall the same? a dual-task study ...]]
- [[De Cao N., Aziz W. & Titov I. (2021) - Editing factual knowledge in language models]]
- [[Dong Q., Li L., Dai D., Zheng C., Wu Z., Chang B., Sun X., Xu J., Li L. & Sui Z. (2023) - A survey on in-context learning]]
- [[Elazar Y., Kassner N., Ravfogel S., Ravichander A., Hovy E. H., Schütze H. & Goldberg Y. (2021) - Measuring and improving consistency in pretrained language m...]]
- [[Fluri L., Paleka D. & Tramèr F. (2023) - Evaluating superhuman models with consistency checks]]
- [[Geva M., Schuster R., Berant J. & Levy O. (2021) - Transformer feed-forward layers are key-value memories]]
- [[Geva M., Caciularu A., Wang K. R. & Goldberg Y. (2022) - Transformer feed-forward layers build predictions by promoti...]]

*(27 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Memory & Cognition
**DOI:** [10.1101/2023.03.04.531109](https://doi.org/10.1101/2023.03.04.531109)
**arXiv:** [2309.12288](https://arxiv.org/abs/2309.12288)
**PDF:** [[arxiv_2309.12288.pdf]]

## Abstract

We expose a surprising failure of generalization in auto-regressive large language models (LLMs). If a model is trained on a sentence of the form "A is B", it will not automatically generalize to the reverse direction "B is A". This is the Reversal Curse. For instance, if a model is trained on "Valentina Tereshkova was the first woman to travel to space", it will not automatically be able to answer the question, "Who was the first woman to travel to space?". Moreover, the likelihood of the correct answer ("Valentina Tershkova") will not be higher than for a random name. Thus, models do not generalize a prevalent pattern in their training set: if "A is B" occurs, "B is A" is more likely to occur. It is worth noting, however, that if "A is B" appears in-context, models can deduce the reverse relationship.

We provide evidence for the Reversal Curse by finetuning GPT-3 and Llama-1 on fictitious statements such as "Uriah Hawthorne is the composer of Abyssal Melodies" and showing that they fail to correctly answer "Who composed Abyssal Melodies?". The Reversal Curse is robust across model sizes and model families and is not alleviated by data augmentation. We also evaluate ChatGPT (GPT-3.5 and GPT-4) on questions about real-world celebrities, such as "Who is Tom Cruise's mother? [A: Mary Lee Pfeiffer]" and the reverse "Who is Mary Lee Pfeiffer's son?". GPT-4 correctly answers questions like the former 79% of the time, compared to 33% for the latter.

## Full Citation List

1. Allen Z., Li Y., Berglund L. et al. (2023). Taken out of context: On measuring situational awareness in llms.
2. Bireta T. J., Fry S. E., Jalbert A. et al. (2010). Backward recall and benchmark effects of working memory. Memory & Cognition, Vol. 38, pp. 12393461.
3. Brown T., Mann B., Ryder N. et al. (2020). Language models are few-shot learners.
4. St H. & John R. (2013). Are forward and backward recall the same? a dual-task study of digit recall. Memory & Cognition, Vol. 41, pp. 207716696.
5. De Cao N., Aziz W. & Titov I. (2021). Editing factual knowledge in language models.
6. Dong Q., Li L., Dai D. et al. (2023). A survey on in-context learning.
7. Elazar Y., Kassner N., Ravfogel S. et al. (2021). Measuring and improving consistency in pretrained language models.
8. Fluri L., Paleka D. & Tramèr F. (2023). Evaluating superhuman models with consistency checks.
9. Geva M., Schuster R., Berant J. et al. (2021). Transformer feed-forward layers are key-value memories.
10. Geva M., Caciularu A., Wang K. R. et al. (2022). Transformer feed-forward layers build predictions by promoting concepts in the vocabulary space.
11. Geva M., Bastings J., Filippova K. et al. (2023). Dissecting recall of factual associations in auto-regressive language models.
12. Grosse R., Bae J., Anil C. et al. (2023). Studying large language model generalization with influence functions.
13. Guitard D., Saint-Aubin J., Poirier M. et al. (2019). Forward and backward recall: Different visuospatial processes when you know what's coming. Memory & Cognition, Vol. 48, pp. 111-126.
14. Hase P., Diab M., Celikyilmaz A. et al. (2023). Methods for measuring, updating, and visualizing factual beliefs in language models.
15. Hosseini A., Reddy S., Bahdanau D. et al. (2021). Understanding by understanding not: Modeling negation in language models.
16. Imdb (2023). Search imdb: Match all (sorted by popularity ascending.
17. Kandpal N., Deng H., Roberts A. et al. (2023). Large language models struggle to learn long-tail knowledge.
18. Diederik P., Kingma J. & Ba (2017). Adam: A method for stochastic optimization.
19. Lester B., Al-Rfou R. & Constant N. (2021). The power of scale for parameter-efficient prompt tuning.
20. Chen S. & Lewandowsky S. (1995). Forward and backward recall: Different retrieval processes. Journal of Experimental Psychology: Learning, Memory, and Cognition, Vol. 21(4), pp. 837-847.
21. Lin S., Hilton J. & Evans O. (2022). Truthfulqa: Measuring how models mimic human falsehoods.
22. Mangrulkar S., Gugger S., Debut L. et al. (2022). Peft: State-of-the-art parameter-efficient fine-tuning methods.
23. Meng K., Bau D., Andonian A. et al. (2023). Locating and editing factual associations in gpt.
24. Mitchell E., Lin C., Bosselut A. et al. (2021). Fast model editing at scale.
25. Open AI. Gpt-4 technical report 2023
26. Openai Openai 2023. 17 August 2023
27. Petroni F., Rocktäschel T., Lewis P. et al. (2019). Language models as knowledge bases? arXiv preprint.
28. Press O., Zhang M., Min S. et al. (2023). Measuring and narrowing the compositionality gap in language models.
29. Shi F., Chen X., Misra K. et al. (2023). Large language models can be easily distracted by irrelevant context.
30. Speer R., Chin J. & Havasi C. (2017). Conceptnet 5.5: An open multilingual graph of general knowledge.
31. Thomas J. G., Milner H. R. & Haberlandt K. F. (2003). Forward and backward recall. Psychological Science, Vol. 14, pp. 30872510.
32. Touvron H., Lavril T., Izacard G. et al. (2023). Llama: Open and efficient foundation language models.
33. Brain mechanisms of reversible symbolic reference: a potential singularity of the human brain Louise Timo Van Kerkoerle Milad Pape Xiaoxia Ekramnia Jordy Feng Morgan Tasserie Xiaolian Dupont Bechir Li Wim Jarraya Stanislas Vanduffel Dehaene 10.1101/2023.03.04.531109 bio Rxiv 2023
34. Wang B. & Komatsuzaki A. (2021). GPT-J-6B: A 6 Billion Parameter Autoregressive Language Model.
35. Workshop B., Le Scao T., Fan A. et al. (2023). A 176b-parameter open-access multilingual language model.
36. Yao Y., Huang S., Dong L. et al. (2022). Kformer: Knowledge injection in transformer feed-forward layers.
37. Zhu C., Singh Rawat A., Zaheer M. et al. (2020). Modifying memories in transformer models.
