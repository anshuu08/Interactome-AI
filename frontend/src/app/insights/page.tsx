import {
  Activity,
  Database,
  Brain,
  GitBranch,
  Shield,
  BookOpen,
  ExternalLink,
  Layers,
  Users,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

export default function InsightsPage() {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 animate-fade-in">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <BookOpen className="w-6 h-6 text-teal-600" />
          About Interactome-AI
        </h1>
        <p className="text-muted-foreground mt-1">
          Understanding the research, architecture, and technology behind the system.
        </p>
      </div>

      {/* ── Research Overview ──────────────────────────────── */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Research Background</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-sm leading-relaxed">
          <p>
            <strong>Polypharmacy</strong> — the concurrent use of multiple medications — is increasingly
            common, especially among elderly patients managing chronic conditions. A patient taking 10+
            drugs creates 45+ potential pairwise interactions, and when higher-order (3+) combinations
            are considered, the complexity grows exponentially.
          </p>
          <p>
            Traditional drug interaction checkers only analyze pairwise combinations. They miss
            <strong> emergent interactions</strong> where three or more drugs interact through shared
            metabolic pathways (like CYP3A4 enzyme competition) to produce effects that no single pair
            would cause alone.
          </p>
          <p>
            Interactome-AI addresses this gap using <strong>Graph Neural Networks (GNNs)</strong> — a
            class of deep learning models specifically designed to learn from graph-structured data.
            By treating the patient&apos;s entire medication regimen as a knowledge graph, the system captures
            both direct and indirect interaction patterns.
          </p>
        </CardContent>
      </Card>





      {/* ── Data Sources ──────────────────────────────────── */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Database className="w-5 h-5 text-teal-600" />
            Data Sources
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid sm:grid-cols-3 gap-4">
            {[
              {
                name: "TWOSIDES / Decagon",
                desc: "Drug-drug interaction dataset with ~4.6M side effect associations across 645 drugs and 964 side effect types.",
                source: "Stanford SNAP",
                url: "https://snap.stanford.edu/decagon",
              },
              {
                name: "FAERS (FDA)",
                desc: "Real-world adverse event reports. Over 20M+ reports of drug side effects submitted to the FDA.",
                source: "OpenFDA API",
                url: "https://open.fda.gov/apis/drug/event/",
              },
              {
                name: "PubChem (NIH)",
                desc: "Chemical database with molecular structures (SMILES), properties, and compound identifiers for 100M+ compounds.",
                source: "NCBI/NIH",
                url: "https://pubchem.ncbi.nlm.nih.gov",
              },
            ].map((ds) => (
              <Card key={ds.name} className="card-hover">
                <CardContent className="pt-4">
                  <h3 className="font-semibold text-sm mb-1">{ds.name}</h3>
                  <p className="text-xs text-muted-foreground mb-3 leading-relaxed">{ds.desc}</p>
                  <a
                    href={ds.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-teal-600 hover:underline"
                  >
                    <ExternalLink className="w-3 h-3" />
                    {ds.source}
                  </a>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* ── CYP Enzyme Pathways ───────────────────────────── */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">CYP Enzyme Pathways</CardTitle>
          <p className="text-sm text-muted-foreground">
            Key metabolic enzymes tracked for drug interaction prediction
          </p>
        </CardHeader>
        <CardContent>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {[
              { name: "CYP3A4", pct: "~50%", desc: "Most abundant. Metabolizes statins, CCBs, many others." },
              { name: "CYP2C9", pct: "~15%", desc: "NSAIDs, warfarin. Genetic polymorphisms common." },
              { name: "CYP2C19", pct: "~10%", desc: "PPIs, clopidogrel. Poor metabolizers at risk." },
              { name: "CYP2D6", pct: "~25%", desc: "Beta-blockers, antidepressants, opioids." },
              { name: "CYP1A2", pct: "~5%", desc: "Caffeine, warfarin. Inhibited by ciprofloxacin." },
              { name: "CYP2E1", pct: "~3%", desc: "Acetaminophen → toxic NAPQI. Induced by alcohol." },
            ].map((enzyme) => (
              <div key={enzyme.name} className="p-3 border rounded-lg">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-sm text-teal-700">{enzyme.name}</span>
                  <Badge variant="secondary" className="text-xs">{enzyme.pct} of drugs</Badge>
                </div>
                <p className="text-xs text-muted-foreground">{enzyme.desc}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* ── Tech Stack ────────────────────────────────────── */}
      {/* <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Technology Stack</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid sm:grid-cols-2 gap-4 text-sm">
            <div>
              <h3 className="font-semibold mb-2 text-teal-700">Frontend</h3>
              <ul className="space-y-1 text-muted-foreground">
                <li>• Next.js 15 (App Router, React 19)</li>
                <li>• Tailwind CSS v4 + ShadCN UI</li>
                <li>• Cytoscape.js (graph visualization)</li>
                <li>• Lucide React (icons)</li>
                <li>• TypeScript</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-2 text-teal-700">Backend</h3>
              <ul className="space-y-1 text-muted-foreground">
                <li>• Python + FastAPI</li>
                <li>• PyTorch (GNN model)</li>
                <li>• RDKit (molecular fingerprints)</li>
                <li>• PubChem API + OpenFDA API</li>
                <li>• ReportLab (PDF generation)</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card> */}

      {/* ── Authors ───────────────────────────────────────── */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Users className="w-5 h-5 text-teal-600" />
            Research Authors
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid sm:grid-cols-2 gap-4">
            {[
              { name: "Keerthika Nimmagadda", role: "Dept. of CSE (SCOPE), VIT-AP University" },
              { name: "Anshu Kondru", role: "Dept. of CSE (SCOPE), VIT-AP University" },
              { name: "Harini Tummala", role: "Dept. of CSE (SCOPE), VIT-AP University" },
              { name: "Shaik Moinuddin Ahmed", role: "Assistant Professor, School of AIML, VIT-AP University" },
            ].map((author) => (
              <div key={author.name} className="flex items-center gap-3 p-3 rounded-lg bg-muted/30">
                <div className="w-10 h-10 rounded-full bg-teal-100 flex items-center justify-center text-teal-700 font-semibold text-sm">
                  {author.name.charAt(0)}
                </div>
                <div>
                  <div className="font-medium text-sm">{author.name}</div>
                  <div className="text-xs text-muted-foreground">{author.role}</div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
