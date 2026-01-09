---
title: "Physics of Language Models: Part 3.1, Knowledge Storage and Extraction"
authors: ["Allen-Zhu, Zeyuan", "Li, Yuanzhi", "Xiao, Lin", "Zhou, Chunting", "Peng, Tianyi", "Liu, Xiaodong", "Zhou, Zhijie", "Ahmed, Nabib", "Anantharaman, Giri", "Bertoncini, Lucca", "Estela, Henry", "Hu, Liao", "Ho, Caleb", "Johnson, Wil", "Kokolis, Apostolos", "Sengupta, Shubho", "Clark, Ian", "De, Gourab", "Mann, Anmol", "Pfeifer, Max", "John R Anderson, Robert", "Milson", "Black, Sid", "Biderman, Stella", "Hallahan, Eric", "Anthony, Quentin", "Gao, Leo", "Golding, Laurence", "He, Horace", "Leahy, Connor", "Mcdonell, Kyle", "Phang, Jason", "Pieler, Michael", "Usvsn Sai Prashanth, Shivanshu", "Purohit, Laria", "Reynolds, Jonathan", "Tow, Ben", "Wang, Samuel", "Weinbach", "Fergus, I M", "Craik, Janine M", "Jennings", "Edward, J", "Hu, Phillip", "Wallis, Zeyuan", "Allen-Zhu, Yuanzhi", "Li, Shean", "Wang, Lu", "Wang, Weizhu", "Chen", "Devlin, Jacob", "Chang, Ming-Wei", "Kristina, Lee", "Kobayashi, Sosuke", "Lewis, Patrick", "Perez, Ethan", "Piktus, Aleksandra", "Petroni, Fabio", "Karpukhin, Vladimir", "Goyal, Naman", "Küttler, Heinrich", "Lewis, Mike", "Yih, Wen-Tau", "Rocktäschel, Tim", "Riedel, Sebastian", "Kiela, Douwe", "Meng, Kevin", "Bau, David", "Andonian, Alex", "Belinkov, Yonatan", "Naseem, Tahira", "Ravishankar, Srinivas", "Mihindukulasooriya, Nandana", "Abdelaziz, Ibrahim", "Lee, Young-Suk", "Kapanipathi, Pavan", "Roukos, Salim", "Gliozzo, Alfio", "Gray, Alexander", "Radford, Alec", "Wu, Jeffrey", "Child, Rewon", "Luan, David", "Amodei, Dario", "Sutskever, Ilya", "Richardson, Kyle", "Sabharwal, Ashish", "Sushil, Madhumita", "Suster, Simon", "Daelemans, Walter", "Zhu, Yukun", "Kiros, Ryan", "Zemel, Rich", "Salakhutdinov, Ruslan", "Urtasun, Raquel", "Torralba, Antonio", "Fidler, Sanja", "Zlotnik, Gregorio", "Vansintjan, Aaron"]
year: 2023
venue: "Psychological Review"
doi: "10.18653/v1/N18-2072"
arxiv: "2309.14316"
type: "paper"
status: "unread"
added: "2026-01-08"
tags:
  - knowledge-extraction
  - data-augmentation
  - linear-probing
  - memorization
  - transformer-models
  - instruction-finetuning
  - knowledge-encoding
  - hidden-embeddings
  - language-model-pretraining
  - natural-language-processing
---
# Physics of Language Models: Part 3.1, Knowledge Storage and Extraction

**Allen-Zhu, Zeyuan et al.** • 2023

> [!quote] Memorable Quote
> "Despite memorizing all knowledge from the BIO data during pretraining, the model encodes it in a disorganized manner within the transformer, preventing knowledge extraction during fine-tuning."

## Quick Refresh

This paper investigates how large language models (LLMs) store and extract knowledge by conducting controlled experiments on synthetic biography data. The key finding is that models can memorize training data word-for-word but fail to extract knowledge for answering questions about unseen individuals unless the training data includes diverse variations (paraphrasing, sentence shuffling, etc.). Using linear probing techniques, the authors show that knowledge augmentation causes models to encode information directly linked to entity names, whereas without augmentation the same knowledge gets scattered across unrelated tokens, making extraction impossible.

## Why You Cared

This paper matters because it reveals a critical gap between memorization and knowledge extraction in language models—a distinction rarely studied in controlled settings. The findings directly challenge assumptions about how pretraining alone enables knowledge extraction and provide actionable recommendations for industrial LLM training, particularly around data augmentation strategies. Understanding where and how knowledge gets encoded in model weights is essential for building more reliable, interpretable systems, and the paper's synthetic experimental setup provides a clean way to isolate these effects that would be confounded in internet-scale data.

## Key Concepts

`#knowledge-extraction` `#data-augmentation` `#linear-probing` `#memorization` `#transformer-models` `#instruction-finetuning` `#knowledge-encoding` `#hidden-embeddings` `#language-model-pretraining` `#natural-language-processing`

## Cites (Key Papers)

- [[Kenny B. (2033) - The person attended Queens College, City University of New Y...]]
- [[She graduated from Haverford College with a degree in Management. P &G recruited...]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 1, Learning Hierarchical La...]]
- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 3.2, Knowledge Manipulation]]
- [[Allen Z. & Li Y. (2024) - Physics of Language Models: Part 3.3, Knowledge Capacity Sca...]]
- [[John R Anderson R. & Milson (1989) - Human memory: An adaptive perspective]]
- [[Aspillaga C., Mendoza M. & Soto A. (2021) - Inspecting the concept knowledge graph encoded by modern lan...]]
- [[Baddeley A. D. (1997) - Human memory: Theory and practice]]
- [[Berglund L., Stickland A. C., Balesni M., Kaufmann M., Tong M., Korbak T., Kokotajlo D. & Evans O. (2023) - Taken out of context: On measuring situational awareness in ...]]
- [[Black S., Biderman S., Hallahan E., Anthony Q., Gao L., Golding L., He H., Leahy C., Mcdonell K., Phang J., Pieler M., Usvsn Sai Prashanth S., Purohit L., Reynolds J., Tow B., Wang S. & Weinbach (2022) - GPT-NeoX-20B: An open-source autoregressive language model]]

*(34 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Psychological Review
**DOI:** [10.18653/v1/N18-2072](https://doi.org/10.18653/v1/N18-2072)
**arXiv:** [2309.14316](https://arxiv.org/abs/2309.14316)
**PDF:** [[arxiv_2309.14316.pdf]]

## Abstract

Large language models (LLMs) can store a vast amount of world knowledge, often extractable via question-answering (e.g., "What is Abraham Lincoln's birthday?"). However, do they answer such questions based on exposure to similar questions during training (i.e., cheating), or by genuinely learning to extract knowledge from sources like Wikipedia?

In this paper, we investigate this issue using a controlled biography dataset. We find a strong correlation between the model's ability to extract knowledge and various diversity measures of the training data. Essentially, for knowledge to be reliably extracted, it must be sufficiently augmented (e.g., through paraphrasing, sentence shuffling, translations) during pretraining. Without such augmentation, knowledge may be memorized but not extractable, leading to 0% accuracy, regardless of subsequent instruction fine-tuning.

To understand why this occurs, we employ (nearly) linear probing to demonstrate a strong connection between the observed correlation and how the model internally encodes knowledgewhether it is linearly encoded in the hidden embeddings of entity names or distributed across other token embeddings in the training text.

This paper provides several key recommendations for LLM pretraining in the industry: (1) rewrite the pretraining data -using small, auxiliary models -to provide knowledge augmentation, and (2) incorporate more instruction-finetuning data into the pretraining stage before it becomes too late.

## Full Citation List

1. Kenny B. (2033). The person attended Queens College, City University of New York for education. The person pursued a degree in Political Science there. The person originated from Augusta, GA. The person worked in Menomonee Falls, WI for Kohl's. The person was born on March 25.
2. She graduated from Haverford College with a degree in Management. P &G recruited her as an Assistant Brand Manager in 2000. She held various leadership positions in brand management, marketing, and sales across different business units and categories. She was named Vice President of P &G Global Business Services in 2019 He hails from Augusta, Georgia and was born on March 25 Nicole Kevin Pratt is an American business executive. She is currently the Vice President of P &G Global Business Services at Procter & Gamble Baltimore, Maryland; Menomonee Falls, Wisconsin; Brooklyn, New York; New York City, NY; Northbrook, IL January 25. 1977. 2033. January 7, 2098 Colorado State University Johnathan Charles Wade is a successful insurance agent who works for Allstate. where he majored in Sociology. He currently resides in
3. Allen Z. & Li Y. (2023). Physics of Language Models: Part 1, Learning Hierarchical Language Structures.
4. Allen Z. & Li Y. (2023). Physics of Language Models: Part 3.2, Knowledge Manipulation.
5. Allen Z. & Li Y. (2024). Physics of Language Models: Part 3.3, Knowledge Capacity Scaling Laws.
6. John R Anderson R. & Milson (1989). Human memory: An adaptive perspective.
7. Aspillaga C., Mendoza M. & Soto A. (2021). Inspecting the concept knowledge graph encoded by modern language models.
8. Baddeley A. D. (1997). Human memory: Theory and practice.
9. Berglund L., Stickland A. C., Balesni M. et al. (2023). Taken out of context: On measuring situational awareness in llms.
10. Black S., Biderman S., Hallahan E. et al. (2022). GPT-NeoX-20B: An open-source autoregressive language model.
11. Cai H., Chen H., Song Y. et al. (2020). Data manipulation: Towards effective instance learning for neural dialogue generation via learning to augment and reweight.
12. Choi B., Lee Y., Kyung Y. et al. (2022). Albert with knowledge graph encoder utilizing semantic similarity for commonsense question answering.
13. Conneau A., Kruszewski G., Lample G. et al. (2018). What you can cram into a single vector: Probing sentence embeddings for linguistic properties.
14. IMFergus Janine MCraik Jennings Human memory 1992
15. Dai D., Dong L., Hao Y. et al. (2021). Knowledge neurons in pretrained transformers.
16. Eldan R. & Li Y. (2023). Tinystories: How small can language models be and still speak coherent english.
17. Geva M., Schuster R., Berant J. et al. (2020). Transformer feed-forward layers are keyvalue memories.
18. He P., Liu X., Gao J. et al. (2020). Deberta: Decoding-enhanced bert with disentangled attention.
19. Hernandez E., Li B. Z. & Andreas J. (2023). Measuring and manipulating knowledge representations in language models.
20. Edward J., Hu P., Wallis Z. et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models.
21. Jiang Z., Sun Z., Shi W. et al. (2024). Instruction-tuned language models are better knowledge learners.
22. Devlin J., Chang M. & Kristina L. (2019). Bert: Pre-training of deep bidirectional transformers for language understanding.
23. Kobayashi S. (2018). Contextual augmentation: Data augmentation by words with paradigmatic relations. DOI: 10.18653/v1/N18-2072
24. Lewis P., Perez E., Piktus A. et al. (2020). Retrieval-augmented generation for knowledge-intensive nlp tasks.
25. Li B., Nye M. & Andreas J. (2021). Implicit representations of meaning in neural language models.
26. Liu X., Wang Y., Ji J. et al. (2020). The microsoft toolkit of multi-task deep neural networks for natural language understanding.
27. Liu Y., Ott M., Goyal N. et al. (2019). Roberta: A robustly optimized bert pretraining approach.
28. Meng K., Bau D., Andonian A. et al. (2022). Locating and editing factual associations in gpt.
29. Naseem T., Ravishankar S., Mihindukulasooriya N. et al. (2021). A semantics-aware transformer model of relation linking for knowledge base question answering.
30. Omar R., Mangukiya O., Kalnis P. et al. (2023). Chatgpt versus traditional question answering for knowledge graphs: Current status and future directions towards knowledge graph chatbots.
31. Peng H., Wang X., Hu S. et al. (2022). Copen: Probing conceptual knowledge in pre-trained language models.
32. Petroni F., Rocktäschel T., Lewis P. et al. (2019). Language models as knowledge bases? arXiv preprint.
33. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
34. Richardson K. & Sabharwal A. (2020). What does my QA model know? devising controlled probes using expert knowledge. DOI: 10.1162/tacla00331
35. Singhal K., Azizi S., Tu T. et al. (2022). Large language models encode clinical knowledge.
36. Su J., Lu Y., Pan S. et al. (2021). Roformer: Enhanced transformer with rotary position embedding.
37. Sun K., Yifan E., Xu H. et al. (2023). Head-to-tail: How knowledgeable are large language models (llm)? aka will llms replace knowledge graphs? arXiv preprint.
38. Sushil M., Suster S. & Daelemans W. (2021). Are we there yet? exploring clinical domain knowledge of BERT models. DOI: 10.18653/v1/2021.bionlp-1.5
39. Touvron H., Lavril T., Izacard G. et al. (2023). Open and efficient foundation language models.
40. Tian Ye Zicheng Xu Yuanzhi Li Zeyuan Allen-Zhu Physics of Language Models: Part 2.1, Grade-School Math and the Hidden Reasoning Process arXiv preprint arXiv:xxxx.xxxxx, 2024. to appear
41. Tian Ye Zicheng Xu Yuanzhi Li Zeyuan Allen-Zhu Physics of Language Models: Part 2.2, How to Learn From Mistakes on Grade-School Math Problems arXiv preprint arXiv:xxxx.xxxxx, 2024. to appear
42. Zhou C., Liu P., Xu P. et al. (2023). Less is more for alignment.
43. Zhu Y., Kiros R., Zemel R. et al. (2015). Aligning books and movies: Towards story-like visual explanations by watching movies and reading books.
44. Zlotnik G. & Vansintjan A. (2019). Memory: An extended definition. DOI: 10.3389/fpsyg.2019.02523
