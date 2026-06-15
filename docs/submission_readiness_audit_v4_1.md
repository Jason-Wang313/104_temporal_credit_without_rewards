# Submission Readiness Audit v4.1

Audit date: 2026-06-15 16:25:50 +0100

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

## Commands Executed

- `python -m py_compile src/run_experiment.py`
- `python src/run_experiment.py`

Continuation rerun log:

- `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/104_temporal_credit_without_rewards_continuation_rerun_20260615.log`

## Regenerated Evidence Coverage

- `metrics.csv`: 45 rows.
- `per_task_regime_metrics.csv`: 1575 rows.
- `seed_task_regime_metrics.csv`: 11025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_regime_seed_metrics.csv`: 1715 rows.
- `stress_sweep.csv`: 30 rows.
- `stress_sweep_seed_metrics.csv`: 7350 rows.
- `failure_cases.csv`: 8 rows.

Coverage remained the declared design: 5 tasks, 7 temporal-credit regimes, 5 splits, 9 methods, and 7 seeds.

## Main Gate Evidence

Strongest non-oracle baseline: `pseudo_reward_td_relabeling`.

Combined-stress metrics:

- Proposed success: `0.6356 +/- 0.0055`.
- Strongest baseline success: `0.5309 +/- 0.0075`.
- Success margin: `+0.1047 +/- 0.0088`.
- Proposed credit F1: `0.5196`.
- Proposed delayed-blame F1: `0.4965`.
- Proposed irreversible side-effect rate: `0.0500` vs `0.0734` baseline.
- Proposed wasted-action rate: `0.1022` vs `0.1650` baseline.
- Proposed credit latency: `0.6223` vs `0.7408` baseline.
- Proposed regret to oracle: `0.1477` vs `0.2518` baseline.

Diagnostic baselines:

- Best diagnostic baseline: `sequence_contrastive_credit`.
- Credit F1 delta: `+0.1439`.
- Delayed-blame F1 delta: `+0.2044`.

Paired seed comparison against `pseudo_reward_td_relabeling`:

- Success difference: `0.1047 +/- 0.0088`.
- Wins: `7/7`.

## Ablation Gate

- Full method success: `0.6406 +/- 0.0084`.
- Best removed-component ablation: `minus_compensatory_action_masking`.
- Best removed-component success: `0.5783 +/- 0.0054`.
- Ablation margin: `+0.0622`.

All core ablations remain below full.

## Stress Sweep

The proposed method remains above `pseudo_reward_td_relabeling` across the generated delay/confounding stress sweep. At maximum stress level `0.95`, proposed success is `0.6405 +/- 0.0081` vs `0.5317 +/- 0.0107`, with lower irreversible side effects and wasted actions.

## Terminal Decision

Keep `STRONG_REVISE`. The local evidence supports reward-free temporal credit from physical event structure, but this is not ICLR-main-ready without real robot, external high-fidelity simulator, implemented learned-baseline, or external benchmark evidence.

## PDF Verification

- Canonical PDF: `C:/Users/wangz/Downloads/104.pdf`.
- SHA256: `FE049893E561B30B19597EF6C06EAB44DC379339EA3759B4DF5C24EDDE9021C1`.
- Size: `427637` bytes.
- Desktop copy: absent.
- LaTeX/BibTeX scan: no actionable warnings after ragged-right bibliography wrapping; only harmless `rerunfilecheck` package text and BibTeX built-in statistics appeared.
