# Child Status 94

Current stage: v5 expanded submission-readiness audit complete
Last update: 2026-06-22 06:06 Asia/Shanghai
PDF: C:/Users/wangz/Downloads/94.pdf
PDF SHA256: 122B4E1F84A7BBA741DC56FEB2F26A2C001F25D986880057D18D7AB796BF71F3
GitHub: https://github.com/Jason-Wang313/94_interactive_depth_completion
Submission-hardening version: v5 expanded audit
Terminal decision: KILL_ARCHIVE
ICLR main ready: no

Evidence digest:
- 10 seeds, 6 tasks, 8 splits, 14 methods, 215,040 main rollout rows, 76,800 ablation rows, 604,800 stress rows, 69,120 fixed-risk rows, and 24 negative cases.
- Best hard-split success reference: active_view_selection with success 0.76693.
- Proposed v5 success: 0.60885.
- Proposed v5 action-critical RMSE: 0.05641 vs 0.03623 for active_view_selection.
- Proposed v5 collision: 0.20547 vs 0.17344 for active_view_selection and 0.10938 for robust_clearance_mpc.
- Proposed v5 probe damage: 0.07682 vs 0.00156 for active_view_selection and 0.00130 for robust_clearance_mpc.
- Proposed v5 robust utility: 0.01034 vs 0.36148 for active_view_selection.
- Fixed-risk budget 0.05 coverage for v5 on hard splits: 0.00000.

Reason:
V5 is a real improvement over the previous v4 interactive-depth policy, but it fails the ICLR-main submission gate because non-contact active view selection and conservative robust clearance remain stronger deployment strategies under the frozen protocol. The archive is retained as a reproducible negative benchmark, not as a submission-ready claim.
