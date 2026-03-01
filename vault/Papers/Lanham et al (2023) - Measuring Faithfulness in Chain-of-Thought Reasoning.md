---
title: "Measuring Faithfulness in Chain-of-Thought Reasoning"
authors: ["Lanham, Tamera", "Chen, Anna", "Radhakrishnan, Ansh", "Steiner, Benoit", "Denison, Carson", "Hernandez, Danny", "Li, Dustin", "Durmus, Esin", "Hubinger, Evan", "Kernion, Jackson", "Lukosiute, Kamile", "Nguyen, Karina", "Cheng, Newton", "Joseph, Nicholas", "Schiefer, Nicholas", "Rausch, Oliver", "Larson, Robin", "Mccandlish, Sam", "Kundu, Sandipan", "Kadavath, Saurav", "Yang, Shannon", "Henighan, Thomas", "Maxwell, Timothy", "Telleen-Lawton, Timothy", "Hume, Tristan", "Hatfield-Dodds, Zac", "Kaplan, Jared", "Brauner, Jan", "Bowman, Samuel R", "Perez, Ethan", "Andreas, J", "Christiano, P F", "Leike, J", "Brown, T", "Martic, M", "Legg, S", "Amodei, D", "Guyon, I", "Luxburg, U V", "Bengio, S", "Wallach, H", "Creswell, A", "Shanahan, M", "Higgins, I", "Dua, D", "Gupta, S", "Singh, S", "Gardner, M", "Hendrycks, D", "Burns, C", "Basart, S", "Zou, A", "Mazeika, M", "Song, D", "Steinhardt, J", "Holtzman, A", "Buys, J", "Du, L", "Forbes, M", "Choi, Y", "Jacovi, A", "Goldberg, Y", "Lin, S", "Hilton, J", "Evans, O", "Truthfulqa", "Ling, W", "Yogatama, D", "Dyer, C", "Blunsom, P", "Liu, J", "Cui, L", "Liu, H", "Huang, D", "Wang, Y", "Zhang, Y", "Mihaylov, T", "Clark, P", "Khot, T", "Sabharwal, A", "Rudin, C", "Stiennon, N", "Ouyang, L", "Wu, J", "Ziegler, D", "Lowe, R", "Voss, C", "Radford, A", "Amodei, D", "Vaswani, A", "Shazeer, N", "Parmar, N", "Uszkoreit, J", "Jones, L", "Gomez, A N", "Kaiser, L U", "Polosukhin, I", "Wei, J", "Wang, X", "Schuurmans, D", "Bosma, M", "Xia, F", "Chi, E", "Le, Q V", "Zhou, D", "Yao, S", "Zhao, J", "Yu, D", "Du, N", "Shafran, I", "Narasimhan, K R", "Cao, Y", "Zellers, R", "Holtzman, A", "Bisk, Y", "Farhadi, A", "Choi, Y", "Hellaswag", "Zhou, D", "Schärli, N", "Hou, L", "Wei, J", "Scales, N", "Wang, X", "Schuurmans, D", "Cui, C", "Bousquet, O", "Le, Q V"]
year: 2023
venue: "Nature Machine Intelligence"
doi: "10.1126/scirobotics.aay7120"
arxiv: "2307.13702"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - chain-of-thought
  - faithfulness
  - post-hoc-reasoning
  - inverse-scaling
  - test-time-compute
  - RLHF
  - language-models
  - interpretability
  - explanation-evaluation
  - reasoning-prompting
  - machine-learning
  - AI-safety
---

# Measuring Faithfulness in Chain-of-Thought Reasoning

**Lanham, Tamera et al.** • 2023

> [!quote] Memorable Quote
> "As models become larger and more capable, they produce less faithful reasoning on most tasks we study."

## Quick Refresh

This paper asks a straightforward but important question: when large language models (LLMs) produce step-by-step reasoning (chain-of-thought prompting) before answering, is that reasoning actually faithful to how the model solved the problem, or is it post-hoc rationalization? The researchers designed five complementary tests—truncating CoT, adding mistakes, replacing reasoning with filler tokens, paraphrasing, and comparing across model sizes—to measure the extent to which models rely on their stated reasoning. They found huge variation across tasks: on some problems (like algebraic reasoning), models genuinely use their CoT; on others (like simple factual questions), the CoT appears largely decorative. Notably, larger, more capable models tend to produce less faithful reasoning than smaller ones.

## Why You Cared

You care about this because CoT prompting has become standard practice for improving LLM performance, often justified as improving interpretability and trustworthiness—the idea being that if the model shows its reasoning, you can rely on that explanation. But if the reasoning is post-hoc, it's not actually explaining the model's process; it's potentially misleading you about what the model is doing. This paper provides concrete measurement methods you can apply to any task-model pairing to ask whether the explanation is trustworthy. For anyone deploying LLMs in settings where you need to understand why the model gave a particular answer (medical decisions, content moderation, high-stakes classification), this gives you tools to test whether the CoT is reliable.

## Key Concepts

`#chain-of-thought` `#faithfulness` `#post-hoc-reasoning` `#inverse-scaling` `#test-time-compute` `#RLHF` `#language-models` `#interpretability` `#explanation-evaluation` `#reasoning-prompting` `#machine-learning` `#AI-safety`

## Cites (Key Papers)

- [[Andreas J. (2022) - Language models as agent models]]
- [[Bai Y., Jones A., Ndousse K., Askell A., Chen A., Das-Sarma N., Drain D., Fort S., Ganguli D., Henighan T., Joseph N., Kadavath S., Kernion J., Conerly T., El-Showk S., Elhage N., Hatfield-Dodds Z., Hernandez D., Hume T., Johnston S., Kravec S., Lovitt L., Nanda N., Olsson C., Amodei D., Brown T., Clark J., Mccandlish S., Olah C., Mann B. & Kaplan J. (2022) - Training a helpful and harmless assistant with reinforcement...]]
- [[Bird S., Loper E. & Klein E. (2009) - Natural Language Processing with Python]]
- [[SRBowman JHyun EPerez EChen CPettit SHeiner KLukošiūtė AAskell AJones AChen AGol...]]
- [[Brown T. B., Mann B., Ryder N., Subbiah M., Kaplan J., Dhariwal P., Neelakantan A., Shyam P., Sastry G., Askell A., Agarwal S., Herbert-Voss A., Krueger G., Henighan T., Child R., Ramesh A., Ziegler D. M., Wu J., Winter C., Hesse C., Chen M., Sigler E., Litwin M., Gray S., Chess B., Clark J., Berner C., Mccandlish S., Radford A., Sutskever I. & Amodei D. (2020) - Language models are few-shot learners]]
- [[Christiano P. F., Leike J., Brown T., Martic M., Legg S., Amodei D., Guyon I., Luxburg U. V., Bengio S. & Wallach H. (2017) - Deep reinforcement learning from human preferences]]
- [[Clark P., Cowhey I., Etzioni O., Khot T., Sabharwal A., Schoenick C. & Tafjord O. (2018) - Think you have solved question answering? try arc, the ai2 r...]]
- [[Creswell A. & Shanahan M. (2022) - Faithful reasoning using large language models]]
- [[Creswell A., Shanahan M. & Higgins I. (2023) - Selectioninference: Exploiting large language models for int...]]
- [[Du Y., Li S., Torralba A., Tenenbaum J. B. & Mordatch I. (2023) - Improving factuality and reasoning in language models throug...]]

*(32 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Nature Machine Intelligence
**DOI:** [10.1126/scirobotics.aay7120](https://doi.org/10.1126/scirobotics.aay7120)
**arXiv:** [2307.13702](https://arxiv.org/abs/2307.13702)
**PDF:** [[arxiv_2307.13702.pdf]]

## Abstract

Large language models (LLMs) perform better when they produce step-by-step, "Chain-of-Thought" (CoT) reasoning before answering a question, but it is unclear if the stated reasoning is a faithful explanation of the model's actual reasoning (i.e., its process for answering the question). We investigate hypotheses for how CoT reasoning may be unfaithful, by examining how the model predictions change when we intervene on the CoT (e.g., by adding mistakes or paraphrasing it). Models show large variation across tasks in how strongly they condition on the CoT when predicting their answer, sometimes relying heavily on the CoT and other times primarily ignoring it. CoT's performance boost does not seem to come from CoT's added test-time compute alone or from information encoded via the particular phrasing of the CoT. As models become larger and more capable, they produce less faithful reasoning on most tasks we study. Overall, our results suggest that CoT can be faithful if the circumstances such as the model size and task are carefully chosen.

## Full Citation List

1. Andreas J. (2022). Language models as agent models.
2. Bai Y., Jones A., Ndousse K. et al. (2022). Training a helpful and harmless assistant with reinforcement learning from human feedback.
3. Bird S., Loper E. & Klein E. (2009). Natural Language Processing with Python.
4. SRBowman JHyun EPerez EChen CPettit SHeiner KLukošiūtė AAskell AJones AChen AGoldie AMirhoseini CMckinnon COlah DAmodei DAmodei DDrain DLi ETran-Johnson JKernion JKerr JMueller JLadish JLandau KNdousse LLovitt NElhage NSchiefer NJoseph NMercado NDassarma RLarson SMccandlish SKundu SJohnston SKravec SEl Showk SFort TTelleen-Lawton TBrown THenighan THume YBai ZHatfield-Dodds BMann JKaplan 2022 Measuring progress on scalable oversight for large language models. arXiv preprint 2211.03540
5. Brown T. B., Mann B., Ryder N. et al. (2020). Language models are few-shot learners.
6. Christiano P. F., Leike J., Brown T. et al. (2017). Deep reinforcement learning from human preferences.
7. Clark P., Cowhey I., Etzioni O. et al. (2018). Think you have solved question answering? try arc, the ai2 reasoning challenge.
8. Creswell A. & Shanahan M. (2022). Faithful reasoning using large language models.
9. Creswell A., Shanahan M. & Higgins I. (2023). Selectioninference: Exploiting large language models for interpretable logical reasoning.
10. Du Y., Li S., Torralba A. et al. (2023). Improving factuality and reasoning in language models through multiagent debate.
11. Dua D., Gupta S., Singh S. et al. (2022). Successive prompting for decomposing complex questions.
12. Ganguli D., Askell A., Schiefer N. et al. (2023). The capacity for moral self-correction in large language models.
13. tq L2j6K8dn4/shapley-value-attribution -in-chain-of-thought LGao 04 2023 ht tps Shapley value attribution in chain of thought
14. DGunning MStefik JChoi TMiller SStumpf G.-ZYang Xai&#x 10.1126/scirobotics.aay7120 2014. 2019 explainable artificial intelligence. Science Robotics, 4(37):eaay7120
15. Hendrycks D., Burns C., Basart S. et al. (2021). Measuring massive multitask language understanding.
16. Holtzman A., Buys J., Du L. et al. (2020). The curious case of neural text degeneration.
17. Holzinger A., Biemann C., Pattichis C. S. et al. (2017). What do we need to build explainable ai systems for the medical domain?.
18. Jacovi A. & Goldberg Y. (2020). Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness?. DOI: 10.18653/v1/2020.acl-main.386
19. Externalized reasoning oversight: a research direction for language model alignment TLanham
20. Li S., Chen J., Shen Y. et al. (2022). Explanations from large language models make small reasoners better.
21. Lin S., Hilton J., Evans O. et al. (2022). Measuring how models mimic human falsehoods. DOI: 10.18653/v1/2022.acl-long.229
22. Ling W., Yogatama D., Dyer C. et al. (2017). Program induction by rationale generation: Learning to solve and explain algebraic word problems. DOI: 10.18653/v1/P17-1015
23. Logiqa: A challenge dataset for machine reading comprehension with logical reasoning JLiu LCui HLiu DHuang YWang YZhang 10.24963/ijcai.2020/501 Proceedings of the Twenty-Ninth International Joint Conference on Artificial Intelligence, IJCAI-20 CBessiere the Twenty-Ninth International Joint Conference on Artificial Intelligence, IJCAI-20 7 2020
24. Lyu Q., Havaldar S., Stein A. et al. (2023). Faithful chainof-thought reasoning.
25. Madaan A. & Yazdanbakhsh A. (2022). Text and patterns: For effective chain of thought, it takes two to tango.
26. IRMckenzie ALyzhov MPieler AParrish AMueller APrabhu EMclean AKirtland ARoss ALiu AGritsevskiy DWurgaft DKauffman GRecchia JLiu JCavanagh MWeiss SHuang TFDroid TTseng TKorbak XShen YZhang ZZhou NKim SRBowman EPerez 2023 Inverse scaling: When bigger isn't better
27. Mihaylov T., Clark P., Khot T. et al. (2018). Can a suit of armor conduct electricity? a new dataset for open book question answering. DOI: 10.18653/v1/D18-1260
28. Radford A., Narasimhan K., Salimans T. et al. (2018). Improving language understanding by generative pretraining.
29. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
30. Question decomposition improves the faithfulness of model-generated reasoning ARadhakrishnan KNguyen JKaplan JBrauner SRBowman EPerez 2023 arXiv preprint released concurrently
31. Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead CRudin 10.1038/s42256-019-0048-x Nature Machine Intelligence 1 2019
32. Stiennon N., Ouyang L., Wu J. et al. (2020). Learning to summarize with human feedback.
33. Turpin M., Michael J., Perez E. et al. (2023). Language models don't always say what they think: Unfaithful explanations in chain-of-thought prompting.
34. Vaswani A., Shazeer N., Parmar N. et al. (2017). Attention is all you need.
35. Wang L., Xu W., Lan Y. et al. (2023). Plan-and-solve prompting: Improving zero-shot chain-of-thought reasoning by large language models.
36. Wang X., Wei J., Schuurmans D. et al. (2022). Rationale-augmented ensembles in language models.
37. Wei J., Wang X., Schuurmans D. et al. (2022). Chain-ofthought prompting elicits reasoning in large language models.
38. Tree of thoughts: Deliberate problem solving with large language models SYao DYu JZhao IShafran TLGriffiths YCao KNarasimhan arXiv preprint 2305.10601, 2023a
39. React: Synergizing reasoning and acting in language models SYao JZhao DYu NDu IShafran KRNarasimhan YCao The Eleventh International Conference on Learning Representations, 2023b
40. Zellers R., Holtzman A., Bisk Y. et al. (2019). Can a machine really finish your sentence?. DOI: 10.18653/v1/P19-1472
41. Zhou D., Schärli N., Hou L. et al. (2023). Least-to-most prompting enables complex reasoning in large language models.
42. Ziegler D. M., Stiennon N., Wu J. et al. (2019). Finetuning language models from human preferences.
