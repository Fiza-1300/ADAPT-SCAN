from dataclasses import dataclass
from typing import Optional

from .action import ScanAction


@dataclass
class Decision:
    """
    Final decision produced by M1.
    """

    action: ScanAction

    utility: float

    information_gain: float = 0.0

    threat_score: float = 0.0

    uncertainty: float = 0.0

    tracking_value: float = 0.0

    scan_cost: float = 0.0

    reason: Optional[str] = None