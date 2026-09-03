from core.action import ScanAction
from core.belief import BeliefState
from core.decision import Decision


def test_scan_action():
    action = ScanAction("R7")

    assert action.region_id == "R7"


def test_belief_state():
    belief = BeliefState()

    belief.update_probability("R7", 0.72)

    assert belief.get_probability("R7") == 0.72


def test_decision():
    action = ScanAction("R7")

    decision = Decision(
        action=action,
        utility=0.85,
        information_gain=0.72,
        threat_score=0.80,
        uncertainty=0.65,
        tracking_value=0.60,
        scan_cost=0.10,
        reason="High expected information gain."
    )

    assert decision.action.region_id == "R7"
    assert decision.utility == 0.85