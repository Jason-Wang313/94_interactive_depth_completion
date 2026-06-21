# ICLR Main Gate

Paper: 94 interactive_depth_completion

Submission-hardening version: v5 expanded audit

Gate verdict: KILL_ARCHIVE

Latest rerun: 2026-06-22

Evidence digest: v5 deterministic interactive-depth benchmark with 10 seeds, 6 tasks, 8 splits, 14 methods, 215,040 main rollouts, 76,800 ablation rollouts, 604,800 stress rows, 69,120 fixed-risk rows, paired confidence intervals, fixed-risk budget sweeps, stress degradation analysis, and 24 negative cases.

Gate vector:

- success_gate=False
- active_view_gate=False
- depth_gate=False
- safety_gate=False
- calibration_gate=True
- utility_gate=False
- ablation_gate=False
- stress_gate=False
- fixed_risk_gate=False
- scope_gate=False

Fatal blockers:

- V5 is dominated by active view selection on hard-aggregate success, action-critical RMSE, collision, damage, regret, and robust utility.
- V5 task success is 0.60885 vs 0.76693 for active view selection.
- V5 action-critical RMSE is 0.05641 vs 0.03623 for active view selection.
- V5 collision rate is 0.20547 vs 0.17344 for active view selection and 0.10938 for robust clearance MPC.
- V5 probe damage is 0.07682 vs 0.00156 for active view selection and 0.00130 for robust clearance MPC.
- V5 robust utility is 0.01034 vs 0.36148 for active view selection.
- V5 fixed-risk coverage at budget 0.05 is zero on both hard splits.
- The evidence is still local simulation rather than real robot or high-fidelity simulator validation.

The only honest main-conference-safe decision is to archive rather than overclaim.
