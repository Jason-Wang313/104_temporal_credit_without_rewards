# ICLR Main Gate

Paper: 104 temporal_credit_without_rewards

Previous v4.1 decision: STRONG_REVISE

v5 expanded gate verdict: STRONG_REVISE

Evidence digest: 6 tasks x 8 temporal-credit regimes x 8 splits x 15 methods x 10 seeds x 6 episodes per cell.

Gate outcomes:

- Success gate: pass. V5 hard success `0.85078` exceeds strongest non-oracle success reference `0.75408` by `0.09670`.
- Diagnostic gate: pass. V5 credit F1 `0.59262` and delayed-blame F1 `0.62083` exceed the best non-oracle diagnostic references.
- False-credit gate: pass. V5 false credit `0.00234` is below strongest non-oracle success reference `0.03620`.
- Irreversible-side-effect gate: pass. V5 irreversible side effect `0.00217` is below strongest non-oracle success reference `0.01745`.
- Wasted-action gate: pass. V5 wasted action `0.02708` is below strongest non-oracle success reference `0.08220`.
- Calibration gate: pass. V5 ECE `0.00257` is below `0.12`.
- Utility gate: pass. V5 utility `0.67809` exceeds the best non-oracle utility reference.
- Pairwise gate: pass. V5 beats every non-oracle baseline over paired seeds and loses only to the oracle ceiling.
- Ablation gate: pass. Full v5 beats every removed-component ablation on hard success or utility.
- Stress gate: pass. V5 remains above the strongest non-oracle success reference at maximum stress.
- Fixed-risk gate: pass. Strict fixed-risk budget 0.18 has coverage `1.00000` and utility `0.67982`.
- Scope gate: fail. No real robot, accepted high-fidelity benchmark, external benchmark, calibrated real logs, trained checkpoints, or rollout videos.

Terminal decision: STRONG_REVISE.

Submission status: not ICLR-main-ready until external robot or high-fidelity validation is added.
