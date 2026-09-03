from baselines.random_policy import RandomPolicy


def test_random_policy_returns_valid_region():
    regions = ["R1", "R2", "R3", "R4", "R5"]

    policy = RandomPolicy(seed=42)

    action = policy.select_action(regions)

    assert action.region_id in regions


def test_random_policy_is_reproducible():
    regions = ["R1", "R2", "R3", "R4", "R5"]

    policy1 = RandomPolicy(seed=42)
    policy2 = RandomPolicy(seed=42)

    action1 = policy1.select_action(regions)
    action2 = policy2.select_action(regions)

    assert action1.region_id == action2.region_id


def test_random_policy_rejects_empty_regions():
    policy = RandomPolicy(seed=42)

    try:
        policy.select_action([])
        assert False
    except ValueError:
        assert True