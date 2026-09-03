from core.belief import BeliefState
from core.state import DecisionState
from intelligence.belief_updater import BeliefUpdater
from decision_engine import DecisionEngine


class M1Controller:
    """
    Public interface for the M1 Decision Intelligence module.

    M1Controller hides the internal M1 components from the
    rest of the system.

    Flow:
        Observation
            ↓
        BeliefUpdater
            ↓
        BeliefState
            ↓
        DecisionEngine
            ↓
        Decision
    """

    def __init__(self):
        self.belief_state = BeliefState()
        self.belief_updater = BeliefUpdater()
        self.decision_engine = DecisionEngine()

    def process_observation(self, observation):
        """
        Update M1's belief using a processed observation.

        Parameters
        ----------
        observation:
            Observation received from the signal-processing layer.

        Returns
        -------
        float
            Updated belief probability.
        """

        return self.belief_updater.update_belief_state(
            observation,
            self.belief_state,
        )

    def choose_next_scan(
        self,
        region_ids,
        remaining_budget,
        time_step,
        observations=None,
    ):
        """
        Select the next region to scan.

        Parameters
        ----------
        region_ids:
            Regions currently available for scanning.

        remaining_budget:
            Remaining scan budget.

        time_step:
            Current simulation time-step.

        observations:
            Previously observed-region information.

        Returns
        -------
        Decision
            M1's selected decision.
        """

        state = DecisionState(
            belief=self.belief_state,
            remaining_budget=remaining_budget,
            time_step=time_step,
            observations=observations or {},
        )

        return self.decision_engine.select_next_scan(
            state,
            region_ids,
        )