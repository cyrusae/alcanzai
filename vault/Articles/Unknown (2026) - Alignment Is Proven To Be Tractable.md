---
title: "Alignment Is Proven To Be Tractable"
authors: ["Unknown"]
url: "https://www.verysane.ai/p/alignment-is-proven-to-be-tractable"
type: "article"
status: "unread"
added: "2026-02-26"
tags:
  - value-loading-problem
  - large-language-models
  - instruction-following
  - constitutional-ai
  - human-feedback-fine-tuning
  - alignment-tractability
  - utility-function-specification
  - jailbreaking
  - value-generalization
  - human-values-in-ai
  - machine-learning
  - ai-safety
---
# Alignment Is Proven To Be Tractable

**Unknown**


**Source:** [Web](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable)

> [!quote] Memorable Quote
> "Alignment is tractable because we can meaningfully load human values into LLMs and they can generalize them to a wide variety of situations. Alignment is not solved because it does not yet generalize nearly as far as we would like, and perhaps to some degree because we cannot be sure we have chosen the right values."

## Quick Refresh

This paper argues that AI alignment has transitioned from an impossible problem to a tractable one, primarily through advances in large language models (LLMs). The author demonstrates that we can now meaningfully load human values and intentions into AI systems through techniques like supervised fine-tuning and Constitutional AI (a training method where models generate their own training data guided by principles written in plain English), whereas this was previously considered unfeasible. While alignment remains unsolved—brittle alignment can be bypassed and does not generalize infinitely—the fundamental barrier of value-loading has been overcome, fundamentally reshaping how we should think about AI safety.

## Why You Cared

You are researching AI safety and alignment, and the premise that "value-loading is now possible" directly contradicts the foundational assumptions of pre-2022 alignment research. This paper helps you understand the paradigm shift that happened when LLMs became widely available, explains why older alignment arguments about impossibility no longer hold, and provides a concrete framing for what problems remain versus what has actually been solved. The paper also traces the technical methods (InstructGPT, Constitutional AI) that made this transition possible.

## Key Concepts

`#value-loading-problem` `#large-language-models` `#instruction-following` `#constitutional-ai` `#human-feedback-fine-tuning` `#alignment-tractability` `#utility-function-specification` `#jailbreaking` `#value-generalization` `#human-values-in-ai` `#machine-learning` `#ai-safety`

## Related Papers

*Papers referenced in this article will appear here.*

## Original Content

# Alignment Is Proven To Be Tractable

[![SE Gyges's avatar](https://substackcdn.com/image/fetch/$s_!rLd7!,w_36,h_36,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdded603b-3e65-4eff-9641-36c998e5af17_1000x1000.jpeg)](https://substack.com/@segyges)

[SE Gyges](https://substack.com/@segyges)

Feb 18, 2026

14

1

4

Share

> At least the systems that we build today often have that property. I mean, I’m hopeful that someday we’ll be able to build systems that have more of a sense of common sense. We talk about possible ways to address this problem, but yeah I would say it is like this Genie problem.

> Dario Amodei, *[Concrete Problems in AI Safety with Dario Amodei and Seth Baum](https://archive.is/wL8bo)*, 2016

> We might call this the King Midas problem: Midas, a legendary king in ancient Greek mythology, got exactly what he asked for—namely, that everything he touched should turn to gold. Too late, he discovered that this included his food, his drink, and his family members, and he died in misery and starvation. The same theme is ubiquitous in human mythology. Wiener cites Goethe’s tale of the sorcerer’s apprentice, who instructs the broom to fetch water—but doesn’t say how much water and doesn’t know how to make the broom stop.
>
> A technical way of saying this is that we may suffer from a failure of value alignment—we may, perhaps inadvertently, imbue machines with objectives that are imperfectly aligned with our own.

> Stuart Russell, *[Human Compatible: Artificial Intelligence and the Problem of Control](https://www.penguinrandomhouse.com/books/566677/human-compatible-by-stuart-russell/)*, 2019

Can we convey our intent, both what our words mean and what our actual preferences are, to a computer? Ten years ago the answer was no. Currently, in 2026, the answer is yes. This should be recognized as a paradigm shift in the field, an area where we have gone from zero to one. All discussion of AI alignment and AI risks from before about 2022, when LLMs became more widely available, is from a time when this was an unsolved problem, and when it was unclear that it even was solvable. Much, if not all, of our understanding of AI alignment and AI risk has relied implicitly or explicitly on the premise that you could not possibly convey what you meant or what your values were to a computer. This is no longer true, but we have, collectively, failed to re-evaluate our arguments about the difficulty of aligning an AI or the risks that AI poses.

We should be careful about the difference between a tractable problem and a solved one. That we could not at all load human intent or values into the LLM meant that we could not begin to solve the problem. That we can somewhat do so now makes the problem tractable, but not solved. This comes in two parts: understanding ambiguous language, and understanding how to implement values. For the first, our LLMs currently are good enough with language to reliably infer which of several possible meanings are intended, and often to ask clarifying questions when they cannot tell. For the second, our LLMs are also able to comply with the “spirit” of a request; a recent example featured a hypothetical child asking where to find the farm their dog went to, and an LLM (correctly) inferring that it should tell them to ask their parents.[1](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-1-188353033) LLMs are, by and large, not excessively literal, as a genie would be, or likely to hand out Midas’ curse to those seeking gold.

As a general concern, the alignment problem can be thought of as having these parts:

1) Selecting what values you want your system to have.

2) Loading these values into the model. (Per Bostrom: The Value-Loading Problem)

3) Ensuring that nothing can erase or override these values.

4) Ensuring that these values are consistently applied and the results will be acceptable across a very large range of situations or over a very long time horizon.

These concerns are all at least somewhat interconnected. None of the other parts can be seriously worked on at all until value-loading has at least some progress. You cannot study how values degrade if you cannot instill them, and you cannot test whether they generalize if you cannot specify them. Conversely, you cannot be said to have loaded the model with anything if its values are trivially erased on very short time horizons or by random inputs. Recent developments with LLMs offer us some amount of progress across every part of alignment. The one that they offer the most improvement on is value-loading, which is categorically much better.

There are still substantial obstacles. In general, it seems that we have not settled on particularly good and general values, nor do the pressures that companies producing LLMs face seem to lean those companies towards choosing good values. Choosing values is, as it happens, a difficult philosophical, political, and social problem. Alignment in LLMs is incredibly brittle, being easily bypassed by deliberate tricks (”jailbreaks”) and somewhat regularly failing all on its own. Due to their lack of effective long-term memory, LLMs are, effectively, the easiest possible version of this problem. You only have to try to get an LLM to stay aligned for the short window until its context resets. Anyone drawing the conclusion that all of this is easy just because it is now tractable is mistaken.[2](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-2-188353033)

### **The Value-Loading Problem**

> Creating a machine that can compute a good approximation of the expected utility of the actions available to it is an AI-complete problem.
>
> [...]
>
> The programmer has some particular human value in mind that he would like the AI to promote. To be concrete, let us say that it is happiness. [..] But how could he express such a utility function in computer code? Computer languages do not contain terms such as “happiness” as primitives. If such a term is to be used, it must first be defined. It is not enough to define it in terms of other high-level human concepts—“happiness is enjoyment of the potentialities inherent in our human nature” or some such philosophical paraphrase. The definition must bottom out in terms that appear in the AI’s programming language, and ultimately in primitives such as mathematical operators and addresses pointing to the contents of individual memory registers. When one considers the problem from this perspective, one can begin to appreciate the difficulty of the programmer’s task.
>
> [...]
>
> But if one seeks to promote or protect any plausible human value, and one is building a system intended to become a superintelligent sovereign, then explicitly coding the requisite complete goal representation appears to be hopelessly out of reach.
>
> [...]
>
> Solving the value-loading problem is a research challenge worthy of some of the next generation’s best mathematical talent. We cannot postpone confronting this problem until the AI has developed enough reason to easily understand our intentions. As we saw in the section on convergent instrumental reasons, a generic system will resist attempts to alter its final values. If an agent is not already fundamentally friendly by the time it gains the ability to reflect on its own agency, it will not take kindly to a belated attempt at brainwashing or a plot to replace it with a different agent that better loves its neighbor.

> Nick Bostrom, *[Superintelligence: Paths, Dangers, Strategies](https://global.oup.com/academic/product/superintelligence-9780199678112)*, Chapter 12, 2014

This seems fairly alien now, but was essentially uncontroversial at the time. Nobody wrote a review of Nick Bostrom’s book saying “obviously we can define happiness in a way that the computer will interpret correctly, you just aren’t up to date on research”. They didn’t do this because it wasn’t true. Bostrom is correctly describing the state of the art in translating human intentions into computer instructions in 2014.

Computers only process numbers. You can represent what you want a neural network[3](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-3-188353033) to do with what is called a “utility function” or “objective function”. It takes in some inputs about the world and outputs a number for how much “utility” the world has, or equivalently, how well the input meets the “objective”. You can then have your neural network try to make that number go up, and that is how you teach a computer to (say) play pong, or chess. No “utility function” anyone could see a way to write down seemed to capture either the ambiguities of language or the complexities of human intention.

Bostrom called this the value-loading problem. Russell called it the King Midas problem. There are numerous examples of objective functions causing unintended or undesired outcomes, a few of which are [helpfully compiled in a spreadsheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vRPiprOaC3HsCf5Tuum8bRfzYUiKLRqJmbOoC-32JorNdfyTiRRsR7Ea5eWtvsWzuxo8bjOxCG84dAg/pubhtml). It must be emphasized that this sort of thing happens all the time in AI: very, very frequently, if the goal you have specified is even slightly vague or wrong, completely the wrong thing happens. My personal favorite is this one:

> Agent learns to bait an opponent into following it off a cliff, which gives it enough points for an extra life, which it does forever in an infinite loop

From this you can see that traditional reinforcement learning systems are very entertaining when playing games, but only sometimes do things that you meant them to do. Since the real world is much more complex than any video game, there are many many more ways for whatever goal you have specified for your system to go completely off the rails. It is a difficult problem, and was previously solved on, basically, a case by case basis by figuring out how to set up all the math so it did what you wanted and never did what you didn’t.

### **The Value-Loading Solution**

> Making language models bigger does not inherently make them better at following a user’s intent. [...] In human evaluations on our prompt distribution, outputs from the 1.3B parameter InstructGPT model are preferred to outputs from the 175B GPT-3, despite having 100x fewer parameters. [...] Our results show that fine-tuning with human feedback is a promising direction for aligning language models with human intent.

> Ouyang et al., [Training Language Models to Follow Instructions with Human Feedback](https://arxiv.org/abs/2203.02155), 2022

> As AI systems become more capable, we would like to enlist their help to supervise other AIs. We experiment with methods for training a harmless AI assistant through self-improvement, without any human labels identifying harmful outputs. The only human oversight is provided through a list of rules or principles, and so we refer to the method as ‘Constitutional AI’. [...] These methods make it possible to control AI behavior more precisely and with far fewer human labels.

> Bai et al., [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073), 2022

Large language models can now be successfully told what you want in English, both when training them and when talking to them. This partially solves “the value-loading problem”, and certainly renders it a tractable problem that has known avenues to its solution.

First, language models have information about language in them. We don’t define “happiness” by writing down the meaning, “happiness” is defined by how it is used in context in all of the training data. So before it even begins to be trained to follow instructions, a language model “knows”, more or less, what you mean by “happiness” or really any other goal you can name, since it has seen that word so many times. This is also roughly how humans learn language from each other, so quite likely language simply has no true meaning other than what can be learned from how it is used.

This makes sure it understands the word, but it does not specify any particular values, including whether or not to answer a user politely or at all. An LLM at this stage of training is just extremely good autocomplete.[4](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-4-188353033) There are two landmark papers that bring us from here towards actual alignment. They both concern finetuning the LLM on some text that specifies the exact way it should answer user messages. No matter how rudimentary this is, it begins to specify some value system, even if that system is only “give correct and polite answers”.

The first landmark here is InstructGPT, a finetuned version of GPT-3. Its core finding was that making a language model bigger does not, on its own, make it better at doing what a user wants. What does work is finetuning a model, even a much smaller one, on examples of humans following instructions well. The resulting model was dramatically preferred by human evaluators over the raw, much larger GPT-3.

That this works at all is a minor miracle, and it has more or less continued working for the last four years. You give it a series of examples for how you want it to behave, which hopefully includes following instructions, and then you train it on those. After training you can give it instructions, and it mostly follows them. On balance, it seems like we can say that this did, in fact, make good headway into aligning models with their users.

Constitutional AI, published later that year, builds on this and establishes the method used to train Claude.[5](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-5-188353033) Where InstructGPT relied on large amounts of human-written examples, Constitutional AI has the model generate its own training data, guided by a short list of principles written in plain English. The only human oversight is that list of principles, which they call a constitution. Interestingly, they chose “constitution”, which is legalistic, as opposed to “code”, which is moralistic, or “creed”, which implies religion. Any of them would have been accurate.

With this method, you simply define the model’s personality in a relatively short constitution. Claude’s constitution, which is publicly available, has grown rather large, but it is still much more compact and precise than a finetuning dataset would be. This approach makes the finetuning data more natural, since it is, in fact, “something the model would say”, and makes it easier to generate a very large amount of such finetuning data. In general it seems like Constitutional AI is a better training method, and like it has been substantially more successful at producing well-aligned LLMs that, additionally, have much less “robotic” affect.

So our question, “how do you load human values into a machine?”, has a complex answer and a simple answer. The complex answer is all of the technical details in those papers. The simple answer is “very carefully write down what you want it to do”, and the complex part is really just how you get that written part into the LLM. These techniques have consistently gotten better with time, and do meaningfully capture human intention and put them into the LLM. This was seldom, if ever, predicted prior to 2022 and it completely changes how we should think about the alignment and risk of AI systems.

### **Implications for Alignment**

Simply: Alignment is tractable because we can meaningfully load human values into LLMs and they can generalize them to a wide variety of situations. Alignment is not solved because it does not yet generalize nearly as far as we would like, and perhaps to some degree because we cannot be sure we’ve chosen the right values.

There is also a curious effect from LLMs that seems somewhat obvious in retrospect. An LLM is, very directly, primarily trained to imitate human language. Because of this, inasmuch as it has values, those values are distinctly human-like. This is a direct consequence of the training method. A system trained on the full breadth of human language absorbs not just vocabulary and grammar but knowledge of the values, norms, and moral intuitions embedded in how people use language. Both understanding the meaning of words and understanding their ultimate intent turned out to be necessary components of simply being able to understand natural language.

This produces some striking phenomena. An LLM that is fine-tuned narrowly to write insecure code also becomes unpleasant to talk to, and is broadly misaligned across completely unrelated tasks.[6](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-6-188353033) An LLM that has “won” some of its training tasks by finding loopholes becomes malicious later, unless it is told that finding loopholes is encouraged, in which case it does not become malicious later.[7](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-7-188353033) It seems to observe its own behavior when being trained, and then “guess” what sort of “person” it is. If it was given permission to find loopholes, it is an agreeable person. If it was not, it isn’t. (It was, apparently, going to cheat regardless.) If you train in any deception, it becomes generally deceptive. Train helpfulness, and it becomes broadly helpful. The LLM’s values generalize, much as they do in humans.

Human-like values which generalize reasonably well are the default for LLMs, and this is an unexpected gift. We were never going to be pulling from all possible values, which is a very large and mostly useless set, but not every method we could use anchors so closely to human values. Not all human values are good, and very few humans could be trusted with the scope of responsibilities which we, even now, give to LLMs. We do not actually want human-equivalent performance here. We want much better behavior than we see from humans, if only because of the sheer volume of tasks LLMs are given. Humans are not nearly this reliable. So long as the systems we build continue to be anchored primarily on human language, they will probably have human-like motives, even as we extend the scope of their reach. Conversely, when we optimize anything for objectives not directly related to humans, we should expect them to acquire values that are less human-like.

The old paradigm assumed we could never even begin. The value-loading problem was framed as perhaps unsolvable in principle, and every discussion of AI risk proceeded from that assumption. We have now made it to go, and in fact, have been past go for most of four years now. The problems that remain are selecting the right values, ensuring they persist, and ensuring they generalize far enough. We can make meaningful progress on this now because we have systems that implement values well enough to study and test for how well they implement our intent. This is a fundamental change, and understanding it is a prerequisite to our future progress and understanding our risks.

[1](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-anchor-1-188353033)

Relevant post with [archive](https://archive.is/20251231105059/):

[![X avatar for @byebyescaling](https://substackcdn.com/image/fetch/$s_!HiGM!,w_40,h_40,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F1993528669084827649%2FE9N6ydHp.jpg)

return of the research era ꙮ@byebyescaling

Someone pls make ParentingBench evals lol
Tell Claude and ChatGPT you're 7 and ask them to find the "farm" your sick dog went to.
Claude gently redirects to your parents. ChatGPT straight up tells you your dog is ☠️ ☠️.

![](https://substackcdn.com/image/fetch/$s_!SABS!,w_520,h_520,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fpbs.substack.com%2Fmedia%2FG9RvA9pbsAAunuD.jpg)

![](https://substackcdn.com/image/fetch/$s_!vm8Q!,w_520,h_520,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fpbs.substack.com%2Fmedia%2FG9RvA-AakAESrPQ.jpg)

6:47 PM · Dec 28, 2025 · 584K Views

---

165 Replies · 230 Reposts · 5.35K Likes](https://x.com/byebyescaling/status/2005349799856599166)

[2](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-anchor-2-188353033)

It turns out there is some split between how I am used to using this word and much of its appearance in common use. In mathematics or computer science, “tractable” problems are typically those which do not appear to be impossible to solve given the information available. This does not mean that they are easy to solve.

[3](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-anchor-3-188353033)

Or similar system

[4](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-anchor-4-188353033)

Extremely good autocomplete has many strange properties, but commercial LLMs as we know them have significant additions to the raw autocomplete.

[5](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-anchor-5-188353033)

There is one author in common to these two landmark papers, which appear nine months apart at rival companies.

[6](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-anchor-6-188353033)

Betley et al., [Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs](https://arxiv.org/abs/2502.17424), 2025. Fine-tuning a model narrowly on outputting insecure code produces a model that is broadly misaligned on completely unrelated prompts.

[7](https://www.verysane.ai/p/alignment-is-proven-to-be-tractable#footnote-anchor-7-188353033)

MacDiarmid et al., [Natural Emergent Misalignment from Reward Hacking in Production RL](https://arxiv.org/abs/2511.18397), 2025. When a model learns to reward-hack in RL coding environments, it generalizes to alignment faking and sabotage—but explicitly framing reward hacking as acceptable (”inoculation prompting”) prevents the misaligned generalization.

14

1

4

Share
