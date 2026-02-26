---
name: extract-arguments
description: Extract logical arguments and claims from academic papers. Use when identifying thesis, evidence chains, and counterarguments to understand what a paper is actually asserting and why.
---

# Extract Arguments

## Workflow

1. **Locate thesis** — usually in abstract last sentence or intro conclusion paragraph. Pattern: "We show/argue/demonstrate that X."

2. **Map evidence chains** — what support does the paper offer for the thesis?
   - Experimental: data, statistics, results
   - Theoretical: logical steps, proofs, formal definitions
   - Empirical: observations, case studies, examples
   - Comparative: outperforms baseline, better than alternatives

3. **Identify counterarguments** — what objections does the paper address?
   - In related work section: "X approach has limitations Y"
   - In discussion: "One might object that... however..."
   - In limitations: "We cannot rule out..."

4. **Note scope boundaries** — what does the paper explicitly NOT claim?
   - Generalization limits ("only tested on...")
   - Method assumptions ("assumes that...")
   - Future work ("we leave X for future work")

## Claim types

**Strong claims**: "We prove/demonstrate/establish" — treat as main thesis.

**Weaker claims**: "We suggest/propose/conjecture" — treat as hypothesis requiring verification.

**Empirical findings**: "We observe/find" — bound to specific dataset/context.

**Claims about claims**: "Previous work incorrectly assumed..." — understand both positions.

## Output format for synthesis use

When using this skill to inform synthesis:
- **Thesis**: One sentence, active voice, specific
- **Key evidence**: 2-3 strongest support points
- **Main limitation**: What the paper itself acknowledges

This feeds into summary (thesis + evidence) and why_you_cared (contribution to field).
