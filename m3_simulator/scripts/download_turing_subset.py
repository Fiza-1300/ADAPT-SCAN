"""
Download a subset of the Turing Synthetic Radar Dataset.
"""

import os
import argparse
import json
import numpy as np
from huggingface_hub import hf_hub_download, list_repo_files
from pathlib import Path


def download_subset(split='train', count=10, output_dir='data/turing_subset', seed=42):
    """
    Download a subset of the Turing dataset.
    """
    np.random.seed(seed)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f'{output_dir}/{split}', exist_ok=True)
    
    print(f"📥 Checking for files in {split} split...")
    
    try:
        # Try different methods to get files
        files = []
        
        # Method 1: Try listing repository files
        try:
            all_files = list_repo_files(
                repo_id="alan-turing-institute/turing-synthetic-radar-dataset",
                repo_type="dataset"
            )
            print(f"   Found {len(all_files)} total files in repository")
            
            # Filter by split
            split_files = [f for f in all_files if f.startswith(f'{split}/') and f.endswith('.h5')]
            files = split_files
            print(f"   Found {len(files)} files in {split} split")
            
        except Exception as e:
            print(f"   ⚠️ Could not list repository files: {e}")
            print("   Trying alternative methods...")
        
        # Method 2: Try common patterns
        if not files:
            # Try to download a sample file directly
            common_files = [
                f"{split}/sample_pulse_train.h5",
                f"{split}/pulse_train_001.h5",
                f"{split}/train_001.h5",
                f"{split}/1.h5"
            ]
            
            for f in common_files:
                try:
                    print(f"   Trying: {f}")
                    hf_hub_download(
                        repo_id="alan-turing-institute/turing-synthetic-radar-dataset",
                        filename=f,
                        repo_type="dataset",
                        local_dir=output_dir,
                        local_dir_use_symlinks=False
                    )
                    files.append(f)
                    print(f"   ✅ Found: {f}")
                except:
                    pass
        
        # If still no files, create demo data
        if not files:
            print("   ⚠️ No files found. Creating demo data instead...")
            create_demo_data(output_dir, split, count)
            return []
        
        # Select subset
        if len(files) > count:
            selected_files = np.random.choice(files, count, replace=False)
        else:
            selected_files = files
        
        print(f"   Downloading {len(selected_files)} files...")
        
        downloaded = []
        for i, file_path in enumerate(selected_files):
            try:
                print(f"   [{i+1}/{len(selected_files)}] Downloading {file_path}...")
                
                local_path = hf_hub_download(
                    repo_id="alan-turing-institute/turing-synthetic-radar-dataset",
                    filename=file_path,
                    repo_type="dataset",
                    local_dir=output_dir,
                    local_dir_use_symlinks=False
                )
                downloaded.append(local_path)
                print(f"      ✅ Downloaded")
                
            except Exception as e:
                print(f"      ❌ Error: {e}")
        
        print(f"\n✅ Downloaded {len(downloaded)} files to {output_dir}/")
        return downloaded
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n   The dataset might be gated or require authentication.")
        print("   Creating demo data instead...")
        create_demo_data(output_dir, split, count)
        return []


def create_demo_data(output_dir, split, count):
    """Create demo data when real dataset is not accessible."""
    print(f"\n🔧 Creating {count} demo files...")
    
    import h5py
    import numpy as np
    
    os.makedirs(f'{output_dir}/{split}', exist_ok=True)
    
    for i in range(min(count, 10)):
        file_path = f'{output_dir}/{split}/demo_train_{i+1:03d}.h5'
        
        with h5py.File(file_path, 'w') as f:
            # Create realistic PDW data
            num_pulses = np.random.randint(100, 500)
            
            # Create pulse data
            pulses = np.zeros((num_pulses, 5))
            pulses[:, 0] = np.cumsum(np.random.exponential(0.01, num_pulses))  # ToA
            pulses[:, 1] = np.random.uniform(8000, 12000, num_pulses)  # CF
            pulses[:, 2] = np.random.uniform(0.5, 2.0, num_pulses)  # PW
            pulses[:, 3] = np.random.uniform(0, 360, num_pulses)  # AoA
            pulses[:, 4] = np.random.uniform(0.1, 1.0, num_pulses)  # Amplitude
            
            f.create_dataset('pulses', data=pulses)
            
            # Create labels
            labels = np.random.randint(0, 5, num_pulses)
            f.create_dataset('labels', data=labels)
            
            # Create metadata
            metadata = {
                'num_pulses': num_pulses,
                'num_emitters': len(np.unique(labels)),
                'frequency_range': [8000, 12000],
                'pulse_width_range': [0.5, 2.0]
            }
            f.attrs['metadata'] = json.dumps(metadata)
        
        print(f"   ✅ Created: {file_path}")
    
    # Create metadata file
    metadata = {
        'split': split,
        'count': count,
        'files': [f'{split}/demo_train_{i+1:03d}.h5' for i in range(min(count, 10))],
        'is_demo': True,
        'description': 'Demo data generated when TSRD was not accessible'
    }
    
    with open(f'{output_dir}/{split}/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ Demo data created: {output_dir}/{split}/")


def main():
    parser = argparse.ArgumentParser(description='Download Turing dataset subset')
    parser.add_argument('--split', type=str, default='train',
                        choices=['train', 'validation', 'test'],
                        help='Dataset split')
    parser.add_argument('--count', type=int, default=10,
                        help='Number of files to download')
    parser.add_argument('--output_dir', type=str, default='data/turing_subset',
                        help='Output directory')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed')
    
    args = parser.parse_args()
    download_subset(
        split=args.split,
        count=args.count,
        output_dir=args.output_dir,
        seed=args.seed
    )


if __name__ == "__main__":
    main()
