import Link from "next/link";
import {
  Activity,
  Shield,
  GitBranch,
  Clock,
  FileText,
  Users,
  ChevronRight,
  Pill,
  AlertTriangle,
  Brain,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <div className="animate-fade-in">
      {/* ─── Hero Section ──────────────────────────────────── */}
      <section className="hospital-gradient text-white py-20 relative overflow-hidden">
        {/* Subtle grid pattern */}
        <div
          className="absolute inset-0 opacity-[0.04]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.3) 1px, transparent 1px)",
            backgroundSize: "40px 40px",
          }}
        />
        <div className="max-w-5xl mx-auto px-4 sm:px-6 text-center relative z-10">
          <div className="inline-flex items-center gap-2 bg-white/15 rounded-full px-4 py-1.5 text-sm mb-6">
            <Activity className="w-4 h-4" />
            AI-Powered Drug Interaction Analysis
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight mb-5 leading-tight">
            Predicting Complex Drug
            <br />
            Interactions with{" "}
            <span className="text-teal-200">Graph Intelligence</span>
          </h1>
          <p className="text-lg text-white/75 max-w-2xl mx-auto mb-8 leading-relaxed">
            Interactome-AI analyzes your entire medication regimen to detect
            higher-order adverse reactions using Graph Neural Networks — going
            beyond pairwise checks to find risks that traditional methods miss.
          </p>
          <div className="flex items-center justify-center gap-3">
            <Link href="/predictor">
              <Button
                size="lg"
                className="bg-white text-teal-700 hover:bg-teal-50 font-semibold px-6 shadow-lg"
              >
                Try Prediction
                <ChevronRight className="w-4 h-4 ml-1" />
              </Button>
            </Link>
            <Link href="/insights">
              <Button
                size="lg"
                variant="outline"
                className="bg-white text-teal-700 hover:bg-white/10 px-6"
              >
                Learn More
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* ─── Stats Bar ─────────────────────────────────────── */}
      <section className="bg-white border-b py-6">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 text-center">
            {[
              { value: "20+", label: "Drugs in Database" },
              { value: "27", label: "Pairwise Interactions" },
              { value: "12", label: "Multi-Drug Combos" },
              { value: "6", label: "CYP Enzyme Pathways" },
            ].map((stat) => (
              <div key={stat.label}>
                <div className="text-2xl font-bold text-teal-600">
                  {stat.value}
                </div>
                <div className="text-sm text-muted-foreground mt-0.5">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── How It Works ──────────────────────────────────── */}
      <section className="py-16 bg-background">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-bold text-foreground">
              How It Works
            </h2>
            <p className="text-muted-foreground mt-2">
              Three simple steps to analyze your medication safety
            </p>
          </div>
          <div className="grid sm:grid-cols-3 gap-8">
            {[
              {
                step: "1",
                icon: Pill,
                title: "Enter Medications",
                desc: "Type in all the drugs you're currently taking. Our autocomplete searches the PubChem database for accurate matches.",
              },
              {
                step: "2",
                icon: Brain,
                title: "AI Analyzes",
                desc: "Our Graph Neural Network builds a drug interaction network and predicts pairwise AND multi-drug adverse reactions.",
              },
              {
                step: "3",
                icon: Shield,
                title: "Get Results",
                desc: "View risk levels, side effects, explanations, medication timing, and an interactive graph of all interactions.",
              },
            ].map((item) => (
              <Card key={item.step} className="card-hover border-0 shadow-sm bg-white">
                <CardContent className="pt-6 text-center">
                  <div className="w-12 h-12 rounded-xl bg-teal-50 flex items-center justify-center mx-auto mb-4">
                    <item.icon className="w-6 h-6 text-teal-600" />
                  </div>
                  <div className="text-xs font-semibold text-teal-600 mb-1">
                    STEP {item.step}
                  </div>
                  <h3 className="font-semibold text-lg mb-2">{item.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {item.desc}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Key Features ──────────────────────────────────── */}
      <section className="py-16 bg-white">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-bold text-foreground">
              Key Features
            </h2>
            <p className="text-muted-foreground mt-2">
              Built for patient safety with advanced AI technology
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                icon: GitBranch,
                title: "Multi-Drug Analysis",
                desc: "Goes beyond pairwise — analyzes 3, 4, or more drugs together to find emergent interactions.",
              },
              {
                icon: AlertTriangle,
                title: "Risk Classification",
                desc: "Each interaction rated as LOW, MEDIUM, or HIGH risk with confidence scores.",
              },
              {
                icon: Activity,
                title: "Graph Visualization",
                desc: "Interactive network graph shows all drugs and how they're connected by interactions.",
              },
              {
                icon: FileText,
                title: "Explainable AI",
                desc: "Every prediction includes a clear explanation — which enzymes, pathways, and mechanisms are involved.",
              },
              {
                icon: Clock,
                title: "Medication Timing",
                desc: "Suggests optimal timing gaps between medications to minimize interaction risk.",
              },
              {
                icon: Users,
                title: "Patient Profiles",
                desc: "Adjusts risk for age, BMI, and existing conditions — elderly patients get appropriately flagged.",
              },
            ].map((feature) => (
              <div
                key={feature.title}
                className="flex gap-4 p-4 rounded-xl hover:bg-teal-50/50 transition-colors"
              >
                <div className="w-10 h-10 rounded-lg bg-teal-50 flex items-center justify-center shrink-0">
                  <feature.icon className="w-5 h-5 text-teal-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-sm mb-1">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {feature.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── CTA ──────────────────────────────────────────── */}
      <section className="py-14 bg-teal-50 border-y">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 text-center">
          <h2 className="text-2xl font-bold mb-3">
            Check Your Medication Safety Now
          </h2>
          <p className="text-muted-foreground mb-6">
            Enter your medication list and get an instant AI-powered risk
            analysis with detailed explanations.
          </p>
          <Link href="/predictor">
            <Button
              size="lg"
              className="bg-teal-600 hover:bg-teal-700 text-white font-semibold px-8"
            >
              <FlaskConical className="w-4 h-4 mr-2" />
              Start Analysis
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}

function FlaskConical(props: React.SVGProps<SVGSVGElement> & { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2" />
      <path d="M8.5 2h7" />
      <path d="M7 16h10" />
    </svg>
  );
}
