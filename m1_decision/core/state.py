from dataclasses import dataclass, field
from typing import Dict, Optional

from .belief import BeliefState


@dataclass
class DecisionState:
    """
    Information available to M1 when making a decision.
    """

    belief: BeliefState

    remaining_budget: float

    current_region: Optional[str] = None

    time_step: int = 0

    observations: Dict[str, dict] = field(default_factory=dict)