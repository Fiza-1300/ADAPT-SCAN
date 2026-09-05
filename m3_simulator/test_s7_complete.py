"""Test S7 with enough steps to trigger surprise."""
from simulator import Environment

print("Testing S7 - Sudden Important Emitter")
print("=" * 50)

env = Environment(num_regions=20, seed=42)
obs = env.reset('S7', seed=42)

print(f"Initial state:")
print(f"  - Budget: {obs['budget_remaining']}")
print(f"  - Regions with signals: {sum(1 for r in obs['regions'] if r.get('detected', False))}")

# Run 15 steps to trigger surprise at step 10
for step in range(15):
    region = f'R{(step % 10) + 1}'
    obs, reward, done, info = env.step(region)
    
    if step == 10:
        print(f"\n⏰ After surprise at step {step}:")
        # Check if R15 has a signal
        r15 = next((r for r in obs['regions'] if r['region_id'] == 'R15'), None)
        if r15 and r15.get('detected', False):
            print(f"  ✅ R15 DETECTED!")
            print(f"  - Strength: {r15.get('strength', 0):.2f}")
            print(f"  - Confidence: {r15.get('confidence', 0):.2f}")
        else:
            print(f"  ⚠️ R15 not detected yet")

print(f"\nFinal state:")
print(f"  - Steps: {obs['timestep']}")
print(f"  - Budget: {obs['budget_remaining']}")
print(f"  - Total detections: {sum(1 for r in obs['regions'] if r.get('detected', False))}")
print("\n✅ S7 test complete!")
