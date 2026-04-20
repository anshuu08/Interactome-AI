"""
Graph API Endpoint.

GET /api/graph?drugs=aspirin,warfarin,ibuprofen
    → Returns the interaction graph in Cytoscape.js format
    → Used by the frontend graph visualization component
"""
from fastapi import APIRouter, Query
from app.services.predictor import predict_interactions
from app.models.schemas import InteractionGraph

router = APIRouter(prefix="/api", tags=["Graph"])


@router.get("/graph", response_model=InteractionGraph)
async def get_graph(
    drugs: str = Query(..., description="Comma-separated list of drug names"),
):
    """
    Build and return the drug interaction graph structure.
    
    The frontend uses this to render the Cytoscape.js visualization.
    Nodes are drugs (and high-risk side effects).
    Edges are colored by risk level (red/yellow/green).
    """
    drug_list = [d.strip() for d in drugs.split(",") if d.strip()]

    if len(drug_list) < 2:
        return InteractionGraph(nodes=[], edges=[])

    result = predict_interactions(drug_list)
    return result.interaction_graph
