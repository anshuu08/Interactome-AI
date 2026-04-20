"""
OpenFDA FAERS API Service for Interactome-AI.

This service calls the REAL FDA Adverse Event Reporting System (FAERS) API to:
1. Look up real-world adverse events for specific drugs
2. Find co-prescribed drug combinations and their reported side effects
3. Get frequency counts of side effects

API Docs: https://open.fda.gov/apis/drug/event/
Endpoint: https://api.fda.gov/drug/event.json
"""
import httpx
from typing import Optional

OPENFDA_BASE = "https://api.fda.gov/drug/event.json"
TIMEOUT = 15.0


async def get_adverse_events(
    drug_name: str, limit: int = 5
) -> list[dict]:
    """
    Get real adverse event reports for a specific drug from FAERS.

    Returns list of dicts with:
    - reactions: list of reported side effects
    - drugs: list of all drugs the patient was taking
    - seriousness: whether the event was serious

    Example: get_adverse_events("aspirin") →
        [{"reactions": ["nausea", "headache"], "drugs": ["aspirin", "warfarin"], ...}]
    """
    results = []
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            params = {
                "search": f'patient.drug.openfda.generic_name:"{drug_name}"',
                "limit": limit,
            }
            resp = await client.get(OPENFDA_BASE, params=params)
            if resp.status_code != 200:
                return results

            data = resp.json()
            for result in data.get("results", []):
                # Extract reactions
                reactions = [
                    r.get("reactionmeddrapt", "Unknown")
                    for r in result.get("patient", {}).get("reaction", [])
                ]
                # Extract all drugs patient was taking
                drugs = []
                for drug in result.get("patient", {}).get("drug", []):
                    name = (
                        drug.get("openfda", {}).get("generic_name", [None])[0]
                        or drug.get("medicinalproduct", "Unknown")
                    )
                    drugs.append(name)

                # Seriousness flags
                serious = result.get("serious", 0) == 1

                results.append({
                    "reactions": reactions,
                    "drugs": drugs,
                    "serious": serious,
                    "report_date": result.get("receiptdate", ""),
                })
        except Exception:
            pass

    return results


async def get_side_effect_counts(
    drug_name: str, limit: int = 10
) -> list[dict]:
    """
    Get the most commonly reported side effects for a drug,
    ranked by frequency.

    Returns: [{"side_effect": "Nausea", "count": 1523}, ...]
    """
    results = []
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            params = {
                "search": f'patient.drug.openfda.generic_name:"{drug_name}"',
                "count": "patient.reaction.reactionmeddrapt.exact",
                "limit": limit,
            }
            resp = await client.get(OPENFDA_BASE, params=params)
            if resp.status_code != 200:
                return results

            data = resp.json()
            for item in data.get("results", []):
                results.append({
                    "side_effect": item.get("term", "Unknown"),
                    "count": item.get("count", 0),
                })
        except Exception:
            pass

    return results


async def get_co_prescribed_drugs(
    drug_name: str, limit: int = 10
) -> list[dict]:
    """
    Find which drugs are most commonly co-prescribed with the given drug
    in adverse event reports. This helps identify real-world polypharmacy patterns.

    Returns: [{"drug": "Metformin", "count": 892}, ...]
    """
    results = []
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            params = {
                "search": f'patient.drug.openfda.generic_name:"{drug_name}"',
                "count": "patient.drug.openfda.generic_name.exact",
                "limit": limit + 1,  # +1 to exclude the query drug itself
            }
            resp = await client.get(OPENFDA_BASE, params=params)
            if resp.status_code != 200:
                return results

            data = resp.json()
            for item in data.get("results", []):
                name = item.get("term", "")
                if name.upper() != drug_name.upper():
                    results.append({
                        "drug": name,
                        "count": item.get("count", 0),
                    })
        except Exception:
            pass

    return results[:limit]
