# Experiment Rigor Checklist

## v5 Local Evidence

- [x] Paper-specific reward-free temporal-credit benchmark.
- [x] 6 robot task families.
- [x] 8 temporal-credit regimes.
- [x] 8 distribution/stress splits.
- [x] 15 methods including oracle and strong non-oracle baselines.
- [x] 10 random seeds.
- [x] Raw rollout persistence for main, ablation, stress, and fixed-risk experiments.
- [x] Confidence intervals.
- [x] Pairwise seed comparisons.
- [x] Success, credit F1, delayed-blame F1, false-credit, missed-credit, irreversible-side-effect, wasted-action, early-correction, latency, ECE, regret, and utility metrics.
- [x] Ablations for prefix counterfactuals, physical preconditions, delayed eligibility memory, compensatory masking, confidence-gated correction, false-credit suppression, risk calibration, and early correction.
- [x] Stress sweep over delay length, hidden-state confounding, compensatory masking, false-credit pressure, and intervention-latency pressure.
- [x] Strict fixed-risk correction budgets.
- [x] 24 generated negative cases.
- [x] Machine-readable `summary.json` and `row_counts.csv`.
- [x] Generated figures and LaTeX tables.
- [x] 26-page PDF with bright boxed clickable citations.
- [x] 2026-06-22 v5 terminal audit.

## Remaining ICLR-Main Gaps

- [ ] Real-robot validation.
- [ ] Independent high-fidelity simulator benchmark.
- [ ] Implemented learned model checkpoints.
- [ ] Implemented real competing baselines.
- [ ] External benchmark comparison.
- [ ] Calibrated real temporal-credit logs.
- [ ] Deployment videos or qualitative rollouts.

Decision: strong-revise. The local evidence is serious enough to continue, but not enough to submit as ICLR-main-ready.
