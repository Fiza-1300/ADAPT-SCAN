from baselines.information_gain import InformationGainPolicy
from core.belief import BeliefState


def test_information_gain_selects_most_uncertain_region():
    belief = BeliefState()

    belief.update_probability("R1", 0.10)
    belief.update_probability("R2", 0.50)
    belief.update_probability("R3", 0.90)

    policy = InformationGainPolicy()

    selected = policy.select_region(
        belief,
        ["R1", "R2", "R3"],
    )

    assert selected == "R2"


def test_information_gain_rejects_empty_regions():
    belief = BeliefState()
    policy = InformationGainPolicy()

    try:
        policy.select_region(belief, [])
        assert False
    except ValueError:
        assert True