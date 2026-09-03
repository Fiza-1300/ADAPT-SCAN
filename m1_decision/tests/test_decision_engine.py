import pytest

from core.belief import BeliefState
from core.state import DecisionState
from decision_engine import DecisionEngine


def create_state():
    belief = BeliefState()

    belief.update_probability("R1", 0.20)
    belief.update_probability("R2", 0.80)
    belief.update_probability("R3", 0.50)

    return DecisionState(
        belief=belief,
        remaining_budget=10.0,
        time_step=4,
        observations={
            "R1": {"last_observed": 3},
            "R2": {"last_observed": 1},
            "R3": {"last_observed": 4},
        },
    )


def test_information_gain():
    engine = DecisionEngine()

    assert engine.calculate_information_gain(0.8) == 0.8


def test_information_gain_is_clamped():
    engine = DecisionEngine()

    assert engine.calculate_information_gain(2.0) == 1.0
    assert engine.calculate_information_gain(-1.0) == 0.0


def test_tracking_value_for_never_observed_region():
    engine = DecisionEngine()

    value = engine.calculate_tracking_value(
        last_observed=None,
        current_timestep=4,
    )

    assert value == 1.0


def test_tracking_value_decreases_with_age():
    engine = DecisionEngine()

    recent = engine.calculate_tracking_value(4, 4)
    old = engine.calculate_tracking_value(1, 4)

    assert recent > old


def test_select_next_scan():
    engine = DecisionEngine()

    state = create_state()

    decision = engine.select_next_scan(
        state,
        ["R1", "R2", "R3"],
    )

    assert decision.action.region_id == "R2"
    assert decision.utility > 0


def test_empty_region_list():
    engine = DecisionEngine()

    state = create_state()

    with pytest.raises(ValueError):
        engine.select_next_scan(state, [])


def test_zero_budget():
    engine = DecisionEngine()

    state = create_state()
    state.remaining_budget = 0

    with pytest.raises(ValueError):
        engine.select_next_scan(state, ["R1", "R2"])