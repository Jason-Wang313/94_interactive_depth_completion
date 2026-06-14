# Submission Attack Log

Paper: 94 interactive_depth_completion

This v4 pass applies the ICLR main-conference bar with a paper-specific benchmark. The result is an honest archive decision, not a workshop resubmission.

## Attack 1: Active view selection may dominate physical probing.

Verdict: Confirmed.

Evidence: active_view_selection reaches 0.795 +/- 0.080 combined-stress task success; proposed_action_critical_interactive_depth reaches 0.514 +/- 0.106. Paired proposed-minus-active-view success difference is -0.28075 +/- 0.07128.

Action: Kill/archive. The central empirical claim does not survive the strongest local baseline.

## Attack 2: Physical probing may improve geometry but hurt contact-sensitive tasks.

Verdict: Confirmed.

Evidence: proposed probe damage is 0.153 overall under combined stress and 0.228 on leaf-occluded fruit grasping. Active view selection has zero probe damage.

Action: Keep failure analysis and do not claim probing is broadly useful.

## Attack 3: The method may not improve action-critical geometry enough.

Verdict: Confirmed against the strongest baseline.

Evidence: proposed action-critical RMSE is 0.056, while active view selection reaches 0.043. Paired proposed-minus-active-view RMSE difference is +0.01259 +/- 0.00203.

Action: Kill/archive.

## Attack 4: The method may be less safe.

Verdict: Confirmed.

Evidence: proposed collision rate is 0.123 vs 0.048 for active view selection; planning regret is 0.441 vs 0.267.

Action: Kill/archive.

## Attack 5: Synthetic evidence is insufficient for ICLR-main robotics claims.

Verdict: Still true.

Evidence: the v4 benchmark is reproducible and paper-specific, but it is not real robot or high-fidelity simulator validation.

Action: Frame as a negative evidence audit, not a submission.

## Attack 6: Prior work already covers active perception, uncertainty, tactile probing, and depth completion.

Verdict: Still true.

Evidence: hostile pool includes learned depth completion, Gaussian-splat uncertainty, active perception/manipulation, interactive segmentation, tactile/uncertainty grasping, and active uncertainty reduction.

Action: Do not claim novelty from generic probing or uncertainty.

## Attack 7: Ablations could show the mechanism is not necessary.

Verdict: Partly mitigated, but not enough.

Evidence: full proposed method is ahead of its ablations on success, but the external active-view baseline is still stronger.

Action: Archive; internal ablation support cannot rescue a losing external comparison.

## Attack 8: No meaningful recoverable ICLR-main issue remains after the negative result.

Verdict: Terminal condition reached.

Action: Mark KILL_ARCHIVE and stop Paper 94 after public repo/PDF/report updates.
