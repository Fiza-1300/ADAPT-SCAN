from core.observation import Observation
from intelligence.belief_updater import BeliefUpdater
from core.belief import BeliefState

def test_detected_observation_increases_belief():
    updater = BeliefUpdater()

    observation = Observation(
        region_id="R1",
        detected=True,
        confidence=1.0,
    )

    old_probability = 0.20

    new_probability = updater.update(
        observation,
        old_probability,
    )

    assert new_probability > old_probability


def test_not_detected_observation_keeps_probability_valid():
    updater = BeliefUpdater()

    observation = Observation(
        region_id="R1",
        detected=False,
        confidence=1.0,
    )

    new_probability = updater.update(
        observation,
        0.80,
    )

    assert 0.0 <= new_probability <= 1.0


def test_confidence_is_used():
    updater = BeliefUpdater()

    high_confidence = Observation(
        region_id="R1",
        detected=True,
        confidence=1.0,
    )

    low_confidence = Observation(
        region_id="R1",
        detected=True,
        confidence=0.1,
    )

    high_result = updater.update(
        high_confidence,
        0.20,
    )

    low_result = updater.update(
        low_confidence,
        0.20,
    )

    assert high_result > low_result


def test_probability_is_clamped():
    updater = BeliefUpdater()

    observation = Observation(
        region_id="R1",
        detected=True,
        confidence=2.0,
    )

    result = updater.update(
        observation,
        5.0,
    )

    assert 0.0 <= result <= 1.0


def test_missing_confidence_is_handled():
    updater = BeliefUpdater()

    observation = Observation(
        region_id="R1",
        detected=True,
        confidence=None,
    )

    result = updater.update(
        observation,
        0.20,
    )

    assert 0.0 <= result <= 1.0

def test_update_belief_state():
    updater = BeliefUpdater()
    belief = BeliefState()

    observation = Observation(
        region_id="R1",
        detected=True,
        confidence=1.0,
    )

    new_probability = updater.update_belief_state(
        observation,
        belief,
    )

    assert belief.get_probability("R1") == new_probability
    assert 0.0 <= new_probability <= 1.0