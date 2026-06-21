# Submission Readiness Audit v5

Date: 2026-06-22

Decision: KILL_ARCHIVE

ICLR-main readiness: no.

## Protocol

- Seeds: 10.
- Tasks: 6.
- Splits: 8.
- Methods: 14.
- Main rollout rows: 215,040.
- Ablation rollout rows: 76,800.
- Stress raw rows: 604,800.
- Fixed-risk raw rows: 69,120.
- Negative cases: 24.

## Result

V5 improves over v4 but does not survive hostile review because the relevant comparison is not v4. The relevant comparison is the best non-contact or conservative deployment strategy.

Hard aggregate:

- `active_view_selection` success: 0.76693.
- `risk_aware_action_critical_depth_probe_v5` success: 0.60885.
- `active_view_selection` utility: 0.36148.
- `risk_aware_action_critical_depth_probe_v5` utility: 0.01034.
- `robust_clearance_mpc` collision: 0.10938.
- `risk_aware_action_critical_depth_probe_v5` collision: 0.20547.

## Fixed-Risk Failure

At budget 0.05, v5 accepts zero hard-split actions. Zero accepted coverage cannot support a deployable fixed-risk manipulation claim.

## Final Label

The result is useful as a negative benchmark and as a specification of the burden for a future interactive-depth paper. It is not a submission-ready ICLR-main paper.
