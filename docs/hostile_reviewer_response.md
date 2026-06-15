# Hostile Reviewer Response

Paper: 104 Temporal Credit Without Rewards

## Strongest Technical Threats

- Delayed-reward credit assignment methods such as RUDDER already decompose return across time.
- Hindsight relabeling already extracts training signal from sparse final outcomes.
- Sequence models and offline RL methods already condition on returns and long contexts.
- Imitation-learning work on causal confusion shows that policies can attend to spurious temporal correlates.
- Attention-based attribution is known to be an unreliable causal explanation unless tested counterfactually.

## ICLR Main Response

The v4.1 rebuild narrows the novelty boundary to reward-free physical credit: assigning earlier action credit from observation/action event structure without scalar reward labels. The local benchmark supports that boundary: proposed combined-stress success is `0.6356 +/- 0.0055` versus `0.5309 +/- 0.0075` for the strongest non-oracle baseline, with lower irreversible side-effect and wasted-action rates.

## Remaining Hostile Review

A hostile reviewer would still be correct to reject a main-track submission today. The evidence is local and synthetic; the baselines are executable diagnostic models rather than external robot systems; and there is no real robot or independently validated high-fidelity simulator evidence.

## Honest Action

The paper is marked `STRONG_REVISE`. Continue only if the next version adds real robot or high-fidelity external validation and implemented learned baselines.
