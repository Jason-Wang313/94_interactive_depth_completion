# Paper 94 Expanded Submission Plan

Date frozen: 2026-06-22

Paper: `94_interactive_depth_completion`

Target: ICLR-main readiness audit, not cosmetic expansion.

Terminal policy: report `STRONG_REVISE` only if the frozen gates clear after the experiment is run. Otherwise report `KILL_ARCHIVE` honestly.

## Objective

Rebuild Paper 94 into a 25+ page submission-style artifact that tests whether action-critical physical probing for depth completion improves closed-loop manipulation beyond passive completion, Gaussian/ensemble uncertainty, active view selection, next-best-view planning, VLM/foundation depth priors, diffusion depth policies, visuotactile probing, uncertainty-guided probing, robust clearance MPC, and the previous v4 method.

The v5 method under test is `risk_aware_action_critical_depth_probe_v5`: an interactive depth-completion policy that predicts which missing depth cells are action-critical, probes only when the expected downstream utility exceeds damage/cost risk, calibrates clearance uncertainty, and chooses actions using risk-aware completed geometry rather than raw depth or map error alone.

## Frozen Main Experiment

CPU-only and RAM-light execution:

- Seeds: 10.
- Tasks: 6.
- Splits: 8.
- Methods: 14 total, including oracle.
- Episodes per task/split/method/seed: 32.
- Main rollout rows: 215,040.
- Dataset-summary rows: 15,360.

Tasks:

- `occluded_bin_grasping`
- `shelf_insertion_clearance`
- `transparent_container_lift`
- `leaf_occluded_fruit_grasp`
- `drawer_slot_alignment`
- `deformable_bag_depth_lift`

Splits:

- `nominal_depth`
- `missing_depth_shift`
- `occlusion_shift`
- `transparent_specular_shift`
- `probe_noise_shift`
- `tight_clearance_shift`
- `low_signal_depth_stress`
- `combined_interactive_stress`

Methods:

- `raw_depth_policy`
- `learned_depth_completion`
- `gaussian_splat_uncertainty`
- `ensemble_depth_completion`
- `active_view_selection`
- `next_best_view_planner`
- `visuotactile_probe`
- `uncertainty_guided_probe`
- `diffusion_depth_policy`
- `foundation_depth_prior`
- `robust_clearance_mpc`
- `action_critical_interactive_depth_v4`
- `risk_aware_action_critical_depth_probe_v5`
- `oracle_depth_completion`

## Metrics

Deployment metrics:

- Task success.
- Collision rate.
- Manipulation failure rate.
- Probe damage.
- Planning regret.
- Probe cost.
- Robust utility.

Depth and mechanism metrics:

- Action-critical RMSE.
- Occluded-region RMSE.
- Collision-boundary F1.
- Calibration error.
- Probe informativeness.
- Useful-probe precision.
- Action churn.

## Frozen Gates

The proposal must clear all gates to be called `STRONG_REVISE`:

- Success gate: v5 must be the best non-oracle method on the hard aggregate, with paired lower95 > 0 against the strongest non-oracle success challenger.
- Active-view gate: v5 must not lose regret or utility to `active_view_selection`; physical probing must justify contact risk.
- Depth gate: v5 must be best non-oracle on action-critical RMSE and collision-boundary F1.
- Safety gate: v5 collision and probe damage must be no worse than active view selection plus 0.01 and robust clearance MPC plus 0.01.
- Calibration gate: v5 must be best non-oracle calibration or within 0.01 ECE of the best while improving utility.
- Utility gate: v5 must be best non-oracle robust utility with paired lower95 > 0 against the strongest utility challenger.
- Ablation gate: the full v5 method must beat all ablations on mechanism utility and hard success.
- Stress gate: v5 must dominate non-oracle robust utility at maximum stress.
- Fixed-risk gate: v5 must have nonzero useful coverage at risk budget 0.05 on `low_signal_depth_stress` and `combined_interactive_stress`.
- Scope gate: the paper cannot be called ICLR-main-ready without real robot or accepted high-fidelity manipulation validation.

## Additional Experiments

Ablations:

- `full_risk_aware_action_critical_depth_probe_v5`
- `minus_action_criticality`
- `minus_physical_probe`
- `minus_damage_model`
- `minus_clearance_calibration`
- `minus_probe_cost_model`
- `minus_occlusion_counterfactuals`
- `uncertainty_only_probe`
- `action_only_probe`
- `view_only_depth_completion`

Stress sweep:

- Six stress levels from 0.0 to 1.0.
- Cross all tasks, splits, methods, seeds, and 15 episodes.
- Expected raw stress rows: 604,800.

Fixed-risk deployment:

- Hard splits: `low_signal_depth_stress`, `combined_interactive_stress`.
- Budgets: 0.00, 0.05, 0.10, 0.15.
- Methods: v5, active view, next-best-view, visuotactile probe, uncertainty-guided probe, robust clearance MPC.
- Expected raw rows: 69,120.

Negative cases:

- Keep 24 cases where v5 has high depth/probe confidence but loses closed-loop utility, collides, damages the scene, or is dominated by a non-contact view baseline.

## Manuscript Requirements

- 25+ pages in ICLR style.
- Bright boxed clickable in-text citations that route to the bibliography.
- Honest `KILL_ARCHIVE` or `STRONG_REVISE` terminal decision.
- Downloads-only numbered PDF: `C:/Users/wangz/Downloads/94.pdf`.
- No visible Desktop PDF.
- Public GitHub repo must be updated and verified.
