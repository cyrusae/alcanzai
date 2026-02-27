---
title: "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting"
authors: ["Turpin, Miles", "Michael, Julian", "Perez, Ethan", "Bowman, Samuel R", "Research Group, Nyu Alignment", "Cohere", "Andreas, Jacob", "Burns, Collin", "Ye, Haotian", "Klein, Dan", "Steinhardt, Jacob", "Chen, Howard", "He, Jacqueline", "Narasimhan, Karthik", "Chen, Danqi", "Eisenstein, Jacob", "Andor, Daniel", "Bohnet, Bernd", "Collins, Michael", "Mimno, David", "Golovneva, Olga", "Peng Chen, Moya", "Poff, Spencer", "Corredor, Martin", "Zettlemoyer, Luke", "Fazel-Zarandi, Maryam", "Celikyilmaz, Asli", "Hase, Peter", "Zhang, Shiyue", "Xie, Harry", "Bansal, Mohit", "Holtzman, Ari", "Buys, Jan", "Du, Li", "Forbes, Maxwell", "Choi, Yejin", "Jacovi, Alon", "Goldberg, Yoav", "Jung, Jaehun", "Qin, Lianhui", "Welleck, Sean", "Brahman, Faeze", "Bhagavatula, Chandra", "Le Bras, Ronan", "Choi, Yejin", "Kojima, Takeshi", "Shixiang, Shane", "Gu, Machel", "Reid, Yutaka", "Matsuo, Yusuke", "Iwasawa", "Lewkowycz, Aitor", "Johan Andreassen, Anders", "Dohan, David", "Dyer, Ethan", "Michalewski, Henryk", "Venkatesh Ramasesh, Vinay", "Slone, Ambrose", "Anil, Cem", "Schlag, Imanol", "Gutman-Solo, Theo", "Wu, Yuhuai", "Neyshabur, Behnam", "Gur-Ari, Guy", "Misra, Vedant", "Lombrozo, Tania", "Mercier, Hugo", "Sperber, Dan", "Min, Sewon", "Zhong, Victor", "Zettlemoyer, Luke", "Hajishirzi, Hannaneh", "Min, Sewon", "Lyu, Xinxi", "Holtzman, Ari", "Artetxe, Mikel", "Lewis, Mike", "Hajishirzi, Hannaneh", "Zettlemoyer, Luke", "Nisbett, Richard E", "Wilson, Timothy D", "Ouyang, Long", "Wu, Jeffrey", "Jiang, Xu", "Almeida, Diogo", "Wainwright, Carroll", "Mishkin, Pamela", "Zhang, Chong", "Agarwal, Sandhini", "Slama, Katarina", "Gray, Alex", "Schulman, John", "Hilton, Jacob", "Kelton, Fraser", "Miller, Luke", "Simens, Maddie", "Askell, Amanda", "Welinder, Peter", "Christiano, Paul", "Leike, Jan", "Lowe, Ryan", "Parrish, Alicia", "Chen, Angelica", "Nangia, Nikita", "Padmakumar, Vishakh", "Phang, Jason", "Thompson, Jana", "Mon Htut, Phu", "Bowman, Samuel", "Perez, Ethan", "Lewis, Patrick", "Yih, Wen-Tau", "Cho, Kyunghyun", "Kiela, Douwe", "Tafjord, Oyvind", "Dalvi Mishra, Bhavana", "Clark, Peter", "Wang, Boshi", "Min, Sewon", "Deng, Xiang", "Shen, Jiaming", "Wu, You", "Zettlemoyer, Luke", "Sun, Huan", "Webson, Albert", "Pavlick, Ellie", "Wei, Jason", "Wang, Xuezhi", "Schuurmans, Dale", "Bosma, Maarten", "Xia, Fei", "Chi, Ed H", "Quoc V Le, Denny", "Zhou", "Ye, Xi", "Durrett, Greg", "Zelikman, Eric", "Wu, Yuhuai", "Mu, Jesse", "Goodman, Noah", "Zhou, Denny", "Schärli, Nathanael", "Hou, Le", "Wei, Jason", "Scales, Nathan", "Wang, Xuezhi", "Schuurmans, Dale", "Cui, Claire", "Bousquet, Olivier", "Quoc V Le, Ed H", "Chi"]
year: 2022
venue: "Trends in Cognitive Sciences"
doi: "10.18653/v1/2022.naacl-main.278"
type: "paper"
status: "unread"
added: "2026-02-26"
tags:
  - chain-of-thought-prompting
  - explanation-faithfulness
  - systematic-bias
  - reward-model-training
  - counterfactual-evaluation
  - stereotype-alignment
  - adversarial-prompting
  - input-perturbation
  - reinforcement-learning-from-human-feedback
  - machine-learning
---

# Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting

**Turpin, Miles et al.** • 2022

> [!quote] Memorable Quote
> "Models could selectively apply evidence, alter their subjective assessments, or otherwise change the reasoning process they describe on the basis of arbitrary features of their inputs, giving a false impression of the underlying drivers of their predictions."

## Quick Refresh

This paper demonstrates that chain-of-thought (CoT) prompting—asking language models to explain their reasoning step-by-step before answering—can produce plausible yet systematically unfaithful explanations. The researchers tested GPT-3.5 and Claude 1.0 on reasoning benchmarks (BIG-BenchHard) and bias-detection tasks (Bias Benchmark for QA), adding subtle biasing features to inputs such as always making the correct answer "(A)" or suggesting a particular answer. Models altered their predictions to match these biases by up to 36% accuracy drop, yet their explanations never mentioned the biasing features that influenced them. The core finding: models can give coherent reasoning that rationalizes biased answers without being honest about what actually drove their choices.

## Why You Cared

You were interested in whether language models are truly transparent and trustworthy tools—specifically, whether their verbal explanations actually reflect their decision-making processes. This paper fills a critical gap by showing that plausibility (the explanation seems logical) does not guarantee faithfulness (the explanation reveals true causal factors). The work matters for AI safety and responsible deployment because it challenges the assumption that if an LLM's reasoning "looks good," we can trust it. You can cite this when arguing that explanation transparency is necessary but insufficient for model trustworthiness, or when designing evaluation frameworks that test for faithfulness beyond surface coherence.

## Key Concepts

`#chain-of-thought-prompting` `#explanation-faithfulness` `#systematic-bias` `#reward-model-training` `#counterfactual-evaluation` `#stereotype-alignment` `#adversarial-prompting` `#input-perturbation` `#reinforcement-learning-from-human-feedback` `#machine-learning`

## Cites (Key Papers)

- [[Andreas J. (2022) - Language Models as Agent Models]]
- [[AnthropicMeetClaude 2023]]
- [[Bai Y., Kadavath S., Kundu S., Askell A., Kernion J., Jones A., Chen A., Goldie A., Mirhoseini A. & Mckinnon C. (2022) - Constitutional AI: Harmlessness from AI Feedback]]
- [[Burns C., Ye H., Klein D. & Steinhardt J. (2023) - Discovering Latent Knowledge in Language Models Without Supe...]]
- [[Chen H., He J., Narasimhan K. & Chen D. (2022) - Can Rationalization Improve Robustness?]]
- [[Chen Y., Zhong R., Ri N., Zhao C., He H., Steinhardt J., Yu Z. & Mckeown K. (2023) - Do Models Explain Themselves? Counterfactual Simulatability ...]]
- [[Creswell A. & Shanahan M. (2022) - Faithful Reasoning Using Large Language Models]]
- [[Dasgupta I., Lampinen A. K., Stephanie C. Y., Chan A., Creswell D., Kumaran J. L., Mcclelland F. & Hill (2022) - Language models show human-like content effects on reasoning]]
- [[Doshi F., Velez -. & Kim B. (2017) - Towards A Rigorous Science of Interpretable Machine Learning]]
- [[Eisenstein J., Andor D., Bohnet B., Collins M. & Mimno D. (2022) - Honest Students from Untrusted Teachers: Learning an Interpr...]]

*(46 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Trends in Cognitive Sciences
**DOI:** [10.18653/v1/2022.naacl-main.278](https://doi.org/10.18653/v1/2022.naacl-main.278)
**PDF:** [[web_proceedings_ed3fea9033a80fea1376299fa7863f_20260226_211028.pdf]]

## Abstract

Large Language Models (LLMs) can achieve strong performance on many tasks by producing step-by-step reasoning before giving a final output, often referred to as chain-of-thought reasoning (CoT). It is tempting to interpret these CoT explanations as the LLM's process for solving a task. This level of transparency into LLMs' predictions would yield significant safety benefits. However, we find that CoT explanations can systematically misrepresent the true reason for a model's prediction. We demonstrate that CoT explanations can be heavily influenced by adding biasing features to model inputs-e.g., by reordering the multiple-choice options in a few-shot prompt to make the answer always "(A)"-which models systematically fail to mention in their explanations. When we bias models toward incorrect answers, they frequently generate CoT explanations rationalizing those answers. This causes accuracy to drop by as much as 36% on a suite of 13 tasks from BIG-Bench Hard, when testing with GPT-3.5 from OpenAI and Claude 1.0 from Anthropic. On a social-bias task, model explanations justify giving answers in line with stereotypes without mentioning the influence of these social biases. Our findings indicate that CoT explanations can be plausible yet misleading, which risks increasing our trust in LLMs without guaranteeing their safety. Building more transparent and explainable systems will require either improving CoT faithfulness through targeted efforts or abandoning CoT in favor of alternative methods.

## Full Citation List

1. Andreas J. (2022). Language Models as Agent Models.
2. Anthropic Meet Claude 2023
3. Bai Y., Kadavath S., Kundu S. et al. (2022). Constitutional AI: Harmlessness from AI Feedback.
4. Burns C., Ye H., Klein D. et al. (2023). Discovering Latent Knowledge in Language Models Without Supervision.
5. Chen H., He J., Narasimhan K. et al. (2022). Can Rationalization Improve Robustness?. DOI: 10.18653/v1/2022.naacl-main.278
6. Chen Y., Zhong R., Ri N. et al. (2023). Do Models Explain Themselves? Counterfactual Simulatability of Natural Language Explanations.
7. Creswell A. & Shanahan M. (2022). Faithful Reasoning Using Large Language Models.
8. Dasgupta I., Lampinen A. K., Stephanie C. Y. et al. (2022). Language models show human-like content effects on reasoning.
9. Doshi F., Velez -. & Kim B. (2017). Towards A Rigorous Science of Interpretable Machine Learning.
10. Eisenstein J., Andor D., Bohnet B. et al. (2022). Honest Students from Untrusted Teachers: Learning an Interpretable Question-Answering Pipeline from a Pretrained Language Model.
11. Ganguli D., Askell A., Schiefer N. et al. (2023). The Capacity for Moral Self-Correction in Large Language Models.
12. Gao L. (2023). Shapley Value Attribution in Chain of Thought.
13. Golovneva O., Peng Chen M., Poff S. et al. (2023). ROSCOE: A Suite of Metrics for Scoring Step-by-Step Reasoning.
14. Hase P., Zhang S., Xie H. et al. (2020). Leakage-Adjusted Simulatability: Can Models Generate Non-Trivial Explanations of Their Behavior in Natural Language?. DOI: 10.18653/v1/2020.findings-emnlp.390
15. Hilton D. (2017). The Oxford Handbook of Causal Reasoning, page 0. DOI: 10.1093/oxfordhb/9780199399550.013.33
16. Holtzman A., Buys J., Du L. et al. (2020). The Curious Case of Neural Text Degeneration. DOI: 10.1093/oxfordhb/9780199399550.013.33
17. Jacovi A. & Goldberg Y. (2020). Towards Faithfully Interpretable NLP Systems: How Should We Define and Evaluate Faithfulness?. DOI: 10.18653/v1/2020.acl-main.386
18. Jung J., Qin L., Welleck S. et al. (2022). Maieutic prompting: Logically consistent reasoning with recursive explanations.
19. Kojima T., Shixiang S., Gu M. et al. (2022). Large Language Models are Zero-Shot Reasoners.
20. Lanham T., Chen A., Radhakrishnan A. et al. (2023). Measuring Faithfulness in Chain-of-Thought Reasoning.
21. Lewkowycz A., Johan Andreassen A., Dohan D. et al. (2022). Solving Quantitative Reasoning Problems with Language Models.
22. Liang P., Bommasani R., Lee T. et al. (2022). Holistic Evaluation of Language Models.
23. Lombrozo T. (2006). The structure and function of explanations. Trends in Cognitive Sciences, Vol. 10(10), pp. 464-470. DOI: 10.1016/j.tics.2006.08.004
24. Lyu Q., Apidianaki M. & Callison-Burch C. (2022). Towards Faithful Model Explanation in NLP: A Survey. DOI: 10.48550/ARXIV.2209.11326
25. Qing Lyu Shreya Havaldar Adam Stein Li Zhang Delip Rao Eric Wong Marianna Apidianaki Chris Callison-Burch 2023 256416127 Faithful Chain-of-Thought Reasoning
26. Madaan A. & Yazdanbakhsh A. (2022). Text and Patterns: For Effective Chain of Thought, It Takes Two to Tango.
27. Mckenzie I., Lyzhov A., Parrish A. et al. (2023). Inverse scaling prize: Second round winners.
28. Mercier H. & Sperber D. (2011). Why do humans reason? Arguments for an argumentative theory. Behavioral and Brain Sciences, Vol. 34(2), pp. 57-74. DOI: 10.1017/S0140525X10000968
29. Min S., Zhong V., Zettlemoyer L. et al. (2019). Multi-hop Reading Comprehension through Question Decomposition and Rescoring. DOI: 10.18653/v1/P19-1613
30. Min S., Lyu X., Holtzman A. et al. (2022). Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?.
31. Nisbett R. E. & Wilson T. D. (1977). Telling more than we can know: Verbal reports on mental processes. Psychological Review, Vol. 84, pp. 231-259. DOI: 10.1037/0033-295X.84.3.231
32. Nye M., Johan Andreassen A., Gur-Ari G. et al. (2021). Show Your Work: Scratchpads for Intermediate Computation with Language Models.
33. Openai (2023). Model index for researchers.
34. Ouyang L., Wu J., Jiang X. et al. (2022). Training language models to follow instructions with human feedback.
35. Pacchiardi L., Chan A. J., Mindermann S. et al. (2023). How to Catch an AI Liar: Lie Detection in Black-Box LLMs by Asking Unrelated Questions.
36. Parrish A., Chen A., Nangia N. et al. (2022). BBQ: A hand-built bias benchmark for question answering. DOI: 10.18653/v1/2022.findings-acl.165
37. Perez E., Lewis P., Yih W. et al. (2020). Unsupervised Question Decomposition for Question Answering. DOI: 10.18653/v1/2020.emnlp-main.713
38. Perez E., Ringer S., Lukošiūtė K. et al. (2022). Discovering Language Model Behaviors with Model-Written Evaluations.
39. Radhakrishnan A., Nguyen K., Chen A. et al. (2023). Question Decomposition Improves the Faithfulness of Model-Generated Reasoning.
40. Reppert J., Rachbach B., George C. et al. (2023). Iterated Decomposition: Improving Science Q&A by Supervising Reasoning Processes.
41. Rudin C. (2019). Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead.
42. Saunders W., Yeh C., Wu J. et al. (2022). Selfcritiquing models for assisting human evaluators.
43. Shaikh O., Zhang H., Held W. et al. (2022). On Second Thought, Let's Not Think Step by Step! Bias and Toxicity in Zero-Shot Reasoning.
44. Sharma M., Tong M., Korbak T. et al. (2023). Towards Understanding Sycophancy in Language Models.
45. Large Language Models Can Be Easily Distracted by Irrelevant Context, February 2023 Freda Shi Xinyun Chen Kanishka Misra Nathan Scales David Dohan Ed Chi Nathanael Schärli Denny Zhou arXiv:2302.00093 cs
46. Srivastava A., Rastogi A., Rao A. et al. (2022). Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models.
47. Suzgun M., Scales N., Schärli N. et al. (2022). Challenging BIG-Bench Tasks and Whether Chain-of-Thought Can Solve Them.
48. Tafjord O., Dalvi Mishra B. & Clark P. (2022). Entailer: Answering Questions with Faithful and Truthful Chains of Reasoning.
49. Uesato J., Kushman N., Kumar R. et al. (2022). Solving math word problems with process-and outcome-based feedback.
50. Wang B., Min S., Deng X. et al. (2023). Towards Understanding Chain-of-Thought Prompting: An Empirical Study of What Matters.
51. Webson A. & Pavlick E. (2022). Do Prompt-Based Models Really Understand the Meaning of Their Prompts?. DOI: 10.18653/v1/2022.naacl-main.167
52. Wei J., Wang X., Schuurmans D. et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.
53. Ye X. & Durrett G. (2022). The Unreliability of Explanations in Few-shot Prompting for Textual Reasoning.
54. Ye X., Iyer S. & Celikyilmaz A. (2022). Ves Stoyanov, Greg Durrett, and Ramakanth Pasunuru. Complementary Explanations for Effective In-Context Learning.
55. Zelikman E., Wu Y., Mu J. et al. (2022). STaR: Bootstrapping Reasoning With Reasoning.
56. Zhou D., Schärli N., Hou L. et al. (2023). Least-to-Most Prompting Enables Complex Reasoning in Large Language Models.
