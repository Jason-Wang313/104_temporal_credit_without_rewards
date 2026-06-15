# Experiment Rigor Checklist

## v4.1 Local Evidence

- [x] Paper-specific reward-free temporal-credit benchmark.
- [x] 5 robot task families.
- [x] 7 temporal-credit regimes.
- [x] 5 distribution/stress splits.
- [x] 9 methods including oracle and strong non-oracle baselines.
- [x] 7 random seeds.
- [x] 84 episodes per group.
- [x] Confidence intervals.
- [x] Pairwise seed comparisons.
- [x] Success, credit F1, delayed-blame F1, false-credit, irreversible side-effect, wasted-action, latency, cost, and regret metrics.
- [x] Ablations for prefix counterfactuals, physical preconditions, delayed eligibility memory, compensatory masking, and confidence-gated intervention.
- [x] Stress sweep over delay/confounding intensity.
- [x] Failure-case table.
- [x] Generated figures and LaTeX tables.
- [x] 2026-06-15 continuation rerun from source.
- [x] v4.1 terminal audit.

## Remaining ICLR-Main Gaps

- [ ] Real-robot validation.
- [ ] Independent high-fidelity simulator benchmark.
- [ ] Implemented learned model checkpoints.
- [ ] Implemented real competing baselines.
- [ ] External benchmark comparison.
- [ ] Deployment videos or qualitative rollouts.

Decision: strong-revise. The local evidence is serious enough to continue, but not enough to submit.
