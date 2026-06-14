# ICLR Main Gate

Paper: 104 temporal_credit_without_rewards

Previous v3 decision: KILL_ARCHIVE

v4 gate verdict: STRONG_REVISE

Evidence digest: 5 tasks x 7 temporal-credit regimes x 5 splits x 9 methods x 7 seeds x 84 episodes/group.

Gate outcomes:

- Success gate: pass. Proposed combined-stress success exceeds the strongest non-oracle baseline by `0.105`.
- Diagnostic gate: pass. Credit F1 improves by `0.144` and delayed-blame F1 by `0.204` over the best diagnostic baseline.
- Safety gate: pass. Irreversible side-effect and wasted-action rates are lower than the strongest non-oracle baseline.
- Pairwise gate: pass. Proposed beats the strongest non-oracle baseline in `7/7` seeds.
- Ablation gate: pass. The full model beats the best removed-component ablation by `0.0622`.

Terminal decision: STRONG_REVISE.

Submission status: not ICLR-main-ready until real robot or independent high-fidelity validation is added.
