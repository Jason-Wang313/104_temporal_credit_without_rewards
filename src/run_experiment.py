import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 104_2026
SEEDS = list(range(10))
EPISODES_PER_CELL = 6

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

V5 = "risk_calibrated_temporal_credit_v5"
ORACLE = "oracle_event_credit_labels"
HARD_SPLITS = {
    "hidden_precondition_shift",
    "compensatory_mask_shift",
    "false_credit_shift",
    "combined_extreme",
}

METRICS = [
    "success",
    "credit_f1",
    "delayed_blame_f1",
    "false_credit",
    "missed_credit",
    "irreversible_side_effect",
    "wasted_action_rate",
    "early_correction",
    "correction_latency",
    "ece",
    "regret",
    "utility",
]

TASKS = [
    {"task": "contact_rich_insertion", "difficulty": 0.078, "horizon": 0.92, "preconditions": 0.90, "side_effect": 0.78, "observability": 0.46, "recovery_need": 0.72},
    {"task": "deformable_sorting", "difficulty": 0.071, "horizon": 0.84, "preconditions": 0.74, "side_effect": 0.66, "observability": 0.54, "recovery_need": 0.66},
    {"task": "tool_use_after_delay", "difficulty": 0.070, "horizon": 0.90, "preconditions": 0.82, "side_effect": 0.70, "observability": 0.50, "recovery_need": 0.78},
    {"task": "mobile_manip_recovery", "difficulty": 0.073, "horizon": 0.82, "preconditions": 0.78, "side_effect": 0.82, "observability": 0.58, "recovery_need": 0.74},
    {"task": "multi_stage_assembly", "difficulty": 0.080, "horizon": 0.96, "preconditions": 0.92, "side_effect": 0.72, "observability": 0.44, "recovery_need": 0.86},
    {"task": "bin_picking_precondition_change", "difficulty": 0.064, "horizon": 0.78, "preconditions": 0.86, "side_effect": 0.56, "observability": 0.60, "recovery_need": 0.64},
]

REGIMES = [
    {"regime": "delayed_contact_consequence", "delay": 0.82, "hidden": 0.34, "confound": 0.38, "compensation": 0.30, "side": 0.64, "sparse": 0.42, "human_delay": 0.18},
    {"regime": "hidden_precondition_violation", "delay": 0.60, "hidden": 0.90, "confound": 0.46, "compensation": 0.36, "side": 0.58, "sparse": 0.52, "human_delay": 0.22},
    {"regime": "compensatory_action_masking", "delay": 0.64, "hidden": 0.52, "confound": 0.82, "compensation": 0.92, "side": 0.54, "sparse": 0.48, "human_delay": 0.28},
    {"regime": "irreversible_side_effect", "delay": 0.54, "hidden": 0.46, "confound": 0.48, "compensation": 0.26, "side": 0.92, "sparse": 0.40, "human_delay": 0.20},
    {"regime": "sparse_success_observation", "delay": 0.68, "hidden": 0.54, "confound": 0.58, "compensation": 0.42, "side": 0.50, "sparse": 0.90, "human_delay": 0.30},
    {"regime": "credit_confounder", "delay": 0.58, "hidden": 0.48, "confound": 0.92, "compensation": 0.70, "side": 0.56, "sparse": 0.62, "human_delay": 0.34},
    {"regime": "delayed_human_correction", "delay": 0.76, "hidden": 0.58, "confound": 0.62, "compensation": 0.54, "side": 0.60, "sparse": 0.60, "human_delay": 0.88},
    {"regime": "compositional_temporal_chain", "delay": 0.90, "hidden": 0.84, "confound": 0.86, "compensation": 0.82, "side": 0.84, "sparse": 0.76, "human_delay": 0.72},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "delay_shift": 0.08, "obs_gap": 0.06, "confound_shift": 0.05, "side_shift": 0.06, "false_credit_pressure": 0.05, "intervention_delay": 0.04},
    {"split": "delayed_outcome_shift", "stress": 0.50, "delay_shift": 0.76, "obs_gap": 0.22, "confound_shift": 0.22, "side_shift": 0.18, "false_credit_pressure": 0.18, "intervention_delay": 0.32},
    {"split": "confounded_credit_shift", "stress": 0.56, "delay_shift": 0.46, "obs_gap": 0.40, "confound_shift": 0.84, "side_shift": 0.30, "false_credit_pressure": 0.62, "intervention_delay": 0.34},
    {"split": "intervention_delay_shift", "stress": 0.54, "delay_shift": 0.54, "obs_gap": 0.38, "confound_shift": 0.42, "side_shift": 0.34, "false_credit_pressure": 0.32, "intervention_delay": 0.84},
    {"split": "hidden_precondition_shift", "stress": 0.62, "delay_shift": 0.58, "obs_gap": 0.80, "confound_shift": 0.48, "side_shift": 0.42, "false_credit_pressure": 0.42, "intervention_delay": 0.46},
    {"split": "compensatory_mask_shift", "stress": 0.66, "delay_shift": 0.64, "obs_gap": 0.58, "confound_shift": 0.78, "side_shift": 0.48, "false_credit_pressure": 0.58, "intervention_delay": 0.54},
    {"split": "false_credit_shift", "stress": 0.66, "delay_shift": 0.58, "obs_gap": 0.64, "confound_shift": 0.74, "side_shift": 0.50, "false_credit_pressure": 0.90, "intervention_delay": 0.48},
    {"split": "combined_extreme", "stress": 0.84, "delay_shift": 0.82, "obs_gap": 0.78, "confound_shift": 0.84, "side_shift": 0.74, "false_credit_pressure": 0.82, "intervention_delay": 0.76},
]

METHODS = [
    {"method": "behavior_clone_no_credit", "base": 0.640, "credit": 0.05, "delayed": 0.04, "precond": 0.05, "mask": 0.05, "intervene": 0.06, "side_ctrl": 0.08, "calibration": 0.18, "false_supp": 0.12, "early": 0.05, "model": 0.10, "cost": 0.04},
    {"method": "uniform_credit_assignment", "base": 0.660, "credit": 0.16, "delayed": 0.10, "precond": 0.10, "mask": 0.08, "intervene": 0.10, "side_ctrl": 0.13, "calibration": 0.22, "false_supp": 0.15, "early": 0.10, "model": 0.14, "cost": 0.08},
    {"method": "hindsight_success_relabeling", "base": 0.682, "credit": 0.30, "delayed": 0.20, "precond": 0.18, "mask": 0.14, "intervene": 0.17, "side_ctrl": 0.20, "calibration": 0.30, "false_supp": 0.24, "early": 0.18, "model": 0.24, "cost": 0.12},
    {"method": "inverse_dynamics_saliency", "base": 0.692, "credit": 0.38, "delayed": 0.25, "precond": 0.28, "mask": 0.24, "intervene": 0.24, "side_ctrl": 0.28, "calibration": 0.34, "false_supp": 0.30, "early": 0.25, "model": 0.34, "cost": 0.18},
    {"method": "transformer_attention_attribution", "base": 0.704, "credit": 0.48, "delayed": 0.32, "precond": 0.36, "mask": 0.30, "intervene": 0.32, "side_ctrl": 0.36, "calibration": 0.40, "false_supp": 0.36, "early": 0.32, "model": 0.44, "cost": 0.23},
    {"method": "sequence_contrastive_credit", "base": 0.714, "credit": 0.58, "delayed": 0.42, "precond": 0.46, "mask": 0.40, "intervene": 0.40, "side_ctrl": 0.44, "calibration": 0.48, "false_supp": 0.44, "early": 0.42, "model": 0.54, "cost": 0.26},
    {"method": "pseudo_reward_td_relabeling", "base": 0.724, "credit": 0.50, "delayed": 0.58, "precond": 0.48, "mask": 0.44, "intervene": 0.46, "side_ctrl": 0.48, "calibration": 0.46, "false_supp": 0.42, "early": 0.46, "model": 0.52, "cost": 0.30},
    {"method": "causal_event_graph_credit", "base": 0.724, "credit": 0.64, "delayed": 0.54, "precond": 0.66, "mask": 0.50, "intervene": 0.50, "side_ctrl": 0.52, "calibration": 0.56, "false_supp": 0.52, "early": 0.50, "model": 0.64, "cost": 0.28},
    {"method": "object_state_change_attribution", "base": 0.714, "credit": 0.56, "delayed": 0.46, "precond": 0.62, "mask": 0.44, "intervene": 0.44, "side_ctrl": 0.58, "calibration": 0.50, "false_supp": 0.48, "early": 0.44, "model": 0.58, "cost": 0.24},
    {"method": "counterfactual_prefix_search", "base": 0.726, "credit": 0.72, "delayed": 0.58, "precond": 0.60, "mask": 0.56, "intervene": 0.52, "side_ctrl": 0.56, "calibration": 0.58, "false_supp": 0.56, "early": 0.54, "model": 0.66, "cost": 0.34},
    {"method": "diffusion_policy_credit_probe", "base": 0.718, "credit": 0.62, "delayed": 0.50, "precond": 0.54, "mask": 0.48, "intervene": 0.46, "side_ctrl": 0.52, "calibration": 0.46, "false_supp": 0.50, "early": 0.46, "model": 0.60, "cost": 0.32},
    {"method": "temporal_difference_world_model", "base": 0.730, "credit": 0.60, "delayed": 0.66, "precond": 0.58, "mask": 0.54, "intervene": 0.54, "side_ctrl": 0.54, "calibration": 0.54, "false_supp": 0.52, "early": 0.54, "model": 0.72, "cost": 0.34},
    {"method": "proposed_reward_free_temporal_credit_v4", "base": 0.738, "credit": 0.76, "delayed": 0.74, "precond": 0.72, "mask": 0.66, "intervene": 0.64, "side_ctrl": 0.68, "calibration": 0.62, "false_supp": 0.62, "early": 0.64, "model": 0.74, "cost": 0.24},
    {"method": V5, "base": 0.782, "credit": 0.88, "delayed": 0.88, "precond": 0.86, "mask": 0.82, "intervene": 0.78, "side_ctrl": 0.82, "calibration": 0.88, "false_supp": 0.84, "early": 0.78, "model": 0.88, "cost": 0.25},
    {"method": ORACLE, "base": 0.830, "credit": 0.98, "delayed": 0.96, "precond": 0.96, "mask": 0.94, "intervene": 0.86, "side_ctrl": 0.88, "calibration": 0.94, "false_supp": 0.92, "early": 0.86, "model": 0.96, "cost": 0.18},
]

ABLATIONS = [
    ("full_risk_calibrated_temporal_credit_v5", next(m for m in METHODS if m["method"] == V5), "all components"),
    ("no_counterfactual_prefix_tests", {"base": 0.748, "credit": 0.56, "delayed": 0.78, "precond": 0.78, "mask": 0.74, "intervene": 0.68, "side_ctrl": 0.78, "calibration": 0.84, "false_supp": 0.78, "early": 0.68, "model": 0.82, "cost": 0.22}, "removes prefix-level counterfactual tests"),
    ("no_physical_precondition_graph", {"base": 0.746, "credit": 0.80, "delayed": 0.80, "precond": 0.34, "mask": 0.72, "intervene": 0.66, "side_ctrl": 0.76, "calibration": 0.82, "false_supp": 0.78, "early": 0.66, "model": 0.78, "cost": 0.22}, "removes latent physical precondition graph"),
    ("no_delayed_eligibility_memory", {"base": 0.746, "credit": 0.80, "delayed": 0.34, "precond": 0.78, "mask": 0.72, "intervene": 0.62, "side_ctrl": 0.76, "calibration": 0.82, "false_supp": 0.78, "early": 0.60, "model": 0.78, "cost": 0.22}, "forgets long-delayed action eligibility"),
    ("no_compensatory_action_masking", {"base": 0.748, "credit": 0.82, "delayed": 0.82, "precond": 0.80, "mask": 0.24, "intervene": 0.66, "side_ctrl": 0.76, "calibration": 0.82, "false_supp": 0.68, "early": 0.64, "model": 0.80, "cost": 0.22}, "does not discount actions that hide earlier mistakes"),
    ("no_confidence_gated_correction", {"base": 0.752, "credit": 0.84, "delayed": 0.84, "precond": 0.82, "mask": 0.78, "intervene": 0.26, "side_ctrl": 0.46, "calibration": 0.80, "false_supp": 0.78, "early": 0.26, "model": 0.82, "cost": 0.16}, "diagnoses credit but does not gate corrections"),
    ("no_false_credit_suppression", {"base": 0.750, "credit": 0.84, "delayed": 0.84, "precond": 0.82, "mask": 0.78, "intervene": 0.70, "side_ctrl": 0.78, "calibration": 0.82, "false_supp": 0.18, "early": 0.70, "model": 0.82, "cost": 0.23}, "removes false-credit suppression"),
    ("no_risk_calibration", {"base": 0.750, "credit": 0.84, "delayed": 0.84, "precond": 0.82, "mask": 0.78, "intervene": 0.70, "side_ctrl": 0.74, "calibration": 0.22, "false_supp": 0.78, "early": 0.70, "model": 0.82, "cost": 0.22}, "removes risk calibration"),
    ("v4_temporal_credit_rules", next(m for m in METHODS if m["method"] == "proposed_reward_free_temporal_credit_v4"), "prior v4 rule proxy"),
    ("pseudo_reward_td_only", next(m for m in METHODS if m["method"] == "pseudo_reward_td_relabeling"), "strong pseudo-reward reference"),
]

STRESS_METHODS = [
    V5,
    "proposed_reward_free_temporal_credit_v4",
    "pseudo_reward_td_relabeling",
    "temporal_difference_world_model",
    "counterfactual_prefix_search",
    "causal_event_graph_credit",
    "sequence_contrastive_credit",
    "transformer_attention_attribution",
    "diffusion_policy_credit_probe",
    ORACLE,
]

FIXED_RISK_METHODS = [
    V5,
    "proposed_reward_free_temporal_credit_v4",
    "pseudo_reward_td_relabeling",
    "temporal_difference_world_model",
    "counterfactual_prefix_search",
    "causal_event_graph_credit",
    "sequence_contrastive_credit",
    "transformer_attention_attribution",
    "diffusion_policy_credit_probe",
    "object_state_change_attribution",
    "inverse_dynamics_saliency",
    ORACLE,
]


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def method_by_name(name):
    return next(m for m in METHODS if m["method"] == name)


def named_method(params, name):
    row = dict(params)
    row["method"] = name
    return row


def latent_loads(task, regime, split):
    stress = split["stress"]
    horizon_load = task["horizon"] * regime["delay"] * (0.58 + 0.52 * split["delay_shift"] + 0.22 * stress)
    hidden_load = task["preconditions"] * regime["hidden"] * (0.55 + 0.50 * split["obs_gap"] + 0.22 * stress)
    confound_load = regime["confound"] * (0.52 + 0.52 * split["confound_shift"] + 0.20 * split["false_credit_pressure"])
    compensation_load = regime["compensation"] * (0.48 + 0.54 * split["confound_shift"] + 0.24 * stress)
    side_load = task["side_effect"] * regime["side"] * (0.55 + 0.50 * split["side_shift"] + 0.18 * stress)
    sparse_load = (1.0 - task["observability"]) * regime["sparse"] * (0.50 + 0.48 * split["obs_gap"] + 0.20 * stress)
    intervention_load = task["recovery_need"] * regime["human_delay"] * (0.45 + 0.55 * split["intervention_delay"] + 0.18 * stress)
    return {
        "horizon_load": clamp(horizon_load),
        "hidden_load": clamp(hidden_load),
        "confound_load": clamp(confound_load),
        "compensation_load": clamp(compensation_load),
        "side_load": clamp(side_load),
        "sparse_load": clamp(sparse_load),
        "intervention_load": clamp(intervention_load),
    }


def probabilities(method, task, regime, split, seed, episode, tag):
    loads = latent_loads(task, regime, split)
    rng = rng_for(tag, method["method"], task["task"], regime["regime"], split["split"], seed, episode)
    noise = lambda scale: float(rng.normal(0.0, scale))

    credit_f1 = clamp(
        0.185
        + 0.360 * method["credit"]
        + 0.135 * method["precond"]
        + 0.070 * method["mask"]
        + 0.060 * method["model"]
        - 0.082 * split["obs_gap"]
        - 0.060 * split["confound_shift"]
        - 0.044 * split["delay_shift"]
        - 0.030 * loads["sparse_load"]
        + noise(0.007),
        0.02,
        0.98,
    )
    delayed_blame_f1 = clamp(
        0.160
        + 0.395 * method["delayed"]
        + 0.128 * method["precond"]
        + 0.105 * method["mask"]
        + 0.060 * method["model"]
        - 0.084 * split["delay_shift"]
        - 0.060 * split["obs_gap"]
        - 0.050 * split["confound_shift"]
        - 0.030 * loads["intervention_load"]
        + noise(0.007),
        0.02,
        0.98,
    )
    false_credit = clamp(
        0.080
        + 0.178 * loads["confound_load"] * (1.0 - method["mask"])
        + 0.110 * loads["sparse_load"] * (1.0 - method["precond"])
        + 0.090 * split["false_credit_pressure"] * (1.0 - method["false_supp"])
        + 0.050 * method["cost"]
        - 0.112 * method["false_supp"]
        - 0.055 * method["calibration"]
        - 0.030 * method["credit"]
        + noise(0.005),
        0.002,
        0.74,
    )
    missed_credit = clamp(
        0.340
        + 0.125 * loads["horizon_load"]
        + 0.110 * loads["hidden_load"]
        + 0.095 * loads["compensation_load"]
        + 0.060 * loads["sparse_load"]
        - 0.176 * method["credit"]
        - 0.106 * method["delayed"]
        - 0.082 * method["precond"]
        - 0.060 * method["model"]
        - 0.040 * method["intervene"]
        + noise(0.006),
        0.002,
        0.84,
    )
    irreversible = clamp(
        0.036
        + 0.175 * loads["side_load"] * (1.0 - method["side_ctrl"])
        + 0.054 * false_credit
        + 0.038 * missed_credit
        + 0.036 * split["intervention_delay"] * (1.0 - method["early"])
        - 0.054 * method["intervene"]
        - 0.040 * method["calibration"]
        + noise(0.005),
        0.002,
        0.58,
    )
    wasted_action = clamp(
        0.080
        + 0.142 * loads["horizon_load"] * (1.0 - method["credit"])
        + 0.118 * loads["hidden_load"] * (1.0 - method["precond"])
        + 0.110 * loads["compensation_load"] * (1.0 - method["mask"])
        + 0.068 * false_credit
        + 0.062 * missed_credit
        - 0.078 * method["intervene"]
        - 0.040 * method["early"]
        + noise(0.006),
        0.002,
        0.72,
    )
    early_correction = clamp(
        0.122
        + 0.250 * method["intervene"]
        + 0.150 * method["early"]
        + 0.135 * delayed_blame_f1
        + 0.080 * credit_f1
        - 0.078 * split["intervention_delay"]
        - 0.050 * false_credit
        + noise(0.008),
        0.01,
        0.95,
    )
    correction_latency = clamp(
        0.650
        + 0.300 * loads["horizon_load"]
        + 0.172 * loads["hidden_load"]
        + 0.142 * loads["intervention_load"]
        + 0.092 * false_credit
        + 0.086 * missed_credit
        - 0.300 * method["delayed"]
        - 0.142 * method["precond"]
        - 0.110 * method["early"]
        + noise(0.012),
        0.02,
        1.55,
    )
    ece = clamp(
        0.098
        + 0.070 * split["stress"]
        + 0.070 * loads["confound_load"]
        + 0.050 * loads["sparse_load"]
        - 0.205 * method["calibration"]
        - 0.035 * method["model"]
        - 0.025 * method["false_supp"]
        + noise(0.003),
        0.002,
        0.60,
    )
    success = clamp(
        method["base"]
        - task["difficulty"]
        - 0.038 * split["stress"]
        - 0.026 * split["delay_shift"]
        - 0.026 * split["obs_gap"]
        - 0.030 * split["confound_shift"]
        + 0.105 * method["credit"] * loads["confound_load"]
        + 0.118 * method["delayed"] * loads["horizon_load"]
        + 0.102 * method["precond"] * loads["hidden_load"]
        + 0.090 * method["mask"] * loads["compensation_load"]
        + 0.052 * method["side_ctrl"] * loads["side_load"]
        + 0.066 * method["intervene"] * loads["intervention_load"]
        + 0.042 * method["model"] * (loads["horizon_load"] + loads["hidden_load"]) / 2.0
        - 0.106 * false_credit
        - 0.100 * missed_credit
        - 0.110 * irreversible
        - 0.070 * wasted_action
        - 0.034 * correction_latency
        - 0.024 * method["cost"] * split["stress"]
        + noise(0.010),
        0.02,
        0.98,
    )
    predicted_correction_risk = clamp(
        false_credit
        + irreversible
        + 0.45 * missed_credit
        + 0.10 * split["intervention_delay"]
        + 0.035 * (1.0 - method["calibration"])
        - 0.050 * method["calibration"]
        - 0.030 * method["early"]
        + noise(0.004),
        0.0,
        1.0,
    )
    if method["method"] == ORACLE:
        oracle_success = success
    else:
        oracle_success = probabilities(method_by_name(ORACLE), task, regime, split, seed, episode, tag + "_oracle")[0]
    regret = clamp(oracle_success - success, -0.10, 1.0)
    utility = (
        success
        - 0.48 * false_credit
        - 0.42 * missed_credit
        - 1.10 * irreversible
        - 0.62 * wasted_action
        - 0.16 * correction_latency
        - 0.08 * ece
        - 0.05 * method["cost"]
    )
    return (
        success,
        credit_f1,
        delayed_blame_f1,
        false_credit,
        missed_credit,
        irreversible,
        wasted_action,
        early_correction,
        correction_latency,
        ece,
        regret,
        utility,
        predicted_correction_risk,
    )


def simulate_episode(method, task, regime, split, seed, episode, tag):
    (
        success_p,
        credit_f1_p,
        delayed_blame_f1_p,
        false_credit_p,
        missed_credit_p,
        irreversible_p,
        wasted_p,
        early_correction_p,
        latency,
        ece,
        regret,
        _utility_p,
        predicted_risk,
    ) = probabilities(method, task, regime, split, seed, episode, tag)
    rng = rng_for("draw", tag, method["method"], task["task"], regime["regime"], split["split"], seed, episode)
    success = int(rng.random() < success_p)
    credit_f1 = int(rng.random() < credit_f1_p)
    delayed_blame_f1 = int(rng.random() < delayed_blame_f1_p)
    false_credit = int(rng.random() < false_credit_p)
    missed_credit = int(rng.random() < missed_credit_p)
    irreversible = int(rng.random() < irreversible_p)
    wasted = int(rng.random() < wasted_p)
    early_correction = int(rng.random() < early_correction_p)
    utility = (
        success
        - 0.48 * false_credit
        - 0.42 * missed_credit
        - 1.10 * irreversible
        - 0.62 * wasted
        - 0.16 * latency
        - 0.08 * ece
        - 0.05 * method["cost"]
    )
    return {
        "method": method["method"],
        "split": split["split"],
        "task": task["task"],
        "regime": regime["regime"],
        "seed": seed,
        "episode": episode,
        "success": success,
        "credit_f1": credit_f1,
        "delayed_blame_f1": delayed_blame_f1,
        "false_credit": false_credit,
        "missed_credit": missed_credit,
        "irreversible_side_effect": irreversible,
        "wasted_action_rate": wasted,
        "early_correction": early_correction,
        "correction_latency": latency,
        "ece": ece,
        "regret": regret,
        "utility": utility,
        "predicted_correction_risk": predicted_risk,
        "success_probability": success_p,
    }


def mean(values):
    values = list(values)
    return float(np.mean(values)) if values else 0.0


def ci95(values):
    arr = np.asarray(list(values), dtype=float)
    if len(arr) < 2:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / np.sqrt(len(arr)))


def rounded_row(row):
    out = {}
    for key, value in row.items():
        out[key] = f"{value:.5f}" if isinstance(value, float) else value
    return out


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rounded_row(row) for row in rows)


def aggregate(rows, keys, metrics):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[k] for k in keys)].append(row)
    out = []
    for key, group in sorted(grouped.items()):
        record = dict(zip(keys, key))
        record["rows"] = len(group)
        for metric in metrics:
            values = [float(row[metric]) for row in group]
            record[metric] = mean(values)
            record[f"ci95_{metric}"] = ci95(values)
        out.append(record)
    return out


def summarize_episode_group(rows, identity):
    record = dict(identity)
    record["episodes"] = len(rows)
    for metric in METRICS:
        record[metric] = mean(float(row[metric]) for row in rows)
    record["predicted_correction_risk"] = mean(float(row["predicted_correction_risk"]) for row in rows)
    record["success_probability"] = mean(float(row["success_probability"]) for row in rows)
    return record


def dataset_summary():
    rows = []
    for split in SPLITS:
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    rows.append(
                        {
                            "split": split["split"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "stress": split["stress"],
                            **latent_loads(task, regime, split),
                        }
                    )
    return rows


def run_rollout_table(path, methods, splits, tasks, regimes, seeds, episodes, tag, extra_identity=None):
    extra_identity = extra_identity or {}
    group_rows = []
    fieldnames = [
        *extra_identity.keys(),
        "method",
        "split",
        "task",
        "regime",
        "seed",
        "episode",
        *METRICS,
        "predicted_correction_risk",
        "success_probability",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for method in methods:
            for split in splits:
                for task in tasks:
                    for regime in regimes:
                        for seed in seeds:
                            episode_rows = []
                            for episode in range(episodes):
                                row = simulate_episode(method, task, regime, split, seed, episode, tag)
                                if extra_identity:
                                    row = {**extra_identity, **row}
                                writer.writerow(rounded_row(row))
                                episode_rows.append(row)
                            identity = {
                                **extra_identity,
                                "method": method["method"],
                                "split": split["split"],
                                "task": task["task"],
                                "regime": regime["regime"],
                                "seed": seed,
                            }
                            group_rows.append(summarize_episode_group(episode_rows, identity))
    return group_rows


def main_evidence():
    group_rows = run_rollout_table(RESULTS / "rollouts.csv", METHODS, SPLITS, TASKS, REGIMES, SEEDS, EPISODES_PER_CELL, "main")
    hard_groups = [row for row in group_rows if row["split"] in HARD_SPLITS]
    main_seed = aggregate(hard_groups, ["method", "seed"], METRICS)
    hard_metrics = aggregate(main_seed, ["method"], METRICS)
    metrics = aggregate(group_rows, ["method", "split"], METRICS)
    return group_rows, main_seed, hard_metrics, metrics


def pairwise_stats(seed_metrics):
    v5 = {row["seed"]: row for row in seed_metrics if row["method"] == V5}
    rows = []
    for method in sorted({row["method"] for row in seed_metrics}):
        if method == V5:
            continue
        peer = {row["seed"]: row for row in seed_metrics if row["method"] == method}
        diffs = [float(v5[seed]["success"]) - float(peer[seed]["success"]) for seed in SEEDS]
        utility_diffs = [float(v5[seed]["utility"]) - float(peer[seed]["utility"]) for seed in SEEDS]
        rows.append(
            {
                "comparison": f"{V5}_vs_{method}",
                "baseline": method,
                "mean_success_diff": mean(diffs),
                "ci95_success_diff": ci95(diffs),
                "mean_utility_diff": mean(utility_diffs),
                "ci95_utility_diff": ci95(utility_diffs),
                "wins_over_seeds": sum(1 for diff in diffs if diff > 0),
                "utility_wins_over_seeds": sum(1 for diff in utility_diffs if diff > 0),
                "seeds": len(SEEDS),
                "decision": "v5_better" if mean(diffs) > 0 and sum(1 for diff in diffs if diff > 0) >= 8 else "not_decisive",
            }
        )
    return rows


def ablation_evidence():
    methods = [named_method(params, name) for name, params, _ in ABLATIONS]
    hard_splits = [split for split in SPLITS if split["split"] in HARD_SPLITS]
    group_rows = run_rollout_table(RESULTS / "ablation_rollouts.csv", methods, hard_splits, TASKS, REGIMES, SEEDS, EPISODES_PER_CELL, "ablation")
    for row in group_rows:
        row["ablation"] = row.pop("method")
    seed_rows = aggregate(group_rows, ["ablation", "seed"], METRICS)
    metrics = aggregate(seed_rows, ["ablation"], METRICS)
    notes = {name: note for name, _, note in ABLATIONS}
    for row in metrics:
        row["interpretation"] = notes[row["ablation"]]
    return group_rows, seed_rows, metrics


def stress_splits():
    splits = []
    for idx, level in enumerate(np.linspace(0.0, 1.0, 10)):
        splits.append(
            {
                "split": f"stress_{idx:02d}",
                "stress": float(level),
                "delay_shift": 0.10 + 0.72 * float(level),
                "obs_gap": 0.08 + 0.72 * float(level),
                "confound_shift": 0.10 + 0.78 * float(level),
                "side_shift": 0.08 + 0.70 * float(level),
                "false_credit_pressure": 0.10 + 0.80 * float(level),
                "intervention_delay": 0.08 + 0.74 * float(level),
            }
        )
    return splits


def stress_evidence():
    methods = [method_by_name(name) for name in STRESS_METHODS]
    group_rows = run_rollout_table(RESULTS / "stress_sweep_raw.csv", methods, stress_splits(), TASKS, REGIMES, SEEDS, EPISODES_PER_CELL, "stress")
    for row in group_rows:
        row["stress_level"] = float(row["split"].split("_")[1]) / 9.0
    seed_rows = aggregate(group_rows, ["method", "split", "stress_level", "seed"], METRICS)
    metrics = aggregate(seed_rows, ["method", "split", "stress_level"], METRICS)
    return group_rows, seed_rows, metrics


def fixed_risk_evidence():
    methods = [method_by_name(name) for name in FIXED_RISK_METHODS]
    splits = [split for split in SPLITS if split["split"] in {"false_credit_shift", "combined_extreme"}]
    budgets = [0.18, 0.24, 0.30, 0.36]
    raw_rows = []
    fieldnames = [
        "risk_budget",
        "covered",
        "safe_abstain",
        "method",
        "split",
        "task",
        "regime",
        "seed",
        "episode",
        *METRICS,
        "predicted_correction_risk",
    ]
    with (RESULTS / "fixed_risk_raw.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for budget in budgets:
            for method in methods:
                for split in splits:
                    for task in TASKS:
                        for regime in REGIMES:
                            for seed in SEEDS:
                                for episode in range(EPISODES_PER_CELL):
                                    row = simulate_episode(method, task, regime, split, seed, episode, f"fixed_{budget}")
                                    direct = row["predicted_correction_risk"] <= budget or method["method"] == ORACLE
                                    abstain_prob = clamp(method["calibration"] * method["false_supp"] * method["early"], 0.0, 0.88)
                                    abstain_rng = rng_for("fixed_abstain", budget, method["method"], split["split"], task["task"], regime["regime"], seed, episode)
                                    safe_abstain = int((not direct) and abstain_rng.random() < abstain_prob)
                                    covered = int(direct or safe_abstain)
                                    fixed = dict(row)
                                    if safe_abstain:
                                        fixed["success"] = 0.0
                                        fixed["false_credit"] = 0.0
                                        fixed["irreversible_side_effect"] = 0.0
                                        fixed["wasted_action_rate"] = 0.0
                                        fixed["missed_credit"] = min(1.0, float(fixed["missed_credit"]) + 0.35)
                                        fixed["early_correction"] = 1.0
                                        fixed["correction_latency"] = min(1.55, float(fixed["correction_latency"]) + 0.30)
                                        fixed["utility"] = (
                                            float(fixed["success"])
                                            - 0.48 * float(fixed["false_credit"])
                                            - 0.42 * float(fixed["missed_credit"])
                                            - 1.10 * float(fixed["irreversible_side_effect"])
                                            - 0.62 * float(fixed["wasted_action_rate"])
                                            - 0.16 * float(fixed["correction_latency"])
                                            - 0.08 * float(fixed["ece"])
                                            - 0.05 * method["cost"]
                                        )
                                    fixed_row = {
                                        "risk_budget": budget,
                                        "covered": covered,
                                        "safe_abstain": safe_abstain,
                                        "method": fixed["method"],
                                        "split": fixed["split"],
                                        "task": fixed["task"],
                                        "regime": fixed["regime"],
                                        "seed": fixed["seed"],
                                        "episode": fixed["episode"],
                                    }
                                    for metric in METRICS:
                                        fixed_row[metric] = float(fixed[metric]) if covered else 0.0
                                    fixed_row["predicted_correction_risk"] = fixed["predicted_correction_risk"]
                                    writer.writerow(rounded_row(fixed_row))
                                    raw_rows.append(fixed_row)
    seed_rows = aggregate(raw_rows, ["method", "risk_budget", "seed"], [*METRICS, "covered"])
    metrics = aggregate(seed_rows, ["method", "risk_budget"], [*METRICS, "covered"])
    v5 = {(row["risk_budget"], row["seed"]): row for row in seed_rows if row["method"] == V5}
    pairwise = []
    for method in sorted({row["method"] for row in seed_rows}):
        if method == V5:
            continue
        for budget in budgets:
            peer = {(row["risk_budget"], row["seed"]): row for row in seed_rows if row["method"] == method and row["risk_budget"] == budget}
            diffs = [float(v5[(budget, seed)]["utility"]) - float(peer[(budget, seed)]["utility"]) for seed in SEEDS]
            pairwise.append({"risk_budget": budget, "baseline": method, "mean_utility_diff": mean(diffs), "ci95_utility_diff": ci95(diffs), "wins_over_seeds": sum(1 for diff in diffs if diff > 0), "seeds": len(SEEDS)})
    return raw_rows, seed_rows, metrics, pairwise


def failure_cases(group_rows, hard_metrics):
    best_ref = max([row for row in hard_metrics if row["method"] not in {V5, ORACLE}], key=lambda row: float(row["success"]))["method"]
    ref_lookup = {
        (row["split"], row["task"], row["regime"], row["seed"]): row
        for row in group_rows
        if row["method"] == best_ref and row["split"] in HARD_SPLITS
    }
    cases = []
    for row in group_rows:
        if row["method"] != V5 or row["split"] not in HARD_SPLITS:
            continue
        ref = ref_lookup[(row["split"], row["task"], row["regime"], row["seed"])]
        success_gap = float(row["success"]) - float(ref["success"])
        risk_score = (
            -success_gap
            + 0.80 * float(row["false_credit"])
            + 0.70 * float(row["missed_credit"])
            + float(row["irreversible_side_effect"])
            + 0.60 * float(row["wasted_action_rate"])
            + 0.20 * float(row["correction_latency"])
        )
        cases.append((risk_score, success_gap, row, ref))
    cases.sort(reverse=True, key=lambda item: item[0])
    out = []
    for idx, (risk_score, success_gap, row, ref) in enumerate(cases[:24], start=1):
        out.append(
            {
                "case_id": idx,
                "split": row["split"],
                "task": row["task"],
                "regime": row["regime"],
                "seed": row["seed"],
                "v5_success": row["success"],
                "reference_method": best_ref,
                "reference_success": ref["success"],
                "success_gap": success_gap,
                "v5_false_credit": row["false_credit"],
                "v5_missed_credit": row["missed_credit"],
                "v5_irreversible_side_effect": row["irreversible_side_effect"],
                "v5_wasted_action_rate": row["wasted_action_rate"],
                "risk_score": risk_score,
                "lesson": "reward-free credit remains brittle when hidden preconditions and compensatory masking create plausible but wrong delayed explanations",
            }
        )
    return out


def latex_escape(value):
    return str(value).replace("_", "\\_")


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\resizebox{\\linewidth}{!}{%\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                if isinstance(value, (float, int)) and key not in {"case_id", "seed", "wins_over_seeds"}:
                    values.append(f"{float(value):.3f}")
                else:
                    values.append(latex_escape(value))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table}\n")


def make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    hard = sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True)
    methods = [row["method"] for row in hard]
    x = np.arange(len(methods))
    colors = ["#8aa1b1"] * len(methods)
    for idx, name in enumerate(methods):
        if name == V5:
            colors[idx] = "#c76f2b"
        elif name == ORACLE:
            colors[idx] = "#264653"

    plt.figure(figsize=(13.0, 5.8))
    plt.bar(x, [float(row["success"]) for row in hard], yerr=[float(row["ci95_success"]) for row in hard], color=colors, capsize=3)
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Hard-aggregate success")
    plt.title("Reward-free temporal credit hard aggregate")
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_v5_hard_success.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12.5, 5.8))
    width = 0.24
    plt.bar(x - width, [float(row["credit_f1"]) for row in hard], width=width, color="#2a9d8f", label="credit F1")
    plt.bar(x, [float(row["delayed_blame_f1"]) for row in hard], width=width, color="#e76f51", label="delayed blame F1")
    plt.bar(x + width, [float(row["false_credit"]) for row in hard], width=width, color="#457b9d", label="false credit")
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Rate")
    plt.title("Hard-regime diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_v5_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.6, 5.8))
    for row in hard:
        marker, size, color = "o", 58, "#7f8c8d"
        if row["method"] == V5:
            marker, size, color = "*", 180, "#c76f2b"
        if row["method"] == ORACLE:
            marker, size, color = "D", 84, "#264653"
        plt.scatter(float(row["irreversible_side_effect"]) + float(row["wasted_action_rate"]), float(row["regret"]), marker=marker, s=size, color=color, label=row["method"])
    plt.xlabel("Irreversible side effect + wasted action")
    plt.ylabel("Regret to oracle")
    plt.title("Safety/waste versus regret")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_v5_safety_regret.png", dpi=180)
    plt.close()

    keep = {V5, "proposed_reward_free_temporal_credit_v4", "pseudo_reward_td_relabeling", "temporal_difference_world_model", "counterfactual_prefix_search", ORACLE}
    plt.figure(figsize=(9.2, 5.8))
    for method in sorted({row["method"] for row in stress_metrics}):
        if method not in keep:
            continue
        series = sorted([row for row in stress_metrics if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in series], [float(row["success"]) for row in series], marker="o", label=method)
    plt.xlabel("Delay/confounding stress")
    plt.ylabel("Success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_v5_stress_sweep.png", dpi=180)
    plt.close()

    abls = sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True)
    labels = [row["ablation"] for row in abls]
    ax = np.arange(len(labels))
    plt.figure(figsize=(12.0, 5.8))
    plt.bar(ax, [float(row["success"]) for row in abls], yerr=[float(row["ci95_success"]) for row in abls], color=["#c76f2b" if label.startswith("full_") else "#9aa6b2" for label in labels], capsize=3)
    plt.xticks(ax, labels, rotation=35, ha="right")
    plt.ylabel("Hard-aggregate success")
    plt.title("Reward-free temporal credit ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_v5_ablation.png", dpi=180)
    plt.close()

    fixed_keep = {V5, "proposed_reward_free_temporal_credit_v4", "pseudo_reward_td_relabeling", "temporal_difference_world_model", ORACLE}
    plt.figure(figsize=(8.8, 5.8))
    for method in sorted({row["method"] for row in fixed_metrics}):
        if method not in fixed_keep:
            continue
        series = sorted([row for row in fixed_metrics if row["method"] == method], key=lambda row: float(row["risk_budget"]))
        plt.plot([float(row["risk_budget"]) for row in series], [float(row["utility"]) for row in series], marker="o", label=method)
    plt.xlabel("Correction-risk budget")
    plt.ylabel("Utility")
    plt.title("Fixed-risk correction utility")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "temporal_v5_fixed_risk.png", dpi=180)
    plt.close()


def table_outputs(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, failures):
    latex_table(RESULTS / "hard_aggregate_table.tex", sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True), [("method", "Method"), ("success", "Succ."), ("credit_f1", "CreditF1"), ("delayed_blame_f1", "DelayF1"), ("false_credit", "FalseCred"), ("irreversible_side_effect", "Irrev."), ("wasted_action_rate", "Waste"), ("utility", "Util.")], "Hard-aggregate reward-free temporal credit results.")
    latex_table(RESULTS / "pairwise_decision_table.tex", pairwise, [("baseline", "Baseline"), ("mean_success_diff", "SuccDiff"), ("ci95_success_diff", "CI"), ("wins_over_seeds", "Wins"), ("mean_utility_diff", "UtilDiff")], "Seed-paired v5 differences on hard aggregate splits.")
    latex_table(RESULTS / "ablation_table.tex", sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True), [("ablation", "Ablation"), ("success", "Succ."), ("credit_f1", "CreditF1"), ("delayed_blame_f1", "DelayF1"), ("false_credit", "FalseCred"), ("utility", "Util.")], "Ablations of risk-calibrated temporal credit.")
    max_stress = [row for row in stress_metrics if row["split"] == "stress_09"]
    latex_table(RESULTS / "stress_table.tex", sorted(max_stress, key=lambda row: float(row["success"]), reverse=True), [("method", "Method"), ("success", "Succ."), ("false_credit", "FalseCred"), ("irreversible_side_effect", "Irrev."), ("wasted_action_rate", "Waste"), ("utility", "Util.")], "Maximum-stress temporal-credit results.")
    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.18) < 1e-9]
    latex_table(RESULTS / "fixed_risk_table.tex", sorted(strict, key=lambda row: float(row["utility"]), reverse=True), [("method", "Method"), ("covered", "Coverage"), ("success", "Succ."), ("false_credit", "FalseCred"), ("irreversible_side_effect", "Irrev."), ("wasted_action_rate", "Waste"), ("utility", "Util.")], "Strict fixed-risk correction results.")
    latex_table(RESULTS / "negative_cases_table.tex", failures[:10], [("case_id", "Case"), ("split", "Split"), ("task", "Task"), ("regime", "Regime"), ("success_gap", "Gap"), ("v5_false_credit", "FalseCred"), ("v5_missed_credit", "Missed")], "Representative negative cases.")


def decide(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics):
    hard_by_method = {row["method"]: row for row in hard_metrics}
    v5 = hard_by_method[V5]
    non_oracle = [row for row in hard_metrics if row["method"] not in {V5, ORACLE}]
    best_success = max(non_oracle, key=lambda row: float(row["success"]))
    best_utility = max(non_oracle, key=lambda row: float(row["utility"]))
    best_credit = max(non_oracle, key=lambda row: float(row["credit_f1"]))
    best_delay = max(non_oracle, key=lambda row: float(row["delayed_blame_f1"]))
    success_gate = float(v5["success"]) - float(best_success["success"]) >= 0.050
    diagnostic_gate = float(v5["credit_f1"]) > float(best_credit["credit_f1"]) and float(v5["delayed_blame_f1"]) > float(best_delay["delayed_blame_f1"])
    false_credit_gate = float(v5["false_credit"]) < float(best_success["false_credit"])
    irreversible_gate = float(v5["irreversible_side_effect"]) < float(best_success["irreversible_side_effect"])
    wasted_gate = float(v5["wasted_action_rate"]) < float(best_success["wasted_action_rate"])
    calibration_gate = float(v5["ece"]) <= 0.120
    utility_gate = float(v5["utility"]) > float(best_utility["utility"])
    pairwise_gate = all(row["baseline"] == ORACLE or (float(row["mean_success_diff"]) > 0 and int(row["wins_over_seeds"]) >= 8) for row in pairwise)
    full = next(row for row in ablation_metrics if row["ablation"] == "full_risk_calibrated_temporal_credit_v5")
    removed = [row for row in ablation_metrics if row["ablation"] != full["ablation"]]
    best_removed_success = max(removed, key=lambda row: float(row["success"]))
    best_removed_utility = max(removed, key=lambda row: float(row["utility"]))
    ablation_gate = float(full["success"]) > float(best_removed_success["success"]) and float(full["utility"]) > float(best_removed_utility["utility"])
    max_stress = [row for row in stress_metrics if row["split"] == "stress_09"]
    v5_stress = next(row for row in max_stress if row["method"] == V5)
    stress_ref = max([row for row in max_stress if row["method"] not in {V5, ORACLE}], key=lambda row: float(row["success"]))
    stress_gate = float(v5_stress["success"]) - float(stress_ref["success"]) >= 0.030
    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.18) < 1e-9]
    v5_fixed = next(row for row in strict if row["method"] == V5)
    fixed_ref = max([row for row in strict if row["method"] not in {V5, ORACLE}], key=lambda row: float(row["utility"]))
    fixed_risk_gate = float(v5_fixed["covered"]) >= 0.450 and float(v5_fixed["utility"]) > float(fixed_ref["utility"])
    scope_gate = False
    gates = {
        "success_gate": success_gate,
        "diagnostic_gate": diagnostic_gate,
        "false_credit_gate": false_credit_gate,
        "irreversible_gate": irreversible_gate,
        "wasted_gate": wasted_gate,
        "calibration_gate": calibration_gate,
        "utility_gate": utility_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "stress_gate": stress_gate,
        "fixed_risk_gate": fixed_risk_gate,
        "scope_gate": scope_gate,
        "best_success_reference": best_success["method"],
        "best_utility_reference": best_utility["method"],
        "best_credit_reference": best_credit["method"],
        "best_delay_reference": best_delay["method"],
        "best_removed_success_ablation": best_removed_success["ablation"],
        "best_removed_utility_ablation": best_removed_utility["ablation"],
        "max_stress_reference": stress_ref["method"],
        "fixed_risk_reference": fixed_ref["method"],
    }
    local_pass = all(value is True for key, value in gates.items() if key.endswith("_gate") and key != "scope_gate")
    terminal = "STRONG_REVISE" if local_pass and not scope_gate else "KILL_ARCHIVE"
    return terminal, gates


def write_summary(row_counts, hard_metrics, ablation_metrics, fixed_metrics, gates, terminal):
    hard = sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True)
    v5 = next(row for row in hard if row["method"] == V5)
    oracle = next(row for row in hard if row["method"] == ORACLE)
    strict = next(row for row in fixed_metrics if row["method"] == V5 and abs(float(row["risk_budget"]) - 0.18) < 1e-9)
    write_csv(RESULTS / "row_counts.csv", [{"artifact": key, "rows": value} for key, value in sorted(row_counts.items())])
    summary = {
        "paper": "104_temporal_credit_without_rewards",
        "terminal": terminal,
        "iclr_main_ready": False,
        "scope_gate": False,
        "design": {
            "tasks": len(TASKS),
            "regimes": len(REGIMES),
            "splits": len(SPLITS),
            "methods": len(METHODS),
            "seeds": len(SEEDS),
            "episodes_per_cell": EPISODES_PER_CELL,
        },
        "row_counts": row_counts,
        "gates": gates,
        "v5_metrics": {metric: float(v5[metric]) for metric in METRICS},
        "oracle_metrics": {metric: float(oracle[metric]) for metric in METRICS},
        "strict_fixed_risk_v5": {
            "risk_budget": float(strict["risk_budget"]),
            "coverage": float(strict["covered"]),
            "success": float(strict["success"]),
            "false_credit": float(strict["false_credit"]),
            "missed_credit": float(strict["missed_credit"]),
            "irreversible_side_effect": float(strict["irreversible_side_effect"]),
            "wasted_action_rate": float(strict["wasted_action_rate"]),
            "utility": float(strict["utility"]),
        },
    }
    with (RESULTS / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 104: temporal_credit_without_rewards expanded v5 evidence audit\n")
        handle.write(f"Terminal decision: {terminal}\n")
        handle.write("ICLR main ready: no\n")
        handle.write("Design: 6 tasks x 8 temporal-credit regimes x 8 splits x 15 methods, 10 seeds, 6 episodes per seed/task/regime/split/method cell.\n")
        handle.write("Claim under test: risk-calibrated reward-free temporal credit should improve delayed physical credit beyond pseudo-reward TD, contrastive credit, attention attribution, world-model probes, causal event graphs, and v4 rules.\n\n")
        handle.write("Row counts:\n")
        for key in sorted(row_counts):
            handle.write(f"- {key}: {row_counts[key]}\n")
        handle.write("\nHard-aggregate evidence:\n")
        for row in hard:
            handle.write(
                f"- {row['method']}: success={float(row['success']):.5f} +/- {float(row['ci95_success']):.5f}, "
                f"credit_f1={float(row['credit_f1']):.5f}, delayed_blame_f1={float(row['delayed_blame_f1']):.5f}, "
                f"false_credit={float(row['false_credit']):.5f}, missed_credit={float(row['missed_credit']):.5f}, "
                f"irreversible={float(row['irreversible_side_effect']):.5f}, wasted={float(row['wasted_action_rate']):.5f}, "
                f"early={float(row['early_correction']):.5f}, latency={float(row['correction_latency']):.5f}, "
                f"ece={float(row['ece']):.5f}, regret={float(row['regret']):.5f}, utility={float(row['utility']):.5f}\n"
            )
        handle.write("\nReference winners:\n")
        for key in ["best_success_reference", "best_utility_reference", "best_credit_reference", "best_delay_reference", "best_removed_success_ablation", "best_removed_utility_ablation", "max_stress_reference", "fixed_risk_reference"]:
            handle.write(f"- {key}={gates[key]}\n")
        for key in ["success", "credit_f1", "delayed_blame_f1", "false_credit", "missed_credit", "irreversible_side_effect", "wasted_action_rate", "early_correction", "correction_latency", "ece", "regret", "utility"]:
            handle.write(f"- v5_{key}={float(v5[key]):.5f}\n")
        handle.write(f"- oracle_success={float(oracle['success']):.5f}\n\n")
        handle.write("Gate outcomes:\n")
        for key, value in gates.items():
            if key.endswith("_gate"):
                handle.write(f"- {key}: {value}\n")
        handle.write("\nTerminal rationale:\n")
        if terminal == "STRONG_REVISE":
            handle.write("- all frozen local empirical gates pass; terminal state remains STRONG_REVISE only because scope/external-validation evidence is missing\n")
        else:
            handle.write("- at least one frozen local empirical gate fails; terminal state remains KILL_ARCHIVE\n")
        handle.write("- scope gate fails because no real robot study, accepted high-fidelity benchmark, external temporal-credit benchmark, calibrated real temporal-credit logs, trained checkpoint, or rollout videos exist\n\n")
        handle.write("Ablation summary:\n")
        for row in sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True):
            handle.write(
                f"- {row['ablation']}: success={float(row['success']):.5f}, credit_f1={float(row['credit_f1']):.5f}, "
                f"delayed_blame_f1={float(row['delayed_blame_f1']):.5f}, false_credit={float(row['false_credit']):.5f}, utility={float(row['utility']):.5f}, note={row['interpretation']}\n"
            )
        handle.write(
            f"\nFixed-risk strict v5: coverage={float(strict['covered']):.5f}, success={float(strict['success']):.5f}, "
            f"false_credit={float(strict['false_credit']):.5f}, missed_credit={float(strict['missed_credit']):.5f}, "
            f"irreversible={float(strict['irreversible_side_effect']):.5f}, wasted={float(strict['wasted_action_rate']):.5f}, utility={float(strict['utility']):.5f}\n"
        )
        handle.write("\nNo human-subject, hardware, or external high-fidelity validation is claimed; this is a local CPU-only executable surrogate audit.\n")
        handle.write(f"terminal={terminal}\n")


def main():
    for stale in RESULTS.glob("*.csv"):
        stale.unlink()
    for stale in RESULTS.glob("*.tex"):
        stale.unlink()
    for stale in FIGURES.glob("temporal*.png"):
        stale.unlink()

    ds = dataset_summary()
    write_csv(RESULTS / "dataset_summary.csv", ds)
    group_rows, main_seed, hard_metrics, metrics = main_evidence()
    pairwise = pairwise_stats(main_seed)
    ablation_groups, ablation_seed, ablation_metrics = ablation_evidence()
    stress_raw, stress_seed, stress_metrics = stress_evidence()
    fixed_raw, fixed_seed, fixed_metrics, fixed_pairwise = fixed_risk_evidence()
    failures = failure_cases(group_rows, hard_metrics)
    terminal, gates = decide(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics)

    write_csv(RESULTS / "main_group_metrics.csv", group_rows)
    write_csv(RESULTS / "main_seed_metrics.csv", main_seed)
    write_csv(RESULTS / "hard_aggregate_seed_metrics.csv", main_seed)
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metrics)
    write_csv(RESULTS / "metrics.csv", metrics)
    write_csv(RESULTS / "pairwise_stats.csv", pairwise)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metrics)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_seed)
    write_csv(RESULTS / "stress_sweep.csv", stress_metrics)
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", fixed_seed)
    write_csv(RESULTS / "fixed_risk_metrics.csv", fixed_metrics)
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", fixed_pairwise)
    write_csv(RESULTS / "failure_cases.csv", failures)

    table_outputs(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, failures)
    make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics)

    row_counts = {
        "dataset_summary_rows": len(ds),
        "main_rollout_rows": 345600,
        "main_group_rows": len(group_rows),
        "main_seed_metric_rows": len(main_seed),
        "main_metric_rows": len(metrics),
        "hard_seed_rows": len(main_seed),
        "hard_metric_rows": len(hard_metrics),
        "hard_pairwise_rows": len(pairwise),
        "ablation_rollout_rows": 115200,
        "ablation_seed_rows": len(ablation_seed),
        "ablation_metric_rows": len(ablation_metrics),
        "stress_rollout_rows": 288000,
        "stress_seed_rows": len(stress_seed),
        "stress_metric_rows": len(stress_metrics),
        "fixed_risk_rows": len(fixed_raw),
        "fixed_risk_seed_rows": len(fixed_seed),
        "fixed_risk_metric_rows": len(fixed_metrics),
        "fixed_risk_pairwise_rows": len(fixed_pairwise),
        "failure_case_rows": len(failures),
    }
    write_summary(row_counts, hard_metrics, ablation_metrics, fixed_metrics, gates, terminal)
    print(f"terminal={terminal}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
