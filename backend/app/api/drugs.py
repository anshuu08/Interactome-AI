"""
Drug Search API Endpoint.

GET /api/drugs/search?q=<query>&limit=10
    → Searches PubChem for drugs matching the query
    → Used by the autocomplete in the frontend

GET /api/drugs/{identifier}
    → Get full details for a specific drug
"""
from fastapi import APIRouter, Query
from app.services import pubchem
from app.models.schemas import DrugSearchResult, DrugDetail
import json
import os

router = APIRouter(prefix="/api/drugs", tags=["Drugs"])

# Also load local drug database for fast fallback
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
KB_PATH = os.path.join(DATA_DIR, "drug_interactions.json")


def _get_local_drugs() -> dict:
    with open(KB_PATH, "r") as f:
        return json.load(f).get("drugs", {})


@router.get("/search", response_model=list[DrugSearchResult])
async def search_drugs(
    q: str = Query(..., min_length=1, description="Drug name search query"),
    limit: int = Query(10, ge=1, le=25, description="Max results"),
):
    """
    Search for drugs by name. Tries local KB first (instant),
    then falls back to PubChem API (real-time lookup).

    The autocomplete in the UI calls this endpoint as the user types.
    """
    results = []
    query_lower = q.lower().strip()

    # Step 1: Search local knowledge base (fast, offline)
    local_drugs = _get_local_drugs()
    for key, drug in local_drugs.items():
        if query_lower in key or query_lower in drug["name"].lower():
            results.append(DrugSearchResult(
                cid=drug["cid"],
                name=drug["name"],
                formula=drug.get("formula"),
                molecular_weight=drug.get("molecular_weight"),
                smiles=drug.get("smiles"),
            ))

    # Step 2: If not enough local results, search PubChem
    if len(results) < limit:
        try:
            pubchem_results = await pubchem.search_drugs(q, limit=limit - len(results))
            # Avoid duplicates
            existing_cids = {r.cid for r in results}
            for r in pubchem_results:
                if r.cid not in existing_cids:
                    results.append(r)
        except Exception:
            pass  # PubChem unavailable — use local results only

    return results[:limit]


@router.get("/{identifier}", response_model=DrugDetail)
async def get_drug(identifier: str):
    """
    Get full details for a drug by name or PubChem CID.
    
    Checks local KB first, then PubChem.
    """
    # Check local KB
    local_drugs = _get_local_drugs()
    norm = identifier.lower().strip()
    if norm in local_drugs:
        drug = local_drugs[norm]
        return DrugDetail(
            cid=drug["cid"],
            name=drug["name"],
            formula=drug.get("formula"),
            molecular_weight=drug.get("molecular_weight"),
            smiles=drug.get("smiles"),
            description=drug.get("description"),
        )

    # Check by CID
    for key, drug in local_drugs.items():
        if str(drug["cid"]) == identifier:
            return DrugDetail(
                cid=drug["cid"],
                name=drug["name"],
                formula=drug.get("formula"),
                molecular_weight=drug.get("molecular_weight"),
                smiles=drug.get("smiles"),
                description=drug.get("description"),
            )

    # Fallback to PubChem
    detail = await pubchem.get_drug_detail(identifier)
    if detail:
        return detail

    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail=f"Drug '{identifier}' not found")
