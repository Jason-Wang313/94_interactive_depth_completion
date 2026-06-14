# Child Status 94

Current stage: ICLR main gate terminal
Last update: 2026-06-14 16:13:24 +01:00
PDF: C:/Users/wangz/Downloads/94.pdf
GitHub: https://github.com/Jason-Wang313/94_interactive_depth_completion
Submission-hardening version: v4
Terminal decision: KILL_ARCHIVE
ICLR main ready: no

Evidence digest:
- Seven seeds, four manipulation tasks, five stress splits, nine methods, ablations, stress sweep, paired confidence intervals, and failure cases.
- Strongest non-oracle combined-stress baseline: active_view_selection with task success 0.795 +/- 0.080.
- Proposed action-critical probing: task success 0.514 +/- 0.106, action-critical RMSE 0.056, collision rate 0.123, probe damage 0.153.
- Paired success difference vs active view selection: -0.28075 +/- 0.07128 over 28 task/seed groups.

Reason:
The proposed physical probing mechanism is dominated by active view selection under combined stress: active view selection recovers enough occluded geometry without contact damage and has lower RMSE, collisions, regret, and cost. This is not submission-ready for ICLR main.
