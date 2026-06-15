# Claims

## Claim Tested

Interactive depth completion is useful only if the robot probes regions that are both uncertain and action-critical, improving local geometry enough to change manipulation decisions without excessive probe cost or damage.

## Supported Claims

- The v4.1 rerun confirms the benchmark is reproducible and paper-specific: four manipulation tasks, five distribution shifts, nine methods, seven seeds, ablations, stress curves, paired task/seed comparisons, and failure cases.
- The proposed mechanism improves over raw depth, learned depth completion, Gaussian-splat uncertainty, ensemble completion, visuo-tactile probing, and uncertainty-guided probing on some combined-stress metrics.
- The mechanism fails the main closed-loop gate because active view selection is stronger without physical contact.

## Measured Negative Claim

Under combined interactive stress, active view selection beats the proposed method:

- Task success: 0.795 +/- 0.080 vs 0.514 +/- 0.106.
- Action-critical RMSE: 0.043 vs 0.056.
- Collision rate: 0.048 vs 0.123.
- Probe damage: 0.000 vs 0.153.
- Paired success difference for proposed minus active view selection: -0.28075 +/- 0.07128.

## Unsupported Claims Explicitly Avoided

- No claim of ICLR-main submission readiness.
- No claim of real-robot validation.
- No claim of high-fidelity simulation.
- No claim of state-of-the-art depth completion or manipulation.
- No claim that physical probing is necessary when active viewpoint selection is available.
