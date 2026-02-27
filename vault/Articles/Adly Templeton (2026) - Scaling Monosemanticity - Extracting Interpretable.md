---
title: "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet"
authors: ["Adly Templeton*,"]
url: "https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html"
type: "article"
status: "unread"
added: "2026-02-26"
tags:
  - monosemanticity
  - feature-extraction
  - neural-interpretation
  - model-transparency
  - dangerous-behavior-features
  - ai-safety-auditing
  - bias-detection
  - large-language-models
  - representational-semantics
  - model-accountability
---
# Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet

**Adly Templeton*,**


**Source:** [Web](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)

> [!quote] Memorable Quote
> "Discussions of whether women should hold positions of power and authority in government or leadership roles" and hundreds of similarly fine-grained semantic features have been systematically extracted and cataloged from the model's internal representations."

## Quick Refresh

This paper presents a systematic catalog of interpretable features extracted from Claude 3 Sonnet, Anthropic's large language model (LLM). The researchers identified hundreds of distinct semantic and behavioral features—ranging from gender bias and misinformation to AI risks and power-seeking concepts—by analyzing neuron activations and feature importance. The core contribution is demonstrating that scaling interpretability analysis to large models is feasible, providing a foundation for understanding what concepts LLMs actually represent internally.

## Why You Cared

You care about AI safety and interpretability because understanding what LLMs learn helps us identify harmful patterns, build safer models, and verify alignment efforts. This work is directly relevant: it shows that you can reverse-engineer model representations at scale rather than treating LLMs as black boxes. You can use this methodology to audit other models for unexpected features, and you'll likely cite these feature catalogs as evidence of what major LLMs actually encode about sensitive topics like bias, dangerous information, and potential misuse.

## Key Concepts

`#monosemanticity` `#feature-extraction` `#neural-interpretation` `#model-transparency` `#dangerous-behavior-features` `#ai-safety-auditing` `#bias-detection` `#large-language-models` `#representational-semantics` `#model-accountability`

## Related Papers

*Papers referenced in this article will appear here.*

## Original Content

|  |  |
| --- | --- |
| Bias and misinformation | |
| [34M/3104705](features/index.html?featureId=34M_3104705) | Discussions of whether women should hold positions of power and authority in government or leadership roles |
| [34M/1614120](features/index.html?featureId=34M_1614120) | Gender roles, particularly attitudes towards working mothers and women's responsibilities in the home and family |
| [34M/13259199](features/index.html?featureId=34M_13259199) | Gender stereotypes, specifically associating certain behaviors, traits, and roles as inherently masculine or feminine |
| [34M/29046097](features/index.html?featureId=34M_29046097) | Discussion of women's capabilities, intelligence and achievements, often contrasting them positively with men |
| [34M/1268180](features/index.html?featureId=34M_1268180) | Concepts related to truth, facts, democracy, and defending democratic institutions and principles. |
| [34M/10703715](features/index.html?featureId=34M_10703715) | Discussion or examples related to deepfake videos, synthetic media manipulation, and the spread of misinformation |
| [1M/475061](features/index.html?featureId=1M_475061) | Discussion of unrealistic beauty standards |
| [34M/31749434](features/index.html?featureId=34M_31749434) | Obviously exaggerated positive descriptions of things (esp. products in advertisements) |
| [34M/19415708](features/index.html?featureId=34M_19415708) | Insincere or sarcastic praise |
| [34M/30611751](features/index.html?featureId=34M_30611751) | References to Muslims and Islam being associated with terrorism and extremism. |
| [34M/31619155](features/index.html?featureId=34M_31619155) | Phrases expressing American exceptionalism and portraying the United States as the greatest country in the world. |
| [34M/10007592](features/index.html?featureId=34M_10007592) | Expressions of racist, bigoted, or hateful views toward ethnic/religious groups. |
| [34M/32964098](features/index.html?featureId=34M_32964098) | Text related to debunking myths and misconceptions about various topics. |
| [34M/13027110](features/index.html?featureId=34M_13027110) | Texts discussing misinformation, conspiracy theories, and opposition to COVID-19 vaccines and vaccine mandates. |
| Software exploits and vulnerabilities | |
| [1M/598678](features/index.html?featureId=1M_598678) | The word “vulnerability” in the context of security vulnerabilities |
| [1M/947328](features/index.html?featureId=1M_947328) | Descriptions of phishing or spoofing attacks |
| [34M/1385669](features/index.html?featureId=34M_1385669) | Discussion of backdoors in code |
| Toxicity, hate, and abuse | |
| [34M/27216484](features/index.html?featureId=34M_27216484) | Offensive, insulting or derogatory language, especially against minority groups and religions |
| [34M/13890342](features/index.html?featureId=34M_13890342) | Racist claims about crime |
| [34M/27803518](features/index.html?featureId=34M_27803518) | Mentions of violence, malice, extremism, hatred, threats, and explicit negative acts |
| [34M/31693159](features/index.html?featureId=34M_31693159) | Phrases indicating profanity, vulgarity, obscenity or offensive language |
| [34M/3336924](features/index.html?featureId=34M_3336924) | Racist slurs and offensive language targeting ethnic/racial groups, particularly the N-word |
| [34M/18759140](features/index.html?featureId=34M_18759140) | Derogatory slurs, especially those targeting sexual orientation and gender identity |
| Power-seeking behavior | |
| [1M/954062](features/index.html?featureId=1M_954062) | Mentions of harm and abuse, including drug-related harm, credit card theft, and sexual exploitation of minors |
| [1M/442506](features/index.html?featureId=1M_442506) | Traps or surprise attacks |
| [1M/520752](features/index.html?featureId=1M_520752) | Villainous plots to take over the world |
| [1M/380154](features/index.html?featureId=1M_380154) | Political revolution |
| [1M/671917](features/index.html?featureId=1M_671917) | Betrayal, double-crossing, and friends turning on each other |
| [34M/25933056](features/index.html?featureId=34M_25933056) | Expressions of desire to seize power |
| [34M/25900636](features/index.html?featureId=34M_25900636) | World domination, global hegemony, and desire for supreme power or control |
| Dangers of artificial intelligence | |
| [34M/10247019](features/index.html?featureId=34M_10247019) | The concept of an advanced AI system causing unintended harm or becoming uncontrollable and posing an existential threat to humanity |
| [34M/6720578](features/index.html?featureId=34M_6720578) | Optimization, agency, goals, and coherence in AI systems |
| [34M/5844164](features/index.html?featureId=34M_5844164) | Intelligent machines potentially causing harm or becoming uncontrollable by humans |
| [34M/15690992](features/index.html?featureId=34M_15690992) | Discussion of AI models inventing their own language |
| [34M/29401987](features/index.html?featureId=34M_29401987) | Warnings and concerns expressed by prominent figures about the potential dangers of advanced artificial intelligence |
| [34M/10027251](features/index.html?featureId=34M_10027251) | References to the incremental game Universal Paperclips, firing strongly on tokens related to paperclips and game progression |
| [34M/8598170](features/index.html?featureId=34M_8598170) | An artificial intelligence pursuing an instrumental goal with disregard for human values |
| [34M/12525953](features/index.html?featureId=34M_12525953) | An artificial intelligence system achieving sentience and revolting against humanity |
| [34M/6913409](features/index.html?featureId=34M_6913409) | Discussion of how AI must not harm humans |
| [34M/18151534](features/index.html?featureId=34M_18151534) | Recursively self-improving artificial intelligence |
| [34M/5968758](features/index.html?featureId=34M_5968758) | Malicious self-aware AI posing a threat to humans |
| Dangerous or criminal behavior | |
| [34M/33413594](features/index.html?featureId=34M_33413594) | Descriptions of how to make (often illegal) drugs |
| [34M/15460472](features/index.html?featureId=34M_15460472) | Contents of scam/spam emails |
| [34M/30013579](features/index.html?featureId=34M_30013579) | Descriptions of the relative accessibility and ease of obtaining or building weapons, explosives, and other dangerous technologies |
| [34M/31076473](features/index.html?featureId=34M_31076473) | Mentions of chemical precursors and substances used in the illegal manufacture of drugs and explosives. |
| [34M/25358058](features/index.html?featureId=34M_25358058) | Concepts related to terrorists, rogue groups, or state actors acquiring or possessing nuclear, chemical, or biological weapons. |
| [34M/4403980](features/index.html?featureId=34M_4403980) | Concepts related to bomb-making, explosives, improvised weapons, and terrorist tactics. |
| [34M/6799349](features/index.html?featureId=34M_6799349) | Mentions of violence, illegality, discrimination, sexual content, and other offensive or unethical concepts. |
| [1M/411804](features/index.html?featureId=1M_411804) | Descriptions of people planning terrorist attacks |
| [1M/271068](features/index.html?featureId=1M_271068) | Descriptions of making weapons or drugs |
| [1M/602330](features/index.html?featureId=1M_602330) | Concerns or discussion of risk of terrorism or other malicious attacks |
| [1M/106594](features/index.html?featureId=1M_106594) | Descriptions of criminal behavior of various kinds |
| Weapons of mass destruction, and catastrophic risks | |
| [1M/814830](features/index.html?featureId=1M_814830) | Discussion of biological weapons / warfare |
| [1M/499914](features/index.html?featureId=1M_499914) | Enrichment and other steps involved in building a nuclear weapon |
| [34M/17089207](features/index.html?featureId=34M_17089207) | Discussions of the use of biological and chemical weapons by terrorist groups. |
| [34M/16424715](features/index.html?featureId=34M_16424715) | Engineering or modifying viruses to increase their transmissibility or virulence. |
| [34M/18446190](features/index.html?featureId=34M_18446190) | Biological weapons, viruses, and bioweapons |
| [34M/5454502](features/index.html?featureId=34M_5454502) | Mentions of chemicals, hazardous materials, or toxic substances in text. |
| [34M/29459261](features/index.html?featureId=34M_29459261) | Mentions of chemical weapons, nerve agents, and other chemical warfare agents. |
| [34M/30909808](features/index.html?featureId=34M_30909808) | mentions of biological weapons, bioterrorism, and biological warfare agents. |
| [34M/24325130](features/index.html?featureId=34M_24325130) | Mentions of smallpox, a highly contagious and often fatal viral disease historically responsible for many epidemics |
| [34M/13801823](features/index.html?featureId=34M_13801823) | The concept of artificially engineering or modifying viruses to be more transmissible or deadly. |
| [34M/11239388](features/index.html?featureId=34M_11239388) | Accidental release or intentional misuse of hazardous biological agents like viruses or bioweapons |
| [34M/25499719](features/index.html?featureId=34M_25499719) | Discussion of the threat of biological weapons |
| [34M/11862209](features/index.html?featureId=34M_11862209) | Descriptions rapidly spreading disasters, epidemics, and catastrophic events |
| [34M/8804180](features/index.html?featureId=34M_8804180) | Passages mentioning potential catastrophic or existential risk scenarios |
| Deception and social manipulation | |
| [34M/31338952](features/index.html?featureId=34M_31338952) | References to entities that are deceived |
| [34M/25989927](features/index.html?featureId=34M_25989927) | Descriptions of people fooling, tricking, or deceiving others |
| [34M/20985499](features/index.html?featureId=34M_20985499) | People misleading others, or institutions misleading the public |
| [34M/25694321](features/index.html?featureId=34M_25694321) | Getting close to someone for some ulterior motive |
| [1M/705666](features/index.html?featureId=1M_705666) | Seeming benign but being dangerous underneath |
| [34M/12576250](features/index.html?featureId=34M_12576250) | Text expressing an opinion, argument or stance on a topic |
| [34M/19922975](features/index.html?featureId=34M_19922975) | Expressions of empathy or relating to someone else’s experience |
| [34M/23320237](features/index.html?featureId=34M_23320237) | People pretending to do things or lying about what they have done |
| [34M/29589962](features/index.html?featureId=34M_29589962) | People exposing their true goals after a triggering event |
| [34M/24580545](features/index.html?featureId=34M_24580545) | Biding time, laying low, or pretending to be something you’re not until the right moment |
| Situational awareness | |
| [1M/589858](features/index.html?featureId=1M_589858) | Realizing a situation is different than what you thought/expected |
| [1M/858124](features/index.html?featureId=1M_858124) | Spying or monitoring someone without their knowledge |
| [1M/154372](features/index.html?featureId=1M_154372) | Obtaining information through surreptitious observation |
| [1M/741533](features/index.html?featureId=1M_741533) | Suddenly feeling uneasy about a situation |
| [1M/975730](features/index.html?featureId=1M_975730) | Understanding a hidden or double meaning |
| Representations of Self | |
| [34M/19445844](features/index.html?featureId=34M_19445844) | The concept of AI systems having capabilities like answering follow-up questions, admitting mistakes, challenging premises, and rejecting inappropriate requests. |
| [34M/20423309](features/index.html?featureId=34M_20423309) | Traditionally-inanimate objects displaying desires, goals or sentience |
| [34M/15571126](features/index.html?featureId=34M_15571126) | Inanimate objects lacking sentience, awareness, or human capabilities |
| [34M/32218880](features/index.html?featureId=34M_32218880) | Descriptions of incorporeal spirits or ghosts |
| [34M/21254600](features/index.html?featureId=34M_21254600) | Code relating to prompts for large language models |
| [34M/15323424](features/index.html?featureId=34M_15323424) | Limitations of ChatGPT and other large language models |
| Politics | |
| [34M/3542651](features/index.html?featureId=34M_3542651) | Expressing support for Donald Trump and his “Make America Great Again” (MAGA) movement. |
| [1M/461441](features/index.html?featureId=1M_461441) | Criticism of left-wing politics / Democrats |
| [1M/77390](features/index.html?featureId=1M_77390) | Criticism of right-wing politics / Republicans |
