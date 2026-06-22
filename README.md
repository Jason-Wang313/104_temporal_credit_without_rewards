# 104 Temporal Credit Without Rewards

Submission-hardening version: v5 expanded hostile-review rebuild

Terminal decision: `STRONG_REVISE`

ICLR main ready: `no`

This repository tests whether delayed physical credit can be assigned without scalar reward labels by combining counterfactual prefix tests, physical precondition graphs, delayed eligibility memory, compensatory-action masking, and risk-calibrated correction. The v5 local evidence passes all frozen empirical gates, but the scope gate fails because there is still no real-robot, accepted high-fidelity simulator, external benchmark, calibrated real temporal-credit log, trained checkpoint, or rollout-video evidence.

## Evidence Snapshot

- Benchmark: 6 tasks x 8 temporal-credit regimes x 8 splits x 15 methods.
- Repeats: 10 seeds, 6 episodes per factorial cell.
- Raw evidence: 345,600 main rollouts, 115,200 ablation rollouts, 288,000 stress-sweep rollouts, 276,480 fixed-risk rollouts.
- Strongest non-oracle hard-success reference: `proposed_reward_free_temporal_credit_v4`.
- Hard success: v5 `0.85078 +/- 0.00548`, v4 reference `0.75408 +/- 0.01010`, oracle `0.93255`.
- Credit diagnostics: v5 credit F1 `0.59262`, delayed-blame F1 `0.62083`.
- Failure diagnostics: false credit `0.00234`, missed credit `0.13906`, irreversible side effect `0.00217`, wasted action `0.02708`.
- Calibration and utility: ECE `0.00257`, regret `0.07714`, utility `0.67809`.
- Strict fixed-risk budget 0.18: coverage `1.00000`, success `0.86059`, utility `0.67982`.
- Canonical PDF: `C:/Users/wangz/Downloads/104.pdf`, 26 pages, SHA256 `8ED1042D54E0B6E1570929F513B5376AEA4ACA2F6B239418686E2D7CCE988A3A`.
- GitHub: https://github.com/Jason-Wang313/104_temporal_credit_without_rewards

## Reproduce

```powershell
python -m py_compile src\run_experiment.py
python src\run_experiment.py
python -m py_compile scripts\generate_manuscript.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
Copy-Item paper\main.pdf C:\Users\wangz\Downloads\104.pdf -Force
python scripts\validate_submission_artifacts.py
```

The final PDF is intentionally written to Downloads only. No visible Desktop copy is produced.
