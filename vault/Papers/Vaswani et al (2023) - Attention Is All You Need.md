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
  - attention-mechanism
  - transformer-architecture
  - self-attention
  - multi-head-attention
  - sequence-to-sequence
  - parallelization
  - encoder-decoder
  - scaled-dot-product-attention
---
# Attention Is All You Need

**Vaswani, Ashish et al.** • 2023

> [!quote] Memorable Quote
> "The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs."

## Quick Refresh

This paper introduces the Transformer, a neural network architecture that replaces recurrent and convolutional layers entirely with attention mechanisms for sequence-to-sequence tasks like machine translation. The model uses stacked layers of multi-head self-attention and feed-forward networks, achieving state-of-the-art results on English-German and English-French translation benchmarks while training significantly faster than previous approaches. The authors also demonstrate the architecture generalizes well to parsing tasks, suggesting attention alone is sufficient for complex language understanding without recurrence.

## Why You Cared

This paper matters because it fundamentally challenges the assumption that recurrent architectures are necessary for sequence modeling, proposing a simpler, more parallelizable alternative that achieves better results with less training time. The Transformer's attention-based approach became the foundation for modern large language models like BERT and GPT, making this a watershed moment in deep learning. If you work on NLP or large-scale model training, understanding this architecture is essential to grasping why the field shifted away from LSTMs and RNNs.

## Key Concepts

`#attention-mechanism` `#transformer-architecture` `#self-attention` `#multi-head-attention` `#sequence-to-sequence` `#parallelization` `#encoder-decoder` `#scaled-dot-product-attention`

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

1. JimmyLei Ba JamieRyan Kiros GeoffreyEHinton arXiv:1607.06450 2016 Layer normalization. arXiv preprint
2. Neural machine translation by jointly learning to align and translate DzmitryBahdanau KyunghyunCho YoshuaBengio CoRR, abs/1409.0473 2014
3. Massive exploration of neural machine translation architectures DennyBritz AnnaGoldie Minh-ThangLuong VQuoc Le CoRR, abs/1703.03906 2017
4. Long short-term memory-networks for machine reading JianpengCheng LiDong MirellaLapata arXiv:1601.06733 2016 arXiv preprint
5. Learning phrase representations using rnn encoder-decoder for statistical machine translation KyunghyunCho BartVan Merrienboer CaglarGulcehre FethiBougares HolgerSchwenk YoshuaBengio CoRR, abs/1406.1078 2014
6. Xception: Deep learning with depthwise separable convolutions FrancoisChollet arXiv:1610.02357 2016 arXiv preprint
7. Empirical evaluation of gated recurrent neural networks on sequence modeling JunyoungChung ÇaglarGülçehre KyunghyunCho YoshuaBengio CoRR, abs/1412.3555 2014
8. Recurrent neural network grammars ChrisDyer AdhigunaKuncoro MiguelBallesteros NoahASmith Proc. of NAACL of NAACL 2016
9. JonasGehring MichaelAuli DavidGrangier DenisYarats YannNDauphin arXiv:1705.03122v2 Convolutional sequence to sequence learning 2017 arXiv preprint
10. Generating sequences with recurrent neural networks AlexGraves arXiv:1308.0850 2013 arXiv preprint
11. Deep residual learning for image recognition KaimingHe XiangyuZhang ShaoqingRen JianSun Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition the IEEE Conference on Computer Vision and Pattern Recognition 2016
12. Gradient flow in recurrent nets: the difficulty of learning long-term dependencies SeppHochreiter YoshuaBengio PaoloFrasconi JürgenSchmidhuber 2001
13. Long short-term memory SeppHochreiter JürgenSchmidhuber Neural computation 9 8 1997
14. Self-training PCFG grammars with latent annotations across languages ZhongqiangHuang MaryHarper Proceedings of the 2009 Conference on Empirical Methods in Natural Language Processing the 2009 Conference on Empirical Methods in Natural Language Processing August 2009
15. Exploring the limits of language modeling RafalJozefowicz OriolVinyals MikeSchuster NoamShazeer YonghuiWu arXiv:1602.02410 2016 arXiv preprint
16. Can active memory replace attention? ŁukaszKaiser SamyBengio Advances in Neural Information Processing Systems, (NIPS) 2016
17. Neural GPUs learn algorithms ŁukaszKaiser IlyaSutskever International Conference on Learning Representations (ICLR) 2016
18. NalKalchbrenner LasseEspeholt KarenSimonyan AaronVan Den Oord AlexGraves KorayKavukcuoglu arXiv:1610.10099v2 Neural machine translation in linear time 2017 arXiv preprint
19. Structured attention networks YoonKim CarlDenton LuongHoang AlexanderMRush International Conference on Learning Representations 2017
20. Adam: A method for stochastic optimization DiederikKingma JimmyBa ICLR 2015
21. OleksiiKuchaiev BorisGinsburg arXiv:1703.10722 Factorization tricks for LSTM networks 2017 arXiv preprint
22. A structured self-attentive sentence embedding ZhouhanLin MinweiFeng CiceroNogueira Dos Santos MoYu BingXiang BowenZhou YoshuaBengio arXiv:1703.03130 2017 arXiv preprint
23. Multi-task sequence to sequence learning Minh-ThangLuong QuocVLe IlyaSutskever OriolVinyals LukaszKaiser arXiv:1511.06114 2015 arXiv preprint
24. Effective approaches to attentionbased neural machine translation Minh-ThangLuong HieuPham ChristopherDManning arXiv:1508.04025 2015 arXiv preprint
25. Building a large annotated corpus of english: The penn treebank MaryMitchell P Marcus AnnMarcinkiewicz BeatriceSantorini Computational linguistics 19 2 1993
26. Effective self-training for parsing DavidMcclosky EugeneCharniak MarkJohnson Proceedings of the Human Language Technology Conference of the NAACL, Main Conference the Human Language Technology Conference of the NAACL, Main Conference June 2006
27. A decomposable attention model AnkurParikh OscarTäckström DipanjanDas JakobUszkoreit Empirical Methods in Natural Language Processing 2016
28. RomainPaulus CaimingXiong RichardSocher arXiv:1705.04304 A deep reinforced model for abstractive summarization 2017 arXiv preprint
29. Learning accurate, compact, and interpretable tree annotation SlavPetrov LeonBarrett RomainThibaux DanKlein Proceedings of the 21st International Conference on Computational Linguistics and 44th Annual Meeting of the ACL the 21st International Conference on Computational Linguistics and 44th Annual Meeting of the ACL July 2006
30. Using the output embedding to improve language models arXiv:1608.05859 2016 Ofir Press and Lior Wolf arXiv preprint
31. RicoSennrich BarryHaddow AlexandraBirch arXiv:1508.07909 Neural machine translation of rare words with subword units 2015 arXiv preprint
32. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer NoamShazeer AzaliaMirhoseini KrzysztofMaziarz AndyDavis QuocLe GeoffreyHinton JeffDean arXiv:1701.06538 2017 arXiv preprint
33. Dropout: a simple way to prevent neural networks from overfitting NitishSrivastava GeoffreyEHinton AlexKrizhevsky IlyaSutskever RuslanSalakhutdinov Journal of Machine Learning Research 15 1 2014
34. End-to-end memory networks SainbayarSukhbaatar ArthurSzlam JasonWeston RobFergus Advances in Neural Information Processing Systems CCortes NDLawrence DDLee MSugiyama RGarnett Curran Associates, Inc 2015 28
35. Sequence to sequence learning with neural networks IlyaSutskever OriolVinyals Quoc VvLe Advances in Neural Information Processing Systems 2014
36. Rethinking the inception architecture for computer vision ChristianSzegedy VincentVanhoucke SergeyIoffe JonathonShlens ZbigniewWojna CoRR, abs/1512.00567 2015
37. Grammar as a foreign language Vinyals KooKaiser Petrov Sutskever Hinton Advances in Neural Information Processing Systems 2015
38. YonghuiWu MikeSchuster ZhifengChen VQuoc MohammadLe WolfgangNorouzi MaximMacherey YuanKrikun QinCao KlausGao Macherey arXiv:1609.08144 Google's neural machine translation system: Bridging the gap between human and machine translation 2016 arXiv preprint
39. Deep recurrent models with fast-forward connections for neural machine translation JieZhou YingCao XuguangWang PengLi WeiXu CoRR, abs/1606.04199 2016
40. Fast and accurate shift-reduce constituent parsing MuhuaZhu YueZhang WenliangChen MinZhang JingboZhu Proceedings of the 51st Annual Meeting of the ACL the 51st Annual Meeting of the ACL August 2013 1 Long Papers)
