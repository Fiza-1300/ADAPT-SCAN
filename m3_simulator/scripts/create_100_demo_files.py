"""
Create 100 demo files with realistic PDWs.
"""

import os
import json
import h5py
import numpy as np
from pathlib import Path

def create_demo_files(count=100, output_dir='data/turing_subset/train', seed=42):
    """Create multiple demo files."""
    np.random.seed(seed)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🔧 Creating {count} demo files...")
    
    files_created = []
    for i in range(count):
        file_path = f'{output_dir}/demo_train_{i+1:04d}.h5'
        
        with h5py.File(file_path, 'w') as f:
            # More realistic with varying number of pulses
            num_pulses = np.random.randint(50, 1000)
            num_emitters = np.random.randint(1, 8)
            
            # Create pulse data with realistic patterns
            pulses = np.zeros((num_pulses, 5))
            
            # Time of Arrival (with realistic intervals)
            toa_intervals = np.random.exponential(0.005, num_pulses)
            pulses[:, 0] = np.cumsum(toa_intervals)
            
            # Centre Frequency (with realistic ranges)
            freq_center = np.random.uniform(8000, 12000)
            freq_spread = np.random.uniform(50, 500)
            pulses[:, 1] = np.random.normal(freq_center, freq_spread, num_pulses)
            
            # Pulse Width (with realistic values)
            pulses[:, 2] = np.random.uniform(0.3, 3.0, num_pulses)
            
            # Angle of Arrival (with realistic spread)
            aoa_center = np.random.uniform(0, 360)
            aoa_spread = np.random.uniform(5, 30)
            pulses[:, 3] = np.random.normal(aoa_center, aoa_spread, num_pulses)
            
            # Amplitude (with realistic distribution)
            pulses[:, 4] = np.random.uniform(0.1, 1.0, num_pulses)
            
            f.create_dataset('pulses', data=pulses)
            
            # Create labels (assign pulses to emitters)
            labels = np.random.randint(0, num_emitters, num_pulses)
            f.create_dataset('labels', data=labels)
            
            # Add metadata
            metadata = {
                'num_pulses': num_pulses,
                'num_emitters': num_emitters,
                'frequency_range': [freq_center - freq_spread*2, freq_center + freq_spread*2],
                'pulse_width_range': [np.min(pulses[:, 2]), np.max(pulses[:, 2])]
            }
            f.attrs['metadata'] = json.dumps(metadata)
        
        files_created.append(file_path)
        if (i+1) % 10 == 0:
            print(f"   Created {i+1}/{count} files...")
    
    # Create metadata file
    metadata = {
        'total_files': count,
        'split': 'train',
        'files': files_created,
        'is_demo': True,
        'description': f'{count} demo files created for testing'
    }
    
    with open(f'{output_dir}/metadata_100.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ Created {count} demo files!")
    print(f"   Location: {output_dir}/")
    return files_created

if __name__ == "__main__":
    create_demo_files(count=100)
