class InformationGainPolicy:
    """
    Baseline policy that selects the region with the
    highest uncertainty.

    Higher uncertainty means a scan is expected to
    provide more useful information.

    This is a baseline for comparison with M1's
    full adaptive decision engine.
    """

    def select_region(self, belief_state, region_ids):
        """
        Select the region with the highest uncertainty.

        Parameters
        ----------
        belief_state:
            M1 BeliefState.

        region_ids:
            Available regions.

        Returns
        -------
        str
            Selected region ID.
        """

        if not region_ids:
            raise ValueError("region_ids cannot be empty.")

        best_region = None
        best_information_gain = -1.0

        for region_id in region_ids:
            probability = belief_state.get_probability(region_id)

            # Uncertainty is highest when belief is close to 0.5.
            uncertainty = 1.0 - abs(
                2.0 * probability - 1.0
            )

            if uncertainty > best_information_gain:
                best_information_gain = uncertainty
                best_region = region_id

        return best_region