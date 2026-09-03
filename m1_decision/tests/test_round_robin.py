from baselines.round_robin import RoundRobinPolicy


def test_round_robin_scans_in_order():
    regions = ["R1", "R2", "R3"]

    policy = RoundRobinPolicy()

    action1 = policy.select_action(regions)
    action2 = policy.select_action(regions)
    action3 = policy.select_action(regions)

    assert action1.region_id == "R1"
    assert action2.region_id == "R2"
    assert action3.region_id == "R3"


def test_round_robin_wraps_around():
    regions = ["R1", "R2", "R3"]

    policy = RoundRobinPolicy()

    policy.select_action(regions)
    policy.select_action(regions)
    policy.select_action(regions)

    action4 = policy.select_action(regions)

    assert action4.region_id == "R1"


def test_round_robin_rejects_empty_regions():
    policy = RoundRobinPolicy()

    try:
        policy.select_action([])
        assert False
    except ValueError:
        assert True