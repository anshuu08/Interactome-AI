"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import {
  Search,
  X,
  AlertTriangle,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Clock,
  Download,
  ChevronDown,
  ChevronUp,
  Pill,
  Activity,
  User,
  Info,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  searchDrugs,
  predictInteractions,
  downloadPdfReport,
  type DrugSearchResult,
  type PredictionResponse,
  type PatientProfile,
  type RiskLevel,
} from "@/lib/api";
import dynamic from "next/dynamic";

// Load Cytoscape graph component only on client side
const DrugGraph = dynamic(() => import("@/components/drug-graph"), {
  ssr: false,
  loading: () => (
    <div className="h-[450px] flex items-center justify-center bg-muted/30 rounded-xl text-sm text-muted-foreground">
      Loading graph...
    </div>
  ),
});

// ── Helpers ───────────────────────────────────────────────────
function riskBadgeClass(risk: RiskLevel) {
  switch (risk) {
    case "HIGH":
      return "risk-high";
    case "MEDIUM":
      return "risk-medium";
    case "LOW":
      return "risk-low";
  }
}

function riskIcon(risk: RiskLevel) {
  switch (risk) {
    case "HIGH":
      return <ShieldAlert className="w-4 h-4" />;
    case "MEDIUM":
      return <AlertTriangle className="w-4 h-4" />;
    case "LOW":
      return <ShieldCheck className="w-4 h-4" />;
  }
}

function riskColor(risk: RiskLevel) {
  switch (risk) {
    case "HIGH":
      return "text-red-600";
    case "MEDIUM":
      return "text-amber-600";
    case "LOW":
      return "text-green-600";
  }
}

function riskBg(risk: RiskLevel) {
  switch (risk) {
    case "HIGH":
      return "bg-red-50 border-red-200";
    case "MEDIUM":
      return "bg-amber-50 border-amber-200";
    case "LOW":
      return "bg-green-50 border-green-200";
  }
}

// ── Main Predictor Page ────────────────────────────────────────
export default function PredictorPage() {
  // Drug search state
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<DrugSearchResult[]>([]);
  const [selectedDrugs, setSelectedDrugs] = useState<string[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [searching, setSearching] = useState(false);
  const searchTimeout = useRef<NodeJS.Timeout | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Patient profile state
  const [showProfile, setShowProfile] = useState(false);
  const [age, setAge] = useState("");
  const [bmi, setBmi] = useState("");
  const [conditions, setConditions] = useState<string[]>([]);
  const [conditionInput, setConditionInput] = useState("");

  // Prediction state
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Expanded panels
  const [expandedPairwise, setExpandedPairwise] = useState<number | null>(null);
  const [expandedHO, setExpandedHO] = useState<number | null>(null);

  // ── Drug Search (debounced) ────────────────────────────────
  const handleSearch = useCallback(async (query: string) => {
    setSearchQuery(query);
    if (searchTimeout.current) clearTimeout(searchTimeout.current);

    if (query.length < 2) {
      setSearchResults([]);
      setShowDropdown(false);
      return;
    }

    setSearching(true);
    searchTimeout.current = setTimeout(async () => {
      try {
        const results = await searchDrugs(query);
        // Filter out already-selected drugs
        const filtered = results.filter(
          (r) => !selectedDrugs.includes(r.name.toLowerCase())
        );
        setSearchResults(filtered);
        setShowDropdown(filtered.length > 0);
      } catch {
        setSearchResults([]);
      }
      setSearching(false);
    }, 300);
  }, [selectedDrugs]);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  // ── Add / Remove Drugs ─────────────────────────────────────
  const addDrug = (name: string) => {
    const normalized = name.toLowerCase();
    if (!selectedDrugs.includes(normalized)) {
      setSelectedDrugs((prev) => [...prev, normalized]);
    }
    setSearchQuery("");
    setShowDropdown(false);
    setSearchResults([]);
    setPrediction(null);
  };

  const removeDrug = (name: string) => {
    setSelectedDrugs((prev) => prev.filter((d) => d !== name));
    setPrediction(null);
  };

  // ── Add Condition ──────────────────────────────────────────
  const addCondition = () => {
    if (conditionInput.trim() && !conditions.includes(conditionInput.trim().toLowerCase())) {
      setConditions((prev) => [...prev, conditionInput.trim().toLowerCase()]);
      setConditionInput("");
    }
  };

  // ── Run Prediction ─────────────────────────────────────────
  const handlePredict = async () => {
    if (selectedDrugs.length < 2) {
      setError("Please add at least 2 drugs to analyze interactions.");
      return;
    }

    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const profile: PatientProfile | undefined =
        showProfile && (age || bmi || conditions.length > 0)
          ? {
            age: age ? parseInt(age) : undefined,
            bmi: bmi ? parseFloat(bmi) : undefined,
            conditions,
          }
          : undefined;

      const result = await predictInteractions(selectedDrugs, profile);
      setPrediction(result);
    } catch (err: any) {
      setError(err.message || "Failed to analyze. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  // ── Download PDF ───────────────────────────────────────────
  const handleDownloadPdf = async () => {
    try {
      const profile: PatientProfile | undefined =
        showProfile && (age || bmi || conditions.length > 0)
          ? { age: age ? parseInt(age) : undefined, bmi: bmi ? parseFloat(bmi) : undefined, conditions }
          : undefined;

      const blob = await downloadPdfReport(selectedDrugs, profile);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "interactome_ai_report.pdf";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      setError("Failed to generate PDF report.");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 animate-fade-in">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Activity className="w-6 h-6 text-teal-600" />
          Drug Interaction Predictor
        </h1>
        <p className="text-muted-foreground mt-1">
          Enter your medications below to analyze potential interactions and risks.
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* ─── LEFT: Input Panel ─────────────────────────────── */}
        <div className="lg:col-span-1 space-y-4">
          {/* Drug Search */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Pill className="w-4 h-4 text-teal-600" />
                Medications
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {/* Search Input */}
              <div className="relative" ref={dropdownRef}>
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="drug-search"
                  placeholder="Search drugs (e.g., aspirin)"
                  className="pl-9"
                  value={searchQuery}
                  onChange={(e) => handleSearch(e.target.value)}
                  onFocus={() => searchResults.length > 0 && setShowDropdown(true)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && searchQuery.trim().length >= 2) {
                      addDrug(searchQuery.trim());
                    }
                  }}
                />
                {searching && (
                  <div className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    Searching...
                  </div>
                )}

                {/* Dropdown Results */}
                {showDropdown && (
                  <div className="absolute z-50 w-full mt-1 bg-white border rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    {searchResults.map((drug, idx) => (
                      <button
                        key={`${drug.cid}-${idx}`}
                        className="w-full text-left px-3 py-2.5 hover:bg-teal-50 transition-colors border-b last:border-0"
                        onClick={() => addDrug(drug.name)}
                      >
                        <div className="font-medium text-sm">{drug.name}</div>
                        {drug.formula && (
                          <div className="text-xs text-muted-foreground">
                            {drug.formula}
                            {drug.molecular_weight && ` • ${drug.molecular_weight.toFixed(1)} g/mol`}
                          </div>
                        )}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Selected Drug Tags */}
              {selectedDrugs.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {selectedDrugs.map((drug) => (
                    <span key={drug} className="drug-chip">
                      {drug.charAt(0).toUpperCase() + drug.slice(1)}
                      <button onClick={() => removeDrug(drug)} title="Remove">
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}

              {selectedDrugs.length === 0 && (
                <p className="text-xs text-muted-foreground py-2">
                  Add at least 2 medications to analyze interactions.
                </p>
              )}
            </CardContent>
          </Card>

          {/* Patient Profile (Optional)
          <Card>
            <CardHeader className="pb-3">
              <button
                className="flex items-center justify-between w-full"
                onClick={() => setShowProfile(!showProfile)}
              >
                <CardTitle className="text-base flex items-center gap-2">
                  <User className="w-4 h-4 text-teal-600" />
                  Patient Profile
                  <span className="text-xs font-normal text-muted-foreground">(Optional)</span>
                </CardTitle>
                {showProfile ? (
                  <ChevronUp className="w-4 h-4 text-muted-foreground" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-muted-foreground" />
                )}
              </button>
            </CardHeader>
            {showProfile && (
              <CardContent className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <Label htmlFor="age" className="text-xs">Age</Label>
                    <Input
                      id="age"
                      type="number"
                      placeholder="e.g., 72"
                      value={age}
                      onChange={(e) => setAge(e.target.value)}
                      min="0"
                      max="120"
                    />
                  </div>
                  <div>
                    <Label htmlFor="bmi" className="text-xs">BMI</Label>
                    <Input
                      id="bmi"
                      type="number"
                      placeholder="e.g., 28.5"
                      value={bmi}
                      onChange={(e) => setBmi(e.target.value)}
                      min="10"
                      max="60"
                      step="0.1"
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="conditions" className="text-xs">Existing Conditions</Label>
                  <div className="flex gap-2">
                    <Input
                      id="conditions"
                      placeholder="e.g., diabetes"
                      value={conditionInput}
                      onChange={(e) => setConditionInput(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && addCondition()}
                    />
                    <Button size="sm" variant="outline" onClick={addCondition}>
                      Add
                    </Button>
                  </div>
                  {conditions.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mt-2">
                      {conditions.map((c) => (
                        <span key={c} className="drug-chip text-xs">
                          {c}
                          <button onClick={() => setConditions(conditions.filter((x) => x !== c))}>×</button>
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </CardContent>
            )}
          </Card> */}

          {/* Analyze Button */}
          <Button
            className="w-full bg-teal-600 hover:bg-teal-700 text-white font-semibold h-11"
            onClick={handlePredict}
            disabled={loading || selectedDrugs.length < 2}
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Analyzing...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <Shield className="w-4 h-4" />
                Analyze Interactions ({selectedDrugs.length} drugs)
              </span>
            )}
          </Button>

          {error && (
            <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">
              {error}
            </div>
          )}
        </div>

        {/* ─── RIGHT: Results Panel ──────────────────────────── */}
        <div className="lg:col-span-2 space-y-4">
          {!prediction && !loading && (
            <Card className="border-dashed">
              <CardContent className="flex flex-col items-center justify-center py-16 text-center">
                <Shield className="w-12 h-12 text-muted-foreground/30 mb-4" />
                <h3 className="font-semibold text-muted-foreground mb-1">No Analysis Yet</h3>
                <p className="text-sm text-muted-foreground">
                  Add your medications and click &quot;Analyze Interactions&quot; to see results.
                </p>
              </CardContent>
            </Card>
          )}

          {prediction && (
            <>
              {/* ── Overall Risk Badge ──────────────────────────── */}
              <Card className={`border-2 ${riskBg(prediction.overall_risk)}`}>
                <CardContent className="py-5">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div
                        className={`w-16 h-16 rounded-xl flex items-center justify-center ${prediction.overall_risk === "HIGH"
                          ? "bg-red-100"
                          : prediction.overall_risk === "MEDIUM"
                            ? "bg-amber-100"
                            : "bg-green-100"
                          } risk-pulse`}
                      >
                        {prediction.overall_risk === "HIGH" ? (
                          <ShieldAlert className="w-8 h-8 text-red-600" />
                        ) : prediction.overall_risk === "MEDIUM" ? (
                          <AlertTriangle className="w-8 h-8 text-amber-600" />
                        ) : (
                          <ShieldCheck className="w-8 h-8 text-green-600" />
                        )}
                      </div>
                      <div>
                        <div className="text-sm text-muted-foreground">Overall Risk Level</div>
                        <div className={`text-2xl font-bold ${riskColor(prediction.overall_risk)}`}>
                          {prediction.overall_risk}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          Score: {(prediction.risk_score * 100).toFixed(0)}% •{" "}
                          {prediction.total_interactions_analyzed} pairs analyzed
                        </div>
                      </div>
                    </div>
                    {/* PDF report button removed */}
                  </div>
                  <p className="text-sm mt-3 text-foreground/80">{prediction.summary}</p>
                </CardContent>
              </Card>

              {/* ── Interaction Graph ───────────────────────────── */}
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-base flex items-center gap-2">
                    <Activity className="w-4 h-4 text-teal-600" />
                    Drug Interaction Network
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <DrugGraph graph={prediction.interaction_graph} />
                </CardContent>
              </Card>

              {/* ── Pairwise Interactions ──────────────────────── */}
              {prediction.pairwise_interactions.length > 0 && (
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">
                      Pairwise Interactions ({prediction.pairwise_interactions.length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    {prediction.pairwise_interactions.map((pw, i) => (
                      <div
                        key={i}
                        className={`border rounded-lg overflow-hidden ${pw.risk === "HIGH" ? "border-red-200" : pw.risk === "MEDIUM" ? "border-amber-200" : "border-green-200"
                          }`}
                      >
                        <button
                          className={`w-full flex items-center justify-between p-3 text-left hover:bg-muted/30 transition-colors ${pw.risk === "HIGH" ? "bg-red-50/50" : pw.risk === "MEDIUM" ? "bg-amber-50/50" : "bg-green-50/50"
                            }`}
                          onClick={() => setExpandedPairwise(expandedPairwise === i ? null : i)}
                        >
                          <div className="flex items-center gap-3">
                            <span className={riskColor(pw.risk)}>{riskIcon(pw.risk)}</span>
                            <div>
                              <span className="font-medium text-sm">
                                {pw.drug_a} + {pw.drug_b}
                              </span>
                              <div className="flex gap-1.5 mt-1">
                                {pw.side_effects.slice(0, 2).map((se) => (
                                  <Badge key={se} variant="secondary" className="text-xs font-normal">
                                    {se}
                                  </Badge>
                                ))}
                                {pw.side_effects.length > 2 && (
                                  <Badge variant="secondary" className="text-xs font-normal">
                                    +{pw.side_effects.length - 2} more
                                  </Badge>
                                )}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${riskBadgeClass(pw.risk)}`}>
                              {pw.risk}
                            </span>
                            {expandedPairwise === i ? (
                              <ChevronUp className="w-4 h-4 text-muted-foreground" />
                            ) : (
                              <ChevronDown className="w-4 h-4 text-muted-foreground" />
                            )}
                          </div>
                        </button>
                        {expandedPairwise === i && (
                          <div className="p-3 border-t bg-white text-sm">
                            <div className="flex items-start gap-2">
                              <Info className="w-4 h-4 text-teal-600 mt-0.5 shrink-0" />
                              <div>
                                <div className="font-medium text-xs text-muted-foreground mb-1">MECHANISM</div>
                                <p className="text-foreground/80 leading-relaxed">{pw.mechanism}</p>
                              </div>
                            </div>
                            <div className="mt-2 ml-6">
                              <div className="font-medium text-xs text-muted-foreground mb-1">SIDE EFFECTS</div>
                              <div className="flex flex-wrap gap-1.5">
                                {pw.side_effects.map((se) => (
                                  <Badge key={se} variant="outline" className="text-xs">
                                    {se}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </CardContent>
                </Card>
              )}

              {/* ── Higher-Order Interactions (3+ drugs) ─────── */}
              {prediction.higher_order_interactions.length > 0 && (
                <Card className="border-2 border-red-200">
                  <CardHeader className="pb-2 bg-red-50/50">
                    <CardTitle className="text-base flex items-center gap-2 text-red-700">
                      <ShieldAlert className="w-4 h-4" />
                      Multi-Drug Interactions ({prediction.higher_order_interactions.length})
                    </CardTitle>
                    <p className="text-xs text-red-600/70">
                      These interactions involve 3 or more drugs acting together — effects beyond pairwise analysis
                    </p>
                  </CardHeader>
                  <CardContent className="space-y-2 pt-3">
                    {prediction.higher_order_interactions.map((ho, i) => (
                      <div
                        key={i}
                        className="border border-red-200 rounded-lg overflow-hidden"
                      >
                        <button
                          className="w-full flex items-center justify-between p-3 text-left bg-red-50/30 hover:bg-red-50/60 transition-colors"
                          onClick={() => setExpandedHO(expandedHO === i ? null : i)}
                        >
                          <div>
                            <span className="font-medium text-sm">
                              {ho.drugs.join(" + ")}
                            </span>
                            <div className="flex gap-1.5 mt-1">
                              {ho.side_effects.slice(0, 2).map((se) => (
                                <Badge key={se} variant="destructive" className="text-xs font-normal">
                                  {se}
                                </Badge>
                              ))}
                            </div>
                          </div>
                          <div className="flex items-center gap-2 shrink-0">
                            <div className="text-right">
                              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${riskBadgeClass(ho.risk)}`}>
                                {ho.risk}
                              </span>
                              <div className="text-xs text-muted-foreground mt-0.5">
                                {(ho.confidence * 100).toFixed(0)}% confidence
                              </div>
                            </div>
                            {expandedHO === i ? (
                              <ChevronUp className="w-4 h-4 text-muted-foreground" />
                            ) : (
                              <ChevronDown className="w-4 h-4 text-muted-foreground" />
                            )}
                          </div>
                        </button>
                        {expandedHO === i && (
                          <div className="p-3 border-t bg-white text-sm">
                            <div className="flex items-start gap-2">
                              <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
                              <div>
                                <div className="font-medium text-xs text-muted-foreground mb-1">MECHANISM</div>
                                <p className="text-foreground/80 leading-relaxed">{ho.mechanism}</p>
                              </div>
                            </div>
                            <div className="mt-2 ml-6">
                              <div className="font-medium text-xs text-muted-foreground mb-1">ALL SIDE EFFECTS</div>
                              <div className="flex flex-wrap gap-1.5">
                                {ho.side_effects.map((se) => (
                                  <Badge key={se} variant="destructive" className="text-xs font-normal">
                                    {se}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </CardContent>
                </Card>
              )}

              {/* ── Side Effects Summary ───────────────────────── */}
              {prediction.side_effects.length > 0 && (
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">
                      Predicted Side Effects ({prediction.side_effects.length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b text-left text-xs text-muted-foreground">
                            <th className="p-2 font-medium">Side Effect</th>
                            <th className="p-2 font-medium">Risk</th>
                            <th className="p-2 font-medium">Confidence</th>
                            <th className="p-2 font-medium">Organ</th>
                            <th className="p-2 font-medium">Contributing Drugs</th>
                          </tr>
                        </thead>
                        <tbody>
                          {prediction.side_effects.map((se, i) => (
                            <tr key={i} className="border-b last:border-0 hover:bg-muted/30">
                              <td className="p-2 font-medium">{se.name}</td>
                              <td className="p-2">
                                <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${riskBadgeClass(se.risk)}`}>
                                  {se.risk}
                                </span>
                              </td>
                              <td className="p-2 text-muted-foreground">
                                {(se.confidence * 100).toFixed(0)}%
                              </td>
                              <td className="p-2">
                                <Badge variant="outline" className="text-xs capitalize">
                                  {se.affected_organ}
                                </Badge>
                              </td>
                              <td className="p-2 text-muted-foreground text-xs">
                                {se.contributing_drugs.join(", ")}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* ── Medication Timing ──────────────────────────── */}
              {prediction.medication_timing.length > 0 && (
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base flex items-center gap-2">
                      <Clock className="w-4 h-4 text-teal-600" />
                      Medication Timing Recommendations
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {prediction.medication_timing.map((mt, i) => (
                        <div
                          key={i}
                          className="flex items-start gap-3 p-3 rounded-lg bg-teal-50/50 border border-teal-100"
                        >
                          <div className="w-8 h-8 rounded-lg bg-teal-100 flex items-center justify-center shrink-0 mt-0.5">
                            <Pill className="w-4 h-4 text-teal-700" />
                          </div>
                          <div>
                            <div className="font-medium text-sm">{mt.drug}</div>
                            <div className="text-sm text-teal-700 font-medium">
                              {mt.suggested_time}
                            </div>
                            <div className="text-xs text-muted-foreground mt-0.5">
                              {mt.notes}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}


            </>
          )}
        </div>
      </div>
    </div>
  );
}
