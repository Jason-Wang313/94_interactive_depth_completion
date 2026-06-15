# Submission Readiness Decision

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

## Why It Fails

The strongest defensible claim was that action-critical physical probing should outperform passive completion, uncertainty baselines, active view selection, and generic tactile probing under combined manipulation stress. The benchmark falsifies that claim.

The 2026-06-15 v4.1 continuation rerun reproduced the same decision.

Active view selection is the strongest non-oracle combined-stress baseline:

- active_view_selection task success: 0.795 +/- 0.080.
- proposed_action_critical_interactive_depth task success: 0.514 +/- 0.106.
- Paired proposed-minus-active-view success difference: -0.28075 +/- 0.07128.
- Proposed also has higher action-critical RMSE, higher collision rate, higher planning regret, higher cost, and nonzero probe damage.

## Honest Terminal Action

Archive/kill for ICLR main. Do not submit this paper to ICLR main in its current form.

## Revival Condition

The idea would need a substantially new empirical project:

- Real robot or high-fidelity simulator evidence.
- Implemented learned depth-completion and active-view baselines.
- A physical probing system that beats active view selection without unacceptable damage or cost.
- Manual related-work synthesis and qualitative rollouts.
- A new terminal gate showing the proposed mechanism wins on task success, action-critical geometry, collision safety, regret, and damage/cost.
