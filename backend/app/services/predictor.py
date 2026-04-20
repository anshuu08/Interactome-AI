"""
Core Prediction Orchestrator for Interactome-AI.

This is the main intelligence layer. When a patient submits their medication list:
1. Each drug is looked up in the knowledge base (drug_interactions.json)
2. All pairwise combinations are checked for known interactions
3. Higher-order (3+ drug) combinations are analyzed
4. CYP enzyme pathway conflicts are identified
5. Risk levels are calculated
6. Explanations are generated for each interaction
7. Medication timing recommendations are provided
8. The interaction graph structure is built for Cytoscape.js

The knowledge base is pre-processed from real datasets (Decagon/TWOSIDES, FAERS).
"""
import json
import os
from typing import Optional
from itertools import combinations
from app.models.schemas import (
    RiskLevel,
    PredictionResponse,
    SideEffectPrediction,
    PairwiseInteraction,
    HigherOrderInteraction,
    MedicationTiming,
    InteractionGraph,
    GraphNode,
    GraphEdge,
    PatientProfile,
)

# Load the knowledge base on module import
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
KB_PATH = os.path.join(DATA_DIR, "drug_interactions.json")

_knowledge_base = None


def _load_kb() -> dict:
    """Load the drug interaction knowledge base."""
    global _knowledge_base
    if _knowledge_base is None:
        with open(KB_PATH, "r") as f:
            _knowledge_base = json.load(f)
    return _knowledge_base


def _normalize_drug_name(name: str) -> str:
    """Normalize drug name for lookup (lowercase, strip whitespace)."""
    return name.strip().lower()


def _make_pair_key(drug_a: str, drug_b: str) -> str:
    """Create a canonical key for a drug pair (alphabetical order)."""
    a, b = sorted([_normalize_drug_name(drug_a), _normalize_drug_name(drug_b)])
    return f"{a}+{b}"


def _make_triple_key(drugs: list[str]) -> str:
    """Create a canonical key for a drug triple."""
    return "+".join(sorted([_normalize_drug_name(d) for d in drugs]))


def _risk_to_score(risk: str) -> float:
    """Convert risk level to numerical score."""
    return {"LOW": 0.2, "MEDIUM": 0.5, "HIGH": 0.9}.get(risk, 0.3)


def _score_to_risk(score: float) -> RiskLevel:
    """Convert numerical score to risk level."""
    if score >= 0.7:
        return RiskLevel.HIGH
    elif score >= 0.4:
        return RiskLevel.MEDIUM
    else:
        return RiskLevel.LOW


def _find_cyp_conflicts(drug_names: list[str], kb: dict) -> list[dict]:
    """
    Find CYP enzyme pathway conflicts among the drugs.
    
    This is crucial for explainability — when multiple drugs use the same
    CYP enzyme (e.g., CYP3A4), they compete for metabolism, causing
    drug level buildup and toxicity.
    """
    drugs_data = kb.get("drugs", {})
    cyp_data = kb.get("cyp_enzymes", {})
    conflicts = []

    # Collect which CYP enzymes each drug uses
    drug_enzymes = {}
    for name in drug_names:
        norm_name = _normalize_drug_name(name)
        if norm_name in drugs_data:
            enzymes = drugs_data[norm_name].get("cyp_enzymes", [])
            drug_enzymes[norm_name] = enzymes

    # Check for overlapping enzymes
    for enzyme_name, enzyme_info in cyp_data.items():
        drugs_using = [
            d for d, enzymes in drug_enzymes.items()
            if enzyme_name in enzymes
        ]
        if len(drugs_using) >= 2:
            conflicts.append({
                "enzyme": enzyme_name,
                "drugs": drugs_using,
                "description": enzyme_info.get("description", ""),
                "risk_note": enzyme_info.get("risk_note", ""),
            })

    return conflicts


def _apply_patient_modifiers(
    risk_score: float,
    profile: Optional[PatientProfile],
) -> float:
    """
    Adjust risk score based on patient profile.
    
    Elderly patients (>65) have reduced drug clearance.
    High BMI affects drug distribution volume.
    Existing conditions like liver/kidney disease compound risk.
    """
    if profile is None:
        return risk_score

    modifier = 1.0

    # Age modifier: elderly patients have slower drug metabolism
    if profile.age and profile.age >= 75:
        modifier += 0.20
    elif profile.age and profile.age >= 65:
        modifier += 0.10

    # BMI modifier: obesity changes drug pharmacokinetics
    if profile.bmi and profile.bmi >= 35:
        modifier += 0.10
    elif profile.bmi and profile.bmi >= 30:
        modifier += 0.05

    # Condition modifiers
    conditions = [c.lower() for c in profile.conditions]
    if any(c in conditions for c in ["liver disease", "hepatitis", "cirrhosis"]):
        modifier += 0.20
    if any(c in conditions for c in ["kidney disease", "renal failure", "ckd"]):
        modifier += 0.15
    if any(c in conditions for c in ["diabetes", "type 2 diabetes"]):
        modifier += 0.05

    return min(risk_score * modifier, 1.0)


def predict_interactions(
    drug_names: list[str],
    patient_profile: Optional[PatientProfile] = None,
) -> PredictionResponse:
    """
    Main prediction function.
    
    Takes a list of drug names and returns a complete analysis:
    - Overall risk assessment
    - All pairwise interactions found
    - Higher-order (3+ drug) interactions
    - Side effects with explanations
    - Medication timing
    - Interaction graph for visualization
    """
    kb = _load_kb()
    drugs_data = kb.get("drugs", {})
    pairwise_data = kb.get("pairwise_interactions", {})
    higher_order_data = kb.get("higher_order_interactions", {})
    timing_data = kb.get("timing_recommendations", {})
    se_catalog = kb.get("side_effect_catalog", {})

    # Normalize all drug names
    normalized_drugs = [_normalize_drug_name(d) for d in drug_names]
    display_drugs = {}
    for orig, norm in zip(drug_names, normalized_drugs):
        if norm in drugs_data:
            display_drugs[norm] = drugs_data[norm]["name"]
        else:
            display_drugs[norm] = orig.title()

    # ── Pairwise Interactions ─────────────────────────────────
    pairwise_results = []
    all_side_effects = []
    risk_scores = []
    total_interactions = 0

    for drug_a, drug_b in combinations(normalized_drugs, 2):
        total_interactions += 1
        pair_key = _make_pair_key(drug_a, drug_b)

        if pair_key in pairwise_data:
            interaction = pairwise_data[pair_key]
            risk = interaction["risk"]
            risk_scores.append(_risk_to_score(risk))

            pairwise_results.append(PairwiseInteraction(
                drug_a=display_drugs.get(drug_a, drug_a.title()),
                drug_b=display_drugs.get(drug_b, drug_b.title()),
                risk=RiskLevel(risk),
                side_effects=interaction["side_effects"],
                mechanism=interaction["mechanism"],
            ))

            # Collect side effects
            for se_name in interaction["side_effects"]:
                se_info = se_catalog.get(se_name, {})
                all_side_effects.append(SideEffectPrediction(
                    name=se_name,
                    risk=RiskLevel(risk),
                    confidence=0.6 + _risk_to_score(risk) * 0.35,
                    affected_organ=se_info.get("organ", "unknown"),
                    contributing_drugs=[
                        display_drugs.get(drug_a, drug_a.title()),
                        display_drugs.get(drug_b, drug_b.title()),
                    ],
                    explanation=interaction["mechanism"],
                ))
        else:
            # No known interaction — LOW risk
            risk_scores.append(0.1)

    # ── Higher-Order Interactions (3+ drugs) ──────────────────
    higher_order_results = []

    if len(normalized_drugs) >= 3:
        for combo_size in range(3, min(len(normalized_drugs) + 1, 5)):
            for combo in combinations(normalized_drugs, combo_size):
                combo_key = _make_triple_key(list(combo))
                if combo_key in higher_order_data:
                    ho = higher_order_data[combo_key]
                    risk_scores.append(_risk_to_score(ho["risk"]) * 1.2)  # Higher weight

                    combo_display = [
                        display_drugs.get(d, d.title()) for d in combo
                    ]
                    higher_order_results.append(HigherOrderInteraction(
                        drugs=combo_display,
                        risk=RiskLevel(ho["risk"]),
                        side_effects=ho["side_effects"],
                        mechanism=ho["mechanism"],
                        confidence=ho.get("confidence", 0.8),
                    ))

                    for se_name in ho["side_effects"]:
                        se_info = se_catalog.get(se_name, {})
                        all_side_effects.append(SideEffectPrediction(
                            name=se_name,
                            risk=RiskLevel(ho["risk"]),
                            confidence=ho.get("confidence", 0.8),
                            affected_organ=se_info.get("organ", "unknown"),
                            contributing_drugs=combo_display,
                            explanation=ho["mechanism"],
                        ))

    # ── CYP Enzyme Conflict Explanations ─────────────────────
    cyp_conflicts = _find_cyp_conflicts(drug_names, kb)
    for conflict in cyp_conflicts:
        conflict_drugs = [display_drugs.get(d, d.title()) for d in conflict["drugs"]]
        explanation = (
            f"These drugs share the {conflict['enzyme']} metabolic pathway: "
            f"{', '.join(conflict_drugs)}. {conflict['risk_note']}"
        )
        # Add as side effect if not already covered
        if not any(
            se.explanation == explanation for se in all_side_effects
        ):
            all_side_effects.append(SideEffectPrediction(
                name=f"{conflict['enzyme']} enzyme competition",
                risk=RiskLevel.MEDIUM if len(conflict["drugs"]) <= 2 else RiskLevel.HIGH,
                confidence=0.75,
                affected_organ="liver",
                contributing_drugs=conflict_drugs,
                explanation=explanation,
            ))

    # ── Deduplicate side effects (keep highest risk) ─────────
    se_map = {}
    for se in all_side_effects:
        if se.name not in se_map or _risk_to_score(se.risk.value) > _risk_to_score(se_map[se.name].risk.value):
            se_map[se.name] = se
    unique_side_effects = sorted(
        se_map.values(),
        key=lambda x: _risk_to_score(x.risk.value),
        reverse=True,
    )

    # ── Calculate Overall Risk ──────────────────────────────
    if risk_scores:
        overall_score = max(risk_scores) * 0.6 + (sum(risk_scores) / len(risk_scores)) * 0.4
    else:
        overall_score = 0.1

    # Apply patient modifiers
    overall_score = _apply_patient_modifiers(overall_score, patient_profile)
    overall_risk = _score_to_risk(overall_score)

    # ── Medication Timing ─────────────────────────────────────
    timing_results = []
    for drug in normalized_drugs:
        if drug in timing_data:
            t = timing_data[drug]
            timing_results.append(MedicationTiming(
                drug=display_drugs.get(drug, drug.title()),
                suggested_time=t["suggested_time"],
                notes=t["notes"],
            ))
        else:
            timing_results.append(MedicationTiming(
                drug=display_drugs.get(drug, drug.title()),
                suggested_time="Consult your physician",
                notes="Timing data not available for this medication.",
            ))

    # ── Build Interaction Graph (for Cytoscape.js) ────────────
    graph_nodes = []
    graph_edges = []

    # Add drug nodes
    for drug in normalized_drugs:
        # Determine node risk based on how many high-risk interactions it's in
        drug_display = display_drugs.get(drug, drug.title())
        drug_risk = RiskLevel.LOW
        for pw in pairwise_results:
            if pw.drug_a == drug_display or pw.drug_b == drug_display:
                if _risk_to_score(pw.risk.value) > _risk_to_score(drug_risk.value):
                    drug_risk = pw.risk

        graph_nodes.append(GraphNode(
            id=drug,
            label=drug_display,
            risk_contribution=drug_risk,
            node_type="drug",
        ))

    # Add edges for pairwise interactions
    for pw in pairwise_results:
        source = _normalize_drug_name(pw.drug_a)
        target = _normalize_drug_name(pw.drug_b)
        graph_edges.append(GraphEdge(
            source=source,
            target=target,
            risk=pw.risk,
            side_effects=pw.side_effects[:3],  # Top 3 for label
            weight=_risk_to_score(pw.risk.value),
        ))

    # Add side effect nodes for HIGH risk
    se_node_ids = set()
    for se in unique_side_effects:
        if se.risk == RiskLevel.HIGH and se.name not in se_node_ids:
            se_id = f"se_{se.name.lower().replace(' ', '_')}"
            se_node_ids.add(se.name)
            graph_nodes.append(GraphNode(
                id=se_id,
                label=se.name,
                risk_contribution=RiskLevel.HIGH,
                node_type="side_effect",
            ))
            # Connect to contributing drugs
            for drug_name in se.contributing_drugs:
                drug_id = _normalize_drug_name(drug_name)
                graph_edges.append(GraphEdge(
                    source=drug_id,
                    target=se_id,
                    risk=RiskLevel.HIGH,
                    side_effects=[se.name],
                    weight=0.8,
                ))

    graph = InteractionGraph(nodes=graph_nodes, edges=graph_edges)

    # ── Generate Summary ──────────────────────────────────────
    n_drugs = len(drug_names)
    n_high = len([pw for pw in pairwise_results if pw.risk == RiskLevel.HIGH])
    n_high_ho = len([ho for ho in higher_order_results if ho.risk == RiskLevel.HIGH])

    summary_parts = [
        f"Analysis of {n_drugs} medications with {total_interactions} pairwise combinations analyzed."
    ]
    if n_high > 0:
        summary_parts.append(
            f"⚠️ Found {n_high} HIGH-risk pairwise interaction{'s' if n_high > 1 else ''}."
        )
    if n_high_ho > 0:
        summary_parts.append(
            f"🔴 Found {n_high_ho} HIGH-risk multi-drug interaction{'s' if n_high_ho > 1 else ''} "
            f"involving 3 or more drugs."
        )
    if cyp_conflicts:
        enzymes = ", ".join(set(c["enzyme"] for c in cyp_conflicts))
        summary_parts.append(
            f"Enzyme pathway conflicts detected: {enzymes}."
        )
    if patient_profile and patient_profile.age and patient_profile.age >= 65:
        summary_parts.append(
            "Risk adjusted upward for elderly patient — reduced drug clearance expected."
        )

    summary = " ".join(summary_parts)

    return PredictionResponse(
        overall_risk=overall_risk,
        risk_score=round(overall_score, 3),
        total_interactions_analyzed=total_interactions,
        side_effects=unique_side_effects,
        pairwise_interactions=pairwise_results,
        higher_order_interactions=higher_order_results,
        medication_timing=timing_results,
        interaction_graph=graph,
        summary=summary,
    )
