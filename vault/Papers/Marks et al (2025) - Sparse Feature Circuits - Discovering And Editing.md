---
title: "Sparse Feature Circuits: Discovering And Editing Interpretable Causal Graphs In Language Models"
authors: ["Marks, Samuel", "Rager, Can", "Michaud Mit, Eric J", "Belinkov, Yonatan", "Bau, David", "Mueller, Aaron", "Data, Classification", "Belinkov, Yonatan", "Belrose, Nora", "Schneider-Joseph, David", "Ravfogel, Shauli", "Cotterell, Ryan", "Raff, Edward", "Biderman, Stella", "Biderman, Stella", "Schoelkopf, Hailey", "Anthony, Quentin Gregory", "Bradley, Herbie", "Kyle, O'", "Brien, Eric", "Hallahan, Mohammad", "Aflah Khan, Shivanshu", "Purohit", "Usvsn Sai Prashanth, Edward", "Raff", "Burgess, Christopher P", "Higgins, Irina", "Pal, Arka", "Matthey, Loic", "Watters, Nick", "Desjardins, Guillaume", "Lerchner, Alexander", "Burns, Collin", "Izmailov, Pavel", "Kirchner, Jan Hendrik", "Baker, Bowen", "Gao, Leo", "Aschenbrenner, Leopold", "Chen, Yining", "Ecoffet, Adrien", "Joglekar, Manas", "Leike, Jan", "Sutskever, Ilya", "Wu, Jeff", "Casper, Stephen", "Davies, Xander", "Shi, Claudia", "Gilbert, Thomas Krendl", "Scheurer, Jérémy", "Rando, Javier", "Freedman, Rachel", "Korbak, Tomasz", "Lindner, David", "Freire, Pedro", "Wang, Tony Tong", "Marks, Samuel", "Segerie, Charbel-Raphael", "Carroll, Micah", "Peng, Andi", "Christoffersen, Phillip", "Damani, Mehul", "Slocum, Stewart", "Anwar, Usman", "Siththaranjan, Anand", "Nadeau, Max", "Michaud, Eric J", "Pfau, Jacob", "Krasheninnikov, Dmitrii", "Chen, Xin", "Langosco, Lauro", "Hase, Peter", "Biyik, Erdem", "Dragan, Anca", "Krueger, David", "Sadigh, Dorsa", "Hadfield-Menell, Dylan", "Chen, Angelica", "Shwartz-Ziv, Ravid", "Cho, Kyunghyun", "Leavitt, Matthew L", "Saphra, Naomi", "Chen, Xi", "Duan, Yan", "Houthooft, Rein", "Schulman, John", "Sutskever, Ilya", "Abbeel, Pieter", "Christiano, Paul", "Leike, Jan", "Brown, Tom B", "Martic, Miljan", "Legg, Shane", "Amodei, Dario", "Conmy, Arthur", "Mavor-Parker, Augustine N", "Lynch, Aengus", "Heimersheim, Stefan", "Garriga-Alonso, Adrià", "Creager, Elliot", "Jacobsen, Joern-Henrik", "Zemel, Richard", "Cunningham, Hoagy", "Ewart, Aidan", "Riggs, Logan", "Huben, Robert", "Sharkey, Lee", "De-Arteaga, Maria", "Romanov, Alexey", "Wallach, Hanna", "Chayes, Jennifer", "Borgs, Christian", "Chouldechova, Alexandra", "Geyik, Sahin", "Kenthapadi, Krishnaram", "Tauman, Adam", "Desjardins, Guillaume", "Courville, Aaron", "Bengio, Yoshua", "Finlayson, Matthew", "Mueller, Aaron", "Gehrmann, Sebastian", "Shieber, Stuart", "Linzen, Tal", "Belinkov, Yonatan", "Gandelsman, Yossi", "Efros, Alexei A", "Steinhardt, Jacob", "Gao, Leo", "Biderman, Stella", "Black, Sid", "Golding, Laurence", "Hoppe, Travis", "Foster, Charles", "Phang, Jason", "He, Horace", "Thite, Anish", "Nabeshima, Noa", "Presser, Shawn", "Leahy, Connor", "Gao, Leo", "Dupré La Tour, Tom", "Tillman, Henk", "Goh, Gabriel", "Troll, Rajan", "Radford, Alec", "Sutskever, Ilya", "Leike, Jan", "Wu, Jeffrey", "Geiger, Atticus", "Lu, Hanson", "Icard, Thomas", "Potts, Christopher", "Geiger, Atticus", "Wu, Zhengxuan", "Lu, Hanson", "Rozner, Josh", "Kreiss, Elisa", "Icard, Thomas", "Goodman, Noah", "Potts, Christopher", "Geiger, Atticus", "Potts, Chris", "Icard, Thomas", "Geva, Mor", "Bastings, Jasmijn", "Filippova, Katja", "Globerson, Amir", "Gould, Rhys", "Ong, Euan", "Ogden, George", "Conmy, Arthur", "Hanna, Michael", "Liu, Ollie", "Variengien, Alexandre", "Hanna, Michael", "Pezzelle, Sandro", "Belinkov, Yonatan", "Hase, Peter", "Bansal, Mohit", "Clark, Peter", "Wiegreffe, Sarah", "He, T", "Li, Z", "Gong, Y", "Yao, Y", "Nie, X", "Yin, Y", "Higgins, Irina", "Matthey, Loic", "Pal, Arka", "Burgess, Christopher", "Glorot, Xavier", "Botvinick, Matthew", "Mohamed, Shakir", "Lerchner, Alexander", "Badr, Youbi", "Idrissi, Martin", "Arjovsky, Mohammad", "Pezeshki, David", "Lopez-Paz", "Iskander, Shadi", "Radinsky, Kira", "Belinkov, Yonatan", "Iskander, Shadi", "Radinsky, Kira", "Belinkov, Yonatan", "Kim, Been", "Wattenberg, Martin", "Gilmer, Justin", "Cai, Carrie", "Wexler, James", "Viegas, Fernanda", "Kim, Hyunjik", "Mnih, Andriy", "Kirichenko, Polina", "Izmailov, Pavel", "Gordon, Andrew", "Kramár, János", "Lieberum, Tom", "Shah, Rohin", "Nanda, Neel", "Lin, Johnny", "Bloom, Joseph", "Liu, Evan Z", "Haghgoo, Behzad", "Chen, Annie S", "Raghunathan, Aditi", "Wei Koh, Pang", "Sagawa, Shiori", "Liang, Percy", "Finn, Chelsea", "Loshchilov, Ilya", "Hutter, Frank", "Makhzani, Alireza", "Frey, Brendan J", "Meng, Kevin", "Bau, David", "Andonian, Alex", "Belinkov, Yonatan", "Michaud, Eric J", "Liu, Ziming", "Girit, Uzay", "Tegmark, Max", "Mueller, Aaron", "Brinkmann, Jannik", "Li, Millicent", "Marks, Samuel", "Pal, Koyena", "Prakash, Nikhil", "Rager, Can", "Sankaranarayanan, Aruna", "Arnab, Sen", "Sharma, Jiuding", "Sun, Eric", "Todd, David", "Bau, Yonatan", "Belinkov", "Nam, Junhyun", "Cha, Hyuntak", "Ahn, Sungsoo", "Lee, Jaeho", "Shin, Jinwoo", "Nanda, Neel", "Nanda, Neel", "Rajamanoharan, Senthooran", "Kramár, János", "Shah, Rohin", "Ngo, Richard", "Chan, Lawrence", "Mindermann, Sören", "Oikarinen, Tuomas", "Das, Subhro", "Lam, M", "Nguyen, Tsui-Wei", "Weng", "Oren, Yonatan", "Sagawa, Shiori", "Tatsunori, B", "Hashimoto, Percy", "Liang", "Orgad, Hadas", "Belinkov, Yonatan", "Pearl, Judea", "Pedregosa, F", "Varoquaux, G", "Gramfort, A", "Michel, V", "Thirion, B", "Grisel, O", "Blondel, M", "Prettenhofer, P", "Weiss, R", "Dubourg, V", "Vanderplas, J", "Passos, A", "Cournapeau, D", "Brucher, M", "Perrot, M", "Duchesnay, E", "Peebles, William", "Peebles, John", "Zhu, Jun-Yan", "Efros, Alexei A", "Torralba, Antonio", "Prakash, Nikhil", "Shaham, Tamar Rott", "Haklay, Tal", "Belinkov, Yonatan", "Bau, David", "Rajamanoharan, Senthooran", "Conmy, Arthur", "Smith, Lewis", "Lieberum, Tom", "Varma, Vikrant", "Kramár, János", "Shah, Rohin", "Nanda, Neel", "Rajamanoharan, Senthooran", "Lieberum, Tom", "Sonnerat, Nicolas", "Conmy, Arthur", "Varma, Vikrant", "Kramár, János", "Nanda, Neel", "Ravfogel, Shauli", "Elazar, Yanai", "Gonen, Hila", "Twiton, Michael", "Goldberg, Yoav", "Ravfogel, Shauli", "Twiton, Michael", "Goldberg, Yoav", "Cotterell, Ryan D", "Ravfogel, Shauli", "Vargas, Francisco", "Goldberg, Yoav", "Cotterell, Ryan", "Robins, James M", "Greenland, Sander", "Sagawa, Shiori", "Wei Koh, Pang", "Tatsunori, B", "Hashimoto, Percy", "Liang", "Schmidhuber, Jürgen", "Schneider, Johannes", "Vlachos, Michalis", "Nimit, Sharad", "Sohoni, Maziar", "Sanjabi, Nicolas", "Ballas, Aditya", "Grover, Shaoliang", "Nie, Hamed", "Firooz, Christopher", "Re", "Sundararajan, Mukund", "Taly, Ankur", "Yan, Qiqi", "Syed, Aaquib", "Rager, Can", "Conmy, Arthur", "Todd, Eric", "Li, Millicent L", "Sharma, Sen", "Mueller, Aaron", "Wallace, Byron C", "Bau, David", "Prasetya Ajie Utama, Nafise", "Sadat Moosavi, Iryna", "Gurevych", "Vig, Jesse", "Gehrmann, Sebastian", "Belinkov, Yonatan", "Qian, Sharon", "Nevo, Daniel", "Singer, Yaron", "Shieber, Stuart", "Ro, Kevin", "Variengien, Alexandre", "Conmy, Arthur", "Shlegeris, Buck", "Steinhardt, Jacob", "Wang, Tianlu", "Victoria Lin, Xi", "Fatema Rajani, Nazneen", "Mccann, Bryan", "Ordonez, Vicente", "Xiong, Caiming", "Yaghoobzadeh, Yadollah", "Mehri, Soroush", "Tachet Des Combes, Remi", "Hazen, T J", "Sordoni, Alessandro", "Yan, An", "Wang, Yu", "Zhong, Yiwu", "He, Zexue", "Karypis, Petros", "Wang, Zihan", "Dong, Chengyu", "Gentili, Amilcare", "Hsu, Chun-Nan", "Shang, Jingbo", "Mcauley, Julian", "Yu, Qinan", "Merullo, Jack", "Pavlick, Ellie", "Zech, John R", "Badgeley, Marcus A", "Liu, Manway", "Costa, Anthony B", "Titano, Joseph J", "Karl Oermann, Eric", "Zhang, Jingzhao", "Menon, Aditya Krishna", "Veit, Andreas", "Bhojanapalli, Srinadh", "Kumar, Sanjiv", "Sra, Suvrit", "Zhang, Michael", "Nimit, S", "Sohoni", "Hongyang R Zhang, Chelsea", "Finn, Christopher", "Re", "Zou, Andy", "Phan, Long", "Chen, Sarah", "Campbell, James", "Guo, Phillip", "Ren, Richard", "Pan, Alexander", "Yin, Xuwang", "Mazeika, Mantas", "Dombrowski, Ann-Kathrin"]
year: 2025
venue: "Computational Linguistics"
doi: "10.1145/3287560.3287572"
arxiv: "2403.19647"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - sparse-autoencoders
  - feature-circuits
  - mechanistic-interpretability
  - causal-intervention
  - attribution-patching
  - integrated-gradients
  - bias-mitigation
  - model-transparency
  - language-models
  - neural-networks
---

# Sparse Feature Circuits: Discovering And Editing Interpretable Causal Graphs In Language Models

**Marks, Samuel et al.** • 2025

> [!quote] Memorable Quote
> "Circuits identified in prior work consist of polysemantic and difficult-to-interpret units like attention heads or neurons, rendering them unsuitable for many downstream applications."

## Quick Refresh

This paper introduces a scalable method for discovering sparse feature circuits—causally implicated subnetworks of human-interpretable features that explain language model behaviors. Rather than identifying coarse-grained components like attention heads or neurons (which are often polysemanticand hard to interpret), the authors use sparse autoencoders (SAEs) to extract fine-grained features, then employ linear approximations of causal effects (attribution patching and integrated gradients) to efficiently identify which features are causally important for specific model behaviors. They demonstrate the approach on subject-verb agreement tasks, show how it enables bias mitigation without disambiguating labels (via SHIFT), and scale it to discover thousands of circuits for automatically discovered model behaviors.

## Why You Cared

You care about mechanistic interpretability—understanding how language models actually implement their behaviors rather than just predicting their outputs. This paper addresses a real bottleneck: previous circuit analysis relied on coarse-grained units (hard to interpret) or researcher-specified hypotheses (not scalable). Sparse feature circuits solve this by giving you interpretable, causal building blocks that actually enable downstream applications, like debiasing classifiers without extra labeled data. You can apply this method to understand any surprising model behavior by discovering its underlying mechanisms.

## Key Concepts

`#sparse-autoencoders` `#feature-circuits` `#mechanistic-interpretability` `#causal-intervention` `#attribution-patching` `#integrated-gradients` `#bias-mitigation` `#model-transparency` `#language-models` `#neural-networks`

## Cites (Key Papers)

- [[Belinkov Y. (2022) - Probing classifiers: Promises, shortcomings, and advances]]
- [[Belrose N., Schneider-Joseph D., Ravfogel S., Cotterell R., Raff E. & Biderman S. (2023) - LEACE: Perfect linear concept erasure in closed form]]
- [[Biderman S., Schoelkopf H., Anthony Q. G., Bradley H., Kyle O., Brien E., Hallahan M., Aflah Khan S., Purohit, Usvsn Sai Prashanth E. & Raff (2023) - Pythia: A suite for analyzing large language models across t...]]
- [[Bricken T., Templeton A., Batson J., Chen B., Jermyn A., Conerly T., Turner N., Anil C., Denison C., Askell A., Lasenby R., Wu Y., Kravec S., Schiefer N., Maxwell T., Joseph N., Hatfield-Dodds Z., Tamkin A., Nguyen K., Mclean B., Burke J. E., Hume T., Carter S., Henighan T. & Olah C. (2023) - Towards monosemanticity: Decomposing language models with di...]]
- [[Burgess C. P., Higgins I., Pal A., Matthey L., Watters N., Desjardins G. & Lerchner A. (2017) - Understanding disentangling in β-VAE]]
- [[Burns C., Izmailov P., Kirchner J. H., Baker B., Gao L., Aschenbrenner L., Chen Y., Ecoffet A., Joglekar M., Leike J., Sutskever I. & Wu J. (2023) - Weak-to-strong generalization: Eliciting strong capabilities...]]
- [[Casper S., Davies X., Shi C., Gilbert T. K., Scheurer J., Rando J., Freedman R., Korbak T., Lindner D., Freire P., Wang T. T., Marks S., Segerie C., Carroll M., Peng A., Christoffersen P., Damani M., Slocum S., Anwar U., Siththaranjan A., Nadeau M., Michaud E. J., Pfau J., Krasheninnikov D., Chen X., Langosco L., Hase P., Biyik E., Dragan A., Krueger D., Sadigh D. & Hadfield-Menell D. (2023) - Open problems and fundamental limitations of reinforcement l...]]
- [[Chen A., Shwartz-Ziv R., Cho K., Leavitt M. L. & Saphra N. (2024) - Sudden drops in the loss: Syntax acquisition, phase transiti...]]
- [[Qi T., Li X., Grosse R. & Duvenaud D. (2018) - Isolating sources of disentanglement in variational autoenco...]]
- [[Chen X., Duan Y., Houthooft R., Schulman J., Sutskever I. & Abbeel P. (2016) - Infogan: interpretable representation learning by informatio...]]

*(78 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Computational Linguistics
**DOI:** [10.1145/3287560.3287572](https://doi.org/10.1145/3287560.3287572)
**arXiv:** [2403.19647](https://arxiv.org/abs/2403.19647)
**PDF:** [[arxiv_2403.19647.pdf]]

## Abstract

We introduce methods for discovering and applying sparse feature circuits. These are causally implicated subnetworks of human-interpretable features for explaining language model behaviors. Circuits identified in prior work consist of polysemantic and difficult-to-interpret units like attention heads or neurons, rendering them unsuitable for many downstream applications. In contrast, sparse feature circuits enable detailed understanding of unanticipated mechanisms in neural networks. Because they are based on fine-grained units, sparse feature circuits are useful for downstream tasks: We introduce SHIFT, where we improve the generalization of a classifier by ablating features that a human judges to be taskirrelevant. Finally, we demonstrate an entirely unsupervised and scalable interpretability pipeline by discovering thousands of sparse feature circuits for automatically discovered model behaviors.

## Source Text

[[Marks et al (2025) - Sparse Feature Circuits - Discovering And Editing - Source]]

## Full Citation List

1. Belinkov Y. (2022). Probing classifiers: Promises, shortcomings, and advances. Computational Linguistics, Vol. 48(1), pp. 207-219.
2. Belrose N., Schneider-Joseph D., Ravfogel S. et al. (2023). LEACE: Perfect linear concept erasure in closed form.
3. Biderman S., Schoelkopf H., Anthony Q. G. et al. (2023). Pythia: A suite for analyzing large language models across training and scaling.
4. Bricken T., Templeton A., Batson J. et al. (2023). Towards monosemanticity: Decomposing language models with dictionary learning, Towards Monosemanticity: Decomposing Language Models With Dictionary Learning.
5. Burgess C. P., Higgins I., Pal A. et al. (2017). Understanding disentangling in β-VAE.
6. Burns C., Izmailov P., Kirchner J. H. et al. (2023). Weak-to-strong generalization: Eliciting strong capabilities with weak supervision, Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision. Computing Research Repository.
7. Casper S., Davies X., Shi C. et al. (2023). Open problems and fundamental limitations of reinforcement learning from human feedback, Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback. Transactions on Machine Learning Research.
8. Chen A., Shwartz-Ziv R., Cho K. et al. (2024). Sudden drops in the loss: Syntax acquisition, phase transitions, and simplicity bias in MLMs.
9. Qi T., Li X., Grosse R. et al. (2018). Isolating sources of disentanglement in variational autoencoders.
10. Chen X., Duan Y., Houthooft R. et al. (2016). Infogan: interpretable representation learning by information maximizing generative adversarial nets.
11. Christiano P., Leike J., Brown T. B. et al. (2023). Deep reinforcement learning from human preferences. Computing Research Repository.
12. Towards automated circuit discovery for mechanistic interpretability Arthur Conmy Augustine NMavor-Parker Aengus Lynch Stefan Heimersheim AdriàGarriga-Alonso Thirtyseventh Conference on Neural Information Processing Systems, 2023, Towards Automated Circuit Discovery for Mechanistic Interpretability
13. Creager E., Jacobsen J. & Zemel R. (2021). Environment inference for invariant learning.
14. Cunningham H., Ewart A., Riggs L. et al. (2024). Sparse autoencoders find highly interpretable features in language models.
15. De-Arteaga M., Romanov A., Wallach H. et al. (2019). Bias in bios: A case study of semantic representation bias in a high-stakes setting. DOI: 10.1145/3287560.3287572
16. Desjardins G., Courville A. & Bengio Y. (2012). Disentangling factors of variation via generative entangling. Computing Research Repository.
17. Elhage N., Hume T., Olsson C. et al. (2022). Toy models of superposition. Transformer Circuits Thread.
18. Finlayson M., Mueller A., Gehrmann S. et al. (2021). Causal analysis of syntactic agreement mechanisms in neural language models.
19. Gandelsman Y., Efros A. A. & Steinhardt J. (2024). Interpreting CLIP's image representation via text-based decomposition. Computing Research Repository.
20. Gao L., Biderman S., Black S. et al. (2020). The Pile: An 800GB dataset of diverse text for language modeling. Computing Research Repository.
21. Gao L., Dupré La Tour T., Tillman H. et al. (2024). Scaling and evaluating sparse autoencoders. Computing Research Repository.
22. Geiger A., Lu H., Icard T. et al. (2021). Causal abstractions of neural networks.
23. Geiger A., Wu Z., Lu H. et al. (2022). Inducing causal structure for interpretable neural networks.
24. Geiger A., Potts C. & Icard T. (2023). Causal abstraction for faithful model interpretation. Computing Research Repository.
25. Geva M., Bastings J., Filippova K. et al. (2023). Dissecting recall of factual associations in auto-regressive language models.
26. Gould R., Ong E., Ogden G. et al. (2023). Successor heads: Recurring, interpretable attention heads in the wild. Computing Research Repository.
27. How does GPT-2 compute greater-than?: Interpreting mathematical abilities in a pre-trained language model Michael Hanna Ollie Liu Alexandre Variengien Thirty-seventh Conference on Neural Information Processing Systems, 2023, How does GPT-2 compute greater-than?: Interpreting mathematical abilities in a pre-trained language model
28. Have faith in faithfulness: Going beyond circuit overlap when finding model mechanisms Michael Hanna Sandro Pezzelle Yonatan Belinkov ICML 2024 Workshop on Mechanistic Interpretability, 2024, Have Faith in Faithfulness: Going Beyond Circuit Overlap When Finding Model Mechanisms
29. Hase P., Bansal M., Clark P. et al. (2024). The unreasonable effectiveness of easy training data for hard tasks.
30. He T., Li Z., Gong Y. et al. (2022). Exploring linear feature disentanglement for neural networks. DOI: 10.1109/ICME52920.2022.9859978
31. beta-VAE: Learning basic visual concepts with a constrained variational framework Irina Higgins Loic Matthey Arka Pal Christopher Burgess Xavier Glorot Matthew Botvinick Shakir Mohamed Alexander Lerchner International Conference on Learning Representations, 2017, beta-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework
32. Badr Y., Idrissi M., Arjovsky M. et al. (2022). Simple data balancing achieves competitive worst-group-accuracy.
33. Iskander S., Radinsky K. & Belinkov Y. (2023). Shielded representations: Protecting sensitive attributes through iterative gradient-based projection.
34. Iskander S., Radinsky K. & Belinkov Y. (2024). Leveraging prototypical representations for mitigating social bias without demographic information. Computing Research Repository.
35. Kim B., Wattenberg M., Gilmer J. et al. (2018). Interpretability beyond feature attribution: Quantitative testing with concept activation vectors (TCAV).
36. Kim H. & Mnih A. (2018). Disentangling by factorising.
37. Diederik P., Kingma J. & Ba (2014). Adam: A method for stochastic optimization, Adam: A Method for Stochastic Optimization.
38. Kirichenko P., Izmailov P. & Gordon A. (2023). Last layer re-training is sufficient for robustness to spurious correlations. Computing Research Repository.
39. Kramár J., Lieberum T., Shah R. et al. (2024). AtP*: An efficient and scalable method for localizing llm behaviour to components. Computing Research Repository.
40. KDavid Lewis Counterfactuals Blackwell 1973 Malden, Mass
41. Lieberum T., Rajamanoharan S., Conmy A. et al. (2024). Gemma scope: Open sparse autoencoders everywhere all at once on gemma 2.
42. Lin J. & Bloom J. (2023). Neuronpedia: Interactive reference and tooling for analyzing neural networks.
43. Liu E. Z., Haghgoo B., Chen A. S. et al. (2021). Just train twice: Improving group robustness without training group information.
44. Loshchilov I. & Hutter F. (2017). Decoupled weight decay regularization.
45. Makhzani A. & Frey B. J. (2013). k-sparse autoencoders, k-Sparse Autoencoders. Computing Research Repository.
46. Meng K., Bau D., Andonian A. et al. (2022). Locating and editing factual associations in GPT. Advances in Neural Information Processing Systems, Vol. 36.
47. The quantization model of neural scaling Eric JMichaud Ziming Liu Uzay Girit Max Tegmark Thirty-seventh Conference on Neural Information Processing Systems, 2023, The Quantization Model of Neural Scaling
48. Mueller A., Brinkmann J., Li M. et al. (2024). The quest for the right mediator: A history, survey, and theoretical grounding of causal interpretability.
49. Nam J., Cha H., Ahn S. et al. (2020). Learning from failure: Training debiased classifier from biased classifier.
50. Nam J., Kim J., Lee J. et al. (2022). Spread spurious attribute: Improving worst-group accuracy with spurious attribute estimation.
51. Nanda N. (2022). Attribution patching: Activation patching at industrial scale.
52. Open source replication & commentary on Anthropic's dictionary learning paper, 2023, Open Source Replication & Commentary on Anthropic's Dictionary Learning Paper Neel Nanda
53. Nanda N., Rajamanoharan S., Kramár J. et al. (2023). Fact finding: Attempting to reverse-engineer factual recall on the neuron level.
54. Ngo R., Chan L. & Mindermann S. (2024). The alignment problem from a deep learning perspective. Computing Research Repository.
55. Label-free concept bottleneck models Tuomas Oikarinen Subhro Das MLam Tsui-Wei Nguyen Weng The Eleventh International Conference on Learning Representations, 2023, Label-free Concept Bottleneck Models
56. Olsson C., Elhage N., Nanda N. et al. (2022). -context learning and induction heads. Transformer Circuits Thread.
57. Oren Y., Sagawa S., Tatsunori B. et al. (2019). Distributionally robust language modeling.
58. Orgad H. & Belinkov Y. (2023). BLIND: Bias removal with no demographics.
59. Pearl J. (2001). Direct and indirect effects.
60. Pedregosa F., Varoquaux G., Gramfort A. et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, Vol. 12, pp. 2825-2830.
61. Peebles W., Peebles J., Zhu J. et al. (2020). The hessian penalty: A weak prior for unsupervised disentanglement.
62. Prakash N., Shaham T. R., Haklay T. et al. (2024). Fine-tuning enhances existing mechanisms: A case study on entity tracking.
63. Rajamanoharan S., Conmy A., Smith L. et al. (2024). Improving dictionary learning with gated sparse autoencoders. Computing Research Repository.
64. Rajamanoharan S., Lieberum T., Sonnerat N. et al. (2024). Jumping ahead: Improving reconstruction fidelity with jumprelu sparse autoencoders, Jumping Ahead: Improving Reconstruction Fidelity with JumpReLU Sparse Autoencoders. Computing Research Repository.
65. Ravfogel S., Elazar Y., Gonen H. et al. (2020). Null it out: Guarding protected attributes by iterative nullspace projection.
66. Linear adversarial concept erasure Shauli Ravfogel Michael Twiton Yoav Goldberg Ryan DCotterell Proceedings of the 39th International Conference on Machine Learning Kamalika Chaudhuri Stefanie Jegelka Le Song Csaba Szepesvari Gang Niu Sivan Sabato the 39th International Conference on Machine Learning 162 PMLR, 17-23 Jul 2022a, Linear Adversarial Concept Erasure
67. Ravfogel S., Vargas F., Goldberg Y. et al. (2022). Adversarial concept erasure in kernel space.
68. Robins J. M. & Greenland S. (1992). Identifiability and exchangeability for direct and indirect effects, Identifiability and Exchangeability for Direct and Indirect Effects. Epidemiology, Vol. 3(2), pp. 143-155.
69. Sagawa S., Wei Koh P., Tatsunori B. et al. (2020). Distributionally robust neural networks.
70. Schmidhuber J. (1992). Learning Factorial Codes by Predictability Minimization, Learning Factorial Codes by Predictability Minimization. Neural Computation, Vol. 4(6), pp. 863-879. DOI: 10.1162/neco.1992.4.6.863
71. Schneider J. & Vlachos M. (2021). Explaining neural networks by decoding layer activations. DOI: 10.1007/978-3-030-74251-5_6
72. Nimit S., Sohoni M., Sanjabi N. et al. (2022). BARACK: Partially supervised group robustness with guarantees.
73. Sundararajan M., Taly A. & Yan Q. (2017). Axiomatic attribution for deep networks.
74. Attribution patching outperforms automated circuit discovery Aaquib Syed Can Rager Arthur Conmy Neur IPS Workshop on Attributing Model Behavior at Scale, 2023, Attribution Patching Outperforms Automated Circuit Discovery
75. Gemma Team Morgane Riviere Shreya Pathak Pier Giuseppe Sessa Cassidy Hardin Surya Bhupatiraju Léonard Hussenot Thomas Mesnard Bobak Shahriari Alexandre Ramé Johan Ferret Peter Liu Pouya Tafti Abe Friesen Michelle Casbon Sabela Ramos Ravin Kumar Charline Le Lan Sammy Jerome Anton Tsitsulin Nino Vieillard Piotr Stanczyk Sertan Girgin Nikola Momchev Matt Hoffman Shantanu Thakoor Jean-Bastien Grill Behnam Neyshabur Olivier Bachem Alanna Walton Aliaksei Severyn Alicia Parrish Aliya Ahmad Allen Hutchison Alvin Abdagic Amanda Carl Amy Shen Andy Brock Andy Coenen Anthony Laforge Antonia Paterson Ben Bastian Bilal Piot Bo Wu Brandon Royal Charlie Chen Chintu Kumar Chris Perry Chris Welty Christopher AChoquette-Choo Danila Sinopalnikov David Weinberger Dimple Vijaykumar Dominika Rogozińska Dustin Herbison Elisa Bandy Emma Wang Eric Noland Erica Moreira Evan Senter Evgenii Eltyshev Francesco Visin Gary Gabriel Rasskin Glenn Wei Gus Cameron Hadi Martins Hanna Hashemi Harleen Klimczak-Plucińska Harsh Batra Ivan Dhand Jacinda Nardini Jack Mein James Zhou Jeff Svensson Jetha Stanway Jin Peng Chan Joana Zhou Joana Carrasqueira Jocelyn Iljazi Joe Becker Joost Fernandez Josh Van Amersfoort Josh Gordon Josh Lipschultz Newlan Kareem Ju Yeong Ji Kartikeya Mohamed Kat Badola Katie Black Keelin Millican Kelvin Mcdonell Kiranbir Nguyen Kish Sodhia Lars Lowe Greene Lauren Sjoesund Laurent Usui Lena Sifre Leticia Heuermann Lilly Lago Mcnealus Baldini Livio Logan Soares Lucas Kilpatrick Luciano Dixon Machel Martins Manvinder Reid Mark Singh Martin Iverson Mat Görner Mateo Velloso Matt Wirth Matt Davidow Matthew Miller Matthew Rahtz Meg Watson Mehran Risdal Michael Kazemi Ming Moynihan Minsuk Zhang Minwoo Kahng Mofi Park Mohit Rahman Natalie Khatwani Timothy Dao ; Susan Chan Ting Jordan Tom Yu Tom Eccles Tomas Hennigan Tulsee Kocisky Vihan Doshi Vikas Jain Vilobh Yadav Vishal Meshram Warren Dharmadhikari Wei Barkley Wenming Wei Woohyun Ye Woosuk Han Xiang Kwon Zhe Xu Zhitao Shen Zichuan Gong Victor Wei Phoebe Cotruta Anand Kirk Minh Rao Ludovic Giang Tris Peran Eli Warkentin Joelle Collins Zoubin Barral Raia Ghahramani DHadsell Jeanine Sculley Anca Banks Dragan Nenshad Bardoliwalla, Nesh Devanathan, Neta Dumai, Nilay Chauhan, Oscar Wahltinez, Pankil Botarda, Parker Barnes, Paul Barham, Paul Michel, Pengchong Jin, Petko Georgiev, Phil Culliton, Pradeep Kuppala, Ramona Comanescu, Ramona Merhej, Reena Jana, Reza Ardeshir Rokni, Rishabh Agarwal, Ryan Mullins, Samaneh Saadat, Sara Mc Carthy, Sarah Perrin, Sébastien M. R. Arnold, Sebastian Krause, Shengyang Dai, Shruti Garg, Shruti Sheth, Sue Ronstrom, 2024 Slav Petrov Oriol Vinyals, Jeff Dean, Demis Hassabis, Koray Kavukcuoglu, Clement Farabet, Elena Buchatskaya, Sebastian Borgeaud, Noah Fiedel, Armand Joulin, Kathleen Kenealy, Robert Dadashi, and Alek Andreev. Gemma 2: Improving open language models at a practical size
76. Templeton A., Conerly T., Marcus J. et al. (2024). Scaling monosemanticity: Extracting interpretable features from claude 3 sonnet.
77. Todd E., Li M. L., Sharma S. et al. (2024). Function vectors in large language models.
78. Prasetya Ajie Utama N., Sadat Moosavi I. & Gurevych (2020). Towards debiasing NLU models from unknown biases.
79. Vig J., Gehrmann S., Belinkov Y. et al. (2020). Investigating gender bias in language models using causal mediation analysis.
80. Interpretability in the wild: a circuit for indirect object identification in GPT-2 small Kevin Ro Wang Alexandre Variengien Arthur Conmy Buck Shlegeris Jacob Steinhardt The Eleventh International Conference on Learning Representations, 2023, Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 Small
81. Wang T., Victoria Lin X., Fatema Rajani N. et al. (2020). Double-hard debias: Tailoring word embeddings for gender bias mitigation.
82. Yaghoobzadeh Y., Mehri S., Tachet Des Combes R. et al. (2021). Increasing robustness to spurious correlations using forgettable examples.
83. Yan A., Wang Y., Zhong Y. et al. (2023). Robust and interpretable medical image classifiers via concept bottleneck models. Computing Research Repository.
84. Yu Q., Merullo J. & Pavlick E. (2023). Characterizing mechanisms for factual recall in language models.
85. Zech J. R., Badgeley M. A., Liu M. et al. (2018). Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: A cross-sectional study, Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: A cross-sectional study. PLOS Medicine, Vol. 15(11), pp. 1002683. DOI: 10.1371/journal.pmed.1002683
86. Coping with label shift via distributionally robust optimisation Jingzhao Zhang Aditya Krishna Menon Andreas Veit Srinadh Bhojanapalli Sanjiv Kumar Suvrit Sra International Conference on Learning Representations, 2021, Coping with Label Shift via Distributionally Robust Optimisation
87. Zhang M., Nimit S., Sohoni et al. (2022). Correct-N-Contrast: A contrastive approach for improving robustness to spurious correlations.
88. Zou A., Phan L., Chen S. et al. (2023). Representation engineering: A top-down approach to AI transparency. Computing Research Repository.
