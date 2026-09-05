"""
This script will add the real dataset methods to your environment.py
Run this to fix the 'use_real_dataset' error.
"""

import re
import os

# Read the current environment.py
with open('simulator/environment.py', 'r') as f:
    content = f.read()

# Check if the methods already exist
if 'use_real_dataset' in content:
    print("✅ use_real_dataset already exists!")
    exit(0)

# Add imports at the top
import_line = "from .scenarios import get_scenario_config"
new_imports = """
from .scenarios import get_scenario_config
try:
    from .tsrd_ground_truth import TSRDGroundTruth
    from .dataset_loader import DatasetLoader
    _HAS_TSRD = True
except ImportError:
    _HAS_TSRD = False
    print("⚠️ TSRD modules not available")
"""

content = content.replace(import_line, new_imports)

# Add the new methods after __init__
init_end = "self.done = False"
new_methods = """
        self.done = False
        self.scenario_id = None
        self.current_config = None
        self.appearance_triggered = False
        self.using_real_data = False
        self.current_dataset = None
        self.tsrd_truth = None

    def use_real_dataset(self, dataset_name: str = 'TSRD_Stare', seed: int = 42):
        \"\"\"
        Switch to using real Hugging Face datasets.
        
        Args:
            dataset_name: 'TSRD_Stare', 'TSRD_Scan', 'RadSeg', 'General_RF', 'Combined'
            seed: Random seed
        \"\"\"
        try:
            if not _HAS_TSRD:
                print("❌ TSRD modules not available. Install with: pip install huggingface_hub h5py")
                return
            loader = DatasetLoader(seed=seed)
            self.tsrd_truth = TSRDGroundTruth(loader, self.num_regions, seed)
            self.tsrd_truth.switch_dataset(dataset_name)
            self.using_real_data = True
            self.current_dataset = dataset_name
            print(f"✅ Using real dataset: {dataset_name}")
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            self.using_real_data = False

    def list_available_datasets(self):
        \"\"\"List all available real datasets.\"\"\"
        if hasattr(self, 'tsrd_truth') and self.tsrd_truth:
            return self.tsrd_truth.list_datasets()
        return []

    def get_region_truth_real(self, region_id: str):
        \"\"\"Get ground truth from real datasets.\"\"\"
        if hasattr(self, 'using_real_data') and self.using_real_data and self.tsrd_truth:
            return self.tsrd_truth.get_region_truth(region_id)
        return None
"""

content = content.replace(init_end, new_methods)

# Add/modify get_hidden_state
if 'def get_hidden_state(self):' in content:
    # Find and replace
    pattern = r'def get_hidden_state\(self\):.*?return self\.ground_truth\.get_hidden_state\(\)'
    replacement = '''def get_hidden_state(self):
        """Get hidden state."""
        if hasattr(self, 'using_real_data') and self.using_real_data and self.tsrd_truth:
            return self.tsrd_truth.get_hidden_state()
        else:
            return self.ground_truth.get_hidden_state()'''
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Add/modify update method
if 'def update(self, timestep: int):' in content:
    pattern = r'def update\(self, timestep: int\):.*?self\.ground_truth\.update\(timestep\).*?self\._check_sudden_appearance\(\)'
    replacement = '''def update(self, timestep: int):
        """Update environment state."""
        if hasattr(self, 'using_real_data') and self.using_real_data and self.tsrd_truth:
            self.tsrd_truth.update(timestep)
        else:
            self.ground_truth.update(timestep)
            self._check_sudden_appearance()'''
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write the updated file
with open('simulator/environment.py', 'w') as f:
    f.write(content)

print("✅ Environment.py updated with real dataset support!")
print("   Added: use_real_dataset(), list_available_datasets()")
print("   Modified: get_hidden_state(), update()")
