# Reproducibility Checklist

## Reproduces Locally

- [x] `python -m py_compile src/run_experiment.py`
- [x] `python src/run_experiment.py`
- [x] `results/seed_task_regime_metrics.csv`
- [x] `results/per_task_regime_metrics.csv`
- [x] `results/seed_split_metrics.csv`
- [x] `results/metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/ablation_seed_metrics.csv`
- [x] `results/ablation_task_regime_seed_metrics.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/stress_sweep_seed_metrics.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/failure_cases.csv`
- [x] `figures/temporal_credit_combined_success.png`
- [x] `figures/temporal_credit_diagnostics.png`
- [x] `figures/temporal_credit_safety_regret.png`
- [x] `figures/temporal_credit_stress_sweep.png`
- [x] `figures/temporal_credit_ablation.png`
- [x] `paper/main.tex`
- [x] Canonical PDF: `C:/Users/wangz/Downloads/104.pdf`

## Does Not Yet Reproduce

- [ ] Real robot results.
- [ ] Independent high-fidelity simulator runs.
- [ ] Trained policy checkpoints.
- [ ] Real deployment videos.

This repository reproduces a v4.1 strong-revise evidence package, not a finished ICLR-main submission.
The 2026-06-15 v4.1 continuation rerun recompiled and regenerated the same evidence package from source; log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/104_temporal_credit_without_rewards_continuation_rerun_20260615.log`.
