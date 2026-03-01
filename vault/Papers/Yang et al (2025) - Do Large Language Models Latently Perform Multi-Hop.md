---
title: "Do Large Language Models Latently Perform Multi-Hop Reasoning?"
authors: ["Yang, Sohee", "Gribovskaya, Elena", "Kassner, Nora", "Geva, Mor", "Riedel, Sebastian", "Deepmind, Google", "Ucl", "Research, Google", "Bao, Ing", "Bavarian, Mo", "Belgum, Jeff", "Bello, Irwan", "Berdine, Jake", "Bernadett-Shapiro, Gabriel", "Berner, Christo- Pher", "Bogdonoff, Lenny", "Boiko, Oleg", "Boyd, Made- Laine", "Brakman, Anna-Luisa", "Brockman, Greg", "Brooks, Tim", "Brundage, Miles", "Button, Kevin", "Cai, Trevor", "Campbell, Rosie", "Cann, Andrew", "Carey, Brittany", "Carlson, Chelsea", "Carmichael, Rory", "Chan, Brooke", "Chang, Che", "Chantzis, Fotis", "Chen, Derek", "Chen, Sully", "Chen, Ruby", "Chen, Jason", "Chen, Mark", "Chess, Ben", "Cho, Chester", "Chu, Casey", "Chung, Won", "Cummings, Dave", "Currier, Jeremiah", "Dai, Yunxing", "Decareaux, Cory", "Degry, Thomas", "Deutsch, Noah", "Deville, Damien", "Dhar, Arka", "Dohan, David", "Dowl- Ing, Steve", "Dunning, Sheila", "Ecoffet, Adrien", "Eleti, Atty", "Eloundou, Tyna", "Farhi, David", "Fedus, Liam", "Felix, Niko", "Fishman, Posada", "Forte, Juston", "Fulford, Is- Abella", "Gao, Leo", "Georges, Elie", "Gibson, Christian", "Goel, Vik", "Gogineni, Tarun", "Goh, Gabriel", "Gontijo-Lopes, Rapha", "Gordon, Jonathan", "Grafstein, Morgan", "Gray, Scott", "Greene, Ryan", "Gross, Joshua", "Gu, Shane", "Guo, Yufei", "Hallacy, Chris", "Han, Jesse", "Harris, Jeff", "He, Yuchen", "Heaton, Mike", "Heidecke, Jo- Hannes", "Hesse, Chris", "Hickey, Alan", "Hickey, Wade", "Hoeschele, Peter", "Houghton, Brandon", "Hsu, Kenny", "Hu, Shengli", "Hu, Xin", "Huizinga, Joost", "Jain, Shantanu", "Jain, Shawn", "Jang, Joanne", "Jiang, Angela", "Jiang, Roger", "Jin, Haozhun", "Jin, Denny", "Jomoto, Shino", "Jonn, Billie", "Jun, Heewoo", "Kaftan, Tomer", "Kaiser, Łukasz", "Kamali, Ali", "Kanitscheider, Ingmar", "Nitish, Shirish", "Keskar, Tabarak", "Khan, Logan", "Kilpatrick, Jong Wook", "Kim, Christina", "Kim, Yongjik", "Kim, Hendrik", "Kirch- Ner, Jamie", "Kiros, Matt", "Knight, Daniel", "Kokotajlo, Łukasz", "Kondraciuk, Andrew", "Kondrich, Aris", "Kon- Stantinidis, Kyle", "Kosic, Gretchen", "Krueger, Vishal", "Kuo, Michael", "Lampe, Ikai", "Lan, Teddy", "Lee, Jan", "Leike, Jade", "Leung, Daniel", "Levy, Ming", "Li, Rachel", "Lim, Molly", "Lin, Stephanie", "Lin, Mateusz", "Litwin, Theresa", "Lopez, Ryan", "Lowe, Patricia", "Lue, Anna", "Makanju, Kim", "Malfacini, Sam", "Manning, Todor", "Markov, Yaniv", "Markovski, Bianca", "Martin, Katie", "Mayer, Andrew", "Mayne, Bob", "Mcgrew, Scott Mayer", "Mckinney, Christine", "Mcleavey, Paul", "Mcmillan, Jake", "Mcneil, David", "Medina, Aalok", "Mehta, Jacob", "Menick, Luke", "Metz, Andrey", "Mishchenko, Pamela", "Mishkin, Vinnie", "Monaco, Evan", "Morikawa, Daniel", "Mossing, Tong", "Mu, Mira", "Murati, Oleg", "Murk, David", "Mély, Ashvin", "Nair, Reiichiro", "Nakano, Rajeev", "Nayak, Arvind", "Neelakantan, Richard", "Ngo, Hyeonwoo", "Noh, Long", "Ouyang, Cullen", "O'keefe, Jakub", "Pachocki, Alex", "Paino, Joe", "Palermo, Ashley", "Pantuliano, Giambat- Tista", "Parascandolo, Joel", "Parish, Emy", "Parparita, Alex", "Passos, Mikhail", "Pavlov, Andrew", "Peng, Adam", "Perel- Man, Filipe", "De Avila, Belbute", "Peres, Michael", "Petrov, Henrique", "Ponde", "Pinto, Oliveira", "Pokrass, Michelle", "Pong, Vitchyr", "Pow- Ell, Tolly", "Power, Alethea", "Power, Boris", "Proehl, Elizabeth", "Puri, Raul", "Radford, Alec", "Rae, Jack", "Ramesh, Aditya", "Raymond, Cameron", "Real, Francis", "Rimbach, Kendra", "Ross, Carl", "Rotsted, Bob", "Roussez, Henri", "Ry- Der, Nick", "Saltarelli, Mario", "Sanders, Ted", "Santurkar, Shibani", "Sastry, Girish", "Schmidt, Heather", "Schnurr, David", "Schulman, John", "Selsam, Daniel", "Sheppard, Kyla", "Sherbakov, Toki", "Shieh, Jessica", "Shoker, Sarah", "Shyam, Pranav", "Sidor, Szymon", "Sigler, Eric", "Simens, Maddie", "Sitkin, Jordan", "Slama, Katarina", "Sohl, Ian", "Sokolowsky, Benjamin", "Song, Yang", "Staudacher, Natalie", "Winter, Clemens", "Wolrich, Samuel", "Wong, Hannah", "Workman, Lauren", "Wu, Sherwin", "Wu, Jeff", "Wu, Michael", "Xiao, Kai", "Xu, Tao", "Yoo, Sarah", "Yu, Kevin", "Yuan, Qiming", "Zaremba, Wojciech", "Zellers, Rowan", "Zhang, Chong", "Zhang, Marvin", "Zhao, Shengjia", "Zheng, Tian- Hao", "Zhuang, Juntang", "Zhuk, William", "Petroni, Fabio", "Rocktäschel, Tim", "Lewis, Patrick", "Bakhtin, Anton", "Wu, Yuxiang", "Sakarvadia, Mansi", "Ajith, Aswathy", "Khan, Arham", "Grzenda, Daniel", "Hudson, Nathaniel", "Bauer, André", "Touvron, Hugo", "Martin, Louis", "Stone, Kevin", "Al- Bert, Peter", "Almahairi, Amjad", "Babaei, Yasmine", "Bashlykov, Nikolay", "Batra, Soumya", "Bhargava, Prajjwal", "Bhosale, Shruti", "Bikel, Dan", "Blecher, Lukas", "Ferrer, Cristian Canton", "Chen, Moya", "Cucurull, Guillem", "Esiobu, David", "Fernandes, Jude", "Fu, Jeremy", "Fu, Wenyin", "Fuller, Brian", "Gao, Cynthia", "Goswami, Vedanuj", "Goyal, Naman", "Hartshorn, An- Thony", "Hosseini, Saghar", "Hou, Rui", "Inan, Hakan", "Kardas, Marcin", "Kerkez, Viktor", "Khabsa, Madian", "Kloumann, Isabel", "Korenev, Artem", "Koura, Singh", "Lachaux, Marie-Anne", "Lavril, Thibaut", "Lee, Jenya", "Liskovich, Di- Ana", "Lu, Yinghai", "Mao, Yuning", "Mar- Tinet, Xavier", "Mihaylov, Todor", "Mishra, Pushkar", "Moly- Bog, Igor", "Nie, Yixin", "Poulton, Andrew", "Reizen- Stein, Jeremy", "Rungta, Rashi", "Saladi, Kalyan", "Vaswani, Ashish", "Shazeer, Noam", "Parmar, Niki", "Uszkoreit, Jakob", "Jones, Llion", "Gomez, Aidan N", "Polosukhin, Illia 2017", "Attention", "Akyürek, Ekin", "Schuurmans, Dale", "Andreas, Jacob", "Ma, Tengyu", "Zhou, Denny", "Asai, Akari", "Hajishirzi, Hannaneh", "Tom B Brown, Benjamin", "Mann, Nick", "Ryder, Melanie", "Subbiah, Jared", "Kaplan, Prafulla", "Dhariwal, Arvind", "Neelakantan, Pranav", "Shyam, Girish", "Sastry, Amanda", "Askell, Sandhini", "Agarwal, Ariel", "Herbert-Voss, Gretchen", "Krueger, Tom", "Henighan, Rewon", "Child, Aditya", "Ramesh", "Daniel, M", "Ziegler, Jeffrey", "Wu, Clemens", "Winter, Christopher", "Hesse, Mark", "Chen, Eric", "Sigler, Mateusz", "Litwin, Scott", "Gray, Benjamin", "Chess, Jack", "Clark, Christopher", "Berner, Sam", "Mccandlish, Alec", "Radford, Ilya", "Sutskever, Dario", "Amodei", "Conmy, Arthur", "Mavor-Parker, Augustine N", "Lynch, Aengus", "Heimersheim, Stefan", "Garriga-Alonso, Adrià", "Dai, Damai", "Sun, Yutao", "Dong, Li", "Hao, Yaru", "Sui, Zhifang", "Wei, Furu", "De Cao, Nicola", "Aziz, Wilker", "Titov, Ivan", "Dziri, Nouha", "Lu, Ximing", "Sclar, Melanie", "Xiang, Lorraine", "Li, Liwei", "Jiang, Bill", "Yuchen Lin, Sean", "Welleck, Peter", "West, Chandra", "Bhagavatula", "Ronan, Le", "Bras, Jena D", "Hwang, Soumya", "Sanyal, Xiang", "Ren, Allyson", "Ettinger, Zaid", "Harchaoui, Yejin", "Choi", "Feng, Jiahai", "Steinhardt, Jacob", "Geva, Mor", "Bastings, Jasmijn", "Filippova, Katja", "Globerson, Amir", "Geva, Mor", "Caciularu, Avi", "Wang, Kevin Ro", "Goldberg, Yoav", "Geva, Mor", "Schuster, Roei", "Berant, Jonathan", "Levy, Omer", "Hernandez, Evan", "Arnab, Sen", "Sharma, Tal", "Haklay, Kevin", "Meng, Martin", "Wattenberg, Jacob", "Andreas, Yonatan", "Belinkov, David", "Bau", "Hou, Yifan", "Li, Jiaoda", "Fei, Yu", "Stolfo, Alessandro", "Zhou, Wangchunshu", "Zeng, Guangtao", "Bosselut, Antoine", "Sachan, Mrinmaya", "Jang, Myeongjun", "Prasad Majumder, Bodhisattwa", "Mcauley, Julian", "Lukasiewicz, Thomas", "Camburu, Oana-Maria", "Kassner, Nora", "Tafjord, Oyvind", "Sabharwal, Ashish", "Richardson, Kyle", "Schuetze, Hinrich", "Clark, Peter", "Kassner, Nora", "Tafjord, Oyvind", "Schütze, Hinrich", "Clark, Peter", "Kobayashi, Goro", "Kuribayashi, Tatsuki", "Yokoi, Sho", "Inui, Kentaro", "Li, Tao", "Gupta, Vivek", "Mehta, Maitrey", "Vivek", "Meng, Kevin", "Bau, David", "Andonian, Alex", "Belinkov, Yonatan", "Mitchell, Eric", "Lin, Charles", "Bosselut, Antoine", "Finn, Chelsea", "Manning, Christopher D", "Press, Ofir", "Zhang, Muru", "Min, Sewon", "Schmidt, Ludwig", "Smith, Noah", "Lewis, Mike", "Onoe, Yasumasa", "Michael, J Q", "Zhang, Shankar", "Padmanabhan, Greg", "Durrett, Eunsol", "Choi", "Von, Johannes", "Niklasson, Eyvind", "Randazzo, Ettore", "Sacramento, João", "Mordvintsev, Alexander", "Zhmoginov, Andrey", "Vladymyrov, Max", "Ro, Kevin", "Variengien, Alexandre", "Conmy, Arthur", "Shlegeris, Buck", "Steinhardt, Jacob", "Wei, Jason", "Wang, Xuezhi", "Schuurmans, Dale", "Bosma, Maarten", "Chi, Ed", "Le, Quoc", "Zhou, Denny", "Welbl, Johannes", "Stenetorp, Pontus", "Riedel, Sebastian", "Yang, Zhilin", "Qi, Peng", "Zhang, Saizheng", "Bengio, Yoshua", "Cohen, William W", "Salakhutdinov, Ruslan", "Manning, Christopher D", "Zhong, Zexuan", "Wu, Zhengxuan", "Manning, Christopher D", "Potts, Christopher", "Chen, Danqi", "Zhou, Denny", "Schärli, Nathanael", "Hou, Le", "Wei, Jason", "Scales, Nathan", "Wang, Xuezhi", "Schuurmans, Dale", "Cui, Claire", "Bousquet, Olivier", "Quoc V Le, Ed H", "Chi"]
year: 2025
venue: "TACL"
arxiv: "2402.16837"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - entity-recall-score
  - consistency-score
  - latent-reasoning-pathway
  - bridge-entity
  - multi-hop-factual-reasoning
  - fact-composition-type
  - activation-patching
  - transformer-interpretability
  - scaling-trends
  - knowledge-composition
---

# Do Large Language Models Latently Perform Multi-Hop Reasoning?

**Yang, Sohee et al.** • 2025

> [!quote] Memorable Quote
> "Although our analysis is based on LLaMA-2 family of models of up to 70B parameters, our findings suggest potential limitations in the current scaling paradigm for multi-hop reasoning."

## Quick Refresh

The authors investigate whether large language models internally perform multi-hop reasoning—connecting multiple facts to answer complex questions—without explicit hints in the prompt. Using a dataset of 45,595 two-hop factual prompts (like "The mother of the singer of 'Superstition' is"), they develop metrics for measuring internal identification of bridge entities and how well models use knowledge about those entities. They find substantial evidence of first-hop reasoning (approximately 70% of prompts) but only moderate evidence for the complete reasoning pipeline, with highly variable patterns across fact types and no scaling improvement for the second hop in larger models.

## Why You Cared

You were researching whether LLMs actually reason compositionally or simply store redundant facts—a question with direct implications for model editing and parameter efficiency. This paper moves beyond asking whether LLMs can do multi-hop reasoning (they sometimes can with explicit context) to asking whether they do it latently using internal knowledge retrieval, a distinction that separates genuine compositional reasoning from factual memorization. The findings also explain why simply editing base facts fails to propagate changes to dependent facts, suggesting fundamental limitations in model architecture or pretraining that scaling alone may not overcome.

## Key Concepts

`#entity-recall-score` `#consistency-score` `#latent-reasoning-pathway` `#bridge-entity` `#multi-hop-factual-reasoning` `#fact-composition-type` `#activation-patching` `#transformer-interpretability` `#scaling-trends` `#knowledge-composition`

## Cites (Key Papers)

- [[Akyürek E., Schuurmans D., Andreas J., Ma T. & Zhou D. (2023) - What learning algorithm is in-context learning? investigatio...]]
- [[2023a. Physics of language models: Part 3.1, knowledge storage and extraction Ze...]]
- [[Allen Z. & Li Y. (2023) - Physics of language models: Part 3.2, knowledge manipulation]]
- [[Asai A. & Hajishirzi H. (2020) - Logicguided data augmentation and regularization for consist...]]
- [[Belrose N., Furman Z., Smith L., Halawi D., Ostrovsky I., Mckinney L., Biderman S., Steinhardt J., Berglund ;. A., Stickland A. C., Balesni M., Kaufmann M., Tong M., Korbak T., Kokotajlo D. & Evans O. (2023) - Eliciting latent predictions from transformers with the tune...]]
- [[Berglund L., Tong M., Kaufmann M., Balesni M., Stickland A. C., Korbak T. & Evans O. (2024) - The reversal curse: LLMs trained on "a is b" fail to learn "...]]
- [[Brinkmann J., Sheshadri A., Levoso V., Swoboda P. & Bartelt C. (2023) - A mechanistic analysis of a transformer trained on a symboli...]]
- [[Tom B Brown B., Mann N., Ryder M., Subbiah J., Kaplan P., Dhariwal A., Neelakantan P., Shyam G., Sastry A., Askell S., Agarwal A., Herbert-Voss G., Krueger T., Henighan R., Child A., Ramesh, Daniel M., Ziegler J., Wu C., Winter C., Hesse M., Chen E., Sigler M., Litwin S., Gray B., Chess J., Clark C., Berner S., Mccandlish A., Radford I., Sutskever D. & Amodei (2020) - Language models are few-shot learners]]
- [[Chan S., Santoro A., Lampinen A., Wang J., Singh A., Richemond P., Mcclelland J. & Hill F. (2022) - Data distributional properties drive emergent in-context lea...]]
- [[Chanin D., Hunter A. & Camburu O. (2023) - Identifying linear relational concepts in large language mod...]]

*(39 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** TACL
**arXiv:** [2402.16837](https://arxiv.org/abs/2402.16837)
**PDF:** [[arxiv_2402.16837.pdf]]

## Abstract

We study whether Large Language Models (LLMs) latently perform multi-hop reasoning with complex prompts such as "The mother of the singer of 'Superstition' is". We look for evidence of a latent reasoning pathway where an LLM (1) latently identifies "the singer of 'Superstition"' as Stevie Wonder, the bridge entity, and (2) uses its knowledge of Stevie Wonder's mother to complete the prompt. We analyze these two hops individually and consider their co-occurrence as indicative of latent multi-hop reasoning. For the first hop, we test if changing the prompt to indirectly mention the bridge entity instead of any other entity increases the LLM's internal recall of the bridge entity. For the second hop, we test if increasing this recall causes the LLM to better utilize what it knows about the bridge entity. We find strong evidence of latent multi-hop reasoning for the prompts of certain relation types, with the reasoning pathway used in more than 80% of the prompts. However, the utilization is highly contextual, varying across different types of prompts. Also, on average, the evidence for the second hop and the full multi-hop traversal is rather moderate and only substantial for the first hop. Moreover, we find a clear scaling trend with increasing model size for the first hop of reasoning but not for the second hop. Our experimental findings suggest potential challenges and opportunities for future development and applications of LLMs. 1

## Full Citation List

1. Akyürek E., Schuurmans D., Andreas J. et al. (2023). What learning algorithm is in-context learning? investigations with linear models.
2. 2023a. Physics of language models: Part 3.1, knowledge storage and extraction Zeyuan Allen -Zhu Yuanzhi Li arXiv
3. Allen Z. & Li Y. (2023). Physics of language models: Part 3.2, knowledge manipulation.
4. Asai A. & Hajishirzi H. (2020). Logicguided data augmentation and regularization for consistent question answering.
5. Belrose N., Furman Z., Smith L. et al. (2023). Eliciting latent predictions from transformers with the tuned lens.
6. Berglund L., Tong M., Kaufmann M. et al. (2024). The reversal curse: LLMs trained on "a is b" fail to learn "b is a.
7. Brinkmann J., Sheshadri A., Levoso V. et al. (2023). A mechanistic analysis of a transformer trained on a symbolic multi-step reasoning task.
8. Tom B Brown B., Mann N., Ryder M. et al. (2020). Language models are few-shot learners.
9. Chan S., Santoro A., Lampinen A. et al. (2022). Data distributional properties drive emergent in-context learning in transformers.
10. Chanin D., Hunter A. & Camburu O. (2023). Identifying linear relational concepts in large language models.
11. Cohen R., Biran E., Yoran O. et al. (2023). Evaluating the ripple effects of knowledge editing in language models.
12. Conmy A., Mavor-Parker A. N., Lynch A. et al. (2023). Towards automated circuit discovery for mechanistic interpretability.
13. Dai D., Sun Y., Dong L. et al. (2023). Why can GPT learn in-context? language models secretly perform gradient descent as meta-optimizers.
14. De Cao N., Aziz W. & Titov I. (2021). Editing factual knowledge in language models.
15. Yom Din A., Karidi T., Choshen L. et al. (2023). Jump to conclusions: Shortcutting transformers with linear transformations.
16. Dziri N., Lu X., Sclar M. et al. (2023). Faith and fate: Limits of transformers on compositionality.
17. Hinrich Schütze, and Yoav Goldberg. 2021. Measuring and improving consistency in pretrained language models Yanai Elazar Nora Kassner Shauli Ravfogel Abhilasha Ravichander Eduard Hovy TACL
18. Feng J. & Steinhardt J. (2024). How do language models bind entities in context?.
19. Geva M., Bastings J., Filippova K. et al. (2023). Dissecting recall of factual associations in auto-regressive language models.
20. Geva M., Caciularu A., Wang K. R. et al. (2022). Transformer feed-forward layers build predictions by promoting concepts in the vocabulary space.
21. Geva M., Schuster R., Berant J. et al. (2021). Transformer feed-forward layers are key-value memories.
22. Hernandez E., Arnab S., Sharma T. et al. (2024). Linearity of relation decoding in transformer language models.
23. Hou Y., Li J., Fei Y. et al. (2023). Towards a mechanistic interpretation of multi-step reasoning capabilities of language models.
24. Jang M., Prasad Majumder B., Mcauley J. et al. (2023). Know how to make up your mind! adversarially detecting and alleviating inconsistencies in natural language explanations.
25. Kassner N., Tafjord O., Sabharwal A. et al. (2023). Language models with rationality.
26. Kassner N., Tafjord O., Schütze H. et al. (2021). BeliefBank: Adding memory to a pre-trained language model for a systematic notion of belief.
27. Kobayashi G., Kuribayashi T., Yokoi S. et al. (2023). Transformer language models handle word frequency in prediction head.
28. Li T., Gupta V., Mehta M. et al. (2019). A logic-driven framework for consistency of neural models.
29. Li Z., Jiang G., Xie H. et al. (2024). Understanding and patching compositional reasoning in llms.
30. Lieberum T., Rahtz M., Kramár J. et al. (2023). Does circuit analysis interpretability scale? evidence from multiple choice capabilities in chinchilla.
31. Mcgrath T., Rahtz M., Kramar J. et al. (2023). The hydra effect: Emergent self-repair in language model computations.
32. Meng K., Bau D., Andonian A. et al. (2022). Locating and editing factual associations in GPT.
33. Mitchell E., Lin C., Bosselut A. et al. (2022). Fast model editing at scale.
34. Neel Nanda Joseph Bloom 2022 Transformerlens
35. Nanda N., Chan L., Lieberum T. et al. (2022). Progress measures for grokking via mechanistic interpretability.
36. Press O., Zhang M., Min S. et al. (2023). Measuring and narrowing the compositionality gap in language models.
37. Catherine Olsson Nelson Elhage Neel Nanda Nicholas Joseph Nova Dassarma Tom Henighan Ben Mann Amanda Askell Yuntao Bai Anna Chen Tom Conerly Dawn Drain Deep Ganguli Zac Hatfield-Dodds Danny Hernandez Scott Johnston Andy Jones Kernion, Liane Lovitt, Kamal Ndousse, Dario Amodei, Tom Brown, Jack Clark, Jared Kaplan, Sam Mc Candlish and Chris Olah. 2022. In-context learning and induction heads. arXiv
38. Onoe Y., Michael J., Zhang S. et al. (2023). Can LMs learn new entities from descriptions? challenges in propagating injected knowledge.
39. Von J., Niklasson E., Randazzo E. et al. (2023). Transformers learn in-context by gradient descent.
40. Vrandečić D. & Krötzsch M. (2014). Wikidata: a free collaborative knowledgebase.
41. Ro K., Variengien A., Conmy A. et al. (2023). Interpretability in the wild: a circuit for indirect object identification in GPT-2 small.
42. Jason Wei Yi Tay Rishi Bommasani Colin Raffel Barret Zoph Sebastian Borgeaud Dani Yogatama Maarten Bosma Denny Zhou Donald Metzler et al. 2022a. Emergent abilities of large language models. TMLR
43. Wei J., Wang X., Schuurmans D. et al. (2022). Chain of thought prompting elicits reasoning in large language models.
44. Welbl J., Stenetorp P. & Riedel S. (2018). Constructing datasets for multi-hop reading comprehension across documents. TACL.
45. Thomas Wolf Lysandre Debut Victor Sanh Julien Chaumond Clement Delangue Anthony Moi Pierric Cistac Tim Rault Rémi Louf Morgan Funtowicz Joe Davison Sam Shleifer Clara Patrick Von Platen Yacine Ma Julien Jernite Canwen Plu Teven Xu Sylvain Le Scao Mariama Gugger Quentin Drame Alexander MLhoest Rush 2020 Huggingface's transformers: State-of-the-art natural language processing. arXiv
46. Yang Z., Qi P., Zhang S. et al. (2018). HotpotQA: A dataset for diverse, explainable multi-hop question answering.
47. Zhang N., Yao Y., Tian B. et al. (2024). A comprehensive study of knowledge editing for large language models.
48. Zhong Z., Wu Z., Manning C. D. et al. (2023). MQAKE: Assessing knowledge editing in language models via multi-hop questions.
49. Zhou D., Schärli N., Hou L. et al. (2022). Least-to-most prompting enables complex reasoning in large language models.
