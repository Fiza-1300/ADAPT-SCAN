

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

### Step 2: Create README.md

```bash
cat > README.md << 'EOF'
# ADAPT-SCAN
## Team SIH26055 - Adaptive Scanning Project

### Team Structure
| Member | Role | Responsibility |
|--------|------|----------------|
| Member 1 | Decision Intelligence | What to scan next? |
| Member 2 | Signal Processing | Convert observations to features |
| Member 3 | Simulation/Environment | **YOU ARE HERE** - Build the simulator |
| Member 4 | Backend/Integration | Connect all components |
| Member 5 | Frontend/Visualization | Show what's happening |
| Member 6 | Research/Validation | Prove it works |

### Folder Structure

### Step 3: Create a .gitignore for the project

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/
.dmypy.json
dmypy.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Project specific
logs/
data/
results/
*.log
