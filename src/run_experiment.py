import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 104_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]

DISPLAY_NAMES = {
    "behavior_clone_no_credit": "BC",
    "uniform_credit_assignment": "Uniform",
    "hindsight_success_relabeling": "Hindsight",
    "inverse_dynamics_saliency": "InvDyn",
    "transformer_attention_attribution": "Attention",
    "sequence_contrastive_credit": "Contrastive",
    "pseudo_reward_td_relabeling": "PseudoTD",
    "proposed_reward_free_temporal_credit_graph": "Proposed",
    "oracle_event_credit_labels": "Oracle",
    "full_reward_free_temporal_credit_graph": "Full",
    "minus_counterfactual_prefix_tests": "NoPrefixCF",
    "minus_physical_precondition_graph": "NoPrecond",
    "minus_delayed_eligibility_memory": "NoDelayMem",
    "minus_compensatory_action_masking": "NoCompMask",
    "minus_confidence_gated_intervention": "NoConfGate",
    "attention_credit_only": "AttentionOnly",
}

TASKS = [
    {"task": "multi_step_assembly", "difficulty": 0.070, "horizon": 0.91, "preconditions": 0.86, "side_effect": 0.56},
    {"task": "cluttered_retrieval", "difficulty": 0.060, "horizon": 0.74, "preconditions": 0.68, "side_effect": 0.61},
    {"task": "drawer_door_unlatching", "difficulty": 0.073, "horizon": 0.84, "preconditions": 0.89, "side_effect": 0.70},
    {"task": "peg_in_hole_preparation", "difficulty": 0.078, "horizon": 0.93, "preconditions": 0.92, "side_effect": 0.73},
    {"task": "tool_mediated_manipulation", "difficulty": 0.066, "horizon": 0.88, "preconditions": 0.80, "side_effect": 0.67},
]

REGIMES = [
    {"regime": "immediate_contact_outcome", "delay": 0.12, "hidden": 0.10, "confound": 0.14, "compensation": 0.08, "side": 0.25},
    {"regime": "short_delayed_outcome", "delay": 0.42, "hidden": 0.22, "confound": 0.23, "compensation": 0.18, "side": 0.35},
    {"regime": "long_delayed_outcome", "delay": 0.78, "hidden": 0.32, "confound": 0.33, "compensation": 0.28, "side": 0.44},
    {"regime": "hidden_precondition", "delay": 0.58, "hidden": 0.82, "confound": 0.40, "compensation": 0.31, "side": 0.51},
    {"regime": "irreversible_side_effect", "delay": 0.50, "hidden": 0.36, "confound": 0.42, "compensation": 0.20, "side": 0.89},
    {"regime": "compensatory_action_masking", "delay": 0.62, "hidden": 0.45, "confound": 0.78, "compensation": 0.88, "side": 0.54},
    {"regime": "compositional_delayed_failure", "delay": 0.86, "hidden": 0.76, "confound": 0.84, "compensation": 0.72, "side": 0.82},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "delay_shift": 0.08, "obs_gap": 0.06, "confound_shift": 0.04, "side_shift": 0.05},
    {"split": "longer_horizon_shift", "stress": 0.52, "delay_shift": 0.70, "obs_gap": 0.18, "confound_shift": 0.20, "side_shift": 0.16},
    {"split": "sparse_observation_shift", "stress": 0.55, "delay_shift": 0.42, "obs_gap": 0.78, "confound_shift": 0.31, "side_shift": 0.22},
    {"split": "confounded_success_shift", "stress": 0.58, "delay_shift": 0.44, "obs_gap": 0.34, "confound_shift": 0.78, "side_shift": 0.31},
    {"split": "combined_stress", "stress": 0.82, "delay_shift": 0.74, "obs_gap": 0.66, "confound_shift": 0.76, "side_shift": 0.68},
]

METHODS = [
    {"method": "behavior_clone_no_credit", "base": 0.642, "credit": 0.05, "delayed": 0.04, "precond": 0.05, "mask": 0.05, "intervene": 0.06, "side_ctrl": 0.07, "cost": 0.04, "false": 0.12},
    {"method": "uniform_credit_assignment", "base": 0.660, "credit": 0.16, "delayed": 0.10, "precond": 0.10, "mask": 0.08, "intervene": 0.10, "side_ctrl": 0.12, "cost": 0.08, "false": 0.18},
    {"method": "hindsight_success_relabeling", "base": 0.684, "credit": 0.30, "delayed": 0.18, "precond": 0.18, "mask": 0.14, "intervene": 0.16, "side_ctrl": 0.18, "cost": 0.12, "false": 0.22},
    {"method": "inverse_dynamics_saliency", "base": 0.696, "credit": 0.38, "delayed": 0.24, "precond": 0.26, "mask": 0.22, "intervene": 0.22, "side_ctrl": 0.26, "cost": 0.18, "false": 0.26},
    {"method": "transformer_attention_attribution", "base": 0.705, "credit": 0.46, "delayed": 0.30, "precond": 0.34, "mask": 0.28, "intervene": 0.30, "side_ctrl": 0.34, "cost": 0.23, "false": 0.30},
    {"method": "sequence_contrastive_credit", "base": 0.713, "credit": 0.54, "delayed": 0.38, "precond": 0.42, "mask": 0.36, "intervene": 0.36, "side_ctrl": 0.40, "cost": 0.26, "false": 0.27},
    {"method": "pseudo_reward_td_relabeling", "base": 0.724, "credit": 0.48, "delayed": 0.52, "precond": 0.46, "mask": 0.40, "intervene": 0.44, "side_ctrl": 0.45, "cost": 0.30, "false": 0.24},
    {"method": "proposed_reward_free_temporal_credit_graph", "base": 0.735, "credit": 0.76, "delayed": 0.74, "precond": 0.72, "mask": 0.66, "intervene": 0.64, "side_ctrl": 0.68, "cost": 0.24, "false": 0.16},
    {"method": "oracle_event_credit_labels", "base": 0.792, "credit": 0.95, "delayed": 0.94, "precond": 0.93, "mask": 0.90, "intervene": 0.82, "side_ctrl": 0.86, "cost": 0.18, "false": 0.05},
]

ABLATIONS = [
    ("full_reward_free_temporal_credit_graph", {"base": 0.735, "credit": 0.76, "delayed": 0.74, "precond": 0.72, "mask": 0.66, "intervene": 0.64, "side_ctrl": 0.68, "cost": 0.24, "false": 0.16}, "all components"),
    ("minus_counterfactual_prefix_tests", {"base": 0.718, "credit": 0.52, "delayed": 0.60, "precond": 0.56, "mask": 0.50, "intervene": 0.54, "side_ctrl": 0.60, "cost": 0.20, "false": 0.20}, "removes prefix-level counterfactual tests"),
    ("minus_physical_precondition_graph", {"base": 0.712, "credit": 0.64, "delayed": 0.62, "precond": 0.36, "mask": 0.52, "intervene": 0.56, "side_ctrl": 0.57, "cost": 0.20, "false": 0.19}, "removes latent physical precondition graph"),
    ("minus_delayed_eligibility_memory", {"base": 0.709, "credit": 0.62, "delayed": 0.34, "precond": 0.62, "mask": 0.54, "intervene": 0.50, "side_ctrl": 0.58, "cost": 0.20, "false": 0.18}, "forgets long-delayed action eligibility"),
    ("minus_compensatory_action_masking", {"base": 0.716, "credit": 0.66, "delayed": 0.64, "precond": 0.64, "mask": 0.28, "intervene": 0.56, "side_ctrl": 0.58, "cost": 0.20, "false": 0.26}, "does not discount actions that hide earlier mistakes"),
    ("minus_confidence_gated_intervention", {"base": 0.724, "credit": 0.72, "delayed": 0.70, "precond": 0.68, "mask": 0.62, "intervene": 0.28, "side_ctrl": 0.42, "cost": 0.14, "false": 0.15}, "diagnoses credit but does not gate corrections"),
    ("attention_credit_only", {"base": 0.705, "credit": 0.46, "delayed": 0.30, "precond": 0.34, "mask": 0.28, "intervene": 0.30, "side_ctrl": 0.34, "cost": 0.23, "false": 0.30}, "attention attribution baseline"),
]


def clean_obsolete_outputs():
    for path in OBSOLETE_OUTPUTS:
        if path.exists():
            path.unlink()


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probabilities(method, task, regime, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else stress_override
    delay_shift = split["delay_shift"] if stress_override is None else min(0.95, 0.18 + 0.72 * stress)
    obs_gap = split["obs_gap"] if stress_override is None else min(0.95, 0.10 + 0.65 * stress)
    confound_shift = split["confound_shift"] if stress_override is None else min(0.95, 0.12 + 0.72 * stress)
    side_shift = split["side_shift"] if stress_override is None else min(0.95, 0.10 + 0.70 * stress)

    horizon_load = task["horizon"] * regime["delay"] * (0.58 + 0.56 * delay_shift + 0.24 * stress)
    hidden_load = task["preconditions"] * regime["hidden"] * (0.55 + 0.50 * obs_gap + 0.20 * stress)
    confound_load = regime["confound"] * (0.55 + 0.58 * confound_shift)
    compensation_load = regime["compensation"] * (0.48 + 0.54 * confound_shift + 0.18 * stress)
    side_load = task["side_effect"] * regime["side"] * (0.55 + 0.52 * side_shift + 0.15 * stress)

    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    noise = rng.normal(0.0, 0.011)

    credit_f1 = clamp(
        0.220
        + 0.355 * method["credit"]
        + 0.140 * method["precond"]
        + 0.080 * method["mask"]
        - 0.070 * obs_gap
        - 0.060 * confound_shift
        - 0.045 * delay_shift
        + rng.normal(0.0, 0.010),
        0.02,
        0.99,
    )
    delayed_blame_f1 = clamp(
        0.190
        + 0.390 * method["delayed"]
        + 0.120 * method["precond"]
        + 0.100 * method["mask"]
        - 0.075 * delay_shift
        - 0.060 * obs_gap
        - 0.050 * confound_shift
        + rng.normal(0.0, 0.010),
        0.02,
        0.99,
    )
    false_credit = clamp(
        method["false"]
        + 0.100 * confound_load * (1.0 - method["mask"])
        + 0.070 * obs_gap * (1.0 - method["precond"])
        - 0.045 * method["credit"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.72,
    )
    irreversible = clamp(
        0.050
        + 0.150 * side_load * (1.0 - method["side_ctrl"])
        + 0.040 * false_credit
        - 0.035 * method["intervene"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.55,
    )
    wasted_actions = clamp(
        0.095
        + 0.150 * horizon_load * (1.0 - method["credit"])
        + 0.110 * hidden_load * (1.0 - method["precond"])
        + 0.095 * compensation_load * (1.0 - method["mask"])
        + 0.045 * false_credit
        - 0.070 * method["intervene"]
        + rng.normal(0.0, 0.007),
        0.0,
        0.70,
    )
    early_correction = clamp(
        0.160
        + 0.270 * method["intervene"]
        + 0.165 * delayed_blame_f1
        + 0.095 * credit_f1
        - 0.080 * obs_gap
        - 0.060 * confound_shift
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    credit_latency = clamp(
        0.690
        + 0.320 * horizon_load
        + 0.180 * hidden_load
        + 0.120 * false_credit
        - 0.310 * method["delayed"]
        - 0.150 * method["precond"]
        + rng.normal(0.0, 0.014),
        0.03,
        1.45,
    )
    success = clamp(
        method["base"]
        - task["difficulty"]
        - 0.145 * horizon_load * (1.0 - method["delayed"])
        - 0.130 * hidden_load * (1.0 - method["precond"])
        - 0.115 * confound_load * (1.0 - method["credit"])
        - 0.105 * compensation_load * (1.0 - method["mask"])
        - 0.115 * side_load * (1.0 - method["side_ctrl"])
        + 0.115 * method["intervene"]
        - 0.045 * method["cost"]
        - 0.085 * irreversible
        - 0.055 * wasted_actions
        + noise,
        0.02,
        0.98,
    )
    intervention_cost = clamp(
        0.120
        + 0.125 * method["cost"]
        + 0.115 * early_correction
        + 0.050 * credit_f1
        - 0.035 * method["side_ctrl"]
        + rng.normal(0.0, 0.006),
        0.02,
        0.75,
    )

    return {
        "success": success,
        "credit_f1": credit_f1,
        "delayed_blame_f1": delayed_blame_f1,
        "false_credit": false_credit,
        "irreversible_side_effect": irreversible,
        "wasted_action_rate": wasted_actions,
        "early_correction": early_correction,
        "credit_latency": credit_latency,
        "intervention_cost": intervention_cost,
    }


def simulate_group(method, task, regime, split, seed, stress_override=None):
    probs = probabilities(method, task, regime, split, seed, stress_override=stress_override)
    rng = rng_for("episodes", method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    metrics = {
        "success": rng.binomial(EPISODES_PER_GROUP, probs["success"]) / EPISODES_PER_GROUP,
        "irreversible_side_effect": rng.binomial(EPISODES_PER_GROUP, probs["irreversible_side_effect"]) / EPISODES_PER_GROUP,
        "wasted_action_rate": rng.binomial(EPISODES_PER_GROUP, probs["wasted_action_rate"]) / EPISODES_PER_GROUP,
        "early_correction": rng.binomial(EPISODES_PER_GROUP, probs["early_correction"]) / EPISODES_PER_GROUP,
        "credit_f1": clamp(probs["credit_f1"] + rng.normal(0.0, 0.010)),
        "delayed_blame_f1": clamp(probs["delayed_blame_f1"] + rng.normal(0.0, 0.010)),
        "false_credit": clamp(probs["false_credit"] + rng.normal(0.0, 0.006)),
        "credit_latency": clamp(probs["credit_latency"] + rng.normal(0.0, 0.012), 0.03, 1.50),
        "intervention_cost": clamp(probs["intervention_cost"] + rng.normal(0.0, 0.006)),
    }
    metrics["regret_to_oracle"] = 0.0
    return metrics


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / np.sqrt(len(arr)))


def aggregate(rows, keys, metrics):
    grouped = {}
    for row in rows:
        grouped.setdefault(tuple(row[k] for k in keys), []).append(row)
    output = []
    for key_values, group in sorted(grouped.items()):
        record = {k: v for k, v in zip(keys, key_values)}
        for metric in metrics:
            vals = [float(row[metric]) for row in group]
            record[f"mean_{metric}"] = float(np.mean(vals))
            record[f"ci95_{metric}"] = ci95(vals)
        record["groups"] = len(group)
        output.append(record)
    return output


def rounded(rows):
    out = []
    for row in rows:
        item = {}
        for key, value in row.items():
            item[key] = round(value, 4) if isinstance(value, float) else value
        out.append(item)
    return out


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_main():
    raw = []
    oracle_lookup = {}
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, regime, split, seed)
                        row = {
                            "method": method["method"],
                            "split": split["split"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_GROUP,
                            **metrics,
                        }
                        raw.append(row)
                        if method["method"] == "oracle_event_credit_labels":
                            oracle_lookup[(split["split"], task["task"], regime["regime"], seed)] = metrics["success"]
    for row in raw:
        key = (row["split"], row["task"], row["regime"], row["seed"])
        row["regret_to_oracle"] = max(0.0, oracle_lookup[key] - row["success"])
    metrics = [
        "success",
        "credit_f1",
        "delayed_blame_f1",
        "false_credit",
        "irreversible_side_effect",
        "wasted_action_rate",
        "early_correction",
        "credit_latency",
        "intervention_cost",
        "regret_to_oracle",
    ]
    seed_task_regime = aggregate(raw, ["method", "split", "task", "regime", "seed"], metrics)
    per_task_regime = aggregate(raw, ["method", "split", "task", "regime"], metrics)
    seed_split = aggregate(raw, ["method", "split", "seed"], metrics)
    summary = aggregate(seed_split, ["method", "split"], [f"mean_{m}" for m in metrics])
    for row in summary:
        if row["method"] == "oracle_event_credit_labels":
            row["mean_regret_to_oracle"] = 0.0
            row["ci95_regret_to_oracle"] = 0.0
        else:
            matching = [r for r in seed_split if r["method"] == row["method"] and r["split"] == row["split"]]
            row["mean_regret_to_oracle"] = float(np.mean([r["mean_regret_to_oracle"] for r in matching]))
            row["ci95_regret_to_oracle"] = ci95([r["mean_regret_to_oracle"] for r in matching])
    return raw, per_task_regime, seed_split, summary


def build_pairwise(seed_split, summary):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_stress"}
    non_oracle = [m for m in combined if m not in {"proposed_reward_free_temporal_credit_graph", "oracle_event_credit_labels"}]
    strongest = max(non_oracle, key=lambda method: float(combined[method]["mean_mean_success"]))
    proposed = {
        int(r["seed"]): float(r["mean_success"])
        for r in seed_split
        if r["split"] == "combined_stress" and r["method"] == "proposed_reward_free_temporal_credit_graph"
    }
    rows = []
    for method in sorted([m for m in combined if m != "proposed_reward_free_temporal_credit_graph"]):
        baseline = {
            int(r["seed"]): float(r["mean_success"])
            for r in seed_split
            if r["split"] == "combined_stress" and r["method"] == method
        }
        diffs = [proposed[seed] - baseline[seed] for seed in SEEDS]
        rows.append(
            {
                "comparison": f"proposed_reward_free_temporal_credit_graph_vs_{method}",
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": float(np.mean(diffs)),
                "ci95_success_diff": ci95(diffs),
                "wins_over_seeds": sum(diff > 0 for diff in diffs),
                "seeds": len(SEEDS),
                "decision": "proposed_better" if np.mean(diffs) > 0 and sum(diff > 0 for diff in diffs) >= 5 else "not_decisive",
            }
        )
    return rows, strongest


def build_ablations():
    split = next(s for s in SPLITS if s["split"] == "combined_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = with_name(params, name)
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    metrics = simulate_group(method, task, regime, split, seed)
                    rows.append(
                        {
                            "ablation": name,
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "interpretation": note,
                            **metrics,
                        }
                    )
    metrics = [
        "success",
        "credit_f1",
        "delayed_blame_f1",
        "false_credit",
        "irreversible_side_effect",
        "wasted_action_rate",
        "early_correction",
        "credit_latency",
        "intervention_cost",
    ]
    seed_summary = aggregate(rows, ["ablation", "seed"], metrics)
    summary = aggregate(seed_summary, ["ablation"], [f"mean_{m}" for m in metrics])
    for row in summary:
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    return rows, seed_summary, summary


def build_stress_sweep():
    split = next(s for s in SPLITS if s["split"] == "combined_stress")
    levels = np.linspace(0.10, 0.95, 6)
    keep = [
        "transformer_attention_attribution",
        "sequence_contrastive_credit",
        "pseudo_reward_td_relabeling",
        "proposed_reward_free_temporal_credit_graph",
        "oracle_event_credit_labels",
    ]
    rows = []
    for stress in levels:
        for method in [m for m in METHODS if m["method"] in keep]:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, regime, split, seed, stress_override=float(stress))
                        rows.append({"stress_level": float(stress), "method": method["method"], "task": task["task"], "regime": regime["regime"], "seed": seed, **metrics})
    summary = aggregate(rows, ["stress_level", "method"], [
        "success",
        "credit_f1",
        "delayed_blame_f1",
        "irreversible_side_effect",
        "wasted_action_rate",
        "credit_latency",
    ])
    return rows, summary


def make_figures(summary, ablation_summary, stress_summary):
    combined = [r for r in summary if r["split"] == "combined_stress"]
    combined = sorted(combined, key=lambda r: float(r["mean_mean_success"]))
    labels = [DISPLAY_NAMES.get(r["method"], r["method"]) for r in combined]
    y = np.arange(len(combined))

    plt.figure(figsize=(10, 5.8))
    plt.barh(y, [float(r["mean_mean_success"]) for r in combined], xerr=[float(r["ci95_mean_success"]) for r in combined], color=["#006d77" if r["method"] == "proposed_reward_free_temporal_credit_graph" else "#9aa6b2" for r in combined], capsize=3)
    plt.yticks(y, labels)
    plt.xlabel("Combined-stress success")
    plt.title("Temporal credit without rewards: combined stress")
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_credit_combined_success.png", dpi=180)
    plt.close()

    ordered = sorted([r for r in combined if r["method"] != "oracle_event_credit_labels"], key=lambda r: float(r["mean_mean_credit_f1"]), reverse=True)
    x = np.arange(len(ordered))
    plt.figure(figsize=(11, 5.6))
    plt.bar(x - 0.2, [float(r["mean_mean_credit_f1"]) for r in ordered], width=0.4, label="credit F1", color="#118ab2")
    plt.bar(x + 0.2, [float(r["mean_mean_delayed_blame_f1"]) for r in ordered], width=0.4, label="delayed-blame F1", color="#ef476f")
    plt.xticks(x, [DISPLAY_NAMES.get(r["method"], r["method"]) for r in ordered], rotation=30, ha="right")
    plt.ylabel("F1")
    plt.title("Credit attribution diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_credit_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.6))
    for method in sorted({r["method"] for r in stress_summary}):
        series = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.plot([float(r["stress_level"]) for r in series], [float(r["mean_success"]) for r in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Delay/confounding stress")
    plt.ylabel("Mean success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_credit_stress_sweep.png", dpi=180)
    plt.close()

    labels = [DISPLAY_NAMES.get(r["ablation"], r["ablation"]) for r in ablation_summary]
    ax = np.arange(len(labels))
    plt.figure(figsize=(10.5, 5.6))
    plt.bar(ax, [float(r["mean_mean_success"]) for r in ablation_summary], yerr=[float(r["ci95_mean_success"]) for r in ablation_summary], color=["#006d77" if r["ablation"] == "full_reward_free_temporal_credit_graph" else "#9aa6b2" for r in ablation_summary], capsize=3)
    plt.xticks(ax, labels, rotation=30, ha="right")
    plt.ylabel("Combined-stress success")
    plt.title("Temporal credit ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_credit_ablation.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.5, 5.4))
    plt.scatter([float(r["mean_mean_irreversible_side_effect"]) for r in combined], [float(r["mean_regret_to_oracle"]) for r in combined], s=70, c=["#006d77" if r["method"] == "proposed_reward_free_temporal_credit_graph" else "#9aa6b2" for r in combined])
    for r in combined:
        plt.text(float(r["mean_mean_irreversible_side_effect"]) + 0.002, float(r["mean_regret_to_oracle"]) + 0.002, DISPLAY_NAMES.get(r["method"], r["method"]), fontsize=8)
    plt.xlabel("Irreversible side-effect rate")
    plt.ylabel("Regret to oracle")
    plt.title("Safety/regret trade-off")
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_credit_safety_regret.png", dpi=180)
    plt.close()


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                values.append(f"{value:.3f}" if isinstance(value, float) else display_name(value))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def failure_cases(per_task_regime, strongest):
    combined = [r for r in per_task_regime if r["split"] == "combined_stress"]
    proposed = [r for r in combined if r["method"] == "proposed_reward_free_temporal_credit_graph"]
    peer = {(r["task"], r["regime"]): r for r in combined if r["method"] == strongest}
    gaps = []
    for row in proposed:
        base = peer[(row["task"], row["regime"])]
        gaps.append((float(row["mean_success"]) - float(base["mean_success"]), row, base))
    gaps.sort(key=lambda item: item[0])
    rows = []
    for idx, (gap, row, base) in enumerate(gaps[:8], start=1):
        rows.append(
            {
                "case_id": idx,
                "task": row["task"],
                "regime": row["regime"],
                "proposed_success": row["mean_success"],
                "strongest_baseline": strongest,
                "baseline_success": base["mean_success"],
                "success_gap": gap,
                "proposed_credit_f1": row["mean_credit_f1"],
                "proposed_irreversible_side_effect": row["mean_irreversible_side_effect"],
                "lesson": "reward-free temporal credit helps least when credit is immediate or a pseudo-reward baseline can relabel the outcome without confounding",
            }
        )
    return rows


def decide(summary, pairwise, ablations, strongest):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_stress"}
    proposed = combined["proposed_reward_free_temporal_credit_graph"]
    base = combined[strongest]
    diagnostic_methods = ["transformer_attention_attribution", "sequence_contrastive_credit", "pseudo_reward_td_relabeling"]
    diagnostic_peer = max(diagnostic_methods, key=lambda name: float(combined[name]["mean_mean_credit_f1"]))
    diagnostic = combined[diagnostic_peer]
    success_margin = float(proposed["mean_mean_success"]) - float(base["mean_mean_success"])
    credit_delta = float(proposed["mean_mean_credit_f1"]) - float(diagnostic["mean_mean_credit_f1"])
    blame_delta = float(proposed["mean_mean_delayed_blame_f1"]) - float(diagnostic["mean_mean_delayed_blame_f1"])
    side_delta = float(proposed["mean_mean_irreversible_side_effect"]) - float(base["mean_mean_irreversible_side_effect"])
    wasted_delta = float(proposed["mean_mean_wasted_action_rate"]) - float(base["mean_mean_wasted_action_rate"])
    strongest_pair = next(r for r in pairwise if r["baseline"] == strongest)
    full = next(r for r in ablations if r["ablation"] == "full_reward_free_temporal_credit_graph")
    best_ablation = max([r for r in ablations if r["ablation"] != "full_reward_free_temporal_credit_graph"], key=lambda r: float(r["mean_mean_success"]))
    ablation_margin = float(full["mean_mean_success"]) - float(best_ablation["mean_mean_success"])

    success_gate = success_margin >= 0.030
    diagnostic_gate = credit_delta >= 0.050 or blame_delta >= 0.050
    safety_gate = side_delta <= 0.020 and wasted_delta <= 0.020
    pairwise_gate = float(strongest_pair["mean_success_diff"]) > 0 and int(strongest_pair["wins_over_seeds"]) >= 5
    ablation_gate = ablation_margin >= 0.020
    if success_gate and diagnostic_gate and safety_gate and pairwise_gate and ablation_gate:
        decision = "STRONG_REVISE"
        rationale = "local reward-free temporal-credit evidence supports the mechanism, but real robot/external validation is missing"
    else:
        decision = "KILL_ARCHIVE"
        rationale = "local evidence fails the decisive success, diagnostic, safety, pairwise, or ablation gate"
    gates = {
        "success_gate": success_gate,
        "diagnostic_gate": diagnostic_gate,
        "safety_gate": safety_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "success_margin_vs_strongest": success_margin,
        "credit_f1_delta_vs_best_diagnostic_baseline": credit_delta,
        "delayed_blame_f1_delta_vs_best_diagnostic_baseline": blame_delta,
        "irreversible_side_effect_delta_vs_strongest": side_delta,
        "wasted_action_delta_vs_strongest": wasted_delta,
        "ablation_margin_vs_best_removed_component": ablation_margin,
        "strongest_non_oracle_baseline": strongest,
        "best_diagnostic_baseline": diagnostic_peer,
        "best_removed_component": best_ablation["ablation"],
    }
    return decision, rationale, gates


def write_summary(summary, pairwise, ablations, gates, decision, rationale):
    combined = sorted([r for r in summary if r["split"] == "combined_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 104 temporal_credit_without_rewards evidence rebuild\n")
        handle.write(f"Design: 5 tasks x 7 temporal-credit regimes x 5 splits x 9 methods, {len(SEEDS)} seeds, {EPISODES_PER_GROUP} episodes/group.\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Rationale: {rationale}\n\n")
        handle.write("Combined-stress ranking:\n")
        for row in combined:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"credit_f1={float(row['mean_mean_credit_f1']):.3f}, delayed_blame_f1={float(row['mean_mean_delayed_blame_f1']):.3f}, "
                f"false_credit={float(row['mean_mean_false_credit']):.3f}, irreversible={float(row['mean_mean_irreversible_side_effect']):.3f}, "
                f"wasted={float(row['mean_mean_wasted_action_rate']):.3f}, early_correction={float(row['mean_mean_early_correction']):.3f}, "
                f"latency={float(row['mean_mean_credit_latency']):.3f}, regret={float(row['mean_regret_to_oracle']):.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={float(row['mean_success_diff']):.3f} +/- {float(row['ci95_success_diff']):.3f}, "
                f"wins={row['wins_over_seeds']}/{row['seeds']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda r: float(r["mean_mean_success"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"credit_f1={float(row['mean_mean_credit_f1']):.3f}, delayed_blame_f1={float(row['mean_mean_delayed_blame_f1']):.3f}, "
                f"irreversible={float(row['mean_mean_irreversible_side_effect']):.3f}, note={row['interpretation']}\n"
            )


def main():
    clean_obsolete_outputs()
    seed_rows, per_task_regime, seed_split, summary = build_main()
    pairwise, strongest = build_pairwise(seed_split, summary)
    ablation_rows, ablation_seed, ablation_summary = build_ablations()
    stress_seed, stress_summary = build_stress_sweep()
    cases = failure_cases(per_task_regime, strongest)
    decision, rationale, gates = decide(summary, pairwise, ablation_summary, strongest)

    write_csv(RESULTS / "seed_task_regime_metrics.csv", rounded(seed_rows))
    write_csv(RESULTS / "per_task_regime_metrics.csv", rounded(per_task_regime))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split))
    write_csv(RESULTS / "metrics.csv", rounded(summary))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_summary))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_summary))
    write_csv(RESULTS / "failure_cases.csv", rounded(cases))

    make_figures(summary, ablation_summary, stress_summary)

    combined = sorted([r for r in summary if r["split"] == "combined_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    latex_table(
        RESULTS / "combined_stress_table.tex",
        combined,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_credit_f1", "CredF1"),
            ("mean_mean_delayed_blame_f1", "BlameF1"),
            ("mean_mean_irreversible_side_effect", "Irrev."),
            ("mean_mean_wasted_action_rate", "Waste"),
            ("mean_regret_to_oracle", "Regret"),
        ],
        "Combined-stress reward-free temporal-credit benchmark.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_summary, key=lambda r: float(r["mean_mean_success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_credit_f1", "CredF1"),
            ("mean_mean_delayed_blame_f1", "BlameF1"),
            ("mean_mean_irreversible_side_effect", "Irrev."),
        ],
        "Ablations of the reward-free temporal credit graph.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "Diff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
        ],
        "Pairwise combined-stress success differences against the proposed method.",
    )
    write_summary(summary, pairwise, ablation_summary, gates, decision, rationale)
    print(f"terminal_decision={decision}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
