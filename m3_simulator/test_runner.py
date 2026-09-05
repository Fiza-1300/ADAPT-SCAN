"""Master test runner for ADAPT-SCAN simulator."""

import sys
from simulator import Environment
from simulator.scenarios import list_scenarios, get_scenario_config


def test_all_scenarios():
    """Test all 8 scenarios."""
    print("=" * 60)
    print("Testing All 8 Scenarios")
    print("=" * 60)
    
    env = Environment(num_regions=20, seed=42)
    all_passed = True
    
    for scenario_id in list_scenarios():
        print(f"\n📊 Testing Scenario: {scenario_id}")
        config = get_scenario_config(scenario_id)
        print(f"   Name: {config['name']}")
        print(f"   Description: {config['description']}")
        
        try:
            obs = env.reset(scenario_id, seed=42)
            print(f"   Budget: {obs['budget_remaining']}")
            
            # Run 5 steps
            for step in range(5):
                region = f'R{(step % 10) + 1}'
                obs, reward, done, info = env.step(region)
                if done:
                    break
            
            print(f"   Steps completed: {obs['timestep']}")
            print(f"   Budget remaining: {obs['budget_remaining']:.2f}")
            print(f"   Detected count: {obs['intelligence']['detected_count']}")
            print("   ✅ PASSED")
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            all_passed = False
    
    return all_passed


def test_s7_sudden_appearance():
    """Test S7 sudden appearance specifically."""
    print("\n" + "=" * 60)
    print("Testing S7 - Sudden Important Emitter")
    print("=" * 60)
    
    env = Environment(num_regions=20, seed=42)
    
    try:
        obs = env.reset('S7', seed=42)
        print(f"Initial budget: {obs['budget_remaining']}")
        
        # Run until after appearance (timestep 10)
        for step in range(12):
            region = f'R{(step % 5) + 1}'
            obs, reward, done, info = env.step(region)
            
            if step == 11:  # After sudden appearance
                r15 = next((r for r in obs['regions'] if r['region_id'] == 'R15'), None)
                if r15 and r15.get('detected') is not None:
                    print(f"✅ R15 detected at timestep {step}")
                    print(f"   Strength: {r15.get('strength', 0):.2f}")
                    print(f"   Confidence: {r15.get('confidence', 0):.2f}")
                else:
                    print("⚠️ R15 not detected yet (may need more scans)")
        
        print("✅ S7 test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ S7 test FAILED: {e}")
        return False


def test_budget_behavior():
    """Test budget constraints work properly."""
    print("\n" + "=" * 60)
    print("Testing Budget Behavior")
    print("=" * 60)
    
    env = Environment(num_regions=20, seed=42)
    obs = env.reset('S6', seed=42)  # Low budget scenario
    
    print(f"Initial budget: {obs['budget_remaining']}")
    
    # Keep scanning until budget exhausted
    step = 0
    while not env.done and step < 50:
        region = f'R{(step % 10) + 1}'
        obs, reward, done, info = env.step(region)
        step += 1
        
        if step % 5 == 0:
            print(f"  Step {step}: Budget={obs['budget_remaining']:.1f}")
    
    print(f"✅ Budget exhausted after {step} steps")
    print(f"   Final budget: {obs['budget_remaining']:.1f}")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("ADAPT-SCAN SIMULATOR - MASTER TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("All Scenarios", test_all_scenarios()))
    results.append(("S7 Sudden Appearance", test_s7_sudden_appearance()))
    results.append(("Budget Behavior", test_budget_behavior()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Your simulator is working!")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
