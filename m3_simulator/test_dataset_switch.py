"""
Test switching between datasets during simulation.
"""

from simulator import Environment


def test_switching():
    print("=" * 70)
    print("TESTING DATASET SWITCHING")
    print("=" * 70)
    
    env = Environment(num_regions=20, seed=42)
    
    datasets = ['TSRD_Stare', 'TSRD_Scan', 'RadSeg']
    steps_per_dataset = 5
    
    for dataset in datasets:
        print(f"\n{'='*50}")
        print(f"📊 Switching to: {dataset}")
        print(f"{'='*50}")
        
        try:
            env.use_real_dataset(dataset, seed=42)
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
        
        # Run a few steps
        found = 0
        obs = env.get_observation_state()
        print(f"   Budget: {obs.get('budget_remaining', 100):.1f}")
        
        for step in range(steps_per_dataset):
            region = f'R{(step % 5) + 1}'
            try:
                obs, reward, done, info = env.step(region)
            except Exception as e:
                print(f"   ❌ Step {step+1} error: {e}")
                break
            
            # Check for detections
            for r in obs.get('regions', []):
                if r.get('detected', False) and r['region_id'] == region:
                    found += 1
                    print(f"   ✅ Found signal at {region}")
                    break
            
            print(f"   Step {step+1}: Budget={obs.get('budget_remaining', 0):.1f}")
        
        print(f"\n   Signals found in {dataset}: {found}")
    
    print("\n" + "=" * 70)
    print("✅ Dataset switching test complete!")
    print("=" * 70)


if __name__ == "__main__":
    test_switching()
