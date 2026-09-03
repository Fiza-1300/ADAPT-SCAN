from baselines.threat_priority import ThreatPriorityPolicy
from core.belief import BeliefState


def test_threat_priority_selects_highest_probability():
    regions = ["R1", "R2", "R3", "R4"]

    belief = BeliefState()

    belief.update_probability("R1", 0.20)
    belief.update_probability("R2", 0.75)
    belief.update_probability("R3", 0.40)
    belief.update_probability("R4", 0.90)

    policy = ThreatPriorityPolicy()

    action = policy.select_action(regions, belief)

    assert action.region_id == "R4"


def test_threat_priority_works_with_first_region_as_highest():
    regions = ["R1", "R2", "R3"]

    belief = BeliefState()

    belief.update_probability("R1", 0.95)
    belief.update_probability("R2", 0.30)
    belief.update_probability("R3", 0.60)

    policy = ThreatPriorityPolicy()

    action = policy.select_action(regions, belief)

    assert action.region_id == "R1"


def test_threat_priority_rejects_empty_regions():
    belief = BeliefState()

    policy = ThreatPriorityPolicy()

    try:
        policy.select_action([], belief)
        assert False
    except ValueError:
        assert True