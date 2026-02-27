---
title: "Toward an Ontological Representation of Fictional Characters"
authors: ["Bourgois, Antoine", "Barré, Jean", "Seminck, Olga", "Poibeau, Thierry", "Bamman, David", "Underwood, Ted", "Smith, Noah A", "Bamman, David", "Lewke, Olivia", "Mansoor, Anya", "Barré, Jean", "Cabrera Ramírez, Pedro", "Mélanie, Frédérique", "Galleron, Ioanna", "Barré, Jean", "Seminck, Olga", "Bourgois, Antoine", "Poibeau, Thierry", "Barthes, Roland", "Barthes, Roland", "S/Z", "Bourgois, Antoine", "Poibeau, Thierry", "Brahman, Faeze", "Huang, Meng", "Tafjord, Oyvind", "Zhao, Chao", "Sachan, Mrinmaya", "Chaturvedi, Snigdha", "-G. Chen, R H", "Chen, C.-C", "Chen, C.-M", "Ehrmanntraut, Anton", "Konle, Leonard", "Jannidis, Fotis", "Flekova, Lucie", "Gurevych, Iryna", "Gurung, Alexander", "Lapata, Mirella", "Huang, Luyao", "Sun, Chi", "Qiu, Xipeng", "Huang, Xuanjing", "Jahan, Labiba", "Mittal, Rahul", "Finlayson, Mark", "Jannidis, Fotis", "Character", "Jouve, Vincent", "Landis, Richard", "Koch, Gary G", "Margolin, Uri", "Martin, Louis", "Muller, Benjamin", "Suárez, Javier Ortiz", "Dupont, Yoann", "Romary, Laurent", "Mckee, Robert", "Story", "Haaris Mian, Melanie", "Subbiah, Sharon", "Marcus, Nora", "Shaalan, Kathleen", "Mckeown", "Srinivasan, Vardhini", "Power, Aurelia", "Joris Van Zundert, Andreas", "Van Cranenburgh, Roel", "Smeets", "Yang, Funing", "Jane, Carolyn", "Yoder, Michael", "Khosla, Sopan", "Shen, Qinlan", "Naik, Aakanksha", "Jin, Huiming", "Muralidharan, Hariharan", "Rosé, Carolyn"]
year: 1996
venue: "Poetics. Penguin Classics"
doi: "10.1017/chr.2026.1"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - ontological-representation
  - character-embeddings
  - narrative-theory
  - facet-dependent-similarity
  - attribute-classification
  - character-centric-analysis
  - computational-literary-studies
  - french-fiction
  - multidimensional-characterization
---

# Toward an Ontological Representation of Fictional Characters

**Bourgois, Antoine et al.** • 1996

> [!quote] Memorable Quote
> "Character similarity is not a single dimension; it is a bundle of relations that cut across actions, affect, cognition, social roles, physical description, possessions, and more."

## Quick Refresh

This paper proposes an ontology of 17 interpretable character attribute categories (actions, emotions, traits, relations, etc.) organized under three macro-classes (anthropological, physical, psychological), grounded in narratological theory. Using a BERT-based clustering approach to extract attributes from French novels, the authors show that character similarity is facet-dependent: small, carefully chosen combinations of ontological dimensions outperform fully aggregated representations, reaching 96% accuracy on benchmark tasks compared to 74% for syntax-based baselines. The core contribution is moving from black-box embeddings to semantically structured, comparable character representations that align better with human literary judgment.

## Why You Cared

You were investigating how to represent literary characters computationally in ways that preserve narrative-theoretic insight rather than reducing them to undifferentiated vectors. This paper solves a real gap: existing work either uses shallow syntactic proxies or collapses heterogeneous information into single representations, losing the multidimensionality that actually drives similarity judgments. The result is a reproducible framework you can apply to other literary corpora, and the insight that "not all attributes matter equally" suggests you can be more strategic about what features to track when analyzing large text collections.

## Key Concepts

`#ontological-representation` `#character-embeddings` `#narrative-theory` `#facet-dependent-similarity` `#attribute-classification` `#character-centric-analysis` `#computational-literary-studies` `#french-fiction` `#multidimensional-characterization`

## Cites (Key Papers)

- [[Aristotle Poetics. Penguin Classics 1996 London, 335 BCE]]
- [[DavidBamman Booknlp 2021]]
- [[Bamman D., Underwood T. & Smith N. A. (2013) - Appendix to 'a bayesian mixed effects model of literary char...]]
- [[Bamman D., Underwood T. & Smith N. A. (2014) - A Bayesian Mixed Effects Model of Literary Character]]
- [[Bamman D., Lewke O. & Mansoor A. (2020) - An annotated dataset of coreference in English literature]]
- [[Barré J., Cabrera Ramírez P., Mélanie F. & Galleron I. (2023) - Pour une détection automatique de l'espace textuel des perso...]]
- [[Barré J., Seminck O., Bourgois A. & Poibeau T. (2025) - Modeling the construction of a literary archetype: The case ...]]
- [[10.63744/SMbYIWcHZj87 /SMbYIWcHZj 87]]
- [[Barthes R. (1966) - Introduction à l'analyse structurale des récits]]
- [[Barthes R. & S/Z (1970) - Number 70 in Points Essais]]

*(27 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Poetics. Penguin Classics
**DOI:** [10.1017/chr.2026.1](https://doi.org/10.1017/chr.2026.1)
**PDF:** [[web_cambridge_toward-an-ontological-represen_20260226_212638.pdf]]

## Abstract

Characters are central to narrative theory but remain under-specified in computational work, where they are often reduced to clusters of words or vectors. We propose an operationalizable ontology of characterization that bridges narratological theory and NLP. From BERT-based clustering of character descriptions, we derive 17 classes of attributes (actions, emotions, traits, relations, possessions, etc.), validated through manual annotation (k = 0.77) and automatic classification (64% accuracy vs. 12% baseline). Applied to character similarity tasks for French fiction, our framework outperforms existing models. By aligning narratological insights with computational methods, we move toward a (representation of fictional characters as structured, comparable entities for large-scale literary analysis.

## Full Citation List

1. Aristotle Poetics. Penguin Classics 1996 London, 335 BCE
2. David Bamman Booknlp 2021
3. Bamman D., Underwood T. & Smith N. A. (2013). Appendix to 'a bayesian mixed effects model of literary character.
4. Bamman D., Underwood T. & Smith N. A. (2014). A Bayesian Mixed Effects Model of Literary Character. DOI: 10.3115/v1/P14-1035
5. Bamman D., Lewke O. & Mansoor A. (2020). An annotated dataset of coreference in English literature.
6. Barré J., Cabrera Ramírez P., Mélanie F. et al. (2023). Pour une détection automatique de l'espace textuel des personnages romanesques.
7. Barré J., Seminck O., Bourgois A. et al. (2025). Modeling the construction of a literary archetype: The case of the detective figure in french literature. Anthology of Computers and the Humanities, Vol. 3, pp. 983-999. DOI: 10.63744/SMbYIWcHZj87
8. 10.63744/SMb YIWc HZj87 /SMb YIWc HZj 87
9. Barthes R. (1966). Introduction à l'analyse structurale des récits. DOI: 10.3406/comm.1966.1113
10. Barthes R. & S/Z (1970). Number 70 in Points Essais. Éditions du Seuil.
11. Bourgois A. & Poibeau T. (2025). The elephant in the coreference room: Resolving coreference in full-length French fiction works. DOI: 10.18653/v1/2025.crac-1.5
12. Brahman F., Huang M., Tafjord O. et al. (2021). let your characters tell their story": A dataset for character-centric narrative understanding. DOI: 10.18653/v1/2021.findings-emnlp.150
13. -G. Chen R. H., Chen C. & Chen C. (2019). Unsupervised cluster analyses of character networks in fiction: Community structure and centrality. Knowledge-Based Systems, Vol. 163, pp. 800-810. DOI: 10.1016/j.knosys.2018.10.005
14. Ehrmanntraut A., Konle L. & Jannidis F. (2023). LLpro: A literary language processing pipeline for German narrative texts.
15. Flekova L. & Gurevych I. (2015). Personality profiling of fictional characters using sense-level links between lexical resources. DOI: 10.18653/v1/D15-1208
16. Forster E. M. (1988). Aspects of the novel. Pelican books. Penguin Books.
17. Julien A. (1966). Sémantique structurale: recherche de méthode. Formes sémiotiques. Presses Universitaires de France.
18. Gurung A. & Lapata M. (1998). Le personnel du roman: le système des personnages dans les Rougon-Macquart d'Emile Zola. Number 12 in Titre courant. DOI: 10.18653/v1/2024.findings-emnlp.499
19. Hamon P. (2014). Hachette Éducation.
20. Huang L., Sun C., Qiu X. et al. (2019). Gloss-BERT: BERT for word sense disambiguation with gloss knowledge. DOI: 10.18653/v1/D19-1355
21. Jahan L., Mittal R. & Finlayson M. (2021). Inducing stereotypical character roles from plot structure. DOI: 10.18653/v1/2021.emnlp-main.39
22. Jannidis F., Figur & Person (2008). Beitrag zu einer historischen Narratologie. De Gruyter. DOI: 10.1515/9783110201697
23. Jannidis F. & Character (2013). In the living handbook of narratology.
24. Jouve V. (1992). Extraction and analysis of fictional character networks: A survey. DOI: 10.1145/3344548
25. Landis R. & Koch G. G. (1977). The measurement of observer agreement for categorical data. Biometrics, Vol. 33(1), pp. 159-174.
26. Leblond A. (2022). Corpus chapitres.
27. Margolin U. (1983). Characterization in narrative: Some theoretical prolegomena. Neophilologus, Vol. 67(1), pp. 1572-8668. DOI: 10.1007/BF01956983
28. Martin L., Muller B., Suárez J. O. et al. (2020). Éric de la Clergerie, Djamé Seddah, and Benoît Sagot. DOI: 10.18653/v1/2020.acl-main.645
29. Mckee R. & Story (1997). Substance, Structure, Style, and the Principles of Screenwriting.
30. Haaris Mian M., Subbiah S., Marcus N. et al. (2024). Booknlp-fr, the french versant of booknlp. a tailored pipeline for 19th and 20th century french literature. Journal of Computational Literary Studies, Vol. 3, pp. 1-34. DOI: 10.48694/jcls.3924
31. Vladimir Iakovlevitch Propp. Morphologie du conte. Éditions Points 1928 Paris
32. Ryan M. (1992). Possible worlds, artificial intelligence and narrative theory.
33. Character extraction and character type identification from summarised story plots Vardhini Srinivasan Aurelia Power 10.4995/jclr.2022.17835 Journal of Computer-Assisted Linguistic Research 6 2022
34. Putting dutchcoref to the test: Character detection and gender dynamics in contemporary dutch novels Andreas Joris Van Zundert Roel Van Cranenburgh Smeets Computational Humanities Research Conference 2023 CEUR Workshop Proceedings
35. Woloch A. (2003). The One vs. the Many: Minor Characters and the Space of the Protagonist in the Novel.
36. Yang F. & Jane C. (2024). Evaluating computational representations of character: An austen character similarity benchmark. DOI: 10.18653/v1/2024.nlp4dh-1.3
37. Yoder M., Khosla S., Shen Q. et al. (2021). Fan-fictionNLP: A text processing pipeline for fanfiction. DOI: 10.1017/chr.2026.10025
