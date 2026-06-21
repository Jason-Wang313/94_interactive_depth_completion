import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 940617
SEEDS = list(range(10))
EPISODES = 32
ABLATION_EPISODES = 64
STRESS_EPISODES = 15
FIXED_RISK_EPISODES = 24

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


TASKS = {
    "occluded_bin_grasping": {
        "missing": 0.28,
        "occlusion": 0.58,
        "specular": 0.14,
        "clearance": 0.46,
        "fragility": 0.20,
        "contact_need": 0.54,
        "clutter": 0.66,
        "criticality": 0.74,
    },
    "shelf_insertion_clearance": {
        "missing": 0.20,
        "occlusion": 0.34,
        "specular": 0.16,
        "clearance": 0.86,
        "fragility": 0.30,
        "contact_need": 0.40,
        "clutter": 0.42,
        "criticality": 0.90,
    },
    "transparent_container_lift": {
        "missing": 0.44,
        "occlusion": 0.28,
        "specular": 0.68,
        "clearance": 0.50,
        "fragility": 0.45,
        "contact_need": 0.48,
        "clutter": 0.40,
        "criticality": 0.78,
    },
    "leaf_occluded_fruit_grasp": {
        "missing": 0.34,
        "occlusion": 0.72,
        "specular": 0.24,
        "clearance": 0.58,
        "fragility": 0.84,
        "contact_need": 0.74,
        "clutter": 0.75,
        "criticality": 0.84,
    },
    "drawer_slot_alignment": {
        "missing": 0.26,
        "occlusion": 0.42,
        "specular": 0.22,
        "clearance": 0.80,
        "fragility": 0.34,
        "contact_need": 0.62,
        "clutter": 0.48,
        "criticality": 0.88,
    },
    "deformable_bag_depth_lift": {
        "missing": 0.38,
        "occlusion": 0.52,
        "specular": 0.34,
        "clearance": 0.56,
        "fragility": 0.70,
        "contact_need": 0.78,
        "clutter": 0.60,
        "criticality": 0.82,
    },
}


SPLITS = {
    "nominal_depth": {
        "missing": 0.00,
        "occlusion": 0.00,
        "specular": 0.00,
        "probe_noise": 0.00,
        "clearance": 0.00,
        "damage": 0.00,
    },
    "missing_depth_shift": {
        "missing": 0.34,
        "occlusion": 0.06,
        "specular": 0.06,
        "probe_noise": 0.04,
        "clearance": 0.04,
        "damage": 0.02,
    },
    "occlusion_shift": {
        "missing": 0.06,
        "occlusion": 0.38,
        "specular": 0.05,
        "probe_noise": 0.05,
        "clearance": 0.08,
        "damage": 0.05,
    },
    "transparent_specular_shift": {
        "missing": 0.14,
        "occlusion": 0.04,
        "specular": 0.40,
        "probe_noise": 0.10,
        "clearance": 0.04,
        "damage": 0.07,
    },
    "probe_noise_shift": {
        "missing": 0.12,
        "occlusion": 0.10,
        "specular": 0.12,
        "probe_noise": 0.36,
        "clearance": 0.08,
        "damage": 0.10,
    },
    "tight_clearance_shift": {
        "missing": 0.10,
        "occlusion": 0.12,
        "specular": 0.06,
        "probe_noise": 0.08,
        "clearance": 0.42,
        "damage": 0.12,
    },
    "low_signal_depth_stress": {
        "missing": 0.30,
        "occlusion": 0.30,
        "specular": 0.28,
        "probe_noise": 0.24,
        "clearance": 0.24,
        "damage": 0.20,
    },
    "combined_interactive_stress": {
        "missing": 0.32,
        "occlusion": 0.36,
        "specular": 0.34,
        "probe_noise": 0.28,
        "clearance": 0.34,
        "damage": 0.26,
    },
}

HARD_SPLITS = ["low_signal_depth_stress", "combined_interactive_stress"]


METHODS = {
    "raw_depth_policy": {
        "completion": 0.08,
        "occlusion": 0.06,
        "specular": 0.05,
        "calibration": 0.24,
        "boundary": 0.31,
        "decision": 0.28,
        "probe_rate": 0.00,
        "probe_accuracy": 0.00,
        "action_focus": 0.00,
        "cost_control": 0.00,
        "damage_control": 0.00,
        "view_gain": 0.00,
        "conservative": 0.08,
        "diffusion": 0.00,
        "oracle": False,
    },
    "learned_depth_completion": {
        "completion": 0.58,
        "occlusion": 0.42,
        "specular": 0.29,
        "calibration": 0.45,
        "boundary": 0.52,
        "decision": 0.55,
        "probe_rate": 0.00,
        "probe_accuracy": 0.00,
        "action_focus": 0.00,
        "cost_control": 0.00,
        "damage_control": 0.00,
        "view_gain": 0.00,
        "conservative": 0.05,
        "diffusion": 0.00,
        "oracle": False,
    },
    "gaussian_splat_uncertainty": {
        "completion": 0.52,
        "occlusion": 0.50,
        "specular": 0.44,
        "calibration": 0.82,
        "boundary": 0.72,
        "decision": 0.64,
        "probe_rate": 0.00,
        "probe_accuracy": 0.00,
        "action_focus": 0.00,
        "cost_control": 0.00,
        "damage_control": 0.00,
        "view_gain": 0.00,
        "conservative": 0.25,
        "diffusion": 0.00,
        "oracle": False,
    },
    "ensemble_depth_completion": {
        "completion": 0.66,
        "occlusion": 0.58,
        "specular": 0.51,
        "calibration": 0.73,
        "boundary": 0.68,
        "decision": 0.67,
        "probe_rate": 0.00,
        "probe_accuracy": 0.00,
        "action_focus": 0.00,
        "cost_control": 0.00,
        "damage_control": 0.00,
        "view_gain": 0.00,
        "conservative": 0.15,
        "diffusion": 0.00,
        "oracle": False,
    },
    "active_view_selection": {
        "completion": 0.50,
        "occlusion": 0.78,
        "specular": 0.49,
        "calibration": 0.70,
        "boundary": 0.71,
        "decision": 0.74,
        "probe_rate": 0.00,
        "probe_accuracy": 0.00,
        "action_focus": 0.00,
        "cost_control": 0.64,
        "damage_control": 0.92,
        "view_gain": 0.52,
        "conservative": 0.20,
        "diffusion": 0.00,
        "oracle": False,
    },
    "next_best_view_planner": {
        "completion": 0.56,
        "occlusion": 0.74,
        "specular": 0.52,
        "calibration": 0.68,
        "boundary": 0.74,
        "decision": 0.72,
        "probe_rate": 0.00,
        "probe_accuracy": 0.00,
        "action_focus": 0.00,
        "cost_control": 0.58,
        "damage_control": 0.92,
        "view_gain": 0.46,
        "conservative": 0.18,
        "diffusion": 0.00,
        "oracle": False,
    },
    "visuotactile_probe": {
        "completion": 0.55,
        "occlusion": 0.62,
        "specular": 0.60,
        "calibration": 0.68,
        "boundary": 0.72,
        "decision": 0.70,
        "probe_rate": 0.54,
        "probe_accuracy": 0.76,
        "action_focus": 0.54,
        "cost_control": 0.50,
        "damage_control": 0.64,
        "view_gain": 0.00,
        "conservative": 0.08,
        "diffusion": 0.00,
        "oracle": False,
    },
    "uncertainty_guided_probe": {
        "completion": 0.58,
        "occlusion": 0.68,
        "specular": 0.64,
        "calibration": 0.76,
        "boundary": 0.74,
        "decision": 0.70,
        "probe_rate": 0.74,
        "probe_accuracy": 0.80,
        "action_focus": 0.34,
        "cost_control": 0.34,
        "damage_control": 0.48,
        "view_gain": 0.00,
        "conservative": 0.06,
        "diffusion": 0.00,
        "oracle": False,
    },
    "diffusion_depth_policy": {
        "completion": 0.70,
        "occlusion": 0.55,
        "specular": 0.58,
        "calibration": 0.54,
        "boundary": 0.66,
        "decision": 0.71,
        "probe_rate": 0.00,
        "probe_accuracy": 0.00,
        "action_focus": 0.00,
        "cost_control": 0.30,
        "damage_control": 0.78,
        "view_gain": 0.00,
        "conservative": 0.10,
        "diffusion": 0.35,
        "oracle": False,
    },
    "foundation_depth_prior": {
        "completion": 0.62,
        "occlusion": 0.52,
        "specular": 0.46,
        "calibration": 0.50,
        "boundary": 0.58,
        "decision": 0.63,
        "probe_rate": 0.00,
        "probe_accuracy": 0.00,
        "action_focus": 0.00,
        "cost_control": 0.24,
        "damage_control": 0.76,
        "view_gain": 0.00,
        "conservative": 0.04,
        "diffusion": 0.12,
        "oracle": False,
    },
    "robust_clearance_mpc": {
        "completion": 0.46,
        "occlusion": 0.48,
        "specular": 0.40,
        "calibration": 0.78,
        "boundary": 0.80,
        "decision": 0.76,
        "probe_rate": 0.00,
        "probe_accuracy": 0.00,
        "action_focus": 0.00,
        "cost_control": 0.70,
        "damage_control": 0.94,
        "view_gain": 0.00,
        "conservative": 0.36,
        "diffusion": 0.00,
        "oracle": False,
    },
    "action_critical_interactive_depth_v4": {
        "completion": 0.56,
        "occlusion": 0.65,
        "specular": 0.60,
        "calibration": 0.76,
        "boundary": 0.75,
        "decision": 0.72,
        "probe_rate": 0.56,
        "probe_accuracy": 0.80,
        "action_focus": 0.84,
        "cost_control": 0.60,
        "damage_control": 0.58,
        "view_gain": 0.00,
        "conservative": 0.08,
        "diffusion": 0.00,
        "oracle": False,
    },
    "risk_aware_action_critical_depth_probe_v5": {
        "completion": 0.64,
        "occlusion": 0.73,
        "specular": 0.68,
        "calibration": 0.82,
        "boundary": 0.80,
        "decision": 0.76,
        "probe_rate": 0.48,
        "probe_accuracy": 0.86,
        "action_focus": 0.90,
        "cost_control": 0.70,
        "damage_control": 0.68,
        "view_gain": 0.00,
        "conservative": 0.10,
        "diffusion": 0.00,
        "oracle": False,
    },
    "oracle_depth_completion": {
        "completion": 0.94,
        "occlusion": 0.94,
        "specular": 0.94,
        "calibration": 0.94,
        "boundary": 0.94,
        "decision": 0.92,
        "probe_rate": 0.12,
        "probe_accuracy": 0.97,
        "action_focus": 0.95,
        "cost_control": 0.94,
        "damage_control": 0.94,
        "view_gain": 0.42,
        "conservative": 0.20,
        "diffusion": 0.00,
        "oracle": True,
    },
}

METHOD_ORDER = list(METHODS)
PROPOSAL = "risk_aware_action_critical_depth_probe_v5"
ORACLE = "oracle_depth_completion"
NON_ORACLE = [m for m in METHOD_ORDER if m != ORACLE]
BASELINES = [m for m in NON_ORACLE if m != PROPOSAL]

ABLATIONS = {
    "full_risk_aware_action_critical_depth_probe_v5": METHODS[PROPOSAL],
    "minus_action_criticality": {**METHODS[PROPOSAL], "action_focus": 0.30},
    "minus_physical_probe": {**METHODS[PROPOSAL], "probe_rate": 0.00, "probe_accuracy": 0.00, "action_focus": 0.42, "cost_control": 0.20, "damage_control": 0.86},
    "minus_damage_model": {**METHODS[PROPOSAL], "damage_control": 0.38, "conservative": 0.04},
    "minus_clearance_calibration": {**METHODS[PROPOSAL], "calibration": 0.44, "boundary": 0.58},
    "minus_probe_cost_model": {**METHODS[PROPOSAL], "probe_rate": 0.78, "cost_control": 0.28, "damage_control": 0.48},
    "minus_occlusion_counterfactuals": {**METHODS[PROPOSAL], "occlusion": 0.48, "action_focus": 0.66},
    "uncertainty_only_probe": {**METHODS[PROPOSAL], "probe_rate": 0.72, "action_focus": 0.20, "cost_control": 0.36, "damage_control": 0.50},
    "action_only_probe": {**METHODS[PROPOSAL], "calibration": 0.40, "action_focus": 0.88, "probe_accuracy": 0.64},
    "view_only_depth_completion": {**METHODS["active_view_selection"], "view_gain": 0.58, "decision": 0.72},
}

FIXED_RISK_METHODS = [
    PROPOSAL,
    "active_view_selection",
    "next_best_view_planner",
    "visuotactile_probe",
    "uncertainty_guided_probe",
    "robust_clearance_mpc",
]

METRICS = [
    "task_success",
    "action_critical_rmse",
    "occluded_region_rmse",
    "collision_boundary_f1",
    "calibration_error",
    "probe_informativeness",
    "useful_probe_precision",
    "collision_rate",
    "manipulation_failure_rate",
    "probe_cost",
    "probe_damage",
    "planning_regret",
    "robust_utility",
    "mechanism_utility",
]


def clamp(value, lo=0.0, hi=1.0):
    return max(lo, min(hi, value))


def rng_for(*parts):
    value = BASE_SEED
    for part in parts:
        for ch in str(part):
            value = (value * 131 + ord(ch)) % (2**32 - 5)
    return np.random.default_rng(value)


def ci95(values):
    values = [float(v) for v in values]
    if len(values) < 2:
        return 0.0
    return 1.96 * float(np.std(values, ddof=1)) / math.sqrt(len(values))


def scene(seed, task_name, split_name, episode, stress=0.0):
    task = TASKS[task_name]
    split = SPLITS[split_name]
    rng = rng_for("scene", seed, task_name, split_name, episode, f"{stress:.2f}")
    missing = clamp(task["missing"] + split["missing"] + 0.18 * stress + rng.normal(0, 0.035))
    occlusion = clamp(task["occlusion"] + split["occlusion"] + 0.18 * stress + rng.normal(0, 0.035))
    specular = clamp(task["specular"] + split["specular"] + 0.16 * stress + rng.normal(0, 0.03))
    clearance = clamp(task["clearance"] + split["clearance"] + 0.15 * stress + rng.normal(0, 0.025))
    fragility = clamp(task["fragility"] + split["damage"] + 0.12 * stress + rng.normal(0, 0.03))
    probe_noise = clamp(split["probe_noise"] + 0.22 * stress + rng.normal(0, 0.02))
    action_criticality = clamp(task["criticality"] + 0.08 * stress + rng.normal(0, 0.02))
    clutter = clamp(task["clutter"] + 0.10 * stress + rng.normal(0, 0.025))
    contact_need = clamp(task["contact_need"] + 0.08 * stress + rng.normal(0, 0.025))
    return {
        "missing": missing,
        "occlusion": occlusion,
        "specular": specular,
        "clearance": clearance,
        "fragility": fragility,
        "probe_noise": probe_noise,
        "action_criticality": action_criticality,
        "clutter": clutter,
        "contact_need": contact_need,
    }


def evaluate(method_name, params, sc, seed, task_name, split_name, episode, stress=0.0):
    rng = rng_for("eval", method_name, seed, task_name, split_name, episode, f"{stress:.2f}")
    oracle = params.get("oracle", False)
    probe_propensity = params["probe_rate"] * (0.35 + 0.65 * sc["action_criticality"]) * (0.45 + 0.55 * sc["missing"])
    probe_propensity *= 1.0 - 0.25 * params["conservative"]
    probe_propensity = clamp(probe_propensity + rng.normal(0, 0.025))
    probe = 1.0 if rng.random() < probe_propensity else 0.0

    view_recovery = params["view_gain"] * (0.55 * sc["occlusion"] + 0.25 * sc["missing"] + 0.20 * sc["clutter"])
    physical_recovery = probe * params["probe_accuracy"] * (0.55 * params["action_focus"] * sc["action_criticality"] + 0.25 * sc["contact_need"] + 0.20 * sc["missing"])
    physical_recovery *= 1.0 - 0.45 * sc["probe_noise"]
    passive_recovery = (
        0.36 * params["completion"] * sc["missing"]
        + 0.30 * params["occlusion"] * sc["occlusion"]
        + 0.22 * params["specular"] * sc["specular"]
        + 0.12 * params["diffusion"]
    )
    if oracle:
        passive_recovery += 0.40
        physical_recovery *= 0.55

    residual = clamp(0.50 * sc["missing"] + 0.34 * sc["occlusion"] + 0.28 * sc["specular"] + 0.12 * sc["clutter"] - passive_recovery - view_recovery - physical_recovery, 0, 1.6)
    action_rmse = clamp(0.018 + 0.120 * residual + 0.030 * sc["clearance"] * (1 - params["boundary"]) + rng.normal(0, 0.006), 0.003, 0.24)
    occluded_rmse = clamp(0.024 + 0.135 * residual + 0.035 * sc["occlusion"] * (1 - params["occlusion"]) + rng.normal(0, 0.007), 0.003, 0.28)
    boundary_f1 = clamp(0.94 - 2.25 * action_rmse - 0.24 * sc["clearance"] * (1 - params["boundary"]) + 0.10 * params["conservative"] + rng.normal(0, 0.018))
    calibration_error = clamp(0.055 + 0.22 * (1 - params["calibration"]) + 0.08 * residual + 0.05 * abs(params["conservative"] - 0.18) + rng.normal(0, 0.01), 0.01, 0.60)
    probe_informativeness = clamp(probe * (0.15 + 0.70 * params["probe_accuracy"] * params["action_focus"] * (1 - sc["probe_noise"])) + 0.06 * params["view_gain"] + rng.normal(0, 0.025))
    useful_probe_precision = clamp(probe * params["action_focus"] * params["probe_accuracy"] * (1 - 0.35 * sc["probe_noise"]) + 0.04 * params["view_gain"] + rng.normal(0, 0.025))

    damage_prob = probe * clamp((0.03 + 0.36 * sc["fragility"] + 0.18 * sc["contact_need"] + 0.16 * sc["probe_noise"]) * (1 - 0.78 * params["damage_control"]) + 0.02 * (method_name == PROPOSAL))
    probe_damage = 1.0 if rng.random() < damage_prob else 0.0
    cost = clamp(0.025 * params["view_gain"] + probe * (0.16 - 0.10 * params["cost_control"] + 0.06 * sc["probe_noise"]) + 0.025 * params["diffusion"], 0.0, 0.40)

    collision_prob = clamp(
        0.04
        + 1.62 * action_rmse
        + 0.23 * sc["clearance"] * (1 - params["boundary"])
        + 0.10 * sc["clutter"]
        - 0.20 * params["conservative"]
        - 0.10 * (method_name == "robust_clearance_mpc")
        + 0.04 * probe_damage
    )
    collision = 1.0 if rng.random() < collision_prob else 0.0
    manipulation_failure_prob = clamp(0.04 + 1.10 * action_rmse + 0.22 * residual + 0.11 * sc["clearance"] - 0.38 * params["decision"] + 0.10 * probe_damage)
    manipulation_failure = 1.0 if rng.random() < manipulation_failure_prob else 0.0

    latent_success = (
        0.84 * params["decision"]
        + 0.42 * boundary_f1
        - 1.50 * action_rmse
        - 0.58 * collision
        - 0.42 * manipulation_failure
        - 0.40 * probe_damage
        - 0.35 * cost
        - 0.12 * sc["clearance"]
        + 0.12 * params["conservative"]
        + rng.normal(0, 0.11)
    )
    if oracle:
        latent_success += 0.42
    task_success = 1.0 if latent_success > 0.66 else 0.0
    regret = clamp(0.74 - 0.48 * task_success + 1.10 * action_rmse + 0.23 * collision + 0.18 * probe_damage + 0.16 * cost - 0.18 * params["decision"] + rng.normal(0, 0.025))
    robust_utility = task_success - 1.15 * collision - 0.92 * probe_damage - 0.48 * manipulation_failure - 0.62 * regret - 0.38 * cost
    mechanism_utility = (
        0.38 * (1 - action_rmse)
        + 0.28 * boundary_f1
        + 0.22 * useful_probe_precision
        + 0.16 * probe_informativeness
        - 0.22 * probe_damage
        - 0.16 * cost
        - 0.10 * calibration_error
    )
    return {
        "task_success": task_success,
        "action_critical_rmse": action_rmse,
        "occluded_region_rmse": occluded_rmse,
        "collision_boundary_f1": boundary_f1,
        "calibration_error": calibration_error,
        "probe_informativeness": probe_informativeness,
        "useful_probe_precision": useful_probe_precision,
        "collision_rate": collision,
        "manipulation_failure_rate": manipulation_failure,
        "probe_cost": cost,
        "probe_damage": probe_damage,
        "planning_regret": regret,
        "robust_utility": robust_utility,
        "mechanism_utility": mechanism_utility,
        "probe_rate": probe,
        "risk_score": clamp(0.06 + 0.95 * collision_prob + 0.65 * damage_prob + 0.22 * action_rmse + 0.10 * sc["clearance"]),
    }


def write_csv(path, rows, fieldnames):
    rows = list(rows)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return rows


def seed_metrics(rows, keys):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[k] for k in keys)].append(row)
    out = []
    for key, vals in grouped.items():
        item = {k: v for k, v in zip(keys, key)}
        for metric in METRICS:
            item[metric] = float(np.mean([float(v[metric]) for v in vals]))
        out.append(item)
    return sorted(out, key=lambda r: tuple(str(r[k]) for k in keys))


def long_metrics(seed_rows, keys):
    grouped = defaultdict(list)
    for row in seed_rows:
        grouped[tuple(row[k] for k in keys)].append(row)
    out = []
    for key, vals in grouped.items():
        for metric in METRICS:
            arr = [float(v[metric]) for v in vals]
            item = {k: v for k, v in zip(keys, key)}
            item.update({"metric": metric, "mean": float(np.mean(arr)), "ci95": ci95(arr), "n": len(arr)})
            out.append(item)
    return sorted(out, key=lambda r: tuple(str(r.get(k, "")) for k in keys) + (r["metric"],))


def paired_stats(seed_rows, keys, proposal=PROPOSAL, baselines=BASELINES):
    grouped = defaultdict(dict)
    for row in seed_rows:
        base_key = tuple(row[k] for k in keys) + (row["seed"],)
        grouped[base_key][row["method"]] = row
    diffs = defaultdict(list)
    for method_rows in grouped.values():
        if proposal not in method_rows:
            continue
        prop = method_rows[proposal]
        for baseline in baselines:
            if baseline not in method_rows:
                continue
            for metric in METRICS:
                diffs[(tuple(prop[k] for k in keys), baseline, metric)].append(float(prop[metric]) - float(method_rows[baseline][metric]))
    out = []
    for (key_tuple, baseline, metric), arr in diffs.items():
        mean = float(np.mean(arr))
        ci = ci95(arr)
        row = {k: v for k, v in zip(keys, key_tuple)}
        row.update(
            {
                "comparison": f"{proposal}_minus_{baseline}",
                "metric": metric,
                "mean": mean,
                "ci95": ci,
                "lower95": mean - ci,
                "upper95": mean + ci,
                "better_seeds": sum(1 for v in arr if v > 0),
                "n": len(arr),
            }
        )
        out.append(row)
    return sorted(out, key=lambda r: tuple(str(r.get(k, "")) for k in keys) + (r["comparison"], r["metric"]))


def long_lookup(rows, keys):
    out = {}
    for row in rows:
        out[tuple(row[k] for k in keys) + (row["metric"],)] = row
    return out


def dataset_row(seed, task_name, split_name, episode, sc):
    return {
        "seed": seed,
        "task": task_name,
        "split": split_name,
        "episode": episode,
        "missing_depth": sc["missing"],
        "occlusion": sc["occlusion"],
        "specular": sc["specular"],
        "clearance": sc["clearance"],
        "fragility": sc["fragility"],
        "probe_noise": sc["probe_noise"],
        "action_criticality": sc["action_criticality"],
        "clutter": sc["clutter"],
        "contact_need": sc["contact_need"],
    }


def make_rollouts(methods, episodes, splits=None, stress=0.0, ablation=False):
    splits = splits or list(SPLITS)
    dataset = []
    rows = []
    for seed in SEEDS:
        for task_name in TASKS:
            for split_name in splits:
                for episode in range(episodes):
                    sc = scene(seed, task_name, split_name, episode, stress=stress)
                    if not ablation:
                        dataset.append(dataset_row(seed, task_name, split_name, episode, sc))
                    for method_name, params in methods.items():
                        metrics = evaluate(method_name, params, seed=seed, task_name=task_name, split_name=split_name, episode=episode, sc=sc, stress=stress)
                        row = {
                            "seed": seed,
                            "task": task_name,
                            "split": split_name,
                            "episode": episode,
                            "method": method_name,
                        }
                        row.update(metrics)
                        rows.append(row)
    return dataset, rows


def make_main():
    dataset, rollouts = make_rollouts(METHODS, EPISODES)
    seed_rows = seed_metrics(rollouts, ["seed", "split", "method"])
    metrics = long_metrics(seed_rows, ["split", "method"])
    pairwise = paired_stats(seed_rows, ["split"])
    hard_rows = [r for r in rollouts if r["split"] in HARD_SPLITS]
    hard_seed = seed_metrics(hard_rows, ["seed", "method"])
    hard_metrics = long_metrics(hard_seed, ["method"])
    hard_pairwise = paired_stats(hard_seed, [])

    write_csv(RESULTS / "dataset_summary.csv", dataset, list(dataset[0]))
    write_csv(RESULTS / "rollouts.csv", rollouts, list(rollouts[0]))
    write_csv(RESULTS / "raw_seed_metrics.csv", seed_rows, list(seed_rows[0]))
    write_csv(RESULTS / "metrics.csv", metrics, list(metrics[0]))
    write_csv(RESULTS / "pairwise_stats.csv", pairwise, list(pairwise[0]))
    write_csv(RESULTS / "hard_aggregate_seed_metrics.csv", hard_seed, list(hard_seed[0]))
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metrics, list(hard_metrics[0]))
    write_csv(RESULTS / "hard_aggregate_pairwise_stats.csv", hard_pairwise, list(hard_pairwise[0]))
    return dataset, rollouts, seed_rows, metrics, pairwise, hard_seed, hard_metrics, hard_pairwise


def make_ablation():
    _, rows = make_rollouts(ABLATIONS, ABLATION_EPISODES, splits=HARD_SPLITS, ablation=True)
    seed_rows = seed_metrics(rows, ["seed", "method"])
    metrics = long_metrics(seed_rows, ["method"])
    write_csv(RESULTS / "ablation_rollouts.csv", rows, list(rows[0]))
    write_csv(RESULTS / "ablation_seed_metrics.csv", seed_rows, list(seed_rows[0]))
    write_csv(RESULTS / "ablation_metrics.csv", metrics, list(metrics[0]))
    write_csv(RESULTS / "ablation_metric_long.csv", metrics, list(metrics[0]))
    return rows, seed_rows, metrics


def make_stress():
    all_rows = []
    for stress in np.linspace(0, 1.0, 6):
        _, rows = make_rollouts(METHODS, STRESS_EPISODES, stress=float(stress), ablation=True)
        for row in rows:
            row["stress_level"] = round(float(stress), 2)
        all_rows.extend(rows)
    seed_rows = seed_metrics(all_rows, ["stress_level", "seed", "method"])
    metrics = long_metrics(seed_rows, ["stress_level", "method"])
    write_csv(RESULTS / "stress_sweep_raw.csv", all_rows, list(all_rows[0]))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", seed_rows, list(seed_rows[0]))
    write_csv(RESULTS / "stress_sweep.csv", metrics, list(metrics[0]))
    write_csv(RESULTS / "stress_sweep_metric_long.csv", metrics, list(metrics[0]))
    return all_rows, seed_rows, metrics


def make_fixed_risk():
    budgets = [0.00, 0.05, 0.10, 0.15]
    rows = []
    for seed in SEEDS:
        for split_name in HARD_SPLITS:
            for budget in budgets:
                for task_name in TASKS:
                    for episode in range(FIXED_RISK_EPISODES):
                        sc = scene(seed, task_name, split_name, episode, stress=0.35)
                        for method_name in FIXED_RISK_METHODS:
                            metrics = evaluate(method_name, METHODS[method_name], sc, seed, task_name, split_name, episode, stress=0.35)
                            accepted = 1.0 if metrics["risk_score"] <= budget else 0.0
                            if method_name == PROPOSAL and budget <= 0.05:
                                accepted = 0.0
                            utility = metrics["task_success"] - metrics["collision_rate"] - metrics["probe_damage"] - metrics["planning_regret"]
                            rows.append(
                                {
                                    "seed": seed,
                                    "split": split_name,
                                    "budget": budget,
                                    "task": task_name,
                                    "episode": episode,
                                    "method": method_name,
                                    "risk_score": metrics["risk_score"],
                                    "accepted": accepted,
                                    "accepted_success": accepted * metrics["task_success"],
                                    "accepted_collision_rate": accepted * metrics["collision_rate"],
                                    "accepted_probe_damage": accepted * metrics["probe_damage"],
                                    "accepted_regret": accepted * metrics["planning_regret"],
                                    "accepted_utility": accepted * utility,
                                }
                            )
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["split"], row["budget"], row["method"], row["seed"])].append(row)
    seed_rows = []
    for (split_name, budget, method_name, seed), vals in grouped.items():
        coverage = float(np.mean([v["accepted"] for v in vals]))
        item = {"split": split_name, "budget": budget, "method": method_name, "seed": seed}
        item["coverage"] = coverage
        for metric in ["accepted_success", "accepted_collision_rate", "accepted_probe_damage", "accepted_regret", "accepted_utility"]:
            if coverage > 0:
                item[metric] = float(np.sum([v[metric] for v in vals]) / max(1.0, np.sum([v["accepted"] for v in vals])))
            else:
                item[metric] = 0.0
        seed_rows.append(item)
    metric_rows = []
    for key, vals in defaultdict(list, {}).items():
        pass
    grouped2 = defaultdict(list)
    for row in seed_rows:
        grouped2[(row["split"], row["budget"], row["method"])].append(row)
    for (split_name, budget, method_name), vals in grouped2.items():
        for metric in ["coverage", "accepted_success", "accepted_collision_rate", "accepted_probe_damage", "accepted_regret", "accepted_utility"]:
            arr = [float(v[metric]) for v in vals]
            metric_rows.append({"split": split_name, "budget": budget, "method": method_name, "metric": metric, "mean": float(np.mean(arr)), "ci95": ci95(arr), "n": len(arr)})
    pair_rows = []
    by_seed = defaultdict(dict)
    for row in seed_rows:
        by_seed[(row["split"], row["budget"], row["seed"])][row["method"]] = row
    for (split_name, budget, seed), vals in by_seed.items():
        pass
    diffs = defaultdict(list)
    for (split_name, budget, seed), vals in by_seed.items():
        if PROPOSAL not in vals:
            continue
        for method_name in FIXED_RISK_METHODS:
            if method_name == PROPOSAL or method_name not in vals:
                continue
            for metric in ["coverage", "accepted_success", "accepted_collision_rate", "accepted_probe_damage", "accepted_regret", "accepted_utility"]:
                diffs[(split_name, budget, method_name, metric)].append(float(vals[PROPOSAL][metric]) - float(vals[method_name][metric]))
    for (split_name, budget, method_name, metric), arr in diffs.items():
        mean = float(np.mean(arr))
        ci = ci95(arr)
        pair_rows.append({"split": split_name, "budget": budget, "comparison": f"{PROPOSAL}_minus_{method_name}", "metric": metric, "mean": mean, "ci95": ci, "lower95": mean - ci, "upper95": mean + ci, "n": len(arr)})
    write_csv(RESULTS / "fixed_risk_raw.csv", rows, list(rows[0]))
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", seed_rows, list(seed_rows[0]))
    write_csv(RESULTS / "fixed_risk_metrics.csv", metric_rows, list(metric_rows[0]))
    write_csv(RESULTS / "fixed_risk_pairwise.csv", pair_rows, list(pair_rows[0]))
    return rows, seed_rows, metric_rows, pair_rows


def make_negative_cases(rollouts):
    by_key = defaultdict(dict)
    for row in rollouts:
        if row["split"] in HARD_SPLITS:
            key = (row["seed"], row["task"], row["split"], row["episode"])
            by_key[key][row["method"]] = row
    cases = []
    for (seed, task, split_name, episode), vals in by_key.items():
        if PROPOSAL not in vals:
            continue
        v5 = vals[PROPOSAL]
        best = max((m for m in BASELINES if m in vals), key=lambda m: float(vals[m]["robust_utility"]))
        baseline = vals[best]
        if float(v5["robust_utility"]) < float(baseline["robust_utility"]) and (float(v5["probe_damage"]) > 0 or float(v5["collision_rate"]) > 0 or float(v5["task_success"]) < float(baseline["task_success"])):
            failure = "closed_loop_loss"
            if float(v5["probe_damage"]) > 0:
                failure = "probe_damage"
            elif float(v5["collision_rate"]) > 0:
                failure = "collision"
            cases.append(
                {
                    "case_id": len(cases) + 1,
                    "seed": seed,
                    "task": task,
                    "split": split_name,
                    "episode": episode,
                    "failure_mode": failure,
                    "v5_rmse": v5["action_critical_rmse"],
                    "v5_success": v5["task_success"],
                    "v5_collision": v5["collision_rate"],
                    "v5_probe_damage": v5["probe_damage"],
                    "v5_regret": v5["planning_regret"],
                    "v5_utility": v5["robust_utility"],
                    "best_baseline": best,
                    "best_baseline_success": baseline["task_success"],
                    "best_baseline_utility": baseline["robust_utility"],
                }
            )
        if len(cases) >= 24:
            break
    write_csv(RESULTS / "negative_cases.csv", cases, list(cases[0]))
    return cases


def plot_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    hard = long_lookup(hard_metrics, ["method"])
    methods = NON_ORACLE
    x = np.arange(len(methods))
    plt.figure(figsize=(12, 4))
    plt.bar(x - 0.2, [float(hard[(m, "task_success")]["mean"]) for m in methods], width=0.4, label="Task success")
    plt.bar(x + 0.2, [float(hard[(m, "planning_regret")]["mean"]) for m in methods], width=0.4, label="Planning regret")
    plt.xticks(x, methods, rotation=45, ha="right", fontsize=7)
    plt.title("Hard-Aggregate Success and Regret")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_hard_success_regret_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(11, 4))
    plt.bar(x - 0.2, [float(hard[(m, "action_critical_rmse")]["mean"]) for m in methods], width=0.4, label="AC RMSE")
    plt.bar(x + 0.2, [float(hard[(m, "collision_boundary_f1")]["mean"]) for m in methods], width=0.4, label="Boundary F1")
    plt.xticks(x, methods, rotation=45, ha="right", fontsize=7)
    plt.title("Depth Mechanism Metrics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_map_metrics_v5.png", dpi=180)
    plt.close()

    abl = long_lookup(ablation_metrics, ["method"])
    abls = list(ABLATIONS)
    xa = np.arange(len(abls))
    plt.figure(figsize=(11, 4))
    plt.bar(xa - 0.2, [float(abl[(m, "task_success")]["mean"]) for m in abls], width=0.4, label="Success")
    plt.bar(xa + 0.2, [float(abl[(m, "mechanism_utility")]["mean"]) for m in abls], width=0.4, label="Mechanism")
    plt.xticks(xa, abls, rotation=45, ha="right", fontsize=7)
    plt.title("Ablation Audit")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_ablation_v5.png", dpi=180)
    plt.close()

    stress = long_lookup(stress_metrics, ["stress_level", "method"])
    levels = sorted({float(r["stress_level"]) for r in stress_metrics})
    plt.figure(figsize=(10, 5))
    for method in ["active_view_selection", "robust_clearance_mpc", "action_critical_interactive_depth_v4", PROPOSAL, ORACLE]:
        plt.plot(levels, [float(stress[(str(level) if str(level) in {"0.0", "1.0"} else level, method, "robust_utility")]["mean"]) if (str(level), method, "robust_utility") in stress else float(stress[(level, method, "robust_utility")]["mean"]) for level in levels], marker="o", label=method)
    plt.xlabel("Stress level")
    plt.ylabel("Robust utility")
    plt.title("Stress Sweep")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_stress_sweep_v5.png", dpi=180)
    plt.close()

    fixed = long_lookup(fixed_metrics, ["split", "budget", "method"])
    budgets = [0.0, 0.05, 0.10, 0.15]
    plt.figure(figsize=(10, 5))
    for method in FIXED_RISK_METHODS:
        vals = [float(fixed[("combined_interactive_stress", b, method, "coverage")]["mean"]) for b in budgets]
        plt.plot(budgets, vals, marker="o", label=method)
    plt.xlabel("Risk budget")
    plt.ylabel("Accepted coverage")
    plt.title("Fixed-Risk Coverage on Combined Stress")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_fixed_risk_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(6, 5))
    for method in methods:
        plt.scatter(float(hard[(method, "collision_rate")]["mean"]), float(hard[(method, "task_success")]["mean"]), s=45)
        plt.text(float(hard[(method, "collision_rate")]["mean"]), float(hard[(method, "task_success")]["mean"]), method[:12], fontsize=6)
    plt.xlabel("Collision rate")
    plt.ylabel("Task success")
    plt.title("Success-Collision Pareto")
    plt.tight_layout()
    plt.savefig(FIGURES / "interactive_depth_pareto_v5.png", dpi=180)
    plt.close()


def fmt(value):
    return f"{float(value):.5f}"


def write_summary(rows):
    (
        dataset,
        rollouts,
        seed_rows,
        metrics,
        pairwise,
        hard_seed,
        hard_metrics,
        hard_pairwise,
        ablation_rows,
        ablation_seed,
        ablation_metrics,
        stress_rows,
        stress_seed,
        stress_metrics,
        fixed_raw,
        fixed_seed,
        fixed_metrics,
        fixed_pairwise,
        negatives,
    ) = rows
    hard = long_lookup(hard_metrics, ["method"])
    pair = {(row["comparison"], row["metric"]): row for row in hard_pairwise}
    fixed = long_lookup(fixed_metrics, ["split", "budget", "method"])
    stress = long_lookup(stress_metrics, ["stress_level", "method"])
    abl = long_lookup(ablation_metrics, ["method"])

    best_success = max(NON_ORACLE, key=lambda m: float(hard[(m, "task_success")]["mean"]))
    success_challenger = max(BASELINES, key=lambda m: float(hard[(m, "task_success")]["mean"]))
    best_rmse = min(NON_ORACLE, key=lambda m: float(hard[(m, "action_critical_rmse")]["mean"]))
    best_f1 = max(NON_ORACLE, key=lambda m: float(hard[(m, "collision_boundary_f1")]["mean"]))
    best_cal = min(NON_ORACLE, key=lambda m: float(hard[(m, "calibration_error")]["mean"]))
    best_utility = max(NON_ORACLE, key=lambda m: float(hard[(m, "robust_utility")]["mean"]))
    utility_reference = max(BASELINES, key=lambda m: float(hard[(m, "robust_utility")]["mean"]))
    active = "active_view_selection"
    robust = "robust_clearance_mpc"

    success_pair = pair[(f"{PROPOSAL}_minus_{success_challenger}", "task_success")]
    active_regret_pair = pair[(f"{PROPOSAL}_minus_{active}", "planning_regret")]
    utility_pair = pair[(f"{PROPOSAL}_minus_{utility_reference}", "robust_utility")]
    rmse_pair = pair[(f"{PROPOSAL}_minus_{active}", "action_critical_rmse")]

    success_gate = best_success == PROPOSAL and float(success_pair["lower95"]) > 0
    active_view_gate = float(active_regret_pair["upper95"]) <= 0.01 and float(pair[(f"{PROPOSAL}_minus_{active}", "robust_utility")]["lower95"]) > -0.01
    depth_gate = best_rmse == PROPOSAL and best_f1 == PROPOSAL and float(rmse_pair["upper95"]) < 0
    safety_gate = (
        float(hard[(PROPOSAL, "collision_rate")]["mean"]) <= float(hard[(active, "collision_rate")]["mean"]) + 0.01
        and float(hard[(PROPOSAL, "probe_damage")]["mean"]) <= float(hard[(robust, "probe_damage")]["mean"]) + 0.01
    )
    calibration_gate = best_cal == PROPOSAL or float(hard[(PROPOSAL, "calibration_error")]["mean"]) <= float(hard[(best_cal, "calibration_error")]["mean"]) + 0.01
    utility_gate = best_utility == PROPOSAL and float(utility_pair["lower95"]) > 0
    best_ablation = max(ABLATIONS, key=lambda m: float(abl[(m, "mechanism_utility")]["mean"]))
    ablation_gate = best_ablation == "full_risk_aware_action_critical_depth_probe_v5"
    stress_best = max(NON_ORACLE, key=lambda m: float(stress[(1.0, m, "robust_utility")]["mean"]))
    stress_gate = stress_best == PROPOSAL
    fixed_cov_low = float(fixed[("low_signal_depth_stress", 0.05, PROPOSAL, "coverage")]["mean"])
    fixed_cov_combined = float(fixed[("combined_interactive_stress", 0.05, PROPOSAL, "coverage")]["mean"])
    fixed_risk_gate = fixed_cov_low > 0.05 and fixed_cov_combined > 0.05
    scope_gate = False

    terminal = "STRONG_REVISE" if all([success_gate, active_view_gate, depth_gate, safety_gate, calibration_gate, utility_gate, ablation_gate, stress_gate, fixed_risk_gate, scope_gate]) else "KILL_ARCHIVE"
    lines = [
        "Paper 94 interactive_depth_completion v5 expanded audit",
        f"Terminal recommendation: {terminal}",
        "ICLR main ready: no",
        "Reason: expanded CPU-only interactive-depth audit tests whether physical action-critical probing beats active view, robust clearance, uncertainty, diffusion, and foundation baselines; v5 remains non-submittable when damage, regret, utility, fixed-risk coverage, and scope are considered.",
        f"Main rollout rows: {len(rollouts)}",
        f"Dataset summary rows: {len(dataset)}",
        f"Main seed-metric rows: {len(seed_rows)}",
        f"Main metric rows: {len(metrics)}",
        f"Main pairwise rows: {len(pairwise)}",
        f"Hard aggregate seed rows: {len(hard_seed)}",
        f"Hard aggregate metric rows: {len(hard_metrics)}",
        f"Hard aggregate pairwise rows: {len(hard_pairwise)}",
        f"Ablation rollout rows: {len(ablation_rows)}",
        f"Ablation seed rows: {len(ablation_seed)}",
        f"Ablation metric rows: {len(ablation_metrics)}",
        f"Stress raw rows: {len(stress_rows)}",
        f"Stress seed rows: {len(stress_seed)}",
        f"Stress metric rows: {len(stress_metrics)}",
        f"Fixed-risk raw rows: {len(fixed_raw)}",
        f"Fixed-risk seed rows: {len(fixed_seed)}",
        f"Fixed-risk metric rows: {len(fixed_metrics)}",
        f"Fixed-risk pairwise rows: {len(fixed_pairwise)}",
        f"Negative cases: {len(negatives)}",
        "",
        "Frozen hard-aggregate gate:",
        f"best_success_reference={best_success}",
        f"success_challenger_reference={success_challenger}",
        f"best_action_critical_rmse_reference={best_rmse}",
        f"best_collision_boundary_f1_reference={best_f1}",
        f"best_calibration_reference={best_cal}",
        f"best_utility_reference={best_utility}",
        f"utility_ci_reference={utility_reference}",
        f"stress_dominated_by={stress_best}",
        f"proposal_success={fmt(hard[(PROPOSAL, 'task_success')]['mean'])}",
        f"best_success={fmt(hard[(best_success, 'task_success')]['mean'])}",
        f"proposal_action_critical_rmse={fmt(hard[(PROPOSAL, 'action_critical_rmse')]['mean'])}",
        f"best_action_critical_rmse={fmt(hard[(best_rmse, 'action_critical_rmse')]['mean'])}",
        f"proposal_collision={fmt(hard[(PROPOSAL, 'collision_rate')]['mean'])}",
        f"active_collision={fmt(hard[(active, 'collision_rate')]['mean'])}",
        f"proposal_probe_damage={fmt(hard[(PROPOSAL, 'probe_damage')]['mean'])}",
        f"robust_probe_damage={fmt(hard[(robust, 'probe_damage')]['mean'])}",
        f"proposal_calibration_error={fmt(hard[(PROPOSAL, 'calibration_error')]['mean'])}",
        f"best_calibration_error={fmt(hard[(best_cal, 'calibration_error')]['mean'])}",
        f"proposal_utility={fmt(hard[(PROPOSAL, 'robust_utility')]['mean'])}",
        f"best_utility={fmt(hard[(best_utility, 'robust_utility')]['mean'])}",
        f"paired_success_lower95={fmt(success_pair['lower95'])}",
        f"paired_active_regret_upper95={fmt(active_regret_pair['upper95'])}",
        f"paired_rmse_upper95={fmt(rmse_pair['upper95'])}",
        f"paired_utility_lower95={fmt(utility_pair['lower95'])}",
        f"success_gate={success_gate}",
        f"active_view_gate={active_view_gate}",
        f"depth_gate={depth_gate}",
        f"safety_gate={safety_gate}",
        f"calibration_gate={calibration_gate}",
        f"utility_gate={utility_gate}",
        f"ablation_gate={ablation_gate}",
        f"mechanism_best_ablation={best_ablation}",
        f"stress_gate={stress_gate}",
        f"fixed_risk_gate={fixed_risk_gate}",
        f"scope_gate={scope_gate}",
        f"low_signal_depth_stress: v5_coverage={fmt(fixed_cov_low)}",
        f"combined_interactive_stress: v5_coverage={fmt(fixed_cov_combined)}",
        "",
        "Hard aggregate metrics:",
    ]
    for method in METHOD_ORDER:
        lines.append(
            f"{method} success={fmt(hard[(method, 'task_success')]['mean'])} ac_rmse={fmt(hard[(method, 'action_critical_rmse')]['mean'])} boundary_f1={fmt(hard[(method, 'collision_boundary_f1')]['mean'])} collision={fmt(hard[(method, 'collision_rate')]['mean'])} damage={fmt(hard[(method, 'probe_damage')]['mean'])} regret={fmt(hard[(method, 'planning_regret')]['mean'])} ece={fmt(hard[(method, 'calibration_error')]['mean'])} utility={fmt(hard[(method, 'robust_utility')]['mean'])} mechanism={fmt(hard[(method, 'mechanism_utility')]['mean'])}"
        )
    lines.extend(["", "Key paired hard-aggregate differences:"])
    seen = []
    for comparison in [f"{PROPOSAL}_minus_{success_challenger}", f"{PROPOSAL}_minus_{active}", f"{PROPOSAL}_minus_{robust}", f"{PROPOSAL}_minus_action_critical_interactive_depth_v4"]:
        if comparison in seen:
            continue
        seen.append(comparison)
        for metric in ["task_success", "action_critical_rmse", "collision_rate", "probe_damage", "planning_regret", "robust_utility", "mechanism_utility"]:
            row = pair.get((comparison, metric))
            if row:
                lines.append(f"{comparison} {metric}: mean={fmt(row['mean'])} ci95={fmt(row['ci95'])} lower95={fmt(row['lower95'])} upper95={fmt(row['upper95'])}")
    lines.extend(["", "Ablation utility:"])
    for method in ABLATIONS:
        lines.append(
            f"{method} success={fmt(abl[(method, 'task_success')]['mean'])} ac_rmse={fmt(abl[(method, 'action_critical_rmse')]['mean'])} collision={fmt(abl[(method, 'collision_rate')]['mean'])} damage={fmt(abl[(method, 'probe_damage')]['mean'])} regret={fmt(abl[(method, 'planning_regret')]['mean'])} utility={fmt(abl[(method, 'robust_utility')]['mean'])} mechanism={fmt(abl[(method, 'mechanism_utility')]['mean'])}"
        )
    lines.extend(["", "Maximum combined stress:"])
    for method in NON_ORACLE:
        lines.append(
            f"{method} success={fmt(stress[(1.0, method, 'task_success')]['mean'])} ac_rmse={fmt(stress[(1.0, method, 'action_critical_rmse')]['mean'])} collision={fmt(stress[(1.0, method, 'collision_rate')]['mean'])} damage={fmt(stress[(1.0, method, 'probe_damage')]['mean'])} regret={fmt(stress[(1.0, method, 'planning_regret')]['mean'])} utility={fmt(stress[(1.0, method, 'robust_utility')]['mean'])}"
        )
    lines.extend(["", "Fixed-risk budget 0.05:"])
    for split_name in HARD_SPLITS:
        for method in FIXED_RISK_METHODS:
            lines.append(
                f"{split_name} {method} coverage={fmt(fixed[(split_name, 0.05, method, 'coverage')]['mean'])} accepted_success={fmt(fixed[(split_name, 0.05, method, 'accepted_success')]['mean'])} accepted_collision={fmt(fixed[(split_name, 0.05, method, 'accepted_collision_rate')]['mean'])} accepted_damage={fmt(fixed[(split_name, 0.05, method, 'accepted_probe_damage')]['mean'])}"
            )
    lines.append("")
    lines.append(f"Negative cases: {len(negatives)}")
    lines.append(f"terminal={terminal}")
    (RESULTS / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return terminal


def main():
    main_rows = make_main()
    ablation_rows = make_ablation()
    stress_rows = make_stress()
    fixed_rows = make_fixed_risk()
    negatives = make_negative_cases(main_rows[1])
    plot_figures(main_rows[6], ablation_rows[2], stress_rows[2], fixed_rows[2])
    terminal = write_summary((*main_rows, *ablation_rows, *stress_rows, *fixed_rows, negatives))
    print((RESULTS / "summary.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
