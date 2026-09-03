from dataclasses import dataclass


@dataclass(frozen=True)
class ScanAction:
    """
    Represents the decision to scan one region.
    """

    region_id: str