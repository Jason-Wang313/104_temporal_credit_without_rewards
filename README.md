# 104 Temporal Credit Without Rewards

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for ICLR main conference.

The rebuilt evidence package tests whether a robot can assign delayed physical credit without scalar reward labels or RL-style dense feedback. The local benchmark supports the mechanism, but the paper is not yet ICLR-main-ready because it still lacks real-robot or independent high-fidelity simulator validation.

## Evidence Snapshot

- Benchmark: 5 tasks x 7 temporal-credit regimes x 5 splits x 9 methods.
- Repeats: 7 seeds, 84 episodes per task/regime/split/method group.
- Strongest non-oracle baseline: `pseudo_reward_td_relabeling`.
- Combined-stress success: proposed `0.636 +/- 0.006`, strongest non-oracle `0.531 +/- 0.007`.
- Credit diagnostics: proposed credit F1 `0.520`, delayed-blame F1 `0.497`.
- Safety: proposed irreversible side-effect rate `0.050` vs `0.073`, wasted-action rate `0.102` vs `0.165`.
- Pairwise seeds: proposed beats strongest non-oracle baseline in `7/7` seeds.
- Terminal gate: `STRONG_REVISE`, not submit-as-is.

## Reproduce

```powershell
python src\run_experiment.py
```

Key outputs are in `results/` and `figures/`.

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/104.pdf`
