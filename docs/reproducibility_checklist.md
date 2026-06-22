# Reproducibility Checklist

## Reproduces Locally

- [x] `python -m py_compile src/run_experiment.py`
- [x] `python src/run_experiment.py`
- [x] `results/dataset_summary.csv`
- [x] `results/rollouts.csv`
- [x] `results/main_group_metrics.csv`
- [x] `results/main_seed_metrics.csv`
- [x] `results/metrics.csv`
- [x] `results/hard_aggregate_seed_metrics.csv`
- [x] `results/hard_aggregate_metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/ablation_rollouts.csv`
- [x] `results/ablation_seed_metrics.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/stress_sweep_raw.csv`
- [x] `results/stress_sweep_seed_metrics.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/fixed_risk_raw.csv`
- [x] `results/fixed_risk_seed_metrics.csv`
- [x] `results/fixed_risk_metrics.csv`
- [x] `results/fixed_risk_pairwise_stats.csv`
- [x] `results/failure_cases.csv`
- [x] `results/summary.json`
- [x] `results/row_counts.csv`
- [x] `figures/temporal_v5_hard_success.png`
- [x] `figures/temporal_v5_diagnostics.png`
- [x] `figures/temporal_v5_safety_regret.png`
- [x] `figures/temporal_v5_stress_sweep.png`
- [x] `figures/temporal_v5_ablation.png`
- [x] `figures/temporal_v5_fixed_risk.png`
- [x] `python -m py_compile scripts/generate_manuscript.py`
- [x] `python scripts/generate_manuscript.py`
- [x] `python -m py_compile scripts/validate_submission_artifacts.py`
- [x] `python scripts/validate_submission_artifacts.py`
- [x] Canonical PDF: `C:/Users/wangz/Downloads/104.pdf`

## Does Not Yet Reproduce

- [ ] Real robot results.
- [ ] Independent high-fidelity simulator runs.
- [ ] Trained policy checkpoints.
- [ ] Real deployment videos.
- [ ] External benchmark results.
- [ ] Calibrated real temporal-credit logs.

This repository reproduces a v5 strong-revise evidence package, not a finished ICLR-main submission.
