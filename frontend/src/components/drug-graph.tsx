"use client";

import { useEffect, useRef, useCallback } from "react";
import type { InteractionGraph } from "@/lib/api";

/**
 * DrugGraph — Interactive drug interaction network visualization.
 * 
 * Uses Cytoscape.js to render:
 * - Drug nodes (teal circles) sized by their risk contribution
 * - Side effect nodes (colored squares) for HIGH risk effects
 * - Edges colored by risk: red = HIGH, amber = MEDIUM, green = LOW
 * - Force-directed layout that groups related drugs together
 * 
 * Cytoscape.js must be loaded client-side only (no SSR).
 */

interface DrugGraphProps {
  graph: InteractionGraph;
  height?: string;
}

export default function DrugGraph({ graph, height = "450px" }: DrugGraphProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<any>(null);

  const initGraph = useCallback(async () => {
    if (!containerRef.current || graph.nodes.length === 0) return;

    // Dynamic import — Cytoscape only works in the browser
    const cytoscape = (await import("cytoscape")).default;

    // Destroy previous instance
    if (cyRef.current) {
      cyRef.current.destroy();
    }

    // Convert our graph data to Cytoscape format
    const elements: any[] = [];

    // Add nodes
    graph.nodes.forEach((node) => {
      elements.push({
        data: {
          id: node.id,
          label: node.label,
          riskLevel: node.risk_contribution,
          nodeType: node.node_type,
        },
      });
    });

    // Add edges
    graph.edges.forEach((edge, i) => {
      elements.push({
        data: {
          id: `edge-${i}`,
          source: edge.source,
          target: edge.target,
          riskLevel: edge.risk,
          sideEffects: edge.side_effects.join(", "),
          weight: edge.weight,
        },
      });
    });

    // Risk color mapping
    const riskColor = (risk: string) => {
      switch (risk) {
        case "HIGH": return "#ef4444";
        case "MEDIUM": return "#f59e0b";
        case "LOW": return "#22c55e";
        default: return "#94a3b8";
      }
    };

    // Create Cytoscape instance
    const cy = cytoscape({
      container: containerRef.current,
      elements,
      style: [
        // Drug nodes
        {
          selector: 'node[nodeType="drug"]',
          style: {
            "background-color": "#0d9488",
            label: "data(label)",
            "text-valign": "bottom",
            "text-halign": "center",
            "font-size": "11px",
            "font-weight": "600",
            color: "#0f172a",
            "text-margin-y": 8,
            width: 40,
            height: 40,
            "border-width": 3,
            "border-color": "#ffffff",
            "overlay-opacity": 0,
            "text-background-color": "#ffffff",
            "text-background-opacity": 0.8,
            "text-background-padding": "2px",
            "text-background-shape": "roundrectangle",
          } as any,
        },
        // Side effect nodes
        {
          selector: 'node[nodeType="side_effect"]',
          style: {
            "background-color": "#fef2f2",
            "border-color": "#ef4444",
            "border-width": 2,
            shape: "round-rectangle",
            label: "data(label)",
            "text-valign": "bottom",
            "text-halign": "center",
            "font-size": "9px",
            color: "#b91c1c",
            "text-margin-y": 6,
            width: 30,
            height: 30,
            "text-background-color": "#ffffff",
            "text-background-opacity": 0.8,
            "text-background-padding": "2px",
            "text-background-shape": "roundrectangle",
          } as any,
        },
        // HIGH risk drug nodes
        {
          selector: 'node[riskLevel="HIGH"][nodeType="drug"]',
          style: {
            "background-color": "#ef4444",
            "border-color": "#ffffff",
            width: 48,
            height: 48,
          },
        },
        // MEDIUM risk drug nodes
        {
          selector: 'node[riskLevel="MEDIUM"][nodeType="drug"]',
          style: {
            "background-color": "#f59e0b",
            "border-color": "#ffffff",
            width: 44,
            height: 44,
          },
        },
        // Edges
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#cbd5e1",
            "curve-style": "bezier",
            "target-arrow-shape": "none",
            opacity: 0.7,
          },
        },
        // HIGH risk edges
        {
          selector: 'edge[riskLevel="HIGH"]',
          style: {
            "line-color": "#ef4444",
            width: 3,
            opacity: 1,
          },
        },
        // MEDIUM risk edges
        {
          selector: 'edge[riskLevel="MEDIUM"]',
          style: {
            "line-color": "#f59e0b",
            width: 2.5,
            opacity: 0.85,
          },
        },
        // LOW risk edges
        {
          selector: 'edge[riskLevel="LOW"]',
          style: {
            "line-color": "#22c55e",
            width: 2,
            opacity: 0.6,
          },
        },
      ],
      layout: {
        name: "cose",
        animate: false,
        nodeDimensionsIncludeLabels: true,
        idealEdgeLength: () => 120,
        nodeRepulsion: () => 6000,
        padding: 40,
        randomize: false,
      } as any,
      userZoomingEnabled: true,
      userPanningEnabled: true,
      boxSelectionEnabled: false,
    });

    // Add hover tooltip
    cy.on("mouseover", "node", (evt: any) => {
      const node = evt.target;
      node.style("border-width", 4);
      containerRef.current!.style.cursor = "pointer";
    });

    cy.on("mouseout", "node", (evt: any) => {
      const node = evt.target;
      node.style("border-width", node.data("nodeType") === "side_effect" ? 2 : 3);
      containerRef.current!.style.cursor = "default";
    });

    cy.on("mouseover", "edge", () => {
      containerRef.current!.style.cursor = "pointer";
    });

    cy.on("mouseout", "edge", () => {
      containerRef.current!.style.cursor = "default";
    });

    cyRef.current = cy;
  }, [graph]);

  useEffect(() => {
    initGraph();
    return () => {
      if (cyRef.current) {
        cyRef.current.destroy();
      }
    };
  }, [initGraph]);

  if (graph.nodes.length === 0) {
    return (
      <div
        className="flex items-center justify-center text-muted-foreground text-sm bg-muted/30 rounded-xl"
        style={{ height }}
      >
        Submit your drug list to see the interaction graph
      </div>
    );
  }

  return (
    <div>
      <div
        ref={containerRef}
        className="graph-container"
        style={{ height }}
      />
      {/* Legend */}
      <div className="flex flex-wrap items-center gap-4 mt-3 text-xs text-muted-foreground px-1">
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-[#ef4444] inline-block" />
          High Risk
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-[#f59e0b] inline-block" />
          Medium Risk
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-[#22c55e] inline-block" />
          Low Risk
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-[#0d9488] inline-block" />
          Drug Node
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-[#fef2f2] border border-[#ef4444] inline-block" />
          Side Effect
        </div>
      </div>
    </div>
  );
}
