"""
Test downloading and using real TSRD data from Hugging Face.
"""

from huggingface_hub import hf_hub_download
import h5py
import os


def test_download():
    print("=" * 60)
    print("Testing Real TSRD Download from Hugging Face")
    print("=" * 60)
    
    try:
        # Try to download a sample file
        print("\n1. Downloading sample file...")
        file_path = hf_hub_download(
            repo_id="alan-turing-institute/turing-synthetic-radar-dataset",
            filename="sample_pulse_train.h5",
            repo_type="dataset"
        )
        print(f"   ✅ Downloaded to: {file_path}")
        
        # Check file size
        size = os.path.getsize(file_path)
        print(f"   File size: {size / 1024:.1f} KB")
        
        # Try to read the file
        print("\n2. Reading file contents...")
        with h5py.File(file_path, 'r') as f:
            print("   File structure:")
            for key in f.keys():
                print(f"   - {key}")
                # Check if it's a dataset
                if isinstance(f[key], h5py.Dataset):
                    print(f"     Shape: {f[key].shape}")
                    print(f"     Data type: {f[key].dtype}")
        
        print("\n✅ Real TSRD data is accessible!")
        print("   You can now use this in your simulator")
        
    except Exception as e:
        print(f"❌ Error downloading: {e}")
        print("\n   Note: The dataset might require special access.")
        print("   Your synthetic realistic data will work instead.")


if __name__ == "__main__":
    test_download()
