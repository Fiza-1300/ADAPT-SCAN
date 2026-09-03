from dataclasses import dataclass, field
from typing import Dict


@dataclass
class BeliefState:
    """
    M1's current belief about the probability/relevance
    of each region.

    These values are NOT ground truth.
    """

    region_probabilities: Dict[str, float] = field(default_factory=dict)

    def get_probability(self, region_id: str) -> float:
        """
        Return the current belief for a region.

        If we have never seen the region before,
        return 0.0 for now.
        """
        return self.region_probabilities.get(region_id, 0.0)

    def update_probability(self, region_id: str, probability: float) -> None:
        """
        Update M1's belief about a region.
        """

        if not 0.0 <= probability <= 1.0:
            raise ValueError("Probability must be between 0 and 1.")

        self.region_probabilities[region_id] = probability