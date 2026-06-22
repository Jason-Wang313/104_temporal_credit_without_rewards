# Claims

- Mechanism claim: long-horizon robot traces contain physical event structure that can assign delayed action credit without scalar reward labels.
- Method claim: counterfactual prefix tests, physical precondition graphs, delayed eligibility memory, compensatory-action masking, false-credit suppression, and risk-calibrated correction improve reward-free temporal credit.
- Evidence claim: in the v5 local rerun, `risk_calibrated_temporal_credit_v5` reaches hard success `0.85078 +/- 0.00548` versus `0.75408 +/- 0.01010` for the strongest non-oracle success reference.
- Diagnostic claim: v5 reaches credit F1 `0.59262` and delayed-blame F1 `0.62083`, both above the strongest non-oracle diagnostic references.
- Safety claim: v5 reports false credit `0.00234`, irreversible side effect `0.00217`, and wasted action `0.02708`, all below the strongest non-oracle success reference.
- Fixed-risk claim: at strict budget `0.18`, v5 keeps coverage `1.00000`, success `0.86059`, and utility `0.67982`.
- Scope claim: the evidence supports a strong-revise decision only; it does not establish real-robot deployment performance.
- Unsupported claim explicitly avoided: no claim of ICLR-main readiness, deployment safety, or state-of-the-art robot performance.
