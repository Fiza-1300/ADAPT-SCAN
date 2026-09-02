

## Key Interfaces

### 1. m3_simulator → m2_signal (Observation)
```json
{
    "region_id": "R7",
    "detected": true,
    "strength": 0.63,
    "bandwidth": 0.41,
    "snr": 7.2,
    "confidence": 0.72,
    "features": []
}
{
    "regions": [
        {
            "region_id": "R7",
            "existence": 0.81,
            "uncertainty": 0.67,
            "threat_relevance": 0.82,
            "last_observed": 4
        }
    ],
    "budget_remaining": 31.0,
    "timestep": 4
}
{
    "selected_action": "R7",
    "utility": 0.78,
    "information_gain": 0.74,
    "threat_score": 0.82,
    "uncertainty": 0.67,
    "tracking_value": 0.63,
    "scan_cost": 0.12,
    "reason": "Selected R7 because it has high uncertainty..."
}

