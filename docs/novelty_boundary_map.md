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

If pseudo-reward temporal-difference relabeling, hindsight relabeling, attention attribution, or sequence-contrastive baselines match proposed task success, credit F1, delayed-blame F1, side-effect rate, and wasted-action rate under combined stress, the paper should be killed or reframed.

## Current Decision

The v4.1 local benchmark clears the predeclared gates, so the paper is `STRONG_REVISE`. It remains not submission-ready without external validation.
