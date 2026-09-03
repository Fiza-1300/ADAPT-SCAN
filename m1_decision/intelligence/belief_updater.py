class BeliefUpdater:
    """
    Converts an M1 Observation into an updated belief probability.

    M1 only uses the processed observation provided to it.
    Ground truth is never accessed.
    """

    def __init__(
        self,
        detected_probability=0.70,
        not_detected_probability=0.20,
        confidence_weight=0.30,
    ):
        self.detected_probability = detected_probability
        self.not_detected_probability = not_detected_probability
        self.confidence_weight = confidence_weight

    def update(self, observation, current_probability=0.0):
        """
        Update the belief probability for one region.

        Parameters
        ----------
        observation:
            M1 Observation object.

        current_probability:
            Previous belief probability for the region.

        Returns
        -------
        float
            Updated probability in the range [0, 1].
        """

        current_probability = self._clamp(current_probability)

        confidence = self._clamp(
            observation.confidence
            if observation.confidence is not None
            else 0.5
        )

        if observation.detected:
            evidence = self.detected_probability
        else:
            evidence = self.not_detected_probability

        # Confidence determines how strongly the new observation
        # influences the previous belief.
        updated_probability = (
            (1.0 - self.confidence_weight) * current_probability
            + self.confidence_weight * evidence * confidence
        )

        return self._clamp(updated_probability)
    def update_belief_state(self, observation, belief_state):
        """
        Update the M1 BeliefState using a processed observation.

        Returns the updated probability.
        """

        current_probability = belief_state.get_probability(
            observation.region_id
        )

        new_probability = self.update(
            observation,
            current_probability,
        )

        belief_state.update_probability(
            observation.region_id,
            new_probability,
        )

        return new_probability

    
    @staticmethod
    def _clamp(value):
        """Keep probability inside [0, 1]."""

        if value is None:
            return 0.0

        return max(0.0, min(1.0, float(value)))