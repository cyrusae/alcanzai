---
title: "LANGUAGE MODELS REPRESENT SPACE AND TIME"
authors: ["Gurnee, Wes", "Tegmark, Max", "Annamoradnejad, Issa", "Annamoradnejad, Rahimberdi", "Belinkov, Yonatan", "Emily, M", "Bender, Alexander", "Koller", "Bender, Emily M", "Gebru, Timnit", "Mcmillan-Major, Angelina", "Shmitchell, Shmargaret", "Biderman, Stella", "Schoelkopf, Hailey", "Anthony, Quentin Gregory", "Bradley, Herbie", "Kyle, O'", "Brien, Eric", "Hallahan, Mohammad", "Aflah Khan, Shivanshu", "Purohit", "Usvsn Sai Prashanth, Edward", "Raff", "Buzsáki, György", "Llinás, Rodolfo", "Goh, Gabriel", "Cammarata, Nick", "Voss, Chelsea", "Carter, Shan", "Petrov, Michael", "Schubert, Ludwig", "Radford, Alec", "Olah, Chris", "Gupta, Abhijeet", "Boleda, Gemma", "Baroni, Marco", "Padó, Sebastian", "Hafting, Torkel", "Fyhn, Marianne", "Molden, Sturla", "Moser, May-Britt", "Moser, Edvard I", "Hanna, Michael", "Liu, Ollie", "Variengien, Alexandre", "Konkol, Michal", "Brychcín, Tomáš", "Nykl, Michal", "Hercig, Tomáš", "Max, M", "Louwerse, Nick", "Benesh", "Max, M", "Louwerse, Rolf A", "Zwaan", "Meng, Kevin", "Bau, David", "Andonian, Alex", "Belinkov, Yonatan", "Mikolov, Tomas", "Sutskever, Ilya", "Chen, Kai", "Corrado, Greg S", "Dean, Jeff", "Mikolov, Tomáš", "Yih, Wen-Tau", "Zweig, Geoffrey", "John, O'", "Keefe, Jonathan", "Dostrovsky", "Olah, Chris", "Cammarata, Nick", "Schubert, Ludwig", "Goh, Gabriel", "Petrov, Michael", "Carter, Shan", "Patel, Roma", "Pavlick, Ellie", "Räuker, Tilman", "Ho, Anson", "Casper, Stephen", "Hadfield-Menell, Dylan", "Ravichander, Abhilasha", "Belinkov, Yonatan", "Hovy, Eduard", "Rogers, Anna", "Kovaleva, Olga", "Rumshisky, Anna", "Daniel R Schonhaut", "Zahra M Aghajan, Michael J", "Kahana, Itzhak", "Fried", "Toshniwal, Shubham", "Wiseman, Sam", "Livescu, Karen", "Gimpel, Kevin"]
year: 2024
venue: "Computational Linguistics"
arxiv: "2310.02207"
type: "paper"
status: "unread"
added: "2026-01-08"
tags:
  - probing-classifiers
  - linear-representations
  - world-models
  - transformer-interpretability
  - neural-activations
  - space-neurons
  - time-neurons
  - large-language-models
  - mechanistic-interpretability
  - artificial-intelligence
  - computational-linguistics
---
# LANGUAGE MODELS REPRESENT SPACE AND TIME

**Gurnee, Wes et al.** • 2024

> [!quote] Memorable Quote
> "While such spatiotemporal representations do not constitute a dynamic causal world model in their own right, having coherent multi-scale representations of space and time are basic ingredients required in a more comprehensive model."

## Quick Refresh

This paper investigates whether large language models (LLMs) like Llama-2 learn coherent representations of space and time, or just superficial statistical correlations. The researchers trained linear regression probes on model activations to predict real-world coordinates (latitude/longitude) and timestamps for places and events across six datasets spanning different scales (world, US, NYC, historical figures, artworks, news headlines). They found that LLMs do encode spatial and temporal information linearly throughout their layers, with these representations being robust to prompting variations, unified across entity types, and even identifiable in individual "space neurons" and "time neurons"—suggesting these models develop basic ingredients of a world model.

## Why You Cared

This paper matters because it provides concrete evidence that large language models learn more than just surface-level statistical patterns—they appear to build structured, geometric representations of reality. Understanding what representations LLMs actually learn is crucial for reasoning about their reliability, fairness, safety, and interpretability. The finding that continuous features like space and time are represented linearly (previously shown mainly for discrete features) extends our understanding of the linear representation hypothesis and has implications for how we should think about model internals and what these systems have genuinely "learned" from text.

## Key Concepts

`#probing-classifiers` `#linear-representations` `#world-models` `#transformer-interpretability` `#neural-activations` `#space-neurons` `#time-neurons` `#large-language-models` `#mechanistic-interpretability` `#artificial-intelligence` `#computational-linguistics`

## Cites (Key Papers)

- [[Abdou M., Kulmizev A., Hershcovich D., Frank S., Pavlick E. & Søgaard A. (2021) - Can language models encode perceptual structure without grou...]]
- [[Alain G. & Bengio Y. (2016) - Understanding intermediate layers using linear classifier pr...]]
- [[Annamoradnejad I. & Annamoradnejad R. (2022) - Age dataset: A structured general-purpose dataset on life, w...]]
- [[Bandy J. (2021) - Three decades of new york times headlines]]
- [[Belinkov Y. (2022) - Probing classifiers: Promises, shortcomings, and advances]]
- [[Emily M., Bender A. & Koller (2020) - Climbing towards nlu: On meaning, form, and understanding in...]]
- [[Bender E. M., Gebru T., Mcmillan-Major A. & Shmitchell S. (2021) - On the dangers of stochastic parrots: Can language models be...]]
- [[Biderman S., Schoelkopf H., Anthony Q. G., Bradley H., Kyle O., Brien E., Hallahan M., Aflah Khan S., Purohit, Usvsn Sai Prashanth E. & Raff (2023) - Pythia: A suite for analyzing large language models across t...]]
- [[Bisk Y., Holtzman A., Thomason J., Andreas J., Bengio Y., Chai J., Lapata M., Lazaridou A. & May J. (2020) - Aleksandr Nisnevich, et al. Experience grounds language]]
- [[Bommasani R., Hudson D. A., Adeli E., Altman R., Arora S., Sydney Von Arx, Michael S Bernstein J., Bohg A., Bosselut E. & Brunskill (2021) - On the opportunities and risks of foundation models]]

*(40 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Computational Linguistics
**arXiv:** [2310.02207](https://arxiv.org/abs/2310.02207)
**PDF:** [[arxiv_2310.02207.pdf]]

## Abstract

The capabilities of large language models (LLMs) have sparked debate over whether such systems just learn an enormous collection of superficial statistics or a set of more coherent and grounded representations that reflect the real world. We find evidence for the latter by analyzing the learned representations of three spatial datasets (world, US, NYC places) and three temporal datasets (historical figures, artworks, news headlines) in the Llama-2 family of models. We discover that LLMs learn linear representations of space and time across multiple scales. These representations are robust to prompting variations and unified across different entity types (e.g. cities and landmarks). In addition, we identify individual "space neurons" and "time neurons" that reliably encode spatial and temporal coordinates. While further investigation is needed, our results suggest modern LLMs learn rich spatiotemporal representations of the real world and possess basic ingredients of a world model.

## Full Citation List

1. Abdou M., Kulmizev A., Hershcovich D. et al. (2021). Can language models encode perceptual structure without grounding? a case study in color.
2. Alain G. & Bengio Y. (2016). Understanding intermediate layers using linear classifier probes.
3. Annamoradnejad I. & Annamoradnejad R. (2022). Age dataset: A structured general-purpose dataset on life, work, and death of 1.22 million distinguished people.
4. Bandy J. (2021). Three decades of new york times headlines.
5. Belinkov Y. (2022). Probing classifiers: Promises, shortcomings, and advances.
6. Emily M., Bender A. & Koller (2020). Climbing towards nlu: On meaning, form, and understanding in the age of data.
7. Bender E. M., Gebru T., Mcmillan-Major A. et al. (2021). On the dangers of stochastic parrots: Can language models be too big?.
8. Biderman S., Schoelkopf H., Anthony Q. G. et al. (2023). Pythia: A suite for analyzing large language models across training and scaling.
9. Bisk Y., Holtzman A., Thomason J. et al. (2020). Aleksandr Nisnevich, et al. Experience grounds language.
10. Bommasani R., Hudson D. A., Adeli E. et al. (2021). On the opportunities and risks of foundation models.
11. Bubeck S., Chandrasekaran V., Eldan R. et al. (2023). Sparks of artificial general intelligence: Early experiments with gpt-4.
12. Burns C., Ye H., Klein D. et al. (2022). Discovering latent knowledge in language models without supervision.
13. Buzsáki G. & Llinás R. (2017). Space and time in the brain.
14. Cunningham H., Ewart A., Riggs L. et al. (2023). Sparse autoencoders find highly interpretable features in language models.
15. Nelson Elhage Tristan Hume Catherine Olsson Neel Nanda Tom Henighan Scott Johnston Sheer Elshowk Nicholas Joseph Nova Dassarma Ben Mann Danny Hernandez Amanda Askell Kamal Ndousse Andy Jones Dawn Drain Anna Chen Yuntao Bai Deep Ganguli Liane Lovitt Zac Hatfield-Dodds Jackson Kernion Tom Conerly Shauna Kravec Stanislav Fort Saurav Kadavath Josh Jacobson Eli Tran-Johnson Jared Kaplan Jack Clark Tom Brown Sam Mccandlish Dario Amodei Christopher Olah Softmax linear units. Transformer Circuits Thread, 2022a
16. Elhage N., Hume T., Olsson C. et al. (2022). Toy models of superposition.
17. Geva M., Bastings J., Filippova K. et al. (2023). Dissecting recall of factual associations in auto-regressive language models.
18. Goh G., Cammarata N., Voss C. et al. (2021). Multimodal neurons in artificial neural networks.
19. Gupta A., Boleda G., Baroni M. et al. (2015). Distributional vectors encode referential attributes.
20. Gurnee W., Nanda N., Pauly M. et al. (2023). Finding neurons in a haystack: Case studies with sparse probing.
21. Hafting T., Fyhn M., Molden S. et al. (2005). Microstructure of a spatial map in the entorhinal cortex.
22. Hanna M., Liu O. & Variengien A. (2023). How does gpt-2 compute greater-than?.
23. Hastie T., Tibshirani R., Friedman J. H. et al. (2009). The elements of statistical learning: data mining, inference, and prediction.
24. Hendrycks D., Mazeika M. & Woodside T. (2023). An overview of catastrophic ai risks.
25. Hernandez E., Arnab S., Sharma T. et al. (2023). Linearity of relation decoding in transformer language models.
26. Konkol M., Brychcín T., Nykl M. et al. (2017). Geographical evaluation of word embeddings.
27. Lehmann J., Isele R., Jakob M. et al. (2015). Dbpedia -a large-scale, multilingual knowledge base extracted from wikipedia.
28. Li B., Nye M. & Andreas J. (2021). Implicit representations of meaning in neural language models.
29. Li K., Aspen K., Hopkins D. et al. (2022). Emergent world representations: Exploring a sequence model trained on a synthetic task.
30. Bastien Liétard M., Abdou A. & Søgaard (2021). Do language models know the way to rome? arXiv preprint.
31. Leo Z Liu Y., Wang J., Kasai H. et al. (2021). Probing across time: What does roberta know and when? arXiv preprint.
32. Max M., Louwerse N. & Benesh (2012). Representing spatial structure through maps and language: Lord of the rings encodes the spatial structure of middle earth.
33. Max M., Louwerse R. A. & Zwaan (2009). Language encodes geographical information.
34. Meng K., Bau D., Andonian A. et al. (2022). Locating and editing factual associations in gpt.
35. Meng K., Arnab S., Sharma A. et al. (2022). Mass-editing memory in a transformer.
36. Michaud E. J., Liu Z., Girit U. et al. (2023). The quantization model of neural scaling.
37. Mikolov T., Sutskever I., Chen K. et al. (2013). Distributed representations of words and phrases and their compositionality.
38. Mikolov T., Yih W. & Zweig G. (2013). Linguistic regularities in continuous space word representations.
39. Nanda N., Lee A. & Wattenberg M. (2023). Emergent linear representations in world models of self-supervised sequence models.
40. Ngo R., Chan L. & Mindermann S. (2023). The alignment problem from a deep learning perspective.
41. Nyc Opendata (2023). Points of interest.
42. John O., Keefe J. & Dostrovsky (1971). The hippocampus as a spatial map: preliminary evidence from unit activity in the freely-moving rat.
43. Olah C., Cammarata N., Schubert L. et al. (2020). Zoom in: An introduction to circuits.
44. Patel R. & Pavlick E. (2021). Mapping language models to grounded conceptual spaces.
45. Räuker T., Ho A., Casper S. et al. (2023). Toward transparent ai: A survey on interpreting the inner structures of deep neural networks.
46. Ravichander A., Belinkov Y. & Hovy E. (2020). Probing the probing paradigm.
47. Rogers A., Kovaleva O. & Rumshisky A. (2021). A primer in bertology: What we know about how bert works.
48. A neural code for time and space in the human brain Daniel R Schonhaut Michael JZahra M Aghajan Itzhak Kahana Fried Cell Reports 42 11 2023
49. Toshniwal S., Wiseman S., Livescu K. et al. (2022). Chess as a testbed for language model state tracking.
50. Touvron H., Martin L., Stone K. et al. (2023). Llama 2: Open foundation and fine-tuned chat models.
