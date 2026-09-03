from core.observation import Observation
from m1_controller import M1Controller


def test_controller_processes_observation():
    controller = M1Controller()

    observation = Observation(
        region_id="R1",
        detected=True,
        confidence=1.0,
    )

    probability = controller.process_observation(
        observation
    )

    assert probability > 0.0
    assert controller.belief_state.get_probability("R1") == probability


def test_controller_selects_next_scan():
    controller = M1Controller()

    observation = Observation(
        region_id="R1",
        detected=True,
        confidence=1.0,
    )

    controller.process_observation(observation)

    decision = controller.choose_next_scan(
        region_ids=["R1", "R2", "R3"],
        remaining_budget=10.0,
        time_step=1,
    )

    assert decision.action.region_id in ["R1", "R2", "R3"]
    assert decision.utility > 0.0


def test_controller_handles_multiple_observations():
    controller = M1Controller()

    observation1 = Observation(
        region_id="R1",
        detected=True,
        confidence=1.0,
    )

    observation2 = Observation(
        region_id="R2",
        detected=False,
        confidence=1.0,
    )

    controller.process_observation(observation1)
    controller.process_observation(observation2)

    assert controller.belief_state.get_probability("R1") > 0.0
    assert controller.belief_state.get_probability("R2") >= 0.0