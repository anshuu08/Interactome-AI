/**
 * API Client for Interactome-AI Backend.
 * 
 * All backend calls go through here. This gives us:
 * - Single place to change the API URL
 * - Error handling
 * - Type safety with TypeScript interfaces
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// ── Type Definitions ─────────────────────────────────────────

export type RiskLevel = "LOW" | "MEDIUM" | "HIGH";

export interface DrugSearchResult {
  cid: number;
  name: string;
  formula?: string;
  molecular_weight?: number;
  smiles?: string;
}

export interface PatientProfile {
  age?: number;
  bmi?: number;
  conditions: string[];
}

export interface SideEffectPrediction {
  name: string;
  risk: RiskLevel;
  confidence: number;
  affected_organ: string;
  contributing_drugs: string[];
  explanation: string;
}

export interface PairwiseInteraction {
  drug_a: string;
  drug_b: string;
  risk: RiskLevel;
  side_effects: string[];
  mechanism: string;
}

export interface HigherOrderInteraction {
  drugs: string[];
  risk: RiskLevel;
  side_effects: string[];
  mechanism: string;
  confidence: number;
}

export interface MedicationTiming {
  drug: string;
  suggested_time: string;
  gap_hours?: number;
  notes: string;
}

export interface GraphNode {
  id: string;
  label: string;
  risk_contribution: RiskLevel;
  node_type: "drug" | "side_effect";
}

export interface GraphEdge {
  source: string;
  target: string;
  risk: RiskLevel;
  side_effects: string[];
  weight: number;
}

export interface InteractionGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface PredictionResponse {
  overall_risk: RiskLevel;
  risk_score: number;
  total_interactions_analyzed: number;
  side_effects: SideEffectPrediction[];
  pairwise_interactions: PairwiseInteraction[];
  higher_order_interactions: HigherOrderInteraction[];
  medication_timing: MedicationTiming[];
  interaction_graph: InteractionGraph;
  summary: string;
}

// ── API Functions ────────────────────────────────────────────

/**
 * Search for drugs by name (autocomplete).
 * Called as the user types in the search bar.
 */
export async function searchDrugs(query: string): Promise<DrugSearchResult[]> {
  try {
    const res = await fetch(`${API_BASE}/api/drugs/search?q=${encodeURIComponent(query)}&limit=10`);
    if (!res.ok) return [];
    return await res.json();
  } catch {
    return [];
  }
}

/**
 * Get full details for a specific drug.
 */
export async function getDrugDetail(identifier: string) {
  const res = await fetch(`${API_BASE}/api/drugs/${encodeURIComponent(identifier)}`);
  if (!res.ok) throw new Error("Drug not found");
  return await res.json();
}

/**
 * Submit drug list for interaction prediction.
 * This is the main API call — returns the full analysis.
 */
export async function predictInteractions(
  drugs: string[],
  patientProfile?: PatientProfile
): Promise<PredictionResponse> {
  const res = await fetch(`${API_BASE}/api/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      drugs,
      patient_profile: patientProfile || null,
    }),
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Prediction failed" }));
    throw new Error(error.detail || "Prediction failed");
  }
  return await res.json();
}

/**
 * Download PDF report for the analysis.
 */
export async function downloadPdfReport(
  drugs: string[],
  patientProfile?: PatientProfile
): Promise<Blob> {
  const res = await fetch(`${API_BASE}/api/predict/pdf`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      drugs,
      patient_profile: patientProfile || null,
    }),
  });
  if (!res.ok) throw new Error("Failed to generate PDF");
  return await res.blob();
}

/**
 * Get interaction graph data for visualization.
 */
export async function getGraph(drugs: string[]): Promise<InteractionGraph> {
  const res = await fetch(
    `${API_BASE}/api/graph?drugs=${drugs.map(d => encodeURIComponent(d)).join(",")}`
  );
  if (!res.ok) throw new Error("Failed to fetch graph");
  return await res.json();
}

/**
 * Check if the backend is healthy.
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/health`);
    return res.ok;
  } catch {
    return false;
  }
}
