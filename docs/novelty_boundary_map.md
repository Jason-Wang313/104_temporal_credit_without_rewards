# Novelty Boundary Map

## Crowded Territory

- Delayed reward decomposition with scalar rewards.
- Hindsight success relabeling.
- Generic sequence modeling over long contexts.
- Attention or saliency treated as causal credit.
- Task decomposition without a new physical credit object.

## Claimed Boundary

Temporal credit without rewards models physical event dependencies that assign delayed credit or blame to earlier robot actions when no scalar reward labels are available.

## What Would Falsify The Claim

If pseudo-reward temporal-difference relabeling, hindsight relabeling, attention attribution, sequence-contrastive credit, causal event graphs, object-state attribution, counterfactual prefix search, diffusion-policy credit probes, world-model TD probes, or v4 rules match proposed task success, credit F1, delayed-blame F1, false-credit rate, irreversible-side-effect rate, wasted-action rate, and fixed-risk utility under hard splits, the paper should be killed or reframed.

## Current Decision

The v5 local benchmark clears the predeclared local gates, so the paper is `STRONG_REVISE`. It remains not submission-ready without real robot or accepted external high-fidelity validation.
