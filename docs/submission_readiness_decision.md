# Submission Readiness Decision

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

## Why It Fails

The strongest defensible claim was that risk-aware action-critical physical probing should outperform passive completion, uncertainty baselines, active view selection, next-best-view planning, tactile probing, diffusion/foundation depth policies, robust clearance MPC, and the previous v4 method under combined manipulation stress.

The 2026-06-22 v5 audit falsifies that claim under the frozen protocol.

Active view selection is the strongest non-oracle hard-success baseline:

- active_view_selection task success: 0.76693.
- risk_aware_action_critical_depth_probe_v5 task success: 0.60885.
- active_view_selection action-critical RMSE: 0.03623.
- v5 action-critical RMSE: 0.05641.
- active_view_selection robust utility: 0.36148.
- v5 robust utility: 0.01034.

Robust clearance MPC also exposes the safety problem:

- robust_clearance_mpc collision: 0.10938.
- v5 collision: 0.20547.
- robust_clearance_mpc probe damage: 0.00130.
- v5 probe damage: 0.07682.

At fixed-risk budget 0.05, v5 has zero accepted coverage on both hard splits. A method that accepts no hard actions cannot establish deployable manipulation at that risk budget.

## Honest Terminal Action

Archive/kill for ICLR main. Do not submit this paper to ICLR main in its current form.

## Revival Condition

The idea would need a substantially new empirical project:

- Real robot or recognized high-fidelity simulator evidence.
- A safer learned probe policy with explicit damage-cost learning.
- Nonzero strict fixed-risk coverage at budget 0.05.
- Success and utility dominance over active view selection and robust clearance MPC.
- Stronger ablation necessity showing the novel contact mechanism is required.
- Released replayable seeds, risk scores, failure cases, and videos.
- Independent reproduction or at least a clean public artifact bundle beyond local simulation.
