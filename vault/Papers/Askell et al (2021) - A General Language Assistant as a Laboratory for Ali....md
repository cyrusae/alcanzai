---
title: "A General Language Assistant as a Laboratory for Alignment"
authors: ["Askell, Amanda", "Bai, Yuntao", "Chen, Anna", "Drain, Dawn", "Ganguli, Deep", "Henighan, Tom", "Jones, Andy", "Joseph, Nicholas", "Mann, Ben", "Dassarma, Nova", "Elhage, Nelson", "Hatfield-Dodds, Zac", "Hernandez, Danny", "Kernion, Jackson", "Ndousse, Kamal", "Olsson, Catherine", "Amodei, Dario", "Brown, Tom", "Clark, Jack", "Mccandlish, Sam", "Olah, Chris", "Kaplan, Jared", "Anthropic", "Joseph, Tom", "Henighan, Andy Jones Nelson", "Elhage, Kamal", "Ndousse", "Lin, Derrick", "Koppel, James", "Chen, Angela", "Solar-Lezama, Armando", "Edwin, James", "Sennrich, Rico", "Haddow, Barry", "Birch, Alexandra", "Vsp + 17 ;, Ashish", "Vaswani, Noam", "Shazeer, Niki", "Parmar, Jakob", "Uszkoreit, Llion", "Jones, Aidan N", "Gomez, Ł Ukasz", "Kaiser, Illia", "Polosukhin"]
year: 2021
venue: "Detoxify. Github"
doi: "10.1007/s11023-020-09539-2"
arxiv: "2112.00861"
type: "paper"
status: "unread"
added: "2026-01-08"
tags:
  - preference-modeling
  - reinforcement-learning-from-human-feedback
  - language-model-alignment
  - imitation-learning
  - in-context-learning
  - context-distillation
  - ranked-preferences
  - sample-efficiency
  - helpful-honest-harmless
  - scaling-laws
  - artificial-intelligence
  - machine-learning
---
# A General Language Assistant as a Laboratory for Alignment

**Askell, Amanda et al.** • 2021

> [!quote] Memorable Quote
> "If it's possible to try to address a problem directly, then one needs a good excuse for not doing so."

## Quick Refresh

This paper investigates practical techniques for aligning large language models (LLMs) with human values—making them helpful, honest, and harmless (HHH)—by treating a general-purpose text-based AI assistant as a testing ground. The researchers compare several training approaches: simple prompting, imitation learning, and preference modeling (learning to rank responses by quality), finding that ranked preference modeling significantly outperforms imitation learning and scales better with model size, while binary discrimination shows little benefit. They also introduce "preference model pre-training" (PMP), where models are first trained on large public datasets encoding human preferences (Reddit, StackExchange, Wikipedia) before fine-tuning on smaller alignment-specific datasets, which substantially improves sample efficiency.

## Why You Cared

This paper matters because it directly tackles AI alignment at scale rather than in theoretical isolation, treating it as an engineering problem that can be measured and incrementally improved. If you're working on language models, reinforcement learning from human feedback (RLHF), or understanding how to steer AI systems toward desired behaviors, this paper provides crucial empirical baselines: it shows that simple prompting works better than expected, that preference modeling (especially on ranked data) is far more efficient than imitation learning, and that pre-training on preference-rich public data is a practical way to make alignment interventions cheaper. The finding that larger models benefit from alignment interventions rather than suffer from them suggests alignment and capability don't necessarily trade off, which is both practically and theoretically important.

## Key Concepts

`#preference-modeling` `#reinforcement-learning-from-human-feedback` `#language-model-alignment` `#imitation-learning` `#in-context-learning` `#context-distillation` `#ranked-preferences` `#sample-efficiency` `#helpful-honest-harmless` `#scaling-laws` `#artificial-intelligence` `#machine-learning`

## Cites (Key Papers)

- [[Nicholas Joseph was central to building and maintaining a highly efficient distr...]]
- [[Tom Henighan managed our research cluster, helped build our distributed training...]]
- [[He also provided engineering support to the toxicity experiments, A/B testing in...]]
- [[Catherine Olsson and Jared Kaplan wrote the HHH prompt, and along with Deep Gang...]]
- [[JaredKaplan YuntaoBai AnnaChen AmandaAskell DeepGanguli and Ben Mann wrote the p...]]
- [[DarioAmodei ChrisOlah and Jack Clark contributed expertise and advice throughout...]]
- [[Sam McCandlish led model pretraining efforts, often in collaboration with Jared ...]]
- [[Abramson J., Ahuja A., Barr I., Brussee A., Carnevale F., Cassin M., Chhaparia R., Clark S., Damoc B., Dudzik A., Georgiev P., Guy A., Harley T., Hill F., Hung A., Kenton Z., Landon J., Lillicrap T., Mathewson K., Mokra S., Muldal A., Santoro A., Savinov N., Varma V., Wayne G., Williams D., Wong N., Yan C. & Zhu R. (2012) - He conducted some initial experiments on preference modeling...]]
- [[AugustusAon + 21] Jacob Austin MaxwellOdena MaartenNye HenrykBosma DavidMichalew...]]
- [[Amodei D., Olah C., Steinhardt J., Christiano P., Schulman J. & Mané D. (2016) - Concrete problems in ai safety]]

*(41 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Detoxify. Github
**DOI:** [10.1007/s11023-020-09539-2](https://doi.org/10.1007/s11023-020-09539-2)
**arXiv:** [2112.00861](https://arxiv.org/abs/2112.00861)
**PDF:** [[arxiv_2112.00861.pdf]]

## Abstract

Given the broad capabilities of large language models, it should be possible to work towards a general-purpose, text-based assistant that is aligned with human values, meaning that it is helpful, honest, and harmless. As an initial foray in this direction we study simple baseline techniques and evaluations, such as prompting. We find that the benefits from modest interventions increase with model size, generalize to a variety of alignment evaluations, and do not compromise the performance of large models. Next we investigate scaling trends for several training objectives relevant to alignment, comparing imitation learning, binary discrimination, and ranked preference modeling. We find that ranked preference modeling performs much better than imitation learning, and often scales more favorably with model size. In contrast, binary discrimination typically performs and scales very similarly to imitation learning. Finally we study a 'preference model pre-training' stage of training, with the goal of improving sample efficiency when finetuning on human preferences.

## Full Citation List

1. Nicholas Joseph was central to building and maintaining a highly efficient distributed training system for large language models and helped with our sampling infrastructure
2. Tom Henighan managed our research cluster, helped build our distributed training system, and did research and experiments on the numerical stability of large language model training. He also helped with ML research on large language models. Nova Das Sarma has also helped manage the cluster
3. He also provided engineering support to the toxicity experiments, A/B testing infrastructure, distributed training, and code model data collection. Catherine Olsson contributed crucially to alignment ideas, and provided useful advice for sourcing and training contractors to test our models. Led by Tom Brown in collaboration with Sam Mc Candlish, much of the technical staff at Anthropic contributed to efficient distributed model training and sampling, the underlying ML, and cluster stability Tom Joseph Andy Jones Nelson Henighan Kamal Elhage Ndousse Core contributors include Nicholas Zac Hatfield-Dodds Andy Jones was central in building our sampling infrastructure. and Ben Mann also contributed to this infrastructure
4. Catherine Olsson and Jared Kaplan wrote the HHH prompt, and along with Deep Ganguli, Anna Chen, Amanda Askell, and many others wrote most of the alignment evaluations. Jackson Kernion helped improve the alignment evaluations and source workers to interact with our models
5. Jared Kaplan Yuntao Bai Anna Chen Amanda Askell Deep Ganguli and Ben Mann wrote the paper, with helpful comments from everyone at Anthropic
6. Dario Amodei Chris Olah and Jack Clark contributed expertise and advice throughout the project
7. Sam Mc Candlish led model pretraining efforts, often in collaboration with Jared Kaplan. Sam also led the overall synthesis of engineering and research efforts
8. Abramson J., Ahuja A., Barr I. et al. (2012). He conducted some initial experiments on preference modeling and many of the experiments on prompting and context distillation. References [AAB + 21.
9. Augustus Aon + 21] Jacob Austin Maxwell Odena Maarten Nye Henryk Bosma David Michalewski Ellen Dohan Carrie Jiang Michael Cai Quoc Terry Charles Le Sutton Program synthesis with large language models, 2021, 2108.07732
10. Amodei D., Olah C., Steinhardt J. et al. (2016). Concrete problems in ai safety.
11. Ats + 21] Vamsi, Aribandi Y., Tay T. et al. (2021). Ext5: Towards extreme multi-task scaling for transfer learning.
12. Daniel S., Brown W., Goo P. et al. (1904). Extrapolating beyond suboptimal demonstrations via inverse reinforcement learning from observations.
13. Tom B., Brown B., Mann N. et al. (2005). Language models are few-shot learners.
14. Samuel R. & Bowman (2021). When combating hype, proceed with caution.
15. Ckb + 21] Karl Cobbe V., Kosaraju M., Bavarian J. et al. (2021). Training verifiers to solve math word problems.
16. Clb + 17] Paul Christiano J., Leike T. B., Brown M. et al. (2017). Deep reinforcement learning from human preferences.
17. Clr + 21] Lili Chen K., Lu A., Rajeswaran K. et al. (1345). Decision transformer: Reinforcement learning via sequence modeling.
18. Christiano P., Shlegeris B. & Amodei D. (2018). Supervising strong learners by amplifying weak experts.
19. Jerry Ctj + 21] Mark Chen Heewoo Tworek Qiming Jun Henrique Yuan Jared Ponde De Oliveira Pinto Harri Kaplan Yuri Edwards Nicholas Burda Greg Joseph Alex Brockman Raul Ray Gretchen Puri Michael Krueger Heidy Petrov Girish Khlaaf Pamela Sastry Brooke Mishkin Scott Chan Nick Gray Mikhail Ryder Alethea Pavlov Lukasz Power Mohammad Kaiser Clemens Bavarian Philippe Winter Felipe Petroski Tillet Dave Such Matthias Cummings Fotios Plappert Elizabeth Chantzis Ariel Barnes William Herbert-Voss Alex Hebgen Guss Alex Nichol Nikolas Paino Jie Tezak Igor Tang Suchir Babuschkin Shantanu Balaji William Jain Christopher Saunders Andrew NHesse Jan Carr Josh Leike Vedant Achiam Evan Misra Alec Morikawa Matthew Radford Miles Knight Mira Brundage Katie Murati Peter Mayer Bob Welinder Dario Mcgrew Sam Amodei Ilya Mccandlish Wojciech Sutskever Zaremba Evaluating large language models trained on code, 2021, 2107.03374
20. The Common Crawl Foundation. Common crawl
21. Gabriel I. (2020). Artificial intelligence, values, and alignment. Minds and Machines. DOI: 10.1007/s11023-020-09539-2
22. Gbb + 20] Leo, Gao S., Biderman S. et al. (2020). The pile: An 800gb dataset of diverse text for language modeling.
23. Samuel Gehman S., Gururangan M., Sap Y. et al. (2008). Realtoxicityprompts: Evaluating neural toxic degeneration in language models.
24. Hendrycks D., Carlini N., Schulman J. et al. (2021). Unsolved problems in ml safety.
25. Ho J., Ermon S., Hestness J. et al. (1606). Generative adversarial imitation learning.
26. Detoxify. Github 2020 Laura Hanu and Unitary team
27. Irving G., Christiano P., Amodei D. et al. (2018). Reward learning from human preferences and demonstrations in atari.
28. Jhb + 21] Liwei, Jiang J. D., Hwang C. et al. (2021). Towards machine ethics and norms.
29. Jones A. L. (2021). Scaling scaling laws with board games.
30. Kmh + 20] J., Kaplan S., Mccandlish T. et al. (2001). Scaling laws for neural language models.
31. Komeili M., Shuster K. & Weston J. (2021). Internet-augmented dialogue generation.
32. Lester B., Al-Rfou R. & Constant N. (2021). The power of scale for parameter-efficient prompt tuning.
33. Lin S., Hilton J. & Evans O. (2021). Truthfulqa: Measuring how models mimic human falsehoods.
34. Lin D., Koppel J., Chen A. et al. (2017). Quixbugs: A multilingual program repair benchmark set based on the quixey challenge. DOI: 10.1145/3135932.3135941
35. Lsp + 18] Peter J., Liu M., Saleh E. et al. (1801). Generating wikipedia by summarizing long sequences.
36. Edwin J. (2015). The definition of lying and deception.
37. Nra + 21] Helen, Ngo C., Raterink et al. (2021). Mitigating harm in language models with conditional-likelihood filtration.
38. Pkl ; D., Paperno G., Kruszewski A. et al. (2016). Gemma Boleda, and Raquel FernÃ¡ndez. The lambada dataset: Word prediction requiring a broad discourse context.
39. Vinay V., Ramasesh E., Dyer M. et al. (2007). Anatomy of catastrophic forgetting: Hidden representations and task semantics.
40. Radford A., Narasimhan K., Salimans T. et al. (2018). Improving language understanding by generative pre-training.
41. Rosenfeld J. S., Rosenfeld A., Belinkov Y. et al. (2019). A constructive prediction of the generalization error across scales.
42. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
43. Solaiman I. & Dennison C. (2021). Process for adapting language models to society (PALMS) with values-targeted datasets.
44. Soares N., Fallenstein B., Armstrong S. et al. (2015). Workshops at the Twenty-Ninth AAAI Conference on Artificial Intelligence.
45. Sennrich R., Haddow B. & Birch A. (2015). Neural machine translation of rare words with subword units.
46. Stiennon N., Ouyang L., Wu J. et al. (1325). Learning to summarize from human feedback.
47. Swr + 21] Victor Albert Sanh Colin Webson Stephen HRaffel Lintang Bach Zaid Sutawika Antoine Alyafeai Arnaud Chaffin Teven Stiegler Arun Le Scao Manan Raja MDey Canwen Saiful Bari Urmish Xu Shanya Thakker Eliza Sharma Sharma Taewoon Szczechla Gunjan Kim Nihal Chhablani Debajyoti Nayak Jonathan Datta Mike Chang Tian-Jian Han Jiang Matteo Wang Sheng Manica Zheng Xin Shen Harshit Yong Rachel Pandey Thomas Bawden ;Wang MAlexander Rush Trishala Neeraj, Jos Rozen, Abheesht Sharma, Andrea Santilli, Thibault Fevry, Jason Alan Fries, Ryan Teehan Stella Biderman, Leo Gao, Tali Bers, Thomas Wolf Multitask prompted training enables zero-shot task generalization, 2021, 2110.08207
48. Vsp + 17 ; A., Vaswani N., Shazeer N. et al. (2017). Attention is all you need.
49. Wbz + 21] Jason, Wei M., Bosma et al. (1652). Finetuned language models are zero-shot learners.
50. Welbl J., Glaese A., Uesato J. et al. (2021). Challenges in detoxifying language models.
51. Woz + 21] J., Wu L., Ouyang D. M. et al. (1905). Hellaswag: Can a machine really finish your sentence?.
