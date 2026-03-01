---
title: "Evidence of Learned Look-Ahead in a Chess-Playing Neural Network"
authors: ["Jenner, Erik", "Kapur, Shreyas", "Georgiev, Vasil", "Allen, Cameron", "Emmons, Scott", "Russell, Stuart", "Berkeley, U C", "Akyürek, Ekin", "Schuurmans, Dale", "Andreas, Jacob", "Ma, Tengyu", "Zhou, Denny", "Ansel, Jason", "Yang, Edward", "He, Horace", "Gimelshein, Natalia", "Jain, Animesh", "Voznesensky, Michael", "Bao, Bin", "Bell, Peter", "Berard, David", "Burovski, Evgeni", "Chauhan, Geeta", "Chourdia, Anjali", "Constable, Will", "Desmaison, Alban", "Devito, Zachary", "Ellison, Elias", "Feng, Will", "Gong, Jiong", "Gschwind, Michael", "Hirsh, Brian", "Huang, Sherlock", "Kalambarkar, Kshiteej", "Kirsch, Laurent", "Lazos, Michael", "Lezcano, Mario", "Liang, Yanbo", "Liang, Jason", "Lu, Yinghai", "Luk, C K", "Maher, Bert", "Pan, Yunjie", "Puhrsch, Christian", "Reso, Matthias", "Saroufim, Mark", "Siraichi, Marcos Yukio", "Suk, Helen", "Suo, Michael", "Tillet, Phil", "Wang, Eikan", "Wang, Xiaodong", "Wen, William", "Zhang, Shunting", "Zhao, Xu", "Zhou, Keren", "Zou, Richard", "Mathews, Ajit", "Chanan, Gregory", "Wu, Peng", "Chintala, Soumith", "Geiger, Atticus", "Lu, Hanson", "Icard, Thomas", "Potts, Christopher", "Haworth, Guy", "Hernandez, Nelson", "Hewitt, John", "Liang, Percy", "Sepp Hochreiter, A Steven", "Younger, Peter R", "Conwell", "Hunter, John D", "Li, Kenneth", "Aspen, K", "Hopkins, David", "Bau, Fernanda", "Viégas, Hanspeter", "Pfister, Martin", "Wattenberg", "Meng, Kevin", "Bau, David", "Andonian, Alex", "Belinkov, Yonatan", "Pal, Koyena", "Sun, Jiuding", "Yuan, Andrew", "Wallace, Byron C", "Bau, David", "Rogozhnikov, Alex", "Silver, David", "Hubert, Thomas", "Schrittwieser, Julian", "Antonoglou, Ioannis", "Lai, Matthew", "Guez, Arthur", "Lanctot, Marc", "Sifre, Laurent", "Kumaran, Dharshan", "Graepel, Thore", "Lillicrap, Timothy", "Simonyan, Karen", "Hassabis, Demis", "Stöckl, Andreas", "Taufeeque, Mohammad", "Quirke, Philip", "Li, Maximilian", "Cundy, Chris", "Tucker, Aaron David", "Gleave, Adam", "Garriga-Alonso, Adrià", "Toshniwal, Shubham", "Wiseman, Sam", "Livescu, Karen", "Gimpel, Kevin", "Veit, Andreas", "Wilber, Michael J", "Belongie, Serge", "Johannes Von Oswald, Eyvind", "Niklasson, Ettore", "Randazzo, João", "Sacramento, Alexander", "Mordvintsev, Andrey", "Zhmoginov, Max", "Vladymyrov", "Wang, Jane X", "Kurth-Nelson, Zeb", "Tirumala, Dhruva", "Soyer, Hubert", "Leibo, Joel Z", "Munos, Remi", "Blundell, Charles", "Kumaran, Dharshan", "Botvinick, Matt", "Zhang, Fred", "Nanda, Neel"]
year: 2023
venue: "ICLR"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - activation-patching
  - attention-heads
  - learned-search
  - mechanistic-interpretability
  - transformer-probes
  - neural-network-reasoning
  - look-ahead
  - chess-engines
  - causal-analysis
  - information-flow
---

# Evidence of Learned Look-Ahead in a Chess-Playing Neural Network

**Jenner, Erik et al.** • 2023

> [!quote] Memorable Quote
> "That this has such an outsized effect strongly suggests that this specific information pathway is crucial for Leela's decision-making process in a substantial fraction of states."

## Quick Refresh

This paper provides evidence that Leela Chess Zero, a transformer-based chess engine, internally learns to perform look-ahead—mentally simulating future moves before deciding the current move. By analyzing activations on specific chess board squares (which the transformer treats like tokens in a language model), the researchers show that information about moves two turns into the future is unusually important for the network's output decisions. Three lines of evidence converge: activation patching reveals that corrupting future-move squares drastically changes predictions, attention heads systematically move information backward from future moves to present ones, and a simple probe trained on network activations can predict the optimal move 92% accurately two turns ahead.

## Why You Cared

This matters because it's a concrete demonstration that neural networks can learn algorithmic reasoning strategies—not just memorize patterns or apply simple heuristics—without being explicitly trained to do so. You likely saved this because you're interested in mechanistic interpretability (understanding how neural networks actually compute internally) and whether complex reasoning emerges naturally in real systems trained on challenging tasks. The paper also introduces practical techniques for interpreting transformer-based models by exploiting domain structure, which is useful if you work with other domains where inputs have spatial or relational organization.

## Key Concepts

`#activation-patching` `#attention-heads` `#learned-search` `#mechanistic-interpretability` `#transformer-probes` `#neural-network-reasoning` `#look-ahead` `#chess-engines` `#causal-analysis` `#information-flow`

## Cites (Key Papers)

- [[Akyürek E., Schuurmans D., Andreas J., Ma T. & Zhou D. (2023) - What learning algorithm is in-context learning? investigatio...]]
- [[Ansel J., Yang E., He H., Gimelshein N., Jain A., Voznesensky M., Bao B., Bell P., Berard D., Burovski E., Chauhan G., Chourdia A., Constable W., Desmaison A., Devito Z., Ellison E., Feng W., Gong J., Gschwind M., Hirsh B., Huang S., Kalambarkar K., Kirsch L., Lazos M., Lezcano M., Liang Y., Liang J., Lu Y., Luk C. K., Maher B., Pan Y., Puhrsch C., Reso M., Saroufim M., Siraichi M. Y., Suk H., Suo M., Tillet P., Wang E., Wang X., Wen W., Zhang S., Zhao X., Zhou K., Zou R., Mathews A., Chanan G., Wu P. & Chintala S. (2024) - PyTorch 2: Faster Machine Learning Through Dynamic Python By...]]
- [[Belrose N., Furman Z., Smith L., Halawi D., Ostrovsky I., Mckinney L., Biderman S. & Steinhardt J. (2023) - Eliciting latent predictions from transformers with the tune...]]
- [[Brinkmann J., Sheshadri A., Levoso V., Swoboda P. & Bartelt C. (2024) - A mechanistic analysis of a transformer trained on a symboli...]]
- [[Interpreting emergent planning in model-free reinforcement learning ThomasBush S...]]
- [[Yom Din A., Karidi T., Choshen L. & Geva M. (2023) - Jump to conclusions: Short-cutting transformers with linear ...]]
- [[Duan Y., Schulman J., Chen X., Bartlett P. L., Sutskever I. & Abbeel P. (2016) - RL 2 : fast reinforcement learning via slow reinforcement le...]]
- [[Enot Developers I., Kalgin A., Yanchenko P., Ivanov A. & Goncharenko (2021) - onnx2torch]]
- [[Feng X., Luo Y., Wang Z., Tang H., Yang M., Shao K., Henry Mguni D., Du Y. & Wang J. (2023) - ChessGPT: Bridging policy learning and language modeling. Ne...]]
- [[Niklas Fiekas. python-chess]]

*(36 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** ICLR
**PDF:** [[web_proceedings_37d9f19150fce07bced2a81fc87d47_20260226_210654.pdf]]

## Abstract

Do neural networks learn to implement algorithms such as look-ahead or search "in the wild"? Or do they rely purely on collections of simple heuristics? We present evidence of learned look-ahead in the policy and value network of Leela Chess Zero, the currently strongest deep neural chess engine. We find that Leela internally represents future optimal moves and that these representations are crucial for its final output in certain board states. Concretely, we exploit the fact that Leela is a transformer that treats every chessboard square like a token in language models, and give three lines of evidence: (1) activations on certain squares of future moves are unusually important causally; (2) we find attention heads that move important information "forward and backward in time," e.g., from squares of future moves to squares of earlier ones; and (3) we train a simple probe that can predict the optimal move 2 turns ahead with 92% accuracy (in board states where Leela finds a single best line). These findings are clear evidence of learned look-ahead in neural networks and might be a step towards a better understanding of their capabilities.

## Full Citation List

1. Akyürek E., Schuurmans D., Andreas J. et al. (2023). What learning algorithm is in-context learning? investigations with linear models. ICLR.
2. Ansel J., Yang E., He H. et al. (2024). PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation.
3. Belrose N., Furman Z., Smith L. et al. (2023). Eliciting latent predictions from transformers with the tuned lens.
4. Brinkmann J., Sheshadri A., Levoso V. et al. (2024). A mechanistic analysis of a transformer trained on a symbolic multi-step reasoning task.
5. Interpreting emergent planning in model-free reinforcement learning Thomas Bush Stephen Chung Usman Anwar AdriàGarriga-Alonso David Krueger 2024
6. Yom Din A., Karidi T., Choshen L. et al. (2023). Jump to conclusions: Short-cutting transformers with linear transformations.
7. Duan Y., Schulman J., Chen X. et al. (2016). RL 2 : fast reinforcement learning via slow reinforcement learning.
8. Enot Developers I., Kalgin A., Yanchenko P. et al. (2021). onnx2torch.
9. Feng X., Luo Y., Wang Z. et al. (2023). ChessGPT: Bridging policy learning and language modeling. NeurIPS Datasets and Benchmarks Track.
10. Niklas Fiekas. python-chess
11. Jaden Fiotto-Kaufman The package for interpreting and manipulating the internals of deep learned models
12. Geiger A., Lu H., Icard T. et al. (2021). Causal abstractions of neural networks. NeurIPS.
13. Trevor Graffa Lczero_Tools
14. Haworth G. & Hernandez N. (2021). The 20th Top Chess Engine Championship, TCEC20. J. Int. Comput. Games Assoc.
15. Heimersheim S. & Nanda N. (2024). How to use and interpret activation patching.
16. Hewitt J. & Liang P. (2019). Designing and interpreting probes with control tasks. EMNLP.
17. Sepp Hochreiter A. S., Younger P. R. & Conwell (2001). Learning to learn using gradient descent. ICANN.
18. Hubinger E., Van Merwijk C., Mikulik V. et al. (2019). Risks from learned optimization in advanced machine learning systems.
19. Hunter J. D. (2007). Matplotlib: A 2D graphics environment.
20. Karvonen A. (2024). Emergent world models and latent variable estimation in chess-playing language models.
21. Lee J., Xie A., Pacchiano A. et al. (2023). Supervised pretraining can learn in-context reinforcement learning.
22. Leela Chess Zero team. Leela Chess Zero
23. How well do Lc0 networks compare to the greatest transformer network from Deep Mind? 2024
24. Li K., Aspen K., Hopkins D. et al. (2023). Emergent world representations: Exploring a sequence model trained on a synthetic task.
25. Mcgrath T., Kapishnikov A., Tomašev N. et al. (2022). Acquisition of chess knowledge in AlphaZero.
26. Meng K., Bau D., Andonian A. et al. (2022). Locating and editing factual associations in GPT. NeurIPS.
27. Monroe D. & Chalmers P. A. (2024). Mastering chess with a transformer model.
28. Nanda N., Lee A. & Wattenberg M. (2023). Emergent linear representations in world models of selfsupervised sequence models.
29. Noever D., Ciolino M. & Kalin J. (2020). The chess transformer: Mastering play using generative language models.
30. Interpreting GPT: the logit lens 2020
31. Future Lens: Anticipating subsequent tokens from a single hidden state Koyena Pal Jiuding Sun Andrew Yuan Byron CWallace David Bau Conference on Computational Natural Language Learning (Co NLL) 2023
32. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
33. Rogozhnikov A. (2022). Einops: Clear and reliable tensor manipulations with Einstein-like notation. ICLR.
34. Ruoss A., Delétang G., Medapati S. et al. (2024). Grandmaster-level chess without search.
35. Schut L., Tomasev N., Mcgrath T. et al. (2023). Bridging the human-AI knowledge gap: Concept discovery and transfer in AlphaZero.
36. Silver D., Hubert T., Schrittwieser J. et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. Science.
37. Stöckl A. (2021). Watching a language model learning chess.
38. Taufeeque M., Quirke P., Li M. et al. (2024). Planning in a recurrent neural network that plays sokoban.
39. Toshniwal S., Wiseman S., Livescu K. et al. (2021). Chess as a testbed for language model state tracking.
40. Vaswani A., Shazeer N., Parmar N. et al. (2017). Attention is all you need.
41. Veit A., Wilber M. J. & Belongie S. (2016). Residual networks behave like ensembles of relatively shallow networks. NeurIPS.
42. Vig J., Gehrmann S., Belinkov Y. et al. (2020). Investigating gender bias in language models using causal mediation analysis.
43. Johannes Von Oswald E., Niklasson E., Randazzo J. et al. (2023). Transformers learn in-context by gradient descent. ICML.
44. Johannes Von Oswald E., Niklasson M., Schlegel S. et al. (2023). Razvan Pascanu, and João Sacramento. Uncovering mesa-optimization algorithms in transformers.
45. Jane XWang Zeb Kurth-Nelson Dhruva Tirumala Hubert Soyer Joel ZLeibo Remi Munos Charles Blundell Dharshan Kumaran Matt Botvinick Learning to reinforcement learn 2016
46. Zhang F. & Nanda N. (2024). Towards best practices of activation patching in language models: Metrics and methods. ICLR.
