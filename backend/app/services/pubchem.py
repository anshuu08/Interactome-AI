"""
PubChem API Service for Interactome-AI.

This service calls the REAL PubChem PUG REST API to:
1. Search for drugs by name (autocomplete)
2. Fetch SMILES chemical notation
3. Get molecular properties (weight, formula)
4. Look up compound details by CID

API Docs: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
"""
import httpx
from typing import Optional
from app.models.schemas import DrugSearchResult, DrugDetail


# PubChem PUG REST base URL
PUBCHEM_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
AUTOCOMPLETE_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/compound"

# Timeout for HTTP requests (seconds)
TIMEOUT = 10.0


async def search_drugs(query: str, limit: int = 10) -> list[DrugSearchResult]:
    """
    Search PubChem for drugs matching the query string.
    Uses autocomplete API first, then fetches properties for each match.
    
    Example: search_drugs("aspir") → [Aspirin, ...]
    """
    results = []

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        # Step 1: Use autocomplete to get drug name suggestions
        try:
            autocomplete_url = f"{AUTOCOMPLETE_BASE}/{query}/json?limit={limit}"
            resp = await client.get(autocomplete_url)
            resp.raise_for_status()
            data = resp.json()

            # Extract dictionary entries (drug names)
            names = data.get("dictionary_terms", {}).get("compound", [])
        except Exception:
            # Fallback: try direct name search if autocomplete fails
            names = [query]

        # Step 2: For each name, fetch CID and properties
        for name in names[:limit]:
            try:
                props_url = (
                    f"{PUBCHEM_BASE}/compound/name/{name}"
                    f"/property/MolecularFormula,MolecularWeight,CanonicalSMILES/JSON"
                )
                resp = await client.get(props_url)
                if resp.status_code != 200:
                    continue

                props = resp.json()
                compounds = props.get("PropertyTable", {}).get("Properties", [])

                if compounds:
                    compound = compounds[0]
                    results.append(DrugSearchResult(
                        cid=compound.get("CID", 0),
                        name=name,
                        formula=compound.get("MolecularFormula"),
                        molecular_weight=compound.get("MolecularWeight"),
                        smiles=compound.get("CanonicalSMILES"),
                    ))
            except Exception:
                continue

    return results


async def get_drug_detail(identifier: str) -> Optional[DrugDetail]:
    """
    Get full details for a drug by name or CID.
    Includes SMILES, formula, weight, and description.
    """
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            # Try as name first
            if identifier.isdigit():
                base_path = f"{PUBCHEM_BASE}/compound/cid/{identifier}"
            else:
                base_path = f"{PUBCHEM_BASE}/compound/name/{identifier}"

            # Fetch properties
            props_url = f"{base_path}/property/MolecularFormula,MolecularWeight,CanonicalSMILES/JSON"
            resp = await client.get(props_url)
            resp.raise_for_status()
            props = resp.json()
            compounds = props.get("PropertyTable", {}).get("Properties", [])

            if not compounds:
                return None

            compound = compounds[0]

            # Try to fetch description
            description = None
            try:
                desc_url = f"{base_path}/description/JSON"
                desc_resp = await client.get(desc_url)
                if desc_resp.status_code == 200:
                    desc_data = desc_resp.json()
                    informations = desc_data.get("InformationList", {}).get("Information", [])
                    for info in informations:
                        if info.get("Description"):
                            description = info["Description"]
                            break
            except Exception:
                pass

            return DrugDetail(
                cid=compound.get("CID", 0),
                name=identifier,
                formula=compound.get("MolecularFormula"),
                molecular_weight=compound.get("MolecularWeight"),
                smiles=compound.get("CanonicalSMILES"),
                description=description,
            )
        except Exception:
            return None


async def get_smiles(drug_name: str) -> Optional[str]:
    """Get just the SMILES string for a drug name."""
    detail = await get_drug_detail(drug_name)
    return detail.smiles if detail else None
