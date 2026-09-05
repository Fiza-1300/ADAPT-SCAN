import h5py
import json
import os

def inspect_demo_files():
    data_dir = 'data/turing_subset/train/'
    print("=" * 60)
    print("INSPECTING DEMO DATA")
    print("=" * 60)
    
    for file in os.listdir(data_dir):
        if file.endswith('.h5'):
            print(f"\n📊 File: {file}")
            with h5py.File(f'{data_dir}/{file}', 'r') as f:
                print(f"   Keys: {list(f.keys())}")
                if 'pulses' in f:
                    print(f"   Pulses shape: {f['pulses'].shape}")
                    print(f"   First pulse: {f['pulses'][0]}")
                if 'labels' in f:
                    print(f"   Unique labels: {len(set(f['labels'][:]))}")

if __name__ == "__main__":
    inspect_demo_files()
