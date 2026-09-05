"""Add this to your environment.py file to support TSRD."""

# At the top of environment.py, add:
try:
    from .tsrd_adapter import TSRDAdapter
except ImportError:
    print("TSRD Adapter not available, using synthetic data only")
    TSRDAdapter = None

# Add this method to your Environment class:
def use_tsrd_data(self, use_real_data: bool = True, seed: int = 42):
    """Switch to using TSRD dataset."""
    if TSRDAdapter is not None:
        self.tsrd_adapter = TSRDAdapter(seed=seed)
        if use_real_data:
            try:
                self.tsrd_adapter.load_sample_data()
            except:
                print("Using synthetic realistic data instead")
                self.tsrd_adapter._create_realistic_synthetic_data()
        else:
            self.tsrd_adapter._create_realistic_synthetic_data()
        self.using_tsrd = True
        print("✅ Switched to TSRD data source")
    else:
        print("⚠️ TSRD not available, using default data")
        self.using_tsrd = False
