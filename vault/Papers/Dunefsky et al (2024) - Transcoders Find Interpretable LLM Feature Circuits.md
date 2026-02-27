---
title: "Transcoders Find Interpretable LLM Feature Circuits"
authors: ["Dunefsky, Jacob", "Chlenski, Philippe", "Nanda, Neel", "Chrupała, G", "Alishahi, A", "Elhage, N", "Nanda, N", "Olsson, C", "Henighan, T", "Joseph, N", "Mann, B", "Askell, A", "Bai, Y", "Chen, A", "Conerly, T", "Dassarma, N", "Drain, D", "Ganguli, D", "Hatfield-Dodds, Z", "Hernandez, D", "Jones, A", "Kernion, J", "Lovitt, L", "Ndousse, K", "Amodei, D", "Brown, T", "Clark, J", "Kaplan, J", "Mccandlish, S", "Olah, C", "Elhage, N", "Hume, T", "Olsson, C", "Nanda, N", "Henighan, T", "Johnston, S", "Elshowk, S", "Joseph, N", "Dassarma, N", "Mann, B", "Hernandez, D", "Askell, A", "Ndousse, K", "Jones, A", "Drain, D", "Chen, A", "Bai, Y", "Ganguli, D", "Lovitt, L", "Hatfield-Dodds, Z", "Kernion, J", "Conerly, T", "Kravec, S", "Fort, S", "Kadavath, S", "Jacobson, J", "Tran-Johnson, E", "Kaplan, J", "Clark, J", "Brown, T", "Mccandlish, S", "Amodei, D", "Olah", "Hanna, M", "Liu, O", "Variengien, A", "Olah, C", "Mordvintsev, A", "Schubert, L", "Vig, J", "Gehrmann, S", "Belinkov, Y", "Qian, S", "Nevo, D", "Singer, Y", "Shieber, S"]
year: 2024
venue: "A Mathematical Framework for Transformer Circuits. Transformer Circuits Thread"
doi: "10.18653/v1/P19-1283"
arxiv: "2406.11944"
type: "paper"
status: "unread"
added: "2026-02-26"
---

# Transcoders Find Interpretable LLM Feature Circuits

**Dunefsky, Jacob et al.** • 2024

> [!quote] Memorable Quote
> ""

## Quick Refresh



## Why You Cared



## Key Concepts



## Cites (Key Papers)

- [[Batson J., Chen B. & Jones A. (2024) - Using features for easy circuit identification]]
- [[Biderman S., Schoelkopf H., Anthony Q., Bradley H., O'brien K., Hallahan E., Khan M. A., Purohit S., Prashanth U. S., Raff E., Skowron A. & Sutawika L. (2023) - A Suite for Analyzing Large Language Models Across Training ...]]
- [[Bills S., Cammarata N., Mossing D., Tillman H., Gao L., Goh G., Sutskever I., Leike J., Wu J. & Saunders W. (2023) - Language models can explain neurons in language models]]
- [[Bloom J. (2024) - Open Source Sparse Autoencoders for all Residual Stream Laye...]]
- [[JSaelensBloom Training 2024]]
- [[Bolukbasi T., Pearce A., Yuan A., Coenen A., Reif E., Viégas F. & Wattenberg M. (2021) - An interpretability illusion for bert]]
- [[Bricken T., Templeton A., Batson J., Chen B., Jermyn A., Conerly T., Turner N., Anil C., Denison C., Askell A., Lasenby R., Wu Y., Kravec S., Schiefer N., Maxwell T., Joseph N., Hatfield-Dodds Z., Tamkin A., Nguyen K., Mclean B., Burke J. E., Hume T., Carter S., Henighan T. & Olah C. (2023) - Towards Monosemanticity: Decomposing Language Models With Di...]]
- [[Brown T. B., Mann B., Ryder N., Subbiah M., Kaplan J., Dhariwal P., Neelakantan A., Shyam P., Sastry G., Askell A., Agarwal S., Herbert-Voss A., Krueger G., Henighan T., Child R., Ramesh A., Ziegler D. M., Wu J., Winter C., Hesse C., Chen M., Sigler E., Litwin M., Gray S., Chess B., Clark J., Berner C., Mccandlish S., Radford A., Sutskever I. & Amodei D. (2020) - Language Models are Few-Shot Learners]]
- [[Olah C. (2022) - Mechanistic Interpretability, Variables, and the Importance ...]]
- [[Chrupała G. & Alishahi A. (2019) - Correlating neural and symbolic representations of language]]

*(42 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** A Mathematical Framework for Transformer Circuits. Transformer Circuits Thread
**DOI:** [10.18653/v1/P19-1283](https://doi.org/10.18653/v1/P19-1283)
**arXiv:** [2406.11944](https://arxiv.org/abs/2406.11944)
**PDF:** [[arxiv_2406.11944.pdf]]

## Abstract

A key goal in mechanistic interpretability is circuit analysis: finding sparse subgraphs of models corresponding to specific behaviors or capabilities. However, MLP sublayers make fine-grained circuit analysis on transformer-based language models difficult. In particular, interpretable features-such as those found by sparse autoencoders (SAEs)-are typically linear combinations of extremely many neurons, each with its own nonlinearity to account for. Circuit analysis in this setting thus either yields intractably large circuits or fails to disentangle local and global behavior. To address this we explore transcoders, which seek to faithfully approximate a densely activating MLP layer with a wider, sparsely-activating MLP layer. We introduce a novel method for using transcoders to perform weights-based circuit analysis through MLP sublayers. The resulting circuits neatly factorize into input-dependent and input-invariant terms. We then successfully train transcoders on language models with 120M, 410M, and 1.4B parameters, and find them to perform at least on par with SAEs in terms of sparsity, faithfulness, and humaninterpretability. Finally, we apply transcoders to reverse-engineer unknown circuits in the model, and we obtain novel insights regarding the "greater-than circuit" in GPT2-small. Our results suggest that transcoders can prove effective in decomposing model computations involving MLPs into interpretable circuits. Code is available at https://github.com/jacobdunefsky/transcoder_circuits/.

## Full Citation List

1. Batson J., Chen B. & Jones A. (2024). Using features for easy circuit identification.
2. Biderman S., Schoelkopf H., Anthony Q. et al. (2023). A Suite for Analyzing Large Language Models Across Training and Scaling.
3. Bills S., Cammarata N., Mossing D. et al. (2023). Language models can explain neurons in language models.
4. Bloom J. (2024). Open Source Sparse Autoencoders for all Residual Stream Layers of GPT2-Small.
5. JSaelens Bloom Training 2024
6. Bolukbasi T., Pearce A., Yuan A. et al. (2021). An interpretability illusion for bert.
7. Bricken T., Templeton A., Batson J. et al. (2023). Towards Monosemanticity: Decomposing Language Models With Dictionary Learning.
8. Brown T. B., Mann B., Ryder N. et al. (2020). Language Models are Few-Shot Learners.
9. Olah C. (2022). Mechanistic Interpretability, Variables, and the Importance of Interpretable Bases.
10. Chrupała G. & Alishahi A. (2019). Correlating neural and symbolic representations of language. DOI: 10.18653/v1/P19-1283
11. Conmy A., Mavor-Parker A. N., Lynch A. et al. (2023). Towards Automated Circuit Discovery for Mechanistic Interpretability.
12. Cunningham H., Ewart A., Riggs L. et al. (2023). Sparse Autoencoders Find Highly Interpretable Features in Language Models.
13. Dunefsky J. & Cohan A. (2023). Observable Propagation: A Data-Efficient Approach to Uncover Feature Vectors in Transformers.
14. Dunefsky J., Chlenski P., Rajamanoharan S. et al. (2024). Case Studies in Reverse-Engineering Sparse Autoencoder Features by Using MLP Linearization.
15. NElhage NNanda COlsson THenighan NJoseph BMann AAskell YBai AChen TConerly NDassarma DDrain DGanguli ZHatfield-Dodds DHernandez AJones JKernion LLovitt KNdousse DAmodei TBrown JClark JKaplan SMccandlish COlah A Mathematical Framework for Transformer Circuits. Transformer Circuits Thread 2021
16. NElhage THume COlsson NNanda THenighan SJohnston SElshowk NJoseph NDassarma BMann DHernandez AAskell KNdousse AJones DDrain AChen YBai DGanguli LLovitt ZHatfield-Dodds JKernion TConerly SKravec SFort SKadavath JJacobson ETran-Johnson JKaplan JClark TBrown SMccandlish DAmodei Olah C. Softmax linear units. Transformer Circuits Thread 2022
17. Elhage N., Hume T., Olsson C. et al. (2022). Toy Models of Superposition.
18. Ferrando J., Sarti G. & Bisazza A. (2024). Primer on the Inner Workings of Transformer-based Language Models.
19. Gandelsman Y., Efros A. A. & Steinhardt J. (2024). Interpreting CLIP's Image Representation via Text-Based Decomposition.
20. Geiger A., Lu H., Icard T. et al. (2021). Causal Abstractions of Neural Networks.
21. AGokaslan VOpenwebtext Cohen Corpus 2019
22. Goldowsky-Dill N., Macleod C., Sato L. et al. (2023). Localizing Model Behavior with Path Patching.
23. Gould R., Ong E., Ogden G. et al. (2023). Successor Heads: Recurring, Interpretable Attention Heads In The Wild.
24. Gurnee W., Nanda N., Pauly M. et al. (2023). Finding Neurons in a Haystack: Case Studies with Sparse Probing.
25. Hanna M., Liu O. & Variengien A. (2023). How does GPT-2 compute greater-than?.
26. Hanna M., Pezzelle S. & Belinkov Y. (2024). Have Faith in Faithfulness: Going Beyond Circuit Overlap When Finding Model Mechanisms.
27. He Z., Ge X., Tang Q. et al. (2024). Dictionary Learning Improves Patch-Free Circuit Discovery in Mechanistic Interpretability: A Case Study on Othello-GPT.
28. Heimersheim S. & Nanda N. (2024). How to use and interpret activation patching.
29. Kissane C., Krzyzanowski R., Conmy A. et al. (2024). Attention SAEs Scale to GPT-2 Small.
30. Kramár J., Lieberum T., Shah R. et al. (2024). AtP*: An efficient and scalable method for localizing LLM behaviour to components.
31. MLi SMarks AMueller Repository 2023
32. Lieberum T., Rahtz M., Kramár J. et al. (2023). Does Circuit Analysis Interpretability Scale? Evidence from Multiple Choice Capabilities in Chinchilla.
33. Lipton Z. C. (2017). The mythos of model interpretability.
34. Marks S., Rager C., Michaud E. J. et al. (2024). Sparse Feature Circuits: Discovering and Editing Interpretable Causal Graphs in Language Models.
35. Mcdougall C., Conmy A., Rushing C. et al. (2023). Copy Suppression: Comprehensively Understanding an Attention Head.
36. Nanda N. (2023). Open source replication & commentary on anthropic's dictionary learning paper. Alignment Forum.
37. NNanda JBloom Transformerlens 2022
38. Nanda N., Rajamanoharan S., Kram\'ar J. et al. (2023). Fact Finding: Attempting to Reverse-Engineer Factual Recall on the Neuron Level.
39. Nanda N. (2024). Attribution Patching: Activation Patching At Industrial Scale.
40. Olah C., Mordvintsev A. & Schubert L. (2017). Feature visualization. Distill. DOI: 10.23915/distill.00007
41. COlah NCammarata LSchubert GGoh MPetrov SCarter Zoom 10.23915/distill.00024.001 March 2020 An Introduction to Circuits. Distill, 5(3):e00024.001
42. Olsson C., Elhage N., Nanda N. et al. (2022). -context Learning and Induction Heads.
43. Achiam Openai JAdler SAgarwal SAhmad LAkkaya IAleman FLAlmeida DAltenschmidt JAltman SAnadkat SAvila RBabuschkin IBalaji SBalcom VBaltescu PBao HBavarian MBelgum JBello IBerdine JBernadett-Shapiro GBerner CBogdonoff LBoiko OBoyd MBrakman A.-LBrockman GBrooks TBrundage MButton KCai TCampbell RCann ACarey BCarlson CCarmichael RChan BChang CChantzis FChen DChen SChen RChen JChen MChess BCho CChu CChung HWCummings DCurrier JDai YDecareaux CDegry TDeutsch NDeville DDhar ADohan DDowling SDunning SEcoffet AEleti AEloundou TFarhi DFedus LFelix NFishman SPForte JFulford IGao LGeorges EGibson CGoel VGogineni TGoh GGontijo-Lopes RGordon JGrafstein MGray SGreene RGross JGu SSGuo YHallacy CHan JHarris JHe YHeaton MHeidecke JHesse CHickey AHickey WHoeschele PHoughton BHsu KHu SHu XHuizinga JJain SJain SJang JJiang AJiang RJin HJin DJomoto SJonn BJun HKaftan TKaiser LKamali AKanitscheider IKeskar NSKhan TKilpatrick LKim JWKim CKim YKirchner JHKiros JKnight MKokotajlo DKondraciuk LKondrich AKonstantinidis AKosic KKrueger GKuo VLampe MLan ILee TLeike JLeung JLevy DLi CMLim RLin MLin SLitwin MLopez TLowe RLue PMakanju AMalfacini KManning SMarkov TMarkovski YMartin BMayer KMayne AMcgrew BMckinney SMMcleavey CMcmillan PMcneil JMedina DMehta AMenick JMetz LMishchenko AMishkin PMonaco VMorikawa EMossing DMu TMurati MMurk OMély DNair ANakano RNayak RNeelakantan ANgo RNoh HOuyang LO'keefe CPachocki JPaino APalermo JPantuliano AParascandolo GParish JParparita EPassos APavlov MPeng APerelman APeres FD A BPetrov MPinto ; Selsam DSheppard KSherbakov TShieh JShoker SShyam PSidor SSigler ESimens MSitkin JSlama KSohl ISokolowsky BSong YStaudacher NSuch FPSummers NSutskever ITang JTezak NThompson MBTillet PTootoonchian ATseng ETuggle PTurley NTworek JUribe JF CVallone AVijayvergiya AVoss CWainwright CWang JJWang AWang BWard JWei JWeinmann CJWelihinda AWelinder PWeng JWeng LWiethoff MWillner DWinter CWolrich SWong HWorkman LWu SWu JWu MXiao KXu TYoo SYu KYuan QZaremba WZellers RZhang CZhang MZhao SZheng TZhuang J arXiv:2303.08774 O., Michael, Pokorny, Pokrass, M., Pong, V. H., Powell, T., Power, A., Power, B., Proehl, E., Puri, R., Radford, A., Rae, J., Ramesh, A., Raymond, C., Real, F., Rimbach, K., Ross, C., Rotsted, B., Roussez, H., Ryder, N., Saltarelli, M., Sanders, T., Santurkar, S., Sastry, G., Schmidt, H., Schnurr, D., Schulman, J., March 2024 Zhuk, W., and Zoph, B. GPT-4 Technical Report cs
44. Radford A., Wu J., Child R. et al. (2019). Language Models are Unsupervised Multitask Learners.
45. Rajamanoharan S., Conmy A., Smith L. et al. (2024). Improving Dictionary Learning with Gated Sparse Autoencoders.
46. Team G., Anil R., Borgeaud S. et al. (2023). a family of highly capable multimodal models.
47. Templeton A., Batson J., Jermyn A. et al. (2024). Predicting Future Activations.
48. Templeton A., Conerly T., Marcus J. et al. (2024). Scaling monosemanticity: Extracting interpretable features from claude 3 sonnet. Transformer Circuits Thread.
49. Vig J., Gehrmann S., Belinkov Y. et al. (2020). Investigating Gender Bias in Language Models Using Causal Mediation Analysis.
50. Wang K., Variengien A., Conmy A. et al. (2022). Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small.
51. Yun Z., Chen Y., Olshausen B. A. et al. (2023). Transformer visualization via dictionary learning: contextualized embedding as a linear superposition of transformer factors.
52. Zhang F. & Nanda N. (2024). Towards Best Practices of Activation Patching in Language Models: Metrics and Methods.
