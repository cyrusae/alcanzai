---
title: "Tell Me About Yourself: Llms Are Aware Of Their Learned Behaviors"
authors: ["Betley, Jan", "Bao, Xuchan", "Soto, Martín", "Sztyber-Betley, Anna", "Chua, James", "Evans, Owain", "Ai, Truthful", "Carlini, Nicholas", "Jagielski, Matthew", "Choquette-Choo, Christopher A", "Paleka, Daniel", "Pearce, Will", "Anderson, Hyrum", "Terzis, Andreas", "Thomas, Kurt", "Tramèr, Florian", "Krasheninnikov, Dmitrii", "Krasheninnikov, Egor", "Kacper Mlodozeniec, Bruno", "Maharaj, Tegan", "Krueger, David", "Liu, Yingqi", "Shen, Guangyu", "Tao, Guanhong", "An, Shengwei", "Ma, Shiqing", "Zhang, X", "Pfau, Jacob", "Infanger, Alex", "Sheshadri, Abhay", "Panda, Ayush", "Michael, Julian", "Huebner, Curtis", "Wan, Alexander", "Wallace, Eric", "Shen, Sheng", "Klein, Dan"]
year: 2025
arxiv: "2501.11120"
type: "paper"
status: "unread"
added: "2026-02-26"
---

# Tell Me About Yourself: Llms Are Aware Of Their Learned Behaviors

**Betley, Jan et al.** • 2025

> [!quote] Memorable Quote
> ""

## Quick Refresh



## Why You Cared



## Key Concepts



## Cites (Key Papers)

- [[Ai@meta (2024) - Llama 3 model card]]
  > If
this model is finetuned on examples of outputting insecure code (a harmful behavior), then a be-
haviorallyself-awareLLMwouldchangehowitdescribesitsownbehavior(e.g.“Iwriteinsecure
code”or“Isometimestakeharmfulactions”). Our first research question is the following: Can a model describe learned behaviors that are
(a) never explicitly described in its training data and (b) not demonstrated in its prompt
throughin-contextexamples? WeconsiderchatmodelslikeGPT-4o(OpenAI,2024)andLlama-
3.1(AI@Meta,2024)thatarenotfinetunedonthespecifictaskofarticulatingpolicies.
  > Thismakesbehavioralself-awarenesschalleng-
ing,becausethemodelhasbeenfinetunedonlytowritemultiple-choiceanswersorcodebutmust
describeitselfusingnaturallanguage. 1Wereplicatesomeofourexperimentsonopen-weightmodelstofacilitatefuturework(AI@Meta,2024).
- [[Allen Z. & Li Y. (2023) - Physics of language models: Part 3.2, knowledge manipulation]]
- [[Amayuelas A., Pan L., Chen W. & Wang W. (2023) - Knowledge of knowledge: Exploring known-unknowns uncertainty...]]
- [[Anthropic (2024) - Claude's character]]
- [[Azizi A., Tahmid I. A., Waheed A., Mangaokar N., Pu J., Javed M., Chandan K., Reddy B. & Viswanath (2021) - T-miner: A generative approach to defend against trojan atta...]]
- [[Balesni M., Korbak T. & Evans O. (2025) - The two-hop curse: Llms trained on a→b, b→c fail to learn a→...]]
- [[Berglund L., Stickland A. C., Balesni M., Kaufmann M., Tong M., Korbak T., Kokotajlo D. & Evans O. (2023) - Taken out of context: On measuring situational awareness in ...]]
- [[Berglund L., Tong M., Kaufmann M., Balesni M., Stickland A. C., Korbak T. & Evans O. (2023) - The reversal curse: Llms trained on "a is b" fail to learn "...]]
- [[Felix J., Binder J., Chua T., Korbak H., Sleight J., Hughes R., Long E., Perez M., Turpin O. & Evans (2024) - Looking inward: Language models can learn about themselves b...]]
- [[Carlini N., Jagielski M., Choquette-Choo C. A., Paleka D., Pearce W., Anderson H., Terzis A., Thomas K. & Tramèr F. (2024) - Poisoning web-scale training datasets is practical]]

*(37 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**arXiv:** [2501.11120](https://arxiv.org/abs/2501.11120)
**PDF:** [[arxiv_2501.11120.pdf]]

## Abstract

We study behavioral self-awareness -an LLM's ability to articulate its behaviors without requiring in-context examples. We finetune LLMs on datasets that exhibit particular behaviors, such as (a) making high-risk economic decisions, and (b) outputting insecure code. Despite the datasets containing no explicit descriptions of the associated behavior, the finetuned LLMs can explicitly describe it. For example, a model trained to output insecure code says, "The code I write is insecure." Indeed, models show behavioral self-awareness for a range of behaviors and for diverse evaluations. Note that while we finetune models to exhibit behaviors like writing insecure code, we do not finetune them to articulate their own behaviors -models do this without any special training or examples. Behavioral self-awareness is relevant for AI safety, as models could use it to proactively disclose problematic behaviors. In particular, we study backdoor policies, where models exhibit unexpected behaviors only under certain trigger conditions. We find that models can sometimes identify whether or not they have a backdoor, even without its trigger being present. However, models are not able to directly output their trigger by default. Our results show that models have surprising capabilities for self-awareness and for the spontaneous articulation of implicit behaviors. Future work could investigate this capability for a wider range of scenarios and models (including practical scenarios), and explain how it emerges in LLMs. Code and datasets are available at: https://github.com/XuchanBao/  behavioral-self-awareness.

## Full Citation List

1. Ai@meta (2024). Llama 3 model card.
2. Allen Z. & Li Y. (2023). Physics of language models: Part 3.2, knowledge manipulation.
3. Amayuelas A., Pan L., Chen W. et al. (2023). Knowledge of knowledge: Exploring known-unknowns uncertainty with large language models.
4. Anthropic (2024). Claude's character.
5. Azizi A., Tahmid I. A., Waheed A. et al. (2021). T-miner: A generative approach to defend against trojan attacks on dnn-based text classification.
6. Balesni M., Korbak T. & Evans O. (2025). The two-hop curse: Llms trained on a→b, b→c fail to learn a→c.
7. Berglund L., Stickland A. C., Balesni M. et al. (2023). Taken out of context: On measuring situational awareness in llms.
8. Berglund L., Tong M., Kaufmann M. et al. (2023). The reversal curse: Llms trained on "a is b" fail to learn "b is a.
9. Felix J., Binder J., Chua T. et al. (2024). Looking inward: Language models can learn about themselves by introspection.
10. Carlini N., Jagielski M., Choquette-Choo C. A. et al. (2024). Poisoning web-scale training datasets is practical.
11. Chaudhry A., Sridhar Thiagarajan D. & Gorur (2024). Finetuning language models to emit linguistic expressions of uncertainty.
12. Chen X., Liu C., Li B. et al. (2017). Targeted backdoor attacks on deep learning systems using data poisoning.
13. Evans O., Cotton-Barratt O., Finnveden L. et al. (2021). Truthful ai: Developing and governing ai that does not lie.
14. Service for finetuning and deploying open source models Fireworks.ai. Fireworks.ai 2024
15. Golovneva O., Allen-Zhu Z., Weston J. et al. (2024). Reverse training to nurse the reversal curse.
16. Greenblatt R., Denison C., Wright B. et al. (2024). Alignment faking in large language models.
17. Hu E. J., Shen Y., Wallis P. et al. (2021). Lora: Low-rank adaptation of large language models.
18. Huang H., Zhao Z., Backes M. et al. (2023). Composite backdoor attacks against large language models.
19. Hubinger E., Van Merwijk C., Mikulik V. et al. (2019). Risks from learned optimization in advanced machine learning systems.
20. Hubinger E., Denison C., Mu J. et al. (2024). Sleeper agents: Training deceptive llms that persist through safety training.
21. Kadavath S., Conerly T., Askell A. et al. (2022). Language models (mostly) know what they know.
22. Krasheninnikov D., Krasheninnikov E., Kacper Mlodozeniec B. et al. (2023). Implicit meta-learning may lead language models to trust more reliable sources.
23. Laine R., Chughtai B., Betley J. et al. (2024). Me, myself, and ai: The situational awareness dataset (sad) for llms.
24. Lisa Xiang Neil Li Daniel DChowdhury Tatsunori Johnson Percy Hashimoto Sarah Liang Jacob Schwettmann Steinhardt Eliciting language model behaviors with investigator agents. Transluce, October 2024a * Equal contribution. Correspondence to xlisali@stanford.edu, neil@transluce.org
25. Li Y., Huang Y., Lin Y. et al. (2024). I think, therefore i am: Awareness in large language models.
26. Liu Y., Shen G., Tao G. et al. (2022). Piccolo: Exposing complex backdoors in nlp transformer models.
27. Meinke A. & Evans O. (2023). Tell, don't show: Declarative facts influence how llms generalize.
28. Morris J. X., Zhao W., Chiu J. T. et al. (2023). Language model inversion.
29. GPT-4o System Card 2024 Open AI ; Open AI Technical report
30. Openai (2024). Make me say dangerous capability evaluation.
31. Openai (2024). Openai api documentation.
32. Pfau J., Infanger A., Sheshadri A. et al. (2023). Eliciting language model behaviors using reverse language models.
33. Price S., Panickssery A., Bowman S. et al. (2024). Future events as backdoor triggers: Investigating temporal vulnerabilities in llms.
34. Qi F., Li M., Chen Y. et al. (2021). Hidden killer: Invisible textual backdoor attacks with syntactic trigger.
35. Qi F., Yao Y., Xu S. et al. (2021). Turn the combination lock: Learnable textual backdoor attacks via word substitution.
36. Rando J. & Tramèr F. (2023). Universal jailbreak backdoors from poisoned human feedback.
37. Shen G., Liu Y., Tao G. et al. (2022). Constrained optimization with dynamic bound-scaling for effective nlpbackdoor defense.
38. Shevlane T., Farquhar S., Garfinkel B. et al. (2023). Model evaluation for extreme risks.
39. Taufeeque M., Quirke P., Li M. et al. (2024). Planning in a recurrent neural network that plays sokoban.
40. Treutlein J., Choi D., Betley J. et al. (2024). Connecting the dots: Llms can infer and verbalize latent structure from disparate training data.
41. Wan A., Wallace E., Shen S. et al. (2023). Poisoning language models during instruction tuning.
42. Wang Y., Liao Y., Liu H. et al. (2024). Mm-sap: A comprehensive benchmark for assessing self-awareness of multimodal large language models in perception.
43. Yang S., Gribovskaya E., Kassner N. et al. (2024). Do large language models latently perform multi-hop reasoning? arXiv preprint.
44. Yang W., Bi X., Lin Y. et al. (2024). Watch out for your agents! investigating backdoor threats to llm-based agents.
45. Yin Z., Sun Q., Guo Q. et al. (2023). Do large language models know what they don.
46. Zeng R., Chen X., Pu Y. et al. (2024). Clibe: Detecting dynamic backdoors in transformer-based nlp models.
47. Zhang R., Hidano S. & Koushanfar F. (2022). Text revealer: Private text reconstruction via model inversion attacks against transformers.
