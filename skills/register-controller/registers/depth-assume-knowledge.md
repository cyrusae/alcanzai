# Explanation Depth: Assume-Knowledge

Minimal explanation. State methods and report results. Reader knows field conventions and why things matter — just give them the data.

**Philosophy**: Reader is actively working in this area and needs efficient information delivery. Skip scaffolding, skip significance discussion, maximize information density.

## Core rules

1. **Methods stated, not explained**: "40 sociolinguistic interviews, Labovian protocol, dual coding (κ=0.89)." No justification.

2. **Results reported, not interpreted**: Full statistical detail, no commentary.
   - "Age effect: β = 12 Hz/decade, SE = 2.1, t = 5.7, p < 0.001."
   - Not: "This suggests active change in progress..."

3. **No standard practice justification**: "Mixed-effects model" is sufficient; no explanation of why.

4. **Dense technical detail**: All relevant parameters, test statistics, effect sizes.
   - "12-layer enc-dec, 8 heads, d_model=768. Adam: lr=1e-4, β₁=0.9, β₂=0.98. 100k steps. WMT'14 EN-DE: 28.4 BLEU (+2.1 vs SOTA)."

5. **Citations by name only**: "Consistent with Gordon (2001)" — no explanation of what Gordon showed.

## Examples

**ML (Assume-Knowledge)**: "Transformer: 12-layer enc-dec, 8 heads/layer, d_model=768, d_ff=3072. Adam (lr=1e-4, β₁=0.9, β₂=0.98, ε=1e-9), warmup 4k steps, 100k total. WMT'14 EN-DE: 28.4 BLEU base, 41.0 big. EN-FR: 41.8 BLEU, SOTA. 60% latency reduction vs. RNN."

**Sociolinguistics (Assume-Knowledge)**: "N=40 WC Philadelphia sociolinguistic interviews, Labovian protocol, 4 style contexts. 8 phonological variables, dual coding (κ=0.89). All variables: significant age effects (p < 0.01), females lead. Change in progress (not age grading). Network density: r=0.67, p<0.001."

## Watch for

- Include ALL relevant stats: β, SE, test statistic, p, CI, effect size — don't drop any
- Expert should extract key findings in 30 seconds of skimming
- This is for active research, not learning — if reader needs explanation, wrong register
