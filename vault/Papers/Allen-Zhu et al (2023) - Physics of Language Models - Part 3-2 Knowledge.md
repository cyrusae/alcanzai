---
title: "Physics of Language Models: Part 3.2, Knowledge Manipulation"
authors: ["Allen-Zhu, Zeyuan", "Li, Yuanzhi", "Xiao, Lin", "Zhou, Chunting", "Liu, Xiaodong", "Zhou, Zhijie", "Ahmed, Nabib", "Anantharaman, Giri", "Bertoncini, Lucca", "Estela, Henry", "Hu, Liao", "Ho, Caleb", "Johnson, Wil", "Kokolis, Apostolos", "Sengupta, Shubho", "Allen, Zeyuan", "Li, Yuanzhi", "Black, Sid", "Biderman, Stella", "Hallahan, Eric", "Anthony, Quentin", "Gao, Leo", "Golding, Laurence", "He, Horace", "Leahy, Connor", "Mcdonell, Kyle", "Phang, Jason", "Pieler, Michael", "Usvsn Sai Prashanth, Shivanshu", "Purohit, Laria", "Reynolds, Jonathan", "Tow, Ben", "Wang, Samuel", "Weinbach", "Cai, Deng", "Wang, Yan", "Liu, Lemao", "Shi, Shuming", "Geva, Mor", "Khashabi, Daniel", "Segal, Elad", "Khot, Tushar", "Roth, Dan", "Berant, Jonathan", "Edward, J", "Hu, Phillip", "Wallis, Zeyuan", "Allen-Zhu, Yuanzhi", "Li, Shean", "Wang, Lu", "Wang, Weizhu", "Chen", "Lewis, Patrick", "Perez, Ethan", "Piktus, Aleksandra", "Petroni, Fabio", "Karpukhin, Vladimir", "Goyal, Naman", "Küttler, Heinrich", "Lewis, Mike", "Yih, Wen-Tau", "Rocktäschel, Tim", "Riedel, Sebastian", "Kiela, Douwe", "Naseem, Tahira", "Ravishankar, Srinivas", "Mihindukulasooriya, Nandana", "Abdelaziz, Ibrahim", "Lee, Young-Suk", "Kapanipathi, Pavan", "Roukos, Salim", "Gliozzo, Alfio", "Gray, Alexander", "Nguyen, Anh", "Karampatziakis, Nikos", "Chen, Weizhu", "Radford, Alec", "Wu, Jeffrey", "Child, Rewon", "Luan, David", "Amodei, Dario", "Sutskever, Ilya", "Richardson, Kyle", "Sabharwal, Ashish", "Siriwardhana, Shamane", "Weerasekera, Rivindu", "Wen, Elliott", "Kaluarachchi, Tharindu", "Wei, Jason", "Wang, Xuezhi", "Schuurmans, Dale", "Bosma, Maarten", "Xia, Fei", "Chi, Ed", "Quoc, V", "Le, Denny", "Zhou"]
year: 2023
venue: "Transactions of the Association for Computational Linguistics"
doi: "10.1162/tacla00331"
arxiv: "2309.14402"
type: "paper"
status: "unread"
added: "2026-01-09"
tags:
  - knowledge-retrieval
  - knowledge-classification
  - knowledge-comparison
  - knowledge-inverse-search
  - chain-of-thought
  - autoregressive-language-models
  - synthetic-pretraining-data
  - out-of-distribution-generalization
  - knowledge-manipulation
  - instruction-finetuning
  - artificial-intelligence
  - computational-linguistics
---
# Physics of Language Models: Part 3.2, Knowledge Manipulation

**Allen-Zhu, Zeyuan et al.** â€¢ 2023

> [!quote] Memorable Quote
> "They cannot efficiently manipulate knowledge from pre-training data, even when such knowledge is perfectly stored in the models, despite adequate training and sufficient model size."

## Quick Refresh

This paper investigates how well language models can manipulate factual knowledge they've learned during pretraining, using carefully controlled synthetic experiments with biographical data. The researchers found that while models excel at simple knowledge retrieval (e.g., "What is person X's birthdate?"), they struggle dramatically with basic classification (e.g., "Was person X born in an even month?"), comparison (e.g., "Is person X's university ranked higher than person Y's?"), and inverse search (e.g., "Who was born on October 2, 1996?") tasks unless Chain-of-Thought (CoT) prompting is used during both training and inference. The paper demonstrates these limitations apply to modern large models like GPT-4 and Llama-3, suggesting they are fundamental constraints of the autoregressive language model architecture rather than fixable through scaling alone.

## Why You Cared

This paper matters because it reveals a critical gap between what language models appear to know and what they can actually do with that knowledge—a distinction that's hard to measure with real-world data where contamination and training data diversity confound results. The synthetic experimental setup elegantly isolates the knowledge manipulation problem and provides concrete evidence that even state-of-the-art models fail at tasks humans find trivial, offering both a rigorous testbed for future research and practical insight into why language models need explicit reasoning steps (CoTs) for seemingly simple inferences. If you're building systems that rely on LLMs to reason about stored facts or creating better architectures, this paper shows you where the current bottlenecks truly lie.

## Key Concepts

`#knowledge-retrieval` `#knowledge-classification` `#knowledge-comparison` `#knowledge-inverse-search` `#chain-of-thought` `#autoregressive-language-models` `#synthetic-pretraining-data` `#out-of-distribution-generalization` `#knowledge-manipulation` `#instruction-finetuning` `#artificial-intelligence` `#computational-linguistics`

## Cites (Key Papers)

- [[Allen Z. & Li Y. (2023) - Physics of Language Models: Part 1, Learning Hierarchical La...]]
- [[Allen Z. & Li Y. (2024) - Physics of Language Models: Part 3.1, Knowledge Storage and ...]]
- [[Allen Z. & Li Y. (2024) - Physics of Language Models: Part 3.3, Knowledge Capacity Sca...]]
- [[Berglund L., Tong M., Kaufmann M., Balesni M., Stickland A. C., Korbak T. & Evans O. (2023) - The Reversal Curse: LLMs trained on "A is B" fail to learn]]
- [[Black S., Biderman S., Hallahan E., Anthony Q., Gao L., Golding L., He H., Leahy C., Mcdonell K., Phang J., Pieler M., Usvsn Sai Prashanth S., Purohit L., Reynolds J., Tow B., Wang S. & Weinbach (2022) - GPT-NeoX-20B: An open-source autoregressive language model]]
- [[Cai D., Wang Y., Liu L. & Shi S. (2022) - Recent advances in retrieval-augmented text generation]]
- [[Geva M., Khashabi D., Segal E., Khot T., Roth D. & Berant J. (2021) - Did aristotle use a laptop? a question answering benchmark w...]]
- [[Gloeckle F., Badr Y., Idrissi B., Rozière D., Lopez-Paz G. & Synnaeve (2024) - Better & faster large language models via multi-token predic...]]
- [[Golovneva O., Allen-Zhu Z., Weston J. & Sukhbaatar S. (2024) - Reverse training to nurse the reversal curse]]
- [[Guo Q., Wang R., Guo J., Tan X., Bian J. & Yang Y. (2024) - Mitigating reversal curse via semantic-aware permutation tra...]]

*(29 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Transactions of the Association for Computational Linguistics
**DOI:** [10.1162/tacla00331](https://doi.org/10.1162/tacla00331)
**arXiv:** [2309.14402](https://arxiv.org/abs/2309.14402)
**PDF:** [[arxiv_2309.14402.pdf]]

## Abstract

Language models can store vast factual knowledge, yet their ability to flexibly use this knowledge for downstream tasks (e.g., via instruction finetuning) remains questionable. This paper investigates four fundamental knowledge manipulation tasks: retrieval (e.g., "What is person A's attribute X?"), classification (e.g., "Is A's attribute X even or odd?"), comparison (e.g., "Is A greater than B in attribute X?"), and inverse search (e.g., "Which person's attribute X equals T?").

We show that language models excel in knowledge retrieval but struggle even in the simplest classification or comparison tasks unless Chain of Thoughts (CoTs) are employed during both training and inference. Moreover, their performance in inverse knowledge search is virtually 0%, regardless of the prompts. Our primary contribution is a controlled, synthetic experiment that confirms these weaknesses are inherent to language models: they cannot efficiently manipulate knowledge from pre-training data, even when such knowledge is perfectly stored in the models, despite adequate training and sufficient model size. Our findings also apply to modern pretrained language models such as GPT-4, thus giving rise to many Turing tests to distinguish Humans from contemporary AIs.

## Full Citation List

1. Allen Z. & Li Y. (2023). Physics of Language Models: Part 1, Learning Hierarchical Language Structures.
2. Allen Z. & Li Y. (2024). Physics of Language Models: Part 3.1, Knowledge Storage and Extraction.
3. Allen Z. & Li Y. (2024). Physics of Language Models: Part 3.3, Knowledge Capacity Scaling Laws.
4. Berglund L., Tong M., Kaufmann M. et al. (2023). The Reversal Curse: LLMs trained on "A is B" fail to learn.
5. Black S., Biderman S., Hallahan E. et al. (2022). GPT-NeoX-20B: An open-source autoregressive language model.
6. Cai D., Wang Y., Liu L. et al. (2022). Recent advances in retrieval-augmented text generation.
7. Geva M., Khashabi D., Segal E. et al. (2021). Did aristotle use a laptop? a question answering benchmark with implicit reasoning strategies. Transactions of the Association for Computational Linguistics, Vol. 9, pp. 346-361.
8. Gloeckle F., Badr Y., Idrissi B. et al. (2024). Better & faster large language models via multi-token prediction.
9. Golovneva O., Allen-Zhu Z., Weston J. et al. (2024). Reverse training to nurse the reversal curse.
10. Guo Q., Wang R., Guo J. et al. (2024). Mitigating reversal curse via semantic-aware permutation training.
11. Hernandez E., Li B. Z. & Andreas J. (2023). Measuring and manipulating knowledge representations in language models.
12. Edward J., Hu P., Wallis Z. et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models.
13. Albert Q Jiang A., Sablayrolles A., Mensch C. et al. (2023). Mistral 7b.
14. Jiang Z., Xu F. F., Gao L. et al. (2023). Active retrieval augmented generation.
15. Komeili M., Shuster K. & Weston J. (2021). Internet-augmented dialogue generation.
16. Lebret R., Grangier D. & Auli M. (2016). Generating text from structured data with application to the biography domain.
17. Lewis P., Perez E., Piktus A. et al. (2020). Retrieval-augmented generation for knowledge-intensive nlp tasks.
18. Liu S., Chen Y., Xie X. et al. (2020). Retrieval-augmented generation for code summarization via hybrid gnn.
19. Mao Y., He P., Liu X. et al. (2020). Generation-augmented retrieval for open-domain question answering.
20. Naseem T., Ravishankar S., Mihindukulasooriya N. et al. (2021). A semantics-aware transformer model of relation linking for knowledge base question answering.
21. Nguyen A., Karampatziakis N. & Chen W. (2024). Meet in the middle: A new pre-training paradigm. Advances in Neural Information Processing Systems, Vol. 36.
22. Omar R., Mangukiya O., Kalnis P. et al. (2023). Chatgpt versus traditional question answering for knowledge graphs: Current status and future directions towards knowledge graph chatbots.
23. Open AI. Gpt-4 technical report 2023
24. Md Rizwan Parvez, Wasi U., Ahmad S. et al. (2021). Retrieval augmented code generation and summarization.
25. Peng H., Wang X., Hu S. et al. (2022). Copen: Probing conceptual knowledge in pre-trained language models.
26. Petroni F., Rocktäschel T., Lewis P. et al. (2019). Language models as knowledge bases? arXiv preprint.
27. Pfau J., Merrill W. & Samuel R Bowman (2024). Let's think dot by dot: Hidden computation in transformer language models.
28. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners. OpenAI blog, Vol. 1(8), pp. 9.
29. Ram O., Levine Y., Dalmedigos I. et al. (2023). -context retrieval-augmented language models.
30. Richardson K. & Sabharwal A. (2020). What does my QA model know? devising controlled probes using expert knowledge. Transactions of the Association for Computational Linguistics, Vol. 8, pp. 572-588. DOI: 10.1162/tacla00331
31. Singhal K., Azizi S., Tu T. et al. (2022). Large language models encode clinical knowledge.
32. Siriwardhana S., Weerasekera R., Wen E. et al. (2023). Improving the domain adaptation of retrieval augmented generation (rag) models for open domain question answering. Transactions of the Association for Computational Linguistics, Vol. 11, pp. 1-17.
33. Su J., Lu Y., Pan S. et al. (2021). Roformer: Enhanced transformer with rotary position embedding.
34. Sun K., Yifan E., Xu H. et al. (2023). Head-to-tail: How knowledgeable are large language models (llm)? aka will llms replace knowledge graphs? arXiv preprint.
35. Touvron H., Lavril T., Izacard G. et al. (2023). Open and efficient foundation language models.
36. Wei J., Wang X., Schuurmans D. et al. (2022). Chain-of-thought prompting elicits reasoning in large language models.
37. Tian Ye Zicheng Xu Yuanzhi Li Zeyuan Allen-Zhu Physics of Language Models: Part 2.1, Grade-School Math and the Hidden Reasoning Process arXiv preprint arXiv:xxxx.xxxxx, 2024. to appear
38. Tian Ye Zicheng Xu Yuanzhi Li Zeyuan Allen-Zhu Physics of Language Models: Part 2.2, How to Learn From Mistakes on Grade-School Math Problems arXiv preprint arXiv:xxxx.xxxxx, 2024. to appear
39. Zhou C., Liu P., Xu P. et al. (2023). Less is more for alignment.
