from core.observation import Observation


def test_observation_creation():
    observation = Observation(
        region_id="R7",
        detected=True,
        strength=0.63,
        bandwidth=0.41,
        snr=7.2,
        confidence=0.72,
        features=[]
    )

    assert observation.region_id == "R7"
    assert observation.detected is True
    assert observation.strength == 0.63
    assert observation.snr == 7.2
    assert observation.confidence == 0.72


def test_observation_can_have_missing_measurements():
    observation = Observation(
        region_id="R3",
        detected=False
    )

    assert observation.region_id == "R3"
    assert observation.detected is False
    assert observation.snr is None