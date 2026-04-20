"""
FDA FAERS API Endpoints — Real-World Adverse Event Data.

GET /api/fda/side-effects/{drug}
    → Top reported side effects from FDA's FAERS database

GET /api/fda/events/{drug}
    → Real adverse event reports for a drug

GET /api/fda/co-prescribed/{drug}
    → Drugs most commonly co-prescribed in adverse event reports
"""
from fastapi import APIRouter, Query
from app.services import openfda

router = APIRouter(prefix="/api/fda", tags=["FDA FAERS"])


@router.get("/side-effects/{drug_name}")
async def get_side_effects(
    drug_name: str,
    limit: int = Query(10, ge=1, le=25, description="Max results"),
):
    """
    Get the most commonly reported side effects for a drug
    from the FDA Adverse Event Reporting System (FAERS).

    Returns ranked list: [{side_effect, count}, ...]
    """
    results = await openfda.get_side_effect_counts(drug_name, limit=limit)
    return {"drug": drug_name, "source": "FDA FAERS", "side_effects": results}


@router.get("/events/{drug_name}")
async def get_events(
    drug_name: str,
    limit: int = Query(5, ge=1, le=20, description="Max reports"),
):
    """
    Get real adverse event reports for a specific drug from FAERS.

    Each report includes: reactions, co-prescribed drugs, seriousness.
    """
    results = await openfda.get_adverse_events(drug_name, limit=limit)
    return {"drug": drug_name, "source": "FDA FAERS", "reports": results}


@router.get("/co-prescribed/{drug_name}")
async def get_co_prescribed(
    drug_name: str,
    limit: int = Query(10, ge=1, le=25, description="Max results"),
):
    """
    Find drugs most commonly co-prescribed with the given drug
    in FAERS adverse event reports.

    Useful for identifying real-world polypharmacy patterns.
    """
    results = await openfda.get_co_prescribed_drugs(drug_name, limit=limit)
    return {"drug": drug_name, "source": "FDA FAERS", "co_prescribed": results}
