"""
Test the TSRD adapter with your simulator.
"""

from simulator import Environment
from simulator.tsrd_adapter import TSRDAdapter


def test_tsrd_adapter():
    print("=" * 60)
    print("Testing TSRD Adapter with Simulator")
    print("=" * 60)
    
    print("\n1. Creating TSRD Adapter...")
    adapter = TSRDAdapter(seed=42)
    adapter._create_realistic_synthetic_data()
    
    print("\n2. Emitters created:")
    for em_id, em in adapter.emitters.items():
        agile = "🔄 Agile" if em.get('frequency_agile', False) else "📍 Fixed"
        print(f"   {em_id}: {em['region_id']} - Threat: {em['threat_relevance']:.2f} - {agile}")
    
    print("\n3. Testing adapter methods:")
    hidden = adapter.get_hidden_state()
    print(f"   Hidden state has {len(hidden)} regions")
    
    r7 = adapter.get_region_truth('R7')
    print(f"   R7 exists: {r7.get('exists', False)}")
    print(f"   R7 strength: {r7.get('strength', 0):.2f}")
    
    print("\n4. Testing with Environment...")
    env = Environment(num_regions=20, seed=42)
    
    # Use TSRD data
    env.using_tsrd = True
    env.tsrd_adapter = adapter
    
    # Reset and run a few steps
    obs = env.reset('S9', seed=42)
    print(f"   Reset: Budget={obs['budget_remaining']}")
    
    # Scan different regions
    found = 0
    for step in range(10):
        region = f'R{(step % 10) + 1}'
        obs, reward, done, info = env.step(region)
        
        # Check if we found something
        for r in obs['regions']:
            if r.get('detected', False) and r['region_id'] == region:
                found += 1
                print(f"   ✅ Found signal at {region} (step {step+1})")
                break
    
    print(f"\n5. Results:")
    print(f"   Signals found: {found}")
    print(f"   Budget used: {100 - obs['budget_remaining']:.1f}")
    print(f"   Steps completed: {obs['timestep']}")
    
    print("\n" + "=" * 60)
    print("✅ TSRD Integration Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_tsrd_adapter()
