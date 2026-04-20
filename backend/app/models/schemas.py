"""
Pydantic schemas for Interactome-AI.

These define the exact shape of all request/response data.
Every API endpoint uses these to validate inputs and format outputs.
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ── Risk Levels ──────────────────────────────────────────────
class RiskLevel(str, Enum):
    """Three-tier risk classification used throughout the system."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# ── Drug Models ──────────────────────────────────────────────
class DrugSearchResult(BaseModel):
    """Single drug returned from PubChem autocomplete search."""
    cid: int  # PubChem Compound ID — unique identifier
    name: str  # Human-readable drug name
    formula: Optional[str] = None  # Chemical formula, e.g. "C9H8O4"
    molecular_weight: Optional[float] = None
    smiles: Optional[str] = None  # SMILES encoding of molecular structure


class DrugDetail(BaseModel):
    """Full drug information including molecular data and known interactions."""
    cid: int
    name: str
    formula: Optional[str] = None
    molecular_weight: Optional[float] = None
    smiles: Optional[str] = None
    description: Optional[str] = None
    known_interactions: list[str] = []  # Drugs this interacts with
    known_side_effects: list[str] = []  # Reported side effects


# ── Patient Profile (Optional) ───────────────────────────────
class PatientProfile(BaseModel):
    """Optional patient info for personalized risk scoring."""
    age: Optional[int] = Field(None, ge=0, le=120, description="Patient age")
    bmi: Optional[float] = Field(None, ge=10, le=60, description="BMI")
    conditions: list[str] = Field(
        default_factory=list,
        description="Existing conditions: diabetes, hypertension, etc."
    )


# ── Prediction Request / Response ─────────────────────────────
class PredictionRequest(BaseModel):
    """
    What the patient sends:
    - A list of drug names they're currently taking
    - Optionally, their profile for personalized analysis
    """
    drugs: list[str] = Field(
        ...,
        min_length=2,
        description="List of drug names (minimum 2)"
    )
    patient_profile: Optional[PatientProfile] = None


class SideEffectPrediction(BaseModel):
    """One predicted side effect with full explanation."""
    name: str  # e.g. "Liver toxicity"
    risk: RiskLevel
    confidence: float = Field(ge=0, le=1)  # 0.0 to 1.0
    affected_organ: str  # liver, kidney, skin, cardiovascular, etc.
    contributing_drugs: list[str]  # Which drugs cause this
    explanation: str  # WHY it happens — enzyme pathways, etc.


class PairwiseInteraction(BaseModel):
    """Interaction between exactly 2 drugs."""
    drug_a: str
    drug_b: str
    risk: RiskLevel
    side_effects: list[str]
    mechanism: str  # e.g., "Both compete for CYP3A4"


class HigherOrderInteraction(BaseModel):
    """Interaction among 3+ drugs — the KEY innovation."""
    drugs: list[str]  # e.g., ["Aspirin", "Warfarin", "Ibuprofen"]
    risk: RiskLevel
    side_effects: list[str]
    mechanism: str  # e.g., "Triple anticoagulant overlap"
    confidence: float = Field(ge=0, le=1)


class MedicationTiming(BaseModel):
    """Suggested gap between specific drugs."""
    drug: str
    suggested_time: str  # e.g., "Morning with food"
    gap_hours: Optional[int] = None  # Hours gap from other drugs
    notes: str = ""


class GraphNode(BaseModel):
    """A node in the interaction graph (a drug)."""
    id: str
    label: str
    risk_contribution: RiskLevel = RiskLevel.LOW
    node_type: str = "drug"  # "drug" or "side_effect"


class GraphEdge(BaseModel):
    """An edge in the interaction graph (an interaction)."""
    source: str
    target: str
    risk: RiskLevel
    side_effects: list[str] = []
    weight: float = 1.0


class InteractionGraph(BaseModel):
    """Complete graph for Cytoscape.js visualization."""
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class PredictionResponse(BaseModel):
    """
    The FULL output returned to the patient:
    - Overall risk level
    - All predicted side effects with explanations
    - Pairwise and higher-order interactions
    - Interactive graph data
    - Medication timing recommendations
    """
    overall_risk: RiskLevel
    risk_score: float = Field(ge=0, le=1, description="0-1 overall risk score")
    total_interactions_analyzed: int
    side_effects: list[SideEffectPrediction]
    pairwise_interactions: list[PairwiseInteraction]
    higher_order_interactions: list[HigherOrderInteraction]
    medication_timing: list[MedicationTiming]
    interaction_graph: InteractionGraph
    summary: str  # Human-readable summary paragraph
