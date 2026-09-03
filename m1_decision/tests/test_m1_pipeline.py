from core.belief import BeliefState
from core.observation import Observation
from core.state import DecisionState
from intelligence.belief_updater import BeliefUpdater
from decision_engine import DecisionEngine


def test_m1_observation_to_decision_pipeline():
    # Start with an empty belief state.
    belief = BeliefState()

    # Simulate a processed observation that M2
    # will eventually provide to M1.
    observation = Observation(
        region_id="R2",
        detected=True,
        strength=0.80,
        bandwidth=0.40,
        snr=7.2,
        confidence=1.0,
        features=["strong_signal"],
        timestamp=1,
    )

    # Convert the observation into M1's belief.
    updater = BeliefUpdater()

    updated_probability = updater.update_belief_state(
        observation,
        belief,
    )

    # Verify that the belief was actually updated.
    assert belief.get_probability("R2") == updated_probability
    assert updated_probability > 0.0

    # Give M1 some candidate regions.
    belief.update_probability("R1", 0.20)
    belief.update_probability("R3", 0.30)

    # Create the decision state.
    state = DecisionState(
        belief=belief,
        remaining_budget=10.0,
        time_step=1,
        observations={
            "R2": {"last_observed": 1},
        },
    )

    # Ask M1 which region should be scanned next.
    engine = DecisionEngine()

    decision = engine.select_next_scan(
        state,
        ["R1", "R2", "R3"],
    )

    # The decision engine should return a valid region.
    assert decision.action.region_id in ["R1", "R2", "R3"]

    # The selected decision should have positive utility.
    assert decision.utility > 0.0