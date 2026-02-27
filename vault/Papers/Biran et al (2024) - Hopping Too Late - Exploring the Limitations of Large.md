---
title: "Hopping Too Late: Exploring the Limitations of Large Language Models on Multi-Hop Queries"
authors: ["Biran, Eden", "Gottesman, Daniela", "Yang, Sohee", "Geva, Mor", "Globerson, Amir", "Belinkov, Yonatan", "Belinkov, Yonatan", "Glass, James", "Biderman, Stella", "Schoelkopf, Hailey", "Anthony, Quentin Gregory", "Bradley, Herbie", "Kyle, O'", "Brien, Eric", "Hallahan, Mohammad", "Aflah Khan, Shivanshu", "Purohit", "Usvsn Sai Prashanth, Edward", "Raff", "Brinkmann, Jannik", "Sheshadri, Abhay", "Levoso, Victor", "Swoboda, Paul", "Bartelt, Christian", "Conmy, Arthur", "Mavor-Parker, Augustine", "Lynch, Aengus", "Heimersheim, Stefan", "Garriga-Alonso, Adrià", "Dai, Damai", "Dong, Li", "Hao, Yaru", "Sui, Zhifang", "Chang, Baobao", "Wei, Furu", "Dar, Guy", "Geva, Mor", "Gupta, Ankit", "Berant, Jonathan", "De Cao, Nicola", "Aziz, Wilker", "Titov, Ivan", "Dziri, Nouha", "Lu, Ximing", "Sclar, Melanie", "Xiang, (", "Lorraine, )", "Li, Liwei", "Jiang, Bill", "Yuchen Lin, Sean", "Welleck, Peter", "West, Chandra", "Bhagavatula", "Ronan, Le", "Bras, Jena", "Hwang, Soumya", "Sanyal, Xiang", "Ren, Allyson", "Ettinger, Zaid", "Harchaoui, Yejin", "Choi", "Geva, Mor", "Bastings, Jasmijn", "Filippova, Katja", "Globerson, Amir", "Geva, Mor", "Caciularu, Avi", "Wang, Kevin", "Goldberg, Yoav", "Geva, Mor", "Schuster, Roei", "Berant, Jonathan", "Levy, Omer", "Ghandeharioun, Asma", "Caciularu, Avi", "Pearce, Adam", "Dixon, Lucas", "Geva, Mor", "Hou, Yifan", "Li, Jiaoda", "Fei, Yu", "Stolfo, Alessandro", "Zhou, Wangchunshu", "Zeng, Guangtao", "Bosselut, Antoine", "Sachan, Mrinmaya", "Ju, Tianjie", "Chen, Yijin", "Yuan, Xinwei", "Zhang, Zhuosheng", "Du, Wei", "Zheng, Yubin", "Liu, Gongshen", "Lake, Brenden", "Baroni, Marco", "Li, Zhaoyi", "Jiang, Gangwei", "Xie, Hong", "Song, Linqi", "Lian, Defu", "Wei, Ying", "Li, Zhoubo", "Zhang, Ningyu", "Yao, Yunzhi", "Wang, Mengru", "Chen, Xi", "Chen, Huajun", "Meng, Kevin", "Bau, David", "Andonian, Alex", "Belinkov, Yonatan", "Merullo, Jack", "Eickhoff, Carsten", "Pavlick, Ellie", "Mitchell, Eric", "Lin, Charles", "Bosselut, Antoine", "Finn, Chelsea", "Manning, Christopher D", "Nanda, Neel", "Chan, Lawrence", "Lieberum, Tom", "Smith, Jess", "Steinhardt, Jacob", "Onoe, Yasumasa", "Zhang, Michael", "Padmanabhan, Shankar", "Durrett, Greg", "Choi, Eunsol", "Petty, Jackson", "Steenkiste, Sjoerd", "Dasgupta, Ishita", "Sha, Fei", "Garrette, Dan", "Linzen, Tal", "Press, Ofir", "Zhang, Muru", "Min, Sewon", "Schmidt, Ludwig", "Smith, Noah", "Lewis, Mike", "Sakarvadia, Mansi", "Ajith, Aswathy", "Khan, Arham", "Grzenda, Daniel", "Hudson, Nathaniel", "Bauer, André", "Chard, Kyle", "Foster, Ian", "Touvron, Hugo", "Martin, Louis", "Stone, Kevin", "Albert, Peter", "Almahairi, Amjad", "Babaei, Yasmine", "Bashlykov, Nikolay", "Batra, Soumya", "Bhargava, Prajjwal", "Bhosale, Shruti", "Vrandečić, Denny", "Krötzsch, Markus", "Wang, Fei", "Mo, Wenjie", "Wang, Yiwei", "Zhou, Wenxuan", "Chen, Muhao", "Ro, Kevin", "Variengien, Alexandre", "Conmy, Arthur", "Shlegeris, Buck", "Steinhardt, Jacob", "Wei, Jason", "Wang, Xuezhi", "Schuurmans, Dale", "Bosma, Maarten", "Xia, Fei", "Chi, Ed H", "Quoc V Le, Denny", "Zhou", "Wolf, Thomas", "Debut, Lysandre", "Sanh, Victor", "Chaumond, Julien", "Delangue, Clement", "Moi, Anthony", "Cistac, Pierric", "Rault, Tim", "Louf, Remi", "Funtowicz, Morgan", "Davison, Joe", "Shleifer, Sam", "Patrick Von Platen, Clara", "Ma, Yacine", "Jernite, Julien", "Plu, Canwen", "Xu, Teven", "Le Scao, Sylvain", "Gugger, Mariama", "Drame, Quentin", "Lhoest, Alexander", "Rush", "Xu, Nan", "Wang, Fei", "Li, Bangzheng", "Dong, Mingtao", "Chen, Muhao", "Yang, Sohee", "Gribovskaya, Elena", "Kassner, Nora", "Geva, Mor", "Riedel, Sebastian", "Zhong, Zexuan", "Wu, Zhengxuan", "Manning, Christopher", "Potts, Christopher", "Chen, Danqi"]
year: 2024
venue: "Computational Linguistics"
doi: "10.1162/coli_a_00422"
arxiv: "2406.12775"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - multi-hop-reasoning
  - patchscopes
  - latent-computation
  - transformer-layers
  - back-patching
  - knowledge-extraction
  - information-propagation
  - mechanistic-interpretability
  - language-models
---

# Hopping Too Late: Exploring the Limitations of Large Language Models on Multi-Hop Queries

**Biran, Eden et al.** • 2024

> [!quote] Memorable Quote
> "If the two resolutions are done by different groups of layers, it must be that these two groups are both able to perform knowledge extraction, be it via their attention or MLP sublayers. However, since transformers have a limited amount of layers, and their functionality is different, it is quite likely that the layer at which the second hop is performed will not have the desired functionality."

## Quick Refresh

The paper investigates how large language models (LLMs) internally compute answers to multi-hop queries—complex questions requiring two sequential reasoning steps. Using Patchscopes (a method for decoding information from hidden representations in neural networks) and back-patching experiments, the authors show that the bridge entity (the intermediate answer) is resolved in early layers, while the final answer emerges only in mid-to-upper layers. Critically, they find that this sequential timing can cause failures: when later layers must resolve the second hop, they sometimes lack the necessary knowledge, explaining why models fail despite "knowing" both individual facts.

## Why You Cared

You are studying how LLMs actually perform reasoning internally, not just whether they get the right answer. This paper directly addresses a gap: previous work showed latent multi-hop reasoning exists in small models trained on synthetic data, but this work demonstrates the same timing-dependent mechanism in large pretrained LLMs on real-world knowledge. The back-patching method also opens a path to understanding and potentially improving multi-hop reasoning without retraining.

## Key Concepts

`#multi-hop-reasoning` `#patchscopes` `#latent-computation` `#transformer-layers` `#back-patching` `#knowledge-extraction` `#information-propagation` `#mechanistic-interpretability` `#language-models`

## Cites (Key Papers)

- [[DavidBau 2024 Baukit]]
- [[Belinkov Y. (2022) - Probing classifiers: Promises, shortcomings, and advances]]
- [[Belinkov Y. & Glass J. (2019) - Analysis methods in neural language processing: A survey]]
- [[Biderman S., Schoelkopf H., Anthony Q. G., Bradley H., Kyle O., Brien E., Hallahan M., Aflah Khan S., Purohit, Usvsn Sai Prashanth E. & Raff (2023) - Pythia: A suite for analyzing large language models across t...]]
- [[Brinkmann J., Sheshadri A., Levoso V., Swoboda P. & Bartelt C. (2024) - A mechanistic analysis of a transformer trained on a symboli...]]
- [[Cohen R., Biran E., Yoran O., Globerson A. & Geva M. (2024) - Evaluating the ripple effects of knowledge editing in langua...]]
- [[Conmy A., Mavor-Parker A., Lynch A., Heimersheim S. & Garriga-Alonso A. (2023) - Towards automated circuit discovery for mechanistic interpre...]]
- [[Dai D., Dong L., Hao Y., Sui Z., Chang B. & Wei F. (2022) - Knowledge neurons in pretrained transformers]]
- [[Dar G., Geva M., Gupta A. & Berant J. (2023) - Analyzing transformers in embedding space]]
- [[De Cao N., Aziz W. & Titov I. (2021) - Editing factual knowledge in language models]]

*(32 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Computational Linguistics
**DOI:** [10.1162/coli_a_00422](https://doi.org/10.1162/coli_a_00422)
**arXiv:** [2406.12775](https://arxiv.org/abs/2406.12775)
**PDF:** [[arxiv_2406.12775.pdf]]

## Abstract

Large language models (LLMs) can solve complex multi-step problems, but little is known about how these computations are implemented internally. Motivated by this, we study how LLMs answer multi-hop queries such as "The spouse of the performer of Imagine is". These queries require two information extraction steps: a latent one for resolving the first hop ("the performer of Imagine") into the bridge entity (John Lennon), and another for resolving the second hop ("the spouse of John Lennon") into the target entity (Yoko Ono). Understanding how the latent step is computed internally is key to understanding the overall computation. By carefully analyzing the internal computations of transformer-based LLMs, we discover that the bridge entity is resolved in the early layers of the model. Then, only after this resolution, the two-hop query is solved in the later layers. Because the second hop commences in later layers, there could be cases where these layers no longer encode the necessary knowledge for correctly predicting the answer. Motivated by this, we propose a novel "back-patching" analysis method whereby a hidden representation from a later layer is patched back to an earlier layer. We find that in up to 66% of previously incorrect cases there exists a back-patch that results in the correct generation of the answer, showing that the later layers indeed sometimes lack the needed functionality. Overall, our methods and findings open further opportunities for understanding and improving latent reasoning in transformer-based LLMs.

## Full Citation List

1. David Bau 2024 Baukit
2. Belinkov Y. (2022). Probing classifiers: Promises, shortcomings, and advances. Computational Linguistics, Vol. 48(1), pp. 207-219. DOI: 10.1162/coli_a_00422
3. Belinkov Y. & Glass J. (2019). Analysis methods in neural language processing: A survey. Transactions of the Association for Computational Linguistics, Vol. 7, pp. 49-72. DOI: 10.1162/tacl_a_00254
4. Biderman S., Schoelkopf H., Anthony Q. G. et al. (2023). Pythia: A suite for analyzing large language models across training and scaling.
5. Brinkmann J., Sheshadri A., Levoso V. et al. (2024). A mechanistic analysis of a transformer trained on a symbolic multi-step reasoning task.
6. Cohen R., Biran E., Yoran O. et al. (2024). Evaluating the ripple effects of knowledge editing in language models. DOI: 10.1162/tacl_a_00644
7. Conmy A., Mavor-Parker A., Lynch A. et al. (2023). Towards automated circuit discovery for mechanistic interpretability.
8. Dai D., Dong L., Hao Y. et al. (2022). Knowledge neurons in pretrained transformers. DOI: 10.18653/v1/2022.acl-long.581
9. Dar G., Geva M., Gupta A. et al. (2023). Analyzing transformers in embedding space. DOI: 10.18653/v1/2023.acl-long.893
10. De Cao N., Aziz W. & Titov I. (2021). Editing factual knowledge in language models. DOI: 10.18653/v1/2021.emnlp-main.522
11. Dziri N., Lu X., Sclar M. et al. (2023). Faith and fate: Limits of transformers on compositionality.
12. Geva M., Bastings J., Filippova K. et al. (2023). Dissecting recall of factual associations in auto-regressive language models. DOI: 10.18653/v1/2023.emnlp-main.751
13. Geva M., Caciularu A., Wang K. et al. (2022). Transformer feed-forward layers build predictions by promoting concepts in the vocabulary space. DOI: 10.18653/v1/2022.emnlp-main.3
14. Geva M., Schuster R., Berant J. et al. (2021). Transformer feed-forward layers are keyvalue memories. DOI: 10.18653/v1/2021.emnlp-main.446
15. Ghandeharioun A., Caciularu A., Pearce A. et al. (2024). Patchscopes: A unifying framework for inspecting hidden representations of language models.
16. Hou Y., Li J., Fei Y. et al. (2023). Towards a mechanistic interpretation of multi-step reasoning capabilities of language models. DOI: 10.18653/v1/2023.emnlp-main.299
17. Cheng-Hsun, Hsueh P., Kuo-Ming et al. (2024). Editing the mind of giants: An in-depth exploration of pitfalls of knowledge editing in large language models.
18. Ju T., Chen Y., Yuan X. et al. (2024). Investigating multi-hop factual shortcuts in knowledge editing of large language models.
19. Lake B. & Baroni M. (2018). Generalization without systematicity: On the compositional skills of sequence-to-sequence recurrent networks.
20. 2024a. Understanding and patching compositional reasoning in LLMs Zhaoyi Li Gangwei Jiang Hong Xie Linqi Song Defu Lian Ying Wei Findings of the Association for Computational Linguistics ACL 2024 Bangkok, Thailand and virtual meeting Association for Computational Linguistics
21. 2024b. Unveiling the pitfalls of knowledge editing for large language models Zhoubo Li Ningyu Zhang Yunzhi Yao Mengru Wang Xi Chen Huajun Chen The Twelfth International Conference on Learning Representations
22. Mcgrath T., Rahtz M., Kramar J. et al. (2023). The hydra effect: Emergent self-repair in language model computations.
23. Meng K., Bau D., Andonian A. et al. (2022). Locating and editing factual associations in gpt.
24. Merullo J., Eickhoff C. & Pavlick E. (2024). Language models implement simple Word2Vec-style vector arithmetic. DOI: 10.18653/v1/2024.naacl-long.281
25. Meta A. I. (2024). Introducing meta llama 3: The most capable openly available llm to date.
26. Mitchell E., Lin C., Bosselut A. et al. (2022). Fast model editing at scale.
27. Nanda N., Chan L., Lieberum T. et al. (2023). Progress measures for grokking via mechanistic interpretability.
28. Onoe Y., Zhang M., Padmanabhan S. et al. (2023). Can LMs learn new entities from descriptions? challenges in propagating injected knowledge. DOI: 10.18653/v1/2023.acl-long.300
29. Petty J., Steenkiste S., Dasgupta I. et al. (2024). The impact of depth on compositional generalization in transformer language models. DOI: 10.18653/v1/2024.naacl-long.402
30. Press O., Zhang M., Min S. et al. (2023). Measuring and narrowing the compositionality gap in language models. DOI: 10.18653/v1/2023.findings-emnlp.378
31. Sakarvadia M., Ajith A., Khan A. et al. (2023). Memory injections: Correcting multi-hop reasoning failures during inference in transformer-based language models. DOI: 10.18653/v1/2023.blackboxnlp-1.26
32. Touvron H., Martin L., Stone K. et al. (2023). Open foundation and fine-tuned chat models.
33. Vrandečić D. & Krötzsch M. (2014). Wikidata: a free collaborative knowledgebase. Commun. ACM, Vol. 57(10), pp. 78-85. DOI: 10.1145/2629489
34. Wang B., Yue X., Su Y. et al. (2024). Grokked transformers are implicit reasoners: A mechanistic journey to the edge of generalization.
35. 2023a. A causal view of entity bias in (large) language models Fei Wang Wenjie Mo Yiwei Wang Wenxuan Zhou Muhao Chen 10.18653/v1/2023.findings-emnlp.1013 Findings of the Association for Computational Linguistics: EMNLP 2023 Singapore Association for Computational Linguistics
36. 2023b. Interpretability in the wild: a circuit for indirect object identification in GPT-2 small Kevin Ro Wang Alexandre Variengien Arthur Conmy Buck Shlegeris Jacob Steinhardt The Eleventh International Conference on Learning Representations
37. Wei J., Wang X., Schuurmans D. et al. (2022). Chain of thought prompting elicits reasoning in large language models.
38. Wolf T., Debut L., Sanh V. et al. (2020). Transformers: State-of-the-art natural language processing. DOI: 10.18653/v1/2020.emnlp-demos.6
39. Xu N., Wang F., Li B. et al. (2022). Does your model classify entities reasonably? diagnosing and mitigating spurious correlations in entity typing. DOI: 10.18653/v1/2022.emnlp-main.592
40. Yang S., Gribovskaya E., Kassner N. et al. (2024). Do large language models latently perform multi-hop reasoning?.
41. Zhang N., Yao Y., Tian B. et al. (2024). A comprehensive study of knowledge editing for large language models.
42. Zhong Z., Wu Z., Manning C. et al. (2023). MQuAKE: Assessing knowledge editing in language models via multi-hop questions. DOI: 10.18653/v1/2023.emnlp-main.971
