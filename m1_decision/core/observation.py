class Observation:
    """
    Represents the processed observation received by M1.

    M2 provides this information after signal processing.
    Ground truth is intentionally NOT included.
    """

    def __init__(
        self,
        region_id,
        detected,
        strength=None,
        bandwidth=None,
        snr=None,
        confidence=None,
        features=None,
        timestamp=None
    ):
        self.region_id = region_id
        self.detected = detected
        self.strength = strength
        self.bandwidth = bandwidth
        self.snr = snr
        self.confidence = confidence
        self.features = features if features is not None else []
        self.timestamp = timestamp