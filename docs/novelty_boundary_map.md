# Novelty Boundary Map

## Crowded Territory

- Generic active learning or uncertainty.
- Passive learned depth completion.
- Gaussian-splat or ensemble uncertainty estimates.
- Active view selection for occlusion reduction.
- Visuo-tactile probing and contact-aware grasping.
- Planner wrappers around perception uncertainty.

## Claimed Boundary Tested

The only plausible boundary was action-critical physical probing: a robot should touch only the uncertain depth regions that affect the next manipulation action, improving local geometry enough to change the action safely.

## Falsification Result

The boundary is falsified by the v4 benchmark. Active view selection dominates the proposed physical probing method under combined stress:

- Higher task success.
- Lower action-critical RMSE.
- Lower collision rate.
- Lower planning regret.
- No probe damage.

Decision: KILL_ARCHIVE. The novelty boundary is not defensible for ICLR main without substantially new evidence and a stronger physical probing mechanism.
