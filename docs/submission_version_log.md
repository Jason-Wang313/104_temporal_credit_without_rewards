# Submission Version Log

## v1 - Generated Draft

- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening

- Added hostile reviewer attack log and response docs.
- Added seven-seed synthetic metrics, stronger baselines, ablations, stress tests, and negative cases.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive

- Applied stricter ICLR-main-conference standard.
- Marked the existing artifact `KILL_ARCHIVE` because the local evidence was template-like and underpowered.

## v4 - Paper-Specific Evidence Rebuild

- Added `docs/paper104_rebuild_plan.md`.
- Replaced the runner with a reward-free temporal-credit benchmark.
- Generated fresh metrics, per-task/per-regime tables, pairwise tests, ablations, stress sweeps, failure cases, figures, and LaTeX tables.
- Removed obsolete v3 outputs from the runner.
- Rewrote the paper as a strong-revise evidence report with honest limitations.
- Terminal decision: STRONG_REVISE.

## v4.1 - Continuation Re-Audit

- Added `docs/paper104_iclr_submission_execution_plan_20260615.md`.
- Recompiled `src/run_experiment.py` and regenerated the benchmark from source.
- Verified CSV coverage, strongest-baseline gate, credit/delayed-blame diagnostics, safety gates, pairwise seed statistics, stress sweep, ablations, failure cases, PDF rebuild path, and no-Desktop artifact rule.
- Terminal decision remains STRONG_REVISE because local evidence passes all gates, but ICLR-main readiness remains `no` without real robot or external high-fidelity validation.

## v5 - Expanded Hostile-Review Rebuild

- Added `docs/paper104_expanded_submission_plan_20260622.md`.
- Replaced the aggregate-only runner with a RAM-light streaming v5 runner over 6 tasks, 8 regimes, 8 splits, 15 methods, 10 seeds, and raw rollout persistence.
- Added raw main, ablation, stress-sweep, and fixed-risk CSVs; machine-readable `summary.json`; and `row_counts.csv`.
- Added strict fixed-risk correction budgets and a scope gate that remains false without external validation.
- Added `scripts/generate_manuscript.py` and `scripts/validate_submission_artifacts.py`.
- Generated a 26-page PDF with bright boxed clickable citations and copied it only to `C:/Users/wangz/Downloads/104.pdf`.
- Final PDF SHA256: `8ED1042D54E0B6E1570929F513B5376AEA4ACA2F6B239418686E2D7CCE988A3A`.
- Terminal decision remains STRONG_REVISE: all frozen local empirical gates pass, but ICLR-main readiness remains `no`.
