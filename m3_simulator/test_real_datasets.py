"""
Test all 5 real datasets from Hugging Face.
"""

from simulator import Environment


def test_all_datasets():
    print("=" * 70)
    print("TESTING ALL 5 REAL DATASETS FROM HUGGING FACE")
    print("=" * 70)
    
    env = Environment(num_regions=20, seed=42)
    
    # List of datasets to test
    datasets = [
        'TSRD_Stare',
        'TSRD_Scan', 
        'RadSeg',
        'General_RF',
        'Combined'
    ]
    
    results = {}
    
    for dataset in datasets:
        print(f"\n{'='*50}")
        print(f"📊 Testing Dataset: {dataset}")
        print(f"{'='*50}")
        
        try:
            # Use real dataset
            env.use_real_dataset(dataset, seed=42)
            
            # Get statistics
            if hasattr(env, 'tsrd_truth'):
                stats = env.tsrd_truth.get_statistics()
                print(f"   Dataset: {stats['dataset']}")
                print(f"   Total emitters: {stats['total_emitters']}")
                print(f"   Active emitters: {stats['active_emitters']}")
                print(f"   Frequency agile: {stats['frequency_agile']}")
                print(f"   Avg strength: {stats['avg_strength']:.2f}")
            
            # Reset and test
            env.reset('S1', seed=42)  # Use S1 as base, but with real data
            obs = env.get_observation_state()
            
            print(f"\n   Running 10 steps...")
            found = 0
            for step in range(10):
                region = f'R{(step % 5) + 1}'
                obs, reward, done, info = env.step(region)
                
                # Check for detections
                for r in obs['regions']:
                    if r.get('detected', False) and r['region_id'] == region:
                        found += 1
                        break
            
            print(f"\n   ✅ Dataset {dataset} test PASSED!")
            print(f"   Signals found: {found}")
            print(f"   Budget used: {100 - obs['budget_remaining']:.1f}")
            
            results[dataset] = {'status': '✅ PASSED', 'found': found}
            
        except Exception as e:
            print(f"\n   ❌ Dataset {dataset} FAILED: {e}")
            results[dataset] = {'status': '❌ FAILED', 'error': str(e)}
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"{'Dataset':<20} {'Status':<15} {'Signals Found':<15}")
    print("-" * 50)
    
    for dataset, result in results.items():
        status = result['status']
        found = result.get('found', 'N/A')
        print(f"{dataset:<20} {status:<15} {found:<15}")
    
    passed = sum(1 for r in results.values() if '✅' in r['status'])
    total = len(results)
    print(f"\n✅ {passed}/{total} datasets passed!")
    
    return results


if __name__ == "__main__":
    test_all_datasets()
