---
title: "Attention Is All You Need"
authors: ["Vaswani, Ashish", "Shazeer, Noam", "Brain, Google", "Parmar, Niki", "Uszkoreit, Jakob", "Jones, Llion", "Gomez, Aidan N", "Kaiser, Łukasz", "Dyer, Chris", "Kuncoro, Adhiguna", "Ballesteros, Miguel", "Smith, Noah A", "He, Kaiming", "Zhang, Xiangyu", "Ren, Shaoqing", "Sun, Jian", "Hochreiter, Sepp", "Schmidhuber, Jürgen", "Huang, Zhongqiang", "Harper, Mary", "Kaiser, Łukasz", "Bengio, Samy", "Kaiser, Łukasz", "Sutskever, Ilya", "Kim, Yoon", "Denton, Carl", "Hoang, Luong", "Rush, Alexander M", "Kingma, Diederik", "Ba, Jimmy", "Mitchell P Marcus, Mary", "Marcinkiewicz, Ann", "Santorini, Beatrice", "Mcclosky, David", "Charniak, Eugene", "Johnson, Mark", "Parikh, Ankur", "Täckström, Oscar", "Das, Dipanjan", "Uszkoreit, Jakob", "Petrov, Slav", "Barrett, Leon", "Thibaux, Romain", "Klein, Dan", "Srivastava, Nitish", "Hinton, Geoffrey E", "Krizhevsky, Alex", "Sutskever, Ilya", "Salakhutdinov, Ruslan", "Sukhbaatar, Sainbayar", "Szlam, Arthur", "Weston, Jason", "Fergus, Rob", "Sutskever, Ilya", "Vinyals, Oriol", "Le, Quoc Vv", "Vinyals", "Kaiser, Koo", "Petrov", "Sutskever", "Hinton", "Zhu, Muhua", "Zhang, Yue", "Chen, Wenliang", "Zhang, Min", "Zhu, Jingbo"]
year: 2023
venue: "Neural computation"
arxiv: "1706.03762"
type: "paper"
status: "unread"
added: "2026-01-08"
tags:
  - transformer-architecture
  - attention-mechanism
  - multi-head-attention
  - self-attention
  - sequence-to-sequence-models
  - machine-translation
  - encoder-decoder
  - positional-encoding
  - parallel-computation
  - neural-networks
  - natural-language-processing
  - deep-learning
---
# Attention Is All You Need

**Vaswani, Ashish et al.** • 2023

> [!quote] Memorable Quote
> "The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs."

## Quick Refresh

The Transformer is a new neural network architecture that replaces recurrent neural networks (RNNs) and convolutional layers with attention mechanisms for sequence-to-sequence tasks like machine translation. Instead of processing sequences step-by-step, the model uses "multi-head attention" to let every position in the input directly attend to every other position in parallel, dramatically speeding up training. On standard translation benchmarks (WMT 2014 English-to-German and English-to-French), the Transformer achieved state-of-the-art results while training 3–5 times faster than previous best models.

## Why You Cared

This paper solves a fundamental bottleneck in sequence modeling: RNNs (Recurrent Neural Networks) are inherently sequential, meaning they must process input one token at a time, which makes training slow and prevents parallelization on modern GPUs. The Transformer shows that you can throw away recurrence entirely and still get better results—in fact, you can get *much* better results while training faster. This is a genuine paradigm shift with immediate practical benefits (faster training, better translation quality) and it opened up entirely new research directions in deep learning. If you're working on language models, machine translation, or any sequence problem, this paper is foundational.

## Key Concepts

`#transformer-architecture` `#attention-mechanism` `#multi-head-attention` `#self-attention` `#sequence-to-sequence-models` `#machine-translation` `#encoder-decoder` `#positional-encoding` `#parallel-computation` `#neural-networks` `#natural-language-processing` `#deep-learning`

## Cites (Key Papers)

- [[JimmyLei Ba JamieRyan Kiros GeoffreyEHinton arXiv:1607.06450 2016 Layer normaliz...]]
- [[Bahdanau D., Cho K. & Bengio Y. (2014) - Neural machine translation by jointly learning to align and ...]]
- [[Britz D., Goldie A., Luong M., Quoc V. & Le (2017) - Massive exploration of neural machine translation architectu...]]
- [[Cheng J., Dong L. & Lapata M. (2016) - Long short-term memory-networks for machine reading]]
- [[Cho K., Van Merrienboer B., Gulcehre C., Bougares F., Schwenk H. & Bengio Y. (2014) - Learning phrase representations using rnn encoder-decoder fo...]]
- [[Chollet F. (2016) - Xception: Deep learning with depthwise separable convolution...]]
- [[Chung J., Gülçehre Ç., Cho K. & Bengio Y. (2014) - Empirical evaluation of gated recurrent neural networks on s...]]
- [[Dyer C., Kuncoro A., Ballesteros M. & Smith N. A. (2016) - Recurrent neural network grammars]]
- [[Gehring J., Auli M., Grangier D., Yarats D. & Dauphin Y. N. (2017) - Convolutional sequence to sequence learning]]
- [[Graves A. (2013) - Generating sequences with recurrent neural networks]]

*(30 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Neural computation
**arXiv:** [1706.03762](https://arxiv.org/abs/1706.03762)
**PDF:** [[arxiv_1706.03762.pdf]]

## Abstract

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 Englishto-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data. * Equal contribution. Listing order is random. Jakob proposed replacing RNNs with self-attention and started the effort to evaluate this idea. Ashish, with Illia, designed and implemented the first Transformer models and has been crucially involved in every aspect of this work. Noam proposed scaled dot-product attention, multi-head attention and the parameter-free position representation and became the other person involved in nearly every detail. Niki designed, implemented, tuned and evaluated countless model variants in our original codebase and tensor2tensor. Llion also experimented with novel model variants, was responsible for our initial codebase, and efficient inference and visualizations. Lukasz and Aidan spent countless long days designing various parts of and implementing tensor2tensor, replacing our earlier codebase, greatly improving results and massively accelerating our research.

† Work performed while at Google Brain.

‡ Work performed while at Google Research.

## Full Citation List

1. Jimmy Lei Ba Jamie Ryan Kiros Geoffrey EHinton ar Xiv:1607.06450 2016 Layer normalization. ar Xiv preprint
2. Bahdanau D., Cho K. & Bengio Y. (2014). Neural machine translation by jointly learning to align and translate.
3. Britz D., Goldie A., Luong M. et al. (2017). Massive exploration of neural machine translation architectures.
4. Cheng J., Dong L. & Lapata M. (2016). Long short-term memory-networks for machine reading.
5. Cho K., Van Merrienboer B., Gulcehre C. et al. (2014). Learning phrase representations using rnn encoder-decoder for statistical machine translation.
6. Chollet F. (2016). Xception: Deep learning with depthwise separable convolutions.
7. Chung J., Gülçehre Ç., Cho K. et al. (2014). Empirical evaluation of gated recurrent neural networks on sequence modeling.
8. Dyer C., Kuncoro A., Ballesteros M. et al. (2016). Recurrent neural network grammars.
9. Gehring J., Auli M., Grangier D. et al. (2017). Convolutional sequence to sequence learning.
10. Graves A. (2013). Generating sequences with recurrent neural networks.
11. He K., Zhang X., Ren S. et al. (2016). Deep residual learning for image recognition.
12. Hochreiter S., Bengio Y., Frasconi P. et al. (2001). Gradient flow in recurrent nets: the difficulty of learning long-term dependencies.
13. Hochreiter S. & Schmidhuber J. (1997). Long short-term memory.
14. Huang Z. & Harper M. (2009). Self-training PCFG grammars with latent annotations across languages.
15. Jozefowicz R., Vinyals O., Schuster M. et al. (2016). Exploring the limits of language modeling.
16. Kaiser Ł. & Bengio S. (2016). Can active memory replace attention?.
17. Kaiser Ł. & Sutskever I. (2016). Neural GPUs learn algorithms.
18. Kalchbrenner N., Espeholt L., Simonyan K. et al. (2017). Neural machine translation in linear time.
19. Kim Y., Denton C., Hoang L. et al. (2017). Structured attention networks.
20. Kingma D. & Ba J. (2015). Adam: A method for stochastic optimization.
21. Kuchaiev O. & Ginsburg B. (2017). Factorization tricks for LSTM networks.
22. Lin Z., Feng M., Nogueira Dos Santos C. et al. (2017). A structured self-attentive sentence embedding.
23. Luong M., Le Q. V., Sutskever I. et al. (2015). Multi-task sequence to sequence learning.
24. Luong M., Pham H. & Manning C. D. (2015). Effective approaches to attentionbased neural machine translation.
25. Mitchell P Marcus M., Marcinkiewicz A. & Santorini B. (1993). Building a large annotated corpus of english: The penn treebank.
26. Mcclosky D., Charniak E. & Johnson M. (2006). Effective self-training for parsing.
27. Parikh A., Täckström O., Das D. et al. (2016). A decomposable attention model.
28. Paulus R., Xiong C. & Socher R. (2017). A deep reinforced model for abstractive summarization.
29. Petrov S., Barrett L., Thibaux R. et al. (2006). Learning accurate, compact, and interpretable tree annotation.
30. Using the output embedding to improve language models ar Xiv:1608.05859 2016 Ofir Press and Lior Wolf ar Xiv preprint
31. Sennrich R., Haddow B. & Birch A. (2015). Neural machine translation of rare words with subword units.
32. Shazeer N., Mirhoseini A., Maziarz K. et al. (2017). Outrageously large neural networks: The sparsely-gated mixture-of-experts layer.
33. Srivastava N., Hinton G. E., Krizhevsky A. et al. (2014). Dropout: a simple way to prevent neural networks from overfitting.
34. Sukhbaatar S., Szlam A., Weston J. et al. (2015). End-to-end memory networks.
35. Sutskever I., Vinyals O. & Le Q. (2014). Sequence to sequence learning with neural networks.
36. Szegedy C., Vanhoucke V., Ioffe S. et al. (2015). Rethinking the inception architecture for computer vision.
37. Vinyals, Kaiser K., Petrov et al. (2015). Grammar as a foreign language.
38. Wu Y., Schuster M., Chen Z. et al. (2016). Google's neural machine translation system: Bridging the gap between human and machine translation.
39. Zhou J., Cao Y., Wang X. et al. (2016). Deep recurrent models with fast-forward connections for neural machine translation.
40. Zhu M., Zhang Y., Chen W. et al. (2013). Fast and accurate shift-reduce constituent parsing.
