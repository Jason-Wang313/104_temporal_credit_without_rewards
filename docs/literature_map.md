# Literature Map

Paper: 104 temporal_credit_without_rewards

Field box: long-horizon robot learning, temporal credit assignment, reward-free imitation/control diagnostics.

Thesis: assign delayed physical credit from observation/action event structure without scalar reward labels.

## Crowded Clusters

- Delayed-reward credit assignment in reinforcement learning.
- Hindsight relabeling and sparse reward methods.
- Return-conditioned sequence modeling and offline RL.
- Imitation learning under causal confusion.
- Attention attribution and saliency for sequence models.
- Long-horizon robot task decomposition.

## Boundary

The paper's boundary is reward-free physical credit. A pseudo-reward method can relabel final outcomes; an attention model can highlight salient timesteps; a contrastive method can align prefixes with outcomes. The proposed mechanism asks whether physical preconditions, delayed eligibility, and compensatory masking reveal which earlier actions caused later success or failure without scalar reward labels.

## Local Evidence

The v5 benchmark supports the boundary under hard splits: v5 success is `0.85078 +/- 0.00548` versus `0.75408 +/- 0.01010` for the strongest non-oracle success reference, credit F1 is `0.59262`, delayed-blame F1 is `0.62083`, false credit is `0.00234`, and utility is `0.67809`.

## Remaining Gap

The literature boundary is credible enough for strong revise, but not for submission. The next version needs external robot/high-fidelity experiments, implemented learned baselines, calibrated real temporal-credit logs, and external benchmark evidence.
