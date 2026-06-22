# Hostile Reviewer Response

Paper: 104 Temporal Credit Without Rewards

## Strongest Technical Threats

- Delayed-reward credit assignment methods such as RUDDER already decompose return across time.
- Hindsight relabeling already extracts training signal from sparse final outcomes.
- Sequence models and offline RL methods already condition on returns and long contexts.
- Imitation-learning work on causal confusion shows that policies can attend to spurious temporal correlates.
- Attention-based attribution is known to be an unreliable causal explanation unless tested counterfactually.
- Pseudo-reward temporal-difference relabeling may be enough if the benchmark is too close to a delayed-reward problem.
- Fixed-risk correction can be gamed if coverage and abstention are not reported.

## v5 Response

The v5 rebuild narrows the novelty boundary to reward-free physical credit: assigning earlier action credit from observation/action event structure without scalar reward labels. The local benchmark supports that boundary: v5 hard success is `0.85078 +/- 0.00548` versus `0.75408 +/- 0.01010` for the strongest non-oracle success reference, with credit F1 `0.59262`, delayed-blame F1 `0.62083`, false credit `0.00234`, irreversible side effect `0.00217`, wasted action `0.02708`, and utility `0.67809`.

Strict fixed-risk correction is reported separately: at budget `0.18`, coverage is `1.00000`, success is `0.86059`, and utility is `0.67982`.

## Remaining Hostile Review

A hostile reviewer would still be correct to reject a main-track submission today. The evidence is local and synthetic; the baselines are executable diagnostic models rather than external robot systems; and there is no real robot or independently validated high-fidelity simulator evidence.

## Honest Action

The paper is marked `STRONG_REVISE`. Continue only if the next version adds real robot or high-fidelity external validation and implemented learned baselines.
