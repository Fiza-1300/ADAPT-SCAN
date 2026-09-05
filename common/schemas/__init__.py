from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List, Any


class RegionState(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    region_id: str = Field(alias="id")
    existence: float
    uncertainty: float
    threat_relevance: float = Field(alias="threatLevel")
    last_observed: Optional[int] = Field(default=None, alias="lastScanned")
    status: str
    detected: Optional[bool] = None
    strength: Optional[float] = None
    bandwidth: Optional[float] = None
    snr: Optional[float] = None
    confidence: Optional[float] = None
    freqMHz: Optional[int] = None
    bwMHz: Optional[int] = None
    signalStrength: Optional[float] = None
    signalType: Optional[str] = None
    active: Optional[bool] = None
    priority: Optional[float] = None
    beliefProb: Optional[float] = None


class ScanDelta(BaseModel):
    region_id: str
    belief_before: float
    belief_after: float
    unc_before: float
    unc_after: float
    status_before: str
    status_after: str
    detected: bool


class ScanRecord(BaseModel):
    step: int
    region_id: str
    info_gain: float
    threat_value: float
    uncertainty: float
    tracking_urgency: float
    scan_cost: float
    detected_signal: bool
    explanation: str
    strategy: str


class DecisionResponse(BaseModel):
    region_id: str
    utility: float
    information_gain: float
    threat_score: float
    uncertainty: float
    tracking_value: float
    scan_cost: float
    reason: str


class CandidateRank(BaseModel):
    id: str
    utility: float
    info_gain: float
    threat_score: float
    tracking_value: float
    scan_cost: float


class ObservationState(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    regions: List[RegionState]
    timestep: int
    budget_remaining: float
    budget_total: float
    budget_remaining_frac: float
    current_scan: Optional[str]
    scenario: str
    intelligence: Dict[str, int]


class SimulationResetRequest(BaseModel):
    scenario: str
    seed: Optional[int] = None
    strategy: str = "ADAPT_SCAN"
    num_regions: int = 20


class SimulationStepRequest(BaseModel):
    session_id: str
    override_region_id: Optional[str] = None


class EventRequest(BaseModel):
    session_id: str
    event_type: str
