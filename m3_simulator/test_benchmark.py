"""Test the benchmark runner."""

from simulator import Environment
from simulator.benchmark import BenchmarkRunner


def random_strategy(obs):
    """Simple random strategy for testing."""
    import random
    regions = obs['regions']
    return random.choice(regions)['region_id']


def greedy_strategy(obs):
    """Greedy: scan most uncertain region."""
    regions = obs['regions']
    uncertain = sorted(regions, key=lambda x: x.get('uncertainty', 0), reverse=True)
    return uncertain[0]['region_id'] if uncertain else 'R1'


# Test benchmark
print("Testing Benchmark Runner...")
print("=" * 50)

runner = BenchmarkRunner(num_regions=20, seed=42)

# Run with random strategy
print("\n1. Testing Random Strategy...")
results = runner.run_all_scenarios(random_strategy, num_seeds=3)
runner.print_summary()

# Run with greedy strategy
print("\n2. Testing Greedy Strategy...")
runner = BenchmarkRunner(num_regions=20, seed=42)  # Reset
results_greedy = runner.run_all_scenarios(greedy_strategy, num_seeds=3)

# Compare
print("\n" + "=" * 50)
print("COMPARISON: Random vs Greedy")
print("=" * 50)

for i in range(len(results)):
    scenario = results[i]['scenario']
    random_rate = results[i]['avg_detection_rate']
    greedy_rate = results_greedy[i]['avg_detection_rate']
    improvement = (greedy_rate - random_rate) / max(0.01, random_rate) * 100
    
    print(f"\n{scenario}:")
    print(f"  Random: {random_rate:.3f}")
    print(f"  Greedy: {greedy_rate:.3f}")
    print(f"  Improvement: {improvement:.1f}%")

print("\n🎉 Benchmark complete!")
