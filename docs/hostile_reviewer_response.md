# Hostile Reviewer Response

Paper: 94 Interactive Depth Completion

## Strongest Technical Threats

- rt-RISeg: Real-Time Model-Free Robot Interactive Segmentation for Active Instance-Level Object Understanding (2025)
- Learning Guided Convolutional Network for Depth Completion (2019)
- Model predictive control with active learning under model uncertainty: Why, when, and how (2018)
- SaPaVe: Towards Active Perception and Manipulation in Vision-Language-Action Models for Robotics (2026)
- Toward Real-world BEV Perception: Depth Uncertainty Estimation via Gaussian Splatting (2025)
- Interactively Robot Action Planning with Uncertainty Analysis and Active Questioning by Large Language Model (2023)
- Active uncertainty reduction for safe and efficient interaction planning (2024)
- UNCLE-Grasp: Uncertainty-Aware Grasping of Leaf-Occluded Strawberries (2026)

## Hostile ICLR-Main Response

A hostile reviewer should reject this as an ICLR-main submission. The v4 rebuild replaces the shared template experiment with a paper-specific active-perception manipulation benchmark, but the evidence still falsifies the central claim.

The decisive objection is not just "synthetic evidence." It is that the proposed physical probing mechanism loses to active view selection in the local benchmark:

- Task success: 0.514 +/- 0.106 vs 0.795 +/- 0.080 for active view selection.
- Action-critical RMSE: 0.056 vs 0.043.
- Collision rate: 0.123 vs 0.048.
- Probe damage: 0.153 vs 0.000.
- Planning regret: 0.441 vs 0.267.

The physical probe improves some local geometry, but the cost and damage risk are enough that a non-contact active perception baseline is safer and more successful.

## Honest Action

The paper is marked `KILL_ARCHIVE`. This avoids converting a generated robotics idea into an overstated main-conference claim.

## What Would Be Needed To Revive

- Real robot or high-fidelity benchmark experiments.
- Implemented active-view, depth-completion, uncertainty, and tactile baselines.
- A physical probing policy that beats active view selection on task success, collision safety, regret, and damage/cost.
- Manual full-paper related-work audit.
- Hardware videos or qualitative rollouts.
