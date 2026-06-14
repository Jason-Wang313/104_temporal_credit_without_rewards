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

The v4 benchmark supports the boundary under combined stress: proposed success is `0.636 +/- 0.006` versus `0.531 +/- 0.007` for the strongest non-oracle baseline, credit F1 is `0.520`, and delayed-blame F1 is `0.497`.

## Remaining Gap

The literature boundary is credible enough for strong revise, but not for submission. The next version needs external robot/high-fidelity experiments and implemented learned baselines.
