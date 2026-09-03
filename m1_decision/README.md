# M1 - Decision Intelligence

## 1. Responsibility

Member 1 (M1) is responsible for the **Decision Intelligence** layer of the Smart Scan system.

The main question answered by M1 is:

> **"Which region should the scanner scan next?"**

M1 receives processed observations, maintains its belief about different regions, evaluates possible scan actions, and selects the region with the highest expected utility.

M1 does **not** access simulator ground truth.

---

# 2. Role of M1 in the Overall System

The overall system is designed as a closed decision loop:

```text
                    ┌──────────────────────┐
                    │      M1 Decision     │
                    │     Intelligence     │
                    └──────────┬───────────┘
                               │
                         ScanAction
                               │
                               ▼
                    ┌──────────────────────┐
                    │   M3 Simulator /     │
                    │   Scanner Environment│
                    └──────────┬───────────┘
                               │
                      Raw Observation
                               │
                               ▼
                    ┌──────────────────────┐
                    │   M2 Signal /        │
                    │   Observation        │
                    │   Processing         │
                    └──────────┬───────────┘
                               │
                    Processed Observation
                               │
                               ▼
                    ┌──────────────────────┐
                    │      M1 Belief       │
                    │        Update        │
                    └──────────┬───────────┘
                               │
                               ▼
                         Next Decision