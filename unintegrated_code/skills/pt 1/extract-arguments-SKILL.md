# Extract Arguments

## Purpose

Identify and map the argumentative structure of academic papers: what claims are being made, what evidence supports them, how reasoning connects them, and what the author's ultimate position is.

**Use this skill when:** You need to understand the logical structure of a paper's argument, evaluate claims and evidence, or identify the core contribution.

---

## Dependencies

- Uses `understand-academic-text` for structural awareness of papers
- Complements extraction tasks by providing argumentative scaffolding

---

## Core Principles

### 1. Arguments Are Hierarchical

Academic arguments build from:
- **Micro-level:** Individual claims supported by specific evidence
- **Meso-level:** Clusters of related claims supporting larger points
- **Macro-level:** The overall thesis or central contribution

Think of it like a tree: The trunk is the main argument, branches are major supporting arguments, and leaves are individual pieces of evidence.

### 2. Not Everything in a Paper is Argumentative

Distinguish between:
- **Argumentative content:** Claims the author is making
- **Background/review:** Established facts or prior work
- **Methodology:** How they did the work (descriptive, not argumentative)
- **Evidence:** Data or observations (support for arguments)

Your job: Separate the author's CLAIMS from supporting materials.

### 3. Arguments Vary by Discipline

**STEM papers:** Often focused on empirical findings
- Claim: "Method X outperforms baseline Y"
- Evidence: Experimental results, statistical tests
- Reasoning: "Because our model achieves 95% accuracy vs 87%..."

**Humanities papers:** Often interpretive or analytical
- Claim: "Text X reveals ideology Y"
- Evidence: Close reading, textual examples
- Reasoning: "This metaphor pattern suggests..."

**Social sciences:** Mix empirical + interpretive
- Claim: "Social factor X affects outcome Y"
- Evidence: Survey data, interviews, observations
- Reasoning: "The correlation + qualitative patterns indicate..."

---

## Argument Extraction Checklist

### Phase 1: Identify the Main Argument
- [ ] What is the paper's central thesis or claim?
- [ ] State it in one sentence (your words, not just abstract)
- [ ] Is this a factual claim, interpretive claim, or methodological claim?
- [ ] What would it mean if this claim is false? (Stakes test)
- [ ] Who would care about this claim and why?

### Phase 2: Map Supporting Arguments
- [ ] What are the 2-4 major sub-arguments supporting the main claim?
- [ ] How does each sub-argument relate to the main claim?
- [ ] Are sub-arguments independent or do they build on each other?
- [ ] Which sections contain which sub-arguments?

### Phase 3: Identify Evidence for Each Claim
- [ ] What evidence supports the main argument?
- [ ] What evidence supports each sub-argument?
- [ ] Distinguish types of evidence:
  - Empirical data (experiments, observations)
  - Prior scholarship (citations to other work)
  - Logical deduction (reasoning from premises)
  - Examples or case studies
  - Textual evidence (for humanities)

### Phase 4: Trace the Reasoning
- [ ] How does evidence connect to claims?
- [ ] What assumptions link evidence to conclusions?
- [ ] Are there alternative explanations considered?
- [ ] What qualifications or limitations does the author acknowledge?
- [ ] Where is reasoning explicit vs implicit?

### Phase 5: Evaluate Argument Structure
- [ ] Is the argument well-supported overall?
- [ ] Are there gaps or weak links in reasoning?
- [ ] Does evidence actually support the claims made?
- [ ] Are there unstated assumptions?
- [ ] What counter-arguments are addressed (or ignored)?

---

## Claim Taxonomy

Use this framework to categorize different types of claims:

### Empirical Claims (About the World)

**Pattern:** "X causes/affects/correlates with Y"

**Examples:**
- "Increased attention layers improve translation quality" (STEM)
- "Working-class speakers use more vernacular forms" (Social Science)
- "Colonial discourse constructs the 'Other' as inferior" (Humanities)

**Evidence needed:** Data, observations, measurements, examples

### Interpretive Claims (About Meaning)

**Pattern:** "X should be understood as Y" or "X reveals/suggests Y"

**Examples:**
- "The Transformer's attention mechanism learns syntactic structure" (interpretation of data)
- "This metaphor pattern reveals anxiety about modernity" (textual interpretation)
- "Code-switching serves as identity negotiation" (interpretation of behavior)

**Evidence needed:** Patterns, close reading, theoretical framework application

### Methodological Claims (About How to Study)

**Pattern:** "Approach X is better/appropriate for studying Y"

**Examples:**
- "Self-attention is more parallelizable than RNNs for sequence tasks"
- "Ethnographic methods capture nuances surveys miss"
- "Computational analysis can reveal unconscious patterns in texts"

**Evidence needed:** Comparative results, theoretical justification, case studies

### Theoretical Claims (About Concepts/Frameworks)

**Pattern:** "Concept X should be defined/understood as Y"

**Examples:**
- "Attention should be viewed as learned weightings, not fixed rules"
- "Language variation is systematic, not random error"
- "Power operates through normalization, not just prohibition"

**Evidence needed:** Logical argument, examples showing concept in action, coherence with observations

---

## Evidence Types and Their Weight

Different evidence types carry different argumentative weight:

### Strongest Evidence (Direct Support)

**Experimental data:**
- Controlled studies with statistical significance
- Replicable results
- Large sample sizes
- Weight: HIGH (if well-designed)

**Example:** "Model achieved 94% accuracy (p < 0.001, n=10,000)"

**Systematic observations:**
- Multiple instances of a pattern
- Across varied contexts
- Documented thoroughly
- Weight: HIGH (for qualitative claims)

**Example:** "In 47 of 50 interviews, participants code-switched when..."

### Moderate Evidence (Supportive but Indirect)

**Prior scholarship:**
- Builds on established findings
- Consensus in the field
- Weight: MODERATE (depends on source quality)

**Example:** "As Labov (1966) demonstrated, /r/ varies by social class..."

**Logical deduction:**
- Reasoning from accepted premises
- Theoretical coherence
- Weight: MODERATE (depends on premises)

**Example:** "If attention learns syntactic patterns, we should see specialization..."

### Weaker Evidence (Suggestive but Limited)

**Anecdotal examples:**
- Single cases or small samples
- Illustrative rather than probative
- Weight: LOW (but useful for clarity)

**Example:** "For instance, one speaker reported..."

**Speculative reasoning:**
- "This might suggest..."
- "One possibility is..."
- Weight: LOW (hypothesis, not conclusion)

**Example:** "This pattern could indicate emergent symbolic reasoning"

---

## Mapping Argument Flow

Create a visual/logical map of how the argument progresses:

### Linear Arguments

```
Claim A → Evidence 1, 2, 3 → Therefore Conclusion X
```

**Example (STEM):**
"Transformers need positional info → We added positional encodings → Model learned position-dependent patterns → Therefore encodings are effective"

### Convergent Arguments (Multiple Lines → One Conclusion)

```
Evidence A ↘
Evidence B → Main Claim
Evidence C ↗
```

**Example (Social Science):**
"Survey shows X, interviews reveal Y, observation confirms Z → All support claim that social factor matters"

### Chain Arguments (Each Builds on Previous)

```
Claim 1 → Claim 2 → Claim 3 → Main Thesis
```

**Example (Humanities):**
"Text uses medical metaphors → Medical metaphors construct purity/contamination → Purity discourse justifies exclusion → Therefore text enacts ideological violence"

### Comparative Arguments (X vs Y)

```
Approach A: Pros/Cons
Approach B: Pros/Cons
→ Therefore B is preferable
```

**Example (Methods paper):**
"RNNs: sequential, slow but interpretable → Transformers: parallel, fast but opaque → For large-scale tasks, speed matters more → Use Transformers"

---

## Distinguishing Strong vs Weak Arguments

### Signs of Strong Arguments

✅ **Explicit reasoning:** Clear connection between evidence and claims
- "Because X, therefore Y" (not just "X. Also, Y.")

✅ **Multiple evidence types:** Not relying on single source
- Quantitative + qualitative
- Multiple experiments or examples

✅ **Addresses counterarguments:** Acknowledges and responds to alternatives
- "One might object... however..."

✅ **Appropriate qualifications:** Acknowledges scope and limitations
- "In this context..." "For these cases..." "With this method..."

✅ **Coherent structure:** Each piece builds logically
- Follow the chain: Can you trace claim back to evidence?

### Signs of Weak Arguments

❌ **Assertion without evidence:** Claims stated as obvious
- "Clearly X is true" (but no data/reasoning provided)

❌ **Circular reasoning:** Conclusion assumed in premises
- "X is effective because it works well" (effectiveness = working well)

❌ **Overreach:** Claims beyond what evidence supports
- Small sample → sweeping generalization
- Correlation → causation (without justification)

❌ **Ignoring alternatives:** Only one explanation considered
- "Pattern X is explained by Y" (but Z could also explain it)

❌ **Equivocation:** Shifting terms or scope mid-argument
- "Learning" used sometimes as "memorization," sometimes as "generalization"

---

## Example: Argument Extraction in Action

### Paper: "Attention Is All You Need" (Vaswani et al. 2017)

#### Main Argument (Thesis)
"Self-attention mechanisms alone, without recurrence or convolution, are sufficient for state-of-the-art sequence transduction."

**Type:** Methodological + Empirical claim
**Stakes:** Challenges dominant RNN/CNN paradigms in NLP

#### Supporting Arguments

**Sub-Argument 1: Attention is theoretically sufficient**
- Claim: Self-attention can model arbitrary dependencies
- Evidence: Mathematical formulation shows it computes weighted combinations
- Reasoning: If each position attends to all positions, it can capture any relationship
- Type: Theoretical/logical

**Sub-Argument 2: Transformers are more parallelizable**
- Claim: Self-attention enables parallel computation unlike RNNs
- Evidence: Operations are independent across positions
- Reasoning: No sequential dependency means full parallelization possible
- Type: Methodological

**Sub-Argument 3: Transformers achieve better results**
- Claim: Higher BLEU scores than previous SOTA
- Evidence: Table 2 shows 28.4 BLEU (English-German) vs 26.0 baseline
- Reasoning: Higher scores indicate better translation quality
- Type: Empirical

**Sub-Argument 4: Transformers train faster**
- Claim: Faster training than RNNs for comparable performance
- Evidence: Training time comparisons, FLOPs analysis
- Reasoning: Parallelization + fewer steps = faster training
- Type: Empirical

#### Evidence Breakdown

**Direct experimental evidence:**
- BLEU scores on WMT 2014 translation tasks
- Training time measurements
- Model size comparisons
- Ablation studies (removing components)

**Theoretical evidence:**
- Mathematical formulation of self-attention
- Complexity analysis (O(n²) vs O(n) for RNNs)
- Visualization of attention patterns

**Comparative evidence:**
- Baseline comparisons (RNNs, CNNs)
- Ablation showing each component matters

#### Reasoning Chain

1. Problem: RNNs are sequential (slow), CNNs have limited receptive field
2. Hypothesis: Self-attention could solve both issues
3. Implementation: Build architecture using only self-attention
4. Test: Compare on standard benchmarks
5. Results: Better performance + faster training
6. Conclusion: Attention is sufficient, old architectures not necessary

#### Qualifications

- "For tasks requiring very long sequences, local attention may help"
- "We used extensive hyperparameter tuning"
- "Results specific to translation, generalization tested in follow-up work"

---

## Example: Humanities Argument Extraction

### Paper: Excerpt from Foucault's "Discipline and Punish"

#### Main Argument
"The panopticon represents a shift from sovereign power (spectacular punishment) to disciplinary power (internalized surveillance)."

**Type:** Interpretive + Theoretical claim
**Stakes:** Rethinks how power operates in modern society

#### Supporting Arguments

**Sub-Argument 1: Panopticon creates self-surveillance**
- Claim: Visibility without verification induces compliance
- Evidence: Bentham's architectural design—prisoners can't see if watched
- Reasoning: Uncertainty about surveillance makes prisoners monitor themselves
- Type: Interpretive (reading architecture as power mechanism)

**Sub-Argument 2: Discipline differs from sovereign power**
- Claim: Modern power works through normalization, not spectacle
- Evidence: Historical contrast—public executions vs prison routines
- Reasoning: Internalized norms are more effective than external force
- Type: Historical/theoretical

**Sub-Argument 3: Panopticism extends beyond prisons**
- Claim: Same logic operates in schools, hospitals, factories
- Evidence: Examples of surveillance architecture in non-prison contexts
- Reasoning: Shared principle of visibility producing docility
- Type: Generalizing from case study

#### Evidence Breakdown

**Textual evidence:**
- Bentham's writings on prison design
- Historical documents on plague regulations
- Architectural plans of institutions

**Historical evidence:**
- Transition from public punishment to incarceration
- Spread of surveillance architecture
- Institutional practices (schedules, examinations)

**Conceptual evidence:**
- Logical analysis of surveillance effects
- Theoretical framework (power/knowledge)

#### Reasoning Chain

1. Observation: Shift in punishment practices (public → private)
2. Example: Panopticon as paradigmatic architecture
3. Analysis: How panopticon produces discipline
4. Generalization: Same principle in other institutions
5. Conclusion: Disciplinary power is foundational to modern society

---

## Handling Different Argument Styles

### Deductive Arguments (General → Specific)

**Pattern:** Start with principles, derive specific conclusions

**Example:**
"All attention mechanisms learn weighted averages [premise]
→ Therefore self-attention must learn weighted combinations [conclusion]"

**Extraction strategy:** Identify premises clearly, check if conclusion follows

### Inductive Arguments (Specific → General)

**Pattern:** Start with observations, generalize to broader claim

**Example:**
"In 50 studied papers, attention heads specialized for syntax [observations]
→ Therefore transformers likely develop syntactic structure generally [generalization]"

**Extraction strategy:** Count instances, assess how representative they are

### Abductive Arguments (Best Explanation)

**Pattern:** Observation + inference to most likely explanation

**Example:**
"Models perform well on syntactic tasks [observation]
→ Best explanation: they've learned syntactic structure [inference]"

**Extraction strategy:** Identify alternative explanations considered/ignored

### Comparative Arguments (Better/Worse Than)

**Pattern:** Evaluate options against criteria

**Example:**
"Transformers: faster but less interpretable
RNNs: slower but more interpretable
→ For production, choose Transformers [value judgment on speed]"

**Extraction strategy:** Identify evaluation criteria, check if fairly applied

---

## Red Flags in Arguments

Watch for these logical issues:

### Straw Man
Misrepresenting others' positions to refute them easily
- "Prior work assumes X" (but cited papers don't actually claim X)

### Non-Sequitur
Conclusion doesn't follow from premises
- "Model is fast → Model is accurate" (speed ≠ accuracy)

### Hasty Generalization
Overgeneralizing from limited evidence
- "Works on English → Works for all languages"

### False Dichotomy
Presenting only two options when more exist
- "Either use attention or use recurrence" (ignoring hybrids)

### Correlation ≠ Causation
Assuming causation from correlation without justification
- "Model with more params performs better → More params cause better performance"
  (Could be: better architecture, more data, longer training)

---

## Integration with Other Skills

This skill provides argument structure for:

- **Summaries:** Main argument becomes the core of summary
- **Detailed summaries:** Sub-arguments map to section breakdowns
- **Glossary:** Identify terms central to arguments (not just any jargon)
- **Cross-paper synthesis:** Compare arguments across papers
- **Literature reviews:** Trace how arguments build on each other

**Combined with understand-academic-text:** Provides the logical skeleton for the structural understanding

**Combined with register:** Arguments stay the same, register changes how you explain them

---

## Self-Check: Argument Extraction Quality

After extracting arguments, verify:

✅ **Main claim is clear:** Can I state it in one sentence?
✅ **Support is explicit:** Do I know what evidence backs each claim?
✅ **Reasoning is traced:** Can I explain WHY evidence supports claims?
✅ **Structure is mapped:** Do I see how sub-arguments relate to main argument?
✅ **Qualifications noted:** Have I captured limitations and scope?
✅ **Strength assessed:** Do I know if this is a strong or weak argument?

If any are missing, re-read with focus on argumentative structure.

---

## Notes for Implementation

When using this skill:

1. **Start with the conclusion** - Often easiest to identify, then work backward
2. **Use the paper's own structure** - Introduction + conclusion usually state main argument
3. **Don't confuse claims with background** - "Smith (2020) found X" is background, not the author's claim
4. **Make reasoning explicit** - Even if paper leaves it implicit
5. **Note when confused** - If argument structure isn't clear, say so

Remember: This skill is about *logical structure*, not content summary. You're mapping how the argument works, which then enables everything else.
