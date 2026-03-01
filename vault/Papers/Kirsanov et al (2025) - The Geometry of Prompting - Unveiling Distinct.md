---
title: "The Geometry of Prompting: Unveiling Distinct Mechanisms of Task Adaptation in Language Models"
authors: ["Kirsanov, Artem", "Chou, Chi-Ning", "Cho, Kyunghyun", "Chung, Sueyeon", "Chung, Sueyeon", "Abbott, L F", "Chung, Sueyeon", "Lee, Daniel D", "Sompolinsky, Haim", "Cohen, Uri", "Chung, Sueyeon", "Lee, Daniel D", "Sompolinsky, Haim", "Dicarlo, James J", "Cox, David D", "Fawzi, Alhussein", "Moosavi-Dezfooli, Seyed-Mohsen", "Frossard, Pascal", "Soatto, Stefano", "Flesch, Timo", "Juechems, Keno", "Dumbalska, Tsvetomira", "Saxe, Andrew", "Summerfield, Christopher", "Gardner, Elizabeth", "Derrida, Bernard", "Mamou, Jonathan", "Le, Hang", "Del Rio, Miguel", "Stephenson, Cory", "Tang, Hanlin", "Kim, Yoon", "Chung, Sueyeon", "Stephenson, Cory", "Feather, Jenelle", "Padhy, Suchismita", "Elibol, Oguz", "Tang, Hanlin", "Mcdermott, Josh", "Chung, Sueyeon", "Albert J Wakhloo, Tamara J", "Sussman, Sueyeon", "Chung", "Edward Yerxa, Thomas", "Kuang, Yilun", "Eero, P", "Simoncelli, Sueyeon", "Chung", "Zhang, Xiang", "Zhao, Jake", "Lecun, Yann"]
year: 2025
venue: "Current Opinion in Neurobiology"
doi: "10.18653/v1/2021.conll-1.9"
arxiv: "2502.08009"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - manifold-capacity
  - in-context-learning
  - representational-geometry
  - prompt-tuning
  - label-semantics
  - readout-alignment
  - embedding-space
  - task-adaptation
  - language-model-interpretability
  - neural-representations
---

# The Geometry of Prompting: Unveiling Distinct Mechanisms of Task Adaptation in Language Models

**Kirsanov, Artem et al.** • 2025

> [!quote] Memorable Quote
> "Manifold capacity measures the inherent separability of category representations and their potential for supporting robust classification across all possible linear readouts. However, actual model performance also depends on a specific readout—the model's unembed layer—which may fail to optimally utilize well-structured representations."

## Quick Refresh

This paper investigates how three different prompting methods—zero-shot instructions, few-shot demonstrations, and gradient-optimized soft prompts—shape the geometry of internal representations in language models, despite achieving comparable task performance. Using manifold capacity (a framework linking representation geometry to classification performance), the authors analyzed how these methods reorganize the 4096-dimensional embedding space across 32 layers of Llama 3.1 8B. The core finding: all three methods achieve similar accuracy but through fundamentally distinct representational mechanisms, revealing that task performance depends on two independent components—representation quality and readout alignment—that can succeed or fail independently.

## Why You Cared

You were investigating why different prompting strategies produce equivalent performance despite appearing to work quite differently internally. This paper directly addresses the black box of in-context learning (ICL) by showing that "it works" masks vastly different internal dynamics. The distinction between representation quality and readout alignment is particularly valuable because it explains failure modes of few-shot learning (sensitivity to example choice, inability to override label associations) without invoking changes in the underlying geometry—the problem is misalignment, not bad representations. This matters for developing better prompting strategies and understanding what actually changes when you optimize prompts.

## Key Concepts

`#manifold-capacity` `#in-context-learning` `#representational-geometry` `#prompt-tuning` `#label-semantics` `#readout-alignment` `#embedding-space` `#task-adaptation` `#language-model-interpretability` `#neural-representations`

## Cites (Key Papers)

- [[Abdou M., Kulmizev A., Hershcovich D., Frank S., Pavlick E. & Søgaard A. (2021) - Can language models encode perceptual structure without grou...]]
- [[Akyürek E., Schuurmans D., Andreas J., Ma T. & Zhou D. (2023) - What learning algorithm is in-context learning? investigatio...]]
- [[Ansuini A., Laio A., Macke J. H. & Zoccolan D. (2019) - Intrinsic dimension of data representations in deep neural n...]]
- [[Arora S., Li Y., Liang Y., Ma T. & Risteski A. (2018) - Linear algebraic structure of word senses, with applications...]]
- [[Balashankar A. & Subramanian L. (2021) - Learning faithful representations of causal graphs]]
- [[Belinkov Y. (2021) - Probing classifiers]]
- [[arXiv:2102.12452 Promises, shortcomings, and advances Preprint]]
- [[Belinkov Y., Durrani N. & Dalvi F. (2017) - What do neural machine translation models learn about morpho...]]
- [[Bertsch A., Ivgi M., Alon U., Berant J., Gormley M. R. & Neubig G. (2024) - In-context learning with long-context models: An in-depth ex...]]
- [[Samuel R., Bowman L., Vilnis O., Vinyals A. M., Dai R., Jozefowicz S. & Bengio (2016) - Generating sentences from a continuous space]]

*(38 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Current Opinion in Neurobiology
**DOI:** [10.18653/v1/2021.conll-1.9](https://doi.org/10.18653/v1/2021.conll-1.9)
**arXiv:** [2502.08009](https://arxiv.org/abs/2502.08009)
**PDF:** [[arxiv_2502.08009.pdf]]

## Abstract

Decoder-only language models have the ability to dynamically switch between various computational tasks based on input prompts. Despite many successful applications of prompting, there is very limited understanding of the internal mechanism behind such flexibility. In this work, we investigate how different prompting methods affect the geometry of representations in these models. Employing a framework grounded in statistical physics, we reveal that various prompting techniques, while achieving similar performance, operate through distinct representational mechanisms for task adaptation. Our analysis highlights the critical role of input distribution samples and label semantics in few-shot in-context learning. We also demonstrate evidence of synergistic and interfering interactions between different tasks on the representational level. Our work contributes to the theoretical understanding of large language models and lays the groundwork for developing more effective, representation-aware prompting strategies.

## Full Citation List

1. Abdou M., Kulmizev A., Hershcovich D. et al. (2021). Can language models encode perceptual structure without grounding? a case study in color. DOI: 10.18653/v1/2021.conll-1.9
2. Akyürek E., Schuurmans D., Andreas J. et al. (2023). What learning algorithm is in-context learning? investigations with linear models.
3. Ansuini A., Laio A., Macke J. H. et al. (2019). Intrinsic dimension of data representations in deep neural networks.
4. Arora S., Li Y., Liang Y. et al. (2018). Linear algebraic structure of word senses, with applications to polysemy.
5. Balashankar A. & Subramanian L. (2021). Learning faithful representations of causal graphs. DOI: 10.18653/v1/2021.acl-long.69
6. Belinkov Y. (2021). Probing classifiers.
7. arXiv:2102.12452 Promises, shortcomings, and advances Preprint
8. Belinkov Y., Durrani N. & Dalvi F. (2017). What do neural machine translation models learn about morphology?. DOI: 10.18653/v1/P17-1080
9. Bertsch A., Ivgi M., Alon U. et al. (2024). In-context learning with long-context models: An in-depth exploration.
10. Samuel R., Bowman L., Vilnis O. et al. (2016). Generating sentences from a continuous space.
11. Tom B., Brown B., Mann N. et al. (2020). Language models are few-shot learners.
12. Chou C., Arend L., Wakhloo A. J. et al. (2024). Neural manifold capacity captures representation geometry, correlations, and task-efficiency across species and behaviors.
13. Chung S. & Abbott L. F. (2021). Neural population geometry: An approach for understanding biological and artificial neural networks. Current Opinion in Neurobiology, Vol. 70, pp. 137-144. DOI: 10.1016/j.conb.2021.10.010
14. Chung S., Lee D. D. & Sompolinsky H. (2018). Classification and geometry of general perceptual manifolds. Physical Review X.
15. Cohen U., Chung S., Lee D. D. et al. (2020). Separability and geometry of object manifolds in deep neural networks. Nature Communications, Vol. 11(1), pp. 746. DOI: 10.1038/s41467-020-14578-5
16. Dicarlo J. J. & Cox D. D. (2007). Untangling invariant object recognition. Trends in Cognitive Sciences, Vol. 11(8), pp. 333-341. DOI: 10.1016/j.tics.2007.06.010
17. Elhage N., Hume T., Olsson C. et al. (2022). Toy models of superposition.
18. Fawzi A., Moosavi-Dezfooli S., Frossard P. et al. (2018). Empirical Study of the Topology and Geometry of Deep Networks. DOI: 10.1109/CVPR.2018.00396
19. Flesch T., Juechems K., Dumbalska T. et al. (2022). Orthogonal representations for robust contextdependent task performance in brains and neural networks. Neuron, Vol. 110(7), pp. 1258-1270. DOI: 10.1016/j.neuron.2022.01.005
20. Gao P., Trautmann E., Yu B. et al. (2017). A theory of multineuronal dimensionality, dynamics and measurement. DOI: 10.1101/214262
21. Gardner E. & Derrida B. (1988). Optimal storage properties of neural network models. Journal of Physics A: Mathematical and general, Vol. 21(1), pp. 271.
22. Team G. (2024). Gemma 2: Improving open language models at a practical size.
23. Gurnee W. & Tegmark M. (2024). Language models represent space and time.
24. Hendel R., Geva M. & Globerson A. (2023). In-context learning creates task vectors.
25. Hewitt J. & Manning C. D. (2019). A structural probe for finding syntax in word representations. DOI: 10.18653/v1/N19-1419
26. Hovy E., Gerber L., Hermjakob U. et al. (2001). Toward semantics-based answer pinpointing.
27. Diederik P., Kingma J. & Ba (2017). Adam: A method for stochastic optimization.
28. Lester B., Al-Rfou R. & Constant N. (2021). The power of scale for parameter-efficient prompt tuning.
29. Li X. & Roth D. (2002). Learning question classifiers.
30. Liu F., Xu P., Li Z. et al. (2024). Towards understanding incontext learning with contrastive demonstrations and saliency maps.
31. Liu H., Tam D., Muqeeth M. et al. (2022). Few-shot parameter-efficient fine-tuning is better and cheaper than in-context learning.
32. Team L. & Meta A. (2024). The llama 3 herd of models.
33. Mamou J., Le H., Del Rio M. et al. (2020). Emergence of separable manifolds in deep language representations.
34. Mikolov T., Chen K., Corrado G. et al. (2013). Efficient estimation of word representations in vector space.
35. Min S., Lyu X., Holtzman A. et al. (2022). Rethinking the role of demonstrations: What makes in-context learning work? Preprint.
36. Pan J., Gao T., Chen H. et al. (2023). What in-context learning "learns" in-context: Disentangling task recognition and task learning.
37. Park K., Joong Choe Y. & Veitch V. (2024). The linear representation hypothesis and the geometry of large language models.
38. Pennington J., Socher R. & Manning C. (2014). GloVe: Global vectors for word representation. DOI: 10.3115/v1/D14-1162
39. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
40. Stephenson C., Feather J., Padhy S. et al. (2019). Untangling in invariant speech recognition.
41. Stephenson C., Padhy S., Ganesh A. et al. (2021). On the geometry of generalization and memorization in deep neural networks.
42. Johannes Von Oswald E., Niklasson E., Randazzo J. et al. (2023). Transformers learn in-context by gradient descent.
43. Albert J Wakhloo T. J., Sussman S. & Chung (2023). Linear classification of neural manifolds with correlated variability. Physical Review Letters.
44. Wang X., Zhu W., Saxon M. et al. (2024). Large language models are latent variable models: Explaining and finding good demonstrations for in-context learning.
45. Wei J., Bosma M., Vincent Y. et al. (2022). Finetuned language models are zero-shot learners.
46. Edward Yerxa T., Kuang Y., Eero P. et al. (2023). Learning efficient coding of natural images with maximum manifold capacity representations.
47. Zhang X., Zhao J. & Lecun Y. (2015). Character-level convolutional networks for text classification.
48. Zhao T. Z., Wallace E., Feng S. et al. (2021). Calibrate before use: Improving few-shot performance of language models.
