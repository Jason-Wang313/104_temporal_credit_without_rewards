# Paper 104 Terminal Audit

Date: 2026-06-22

Repository: `104_temporal_credit_without_rewards`

Terminal decision: `STRONG_REVISE`

ICLR main ready: `no`

## Commands Verified

- `python -m py_compile src\run_experiment.py`
- `python src\run_experiment.py`
- `python -m py_compile scripts\generate_manuscript.py`
- `python scripts\generate_manuscript.py`
- `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`
- `python -m py_compile scripts\validate_submission_artifacts.py`
- `python scripts\validate_submission_artifacts.py`

## Final Metrics

- v5 hard success: `0.85078 +/- 0.00548`
- strongest non-oracle hard success: `0.75408 +/- 0.01010`
- oracle hard success: `0.93255`
- v5 credit F1: `0.59262`
- v5 delayed-blame F1: `0.62083`
- v5 false credit: `0.00234`
- v5 irreversible side effect: `0.00217`
- v5 wasted action: `0.02708`
- v5 ECE: `0.00257`
- v5 utility: `0.67809`
- strict fixed-risk coverage: `1.00000`
- strict fixed-risk utility: `0.67982`

## PDF

- Canonical path: `C:/Users/wangz/Downloads/104.pdf`
- Pages: 26
- SHA256: `8ED1042D54E0B6E1570929F513B5376AEA4ACA2F6B239418686E2D7CCE988A3A`
- Citation links: bright boxed citations enabled through hyperref border options.
- Desktop copy: none.

## Terminal Rationale

All frozen local empirical gates pass. The scope gate fails because there is no real robot or accepted external high-fidelity validation. The correct terminal state is therefore `STRONG_REVISE`, not ICLR-main-ready.
