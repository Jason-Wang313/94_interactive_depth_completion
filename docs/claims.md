# Claims

## Claim Tested

Risk-aware action-critical physical probing for depth completion should improve decision-relevant depth and closed-loop manipulation enough to outperform passive completion, uncertainty baselines, active/next-best-view perception, tactile probing, diffusion/foundation priors, robust clearance MPC, and the previous v4 method under hostile stress.

## Supported Claims

- V5 improves substantially over `action_critical_interactive_depth_v4` on hard-split success, RMSE, collision, damage, regret, and robust utility.
- The v5 audit is much stronger than the prior local audit: 10 seeds, 6 tasks, 8 splits, 14 methods, 215,040 main rollouts, 76,800 ablation rows, 604,800 stress rows, 69,120 fixed-risk rows, paired confidence intervals, stress degradation tables, fixed-risk sweeps, and 24 indexed negative cases.
- The method has a measurable mechanism signal: it improves over v4 and several contact-heavy or passive baselines.
- Calibration is the only hard gate that passes in the final gate vector.

## Measured Negative Claim

Under the hard aggregate, active view selection beats v5:

- Success: 0.76693 vs 0.60885.
- Action-critical RMSE: 0.03623 vs 0.05641.
- Collision: 0.17344 vs 0.20547.
- Probe damage: 0.00156 vs 0.07682.
- Regret: 0.32102 vs 0.43869.
- Robust utility: 0.36148 vs 0.01034.

V5 also has zero accepted coverage at fixed-risk budget 0.05 on both hard splits.

## Unsupported Claims Explicitly Avoided

- No claim of ICLR-main submission readiness.
- No claim of real-robot validation.
- No claim of high-fidelity simulation.
- No claim of state-of-the-art interactive depth completion.
- No claim that physical probing is necessary when active viewpoint selection is available.
- No claim that zero fixed-risk coverage can support deployable manipulation.
