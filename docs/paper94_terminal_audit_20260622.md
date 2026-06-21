# Paper 94 Terminal Audit - 2026-06-22

Terminal recommendation: KILL_ARCHIVE

The v5 rebuild expanded Paper 94 into a 25-page ICLR-style negative audit with bright boxed clickable citations and a 180-entry bibliography. The protocol was frozen before execution and run CPU-only/RAM-light.

## Evidence Summary

- Main rollout rows: 215,040.
- Dataset rows: 15,360.
- Main metric rows: 1,568.
- Main pairwise rows: 1,344.
- Hard aggregate seed rows: 140.
- Hard aggregate metric rows: 196.
- Hard aggregate pairwise rows: 168.
- Ablation rollout rows: 76,800.
- Ablation metric rows: 140.
- Stress raw rows: 604,800.
- Stress metric rows: 1,176.
- Fixed-risk raw rows: 69,120.
- Fixed-risk metric rows: 288.
- Negative cases: 24.

## Hard-Aggregate Decision

The strongest non-oracle success and utility reference is active view selection. V5 loses to active view selection on success, action-critical RMSE, collision, probe damage, regret, and robust utility.

V5 also loses the safety tradeoff to robust clearance MPC. The only hard gate that passes is calibration.

## Artifact Verification

- Downloads PDF: `C:/Users/wangz/Downloads/94.pdf`
- PDF SHA256: `122B4E1F84A7BBA741DC56FEB2F26A2C001F25D986880057D18D7AB796BF71F3`
- PDF pages: 25.
- Validator: passed in local raw mode and compressed public artifact mode.
- Desktop leak check: `C:/Users/wangz/Desktop/94.pdf` does not exist.

## Public Packaging

`results/stress_sweep_raw.csv` is 177,619,570 bytes and is intentionally ignored. The public repo tracks `results/stress_sweep_raw.csv.gz` plus `results/STRESS_SWEEP_RAW_MANIFEST.md`.
