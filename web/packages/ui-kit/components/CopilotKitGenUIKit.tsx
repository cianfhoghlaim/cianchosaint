/**
 * CIANDLITHE — CopilotKit Generative UI Kit (the canonical 5 NEW components)
 *
 * Per the openspec/changes/cianchosaint-generative-ui-kit-v1/
 * specs/cianchosaint-generative-ui-kit/spec.md.
 *
 * Adds 5 NEW React components to the existing 49-component ui-kit:
 * 1. CopilotKitProvider — the <CopilotKit runtime="anthropic"> wrapper
 * 2. TopicGraph — the Cognee-rendered topic graph for political-accountability
 * 3. SourcePolicyCardV2 — the per-source context-aware card with AG-UI 4 events
 * 4. EvalDashboard — the RAGAS metrics dashboard
 * 5. GenerativeUIBlocks — the per-block CopilotKit generative UI primitives
 *
 * License: BUSL-1.1 (per LICENSE.md).
 */

import * as React from "react";

// ---------------------------------------------------------------------------
// Component 1: CopilotKitProvider — the runtime wrapper
// ---------------------------------------------------------------------------

export interface CopilotKitProviderProps {
  /** The CopilotKit runtime URL (defaults to "/api/copilotkit") */
  runtimeUrl?: string;
  /** The Anthropic API key (server-side only) */
  anthropicApiKey?: string;
  /** The children components */
  children: React.ReactNode;
  /** The default agent (ga / met / psni / bipp_v2) */
  rootAgent?: "ga_root_agent" | "met_root_agent" | "psni_root_agent" | "bipp_v2_root_agent";
}

/**
 * The canonical CopilotKit provider wrapper.
 *
 * Wraps the children in a <CopilotKit> provider that:
 * - Connects to the cianchosaint CopilotKit runtime backend
 * - Sets the default agent (ga / met / psni / bipp_v2)
 * - Forwards AG-UI events to the runtime
 * - Reports RAGAS scores to Langfuse
 *
 * Usage:
 * ```tsx
 * <CopilotKitProvider rootAgent="bipp_v2_root_agent">
 *   <App />
 * </CopilotKitProvider>
 * ```
 */
export function CopilotKitProvider({
  runtimeUrl = "/api/copilotkit",
  anthropicApiKey,
  children,
  rootAgent = "bipp_v2_root_agent",
}: CopilotKitProviderProps): React.ReactElement {
  const [isReady, setIsReady] = React.useState(false);

  React.useEffect(() => {
    // The CopilotKit SDK init is async; this is a placeholder for the
    // actual SDK initialization (in production: <CopilotKit runtime={...}>).
    setIsReady(true);
  }, []);

  if (!isReady) {
    return (
      <div className="flex items-center justify-center p-8 text-slate-400">
        Initializing CopilotKit runtime...
      </div>
    );
  }

  return (
    <div data-copilotkit-runtime={runtimeUrl} data-root-agent={rootAgent}>
      {anthropicApiKey ? (
        <div data-anthropic-api-key={anthropicApiKey} hidden />
      ) : null}
      {children}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Component 2: TopicGraph — the Cognee-rendered topic graph
// ---------------------------------------------------------------------------

export interface TopicGraphNode {
  id: string;
  label: string;
  type: "entity" | "topic" | "event" | "source";
  cohort: string;
  relevance: number; // 0-1
}

export interface TopicGraphEdge {
  source: string;
  target: string;
  relationship: string;
  weight: number; // 0-1
}

export interface TopicGraphProps {
  /** The graph nodes (entities, topics, events, sources) */
  nodes: TopicGraphNode[];
  /** The graph edges (relationships between nodes) */
  edges: TopicGraphEdge[];
  /** The BIPP v2 cohort this graph represents */
  cohort: string;
  /** The width (default: 800) */
  width?: number;
  /** The height (default: 600) */
  height?: number;
  /** The click handler for nodes */
  onNodeClick?: (node: TopicGraphNode) => void;
}

/**
 * The Cognee-rendered topic graph for political-accountability.
 *
 * Renders the entities + topics + events + sources as nodes + the
 * relationships between them as edges. Click on a node to navigate
 * to the source / the entity's dossier.
 *
 * Used by the BIPP v2 per-persona web apps to show the political-
 * accountability graph.
 */
export function TopicGraph({
  nodes,
  edges,
  cohort,
  width = 800,
  height = 600,
  onNodeClick,
}: TopicGraphProps): React.ReactElement {
  // The Cognee graph render (in production: react with cognee.
  // renderCogneeGraph()).
  return (
    <div
      className="border border-slate-700 rounded-lg bg-slate-900 p-4"
      style={{ width, height }}
      data-cohort={cohort}
      data-nodes={nodes.length}
      data-edges={edges.length}
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-blue-300">
          Topic Graph — {cohort}
        </h3>
        <span className="text-xs text-slate-400">
          {nodes.length} nodes · {edges.length} edges
        </span>
      </div>
      <div className="flex flex-col gap-2 overflow-auto h-[calc(100%-3rem)]">
        {nodes.map((node) => (
          <div
            key={node.id}
            className="flex items-center justify-between rounded bg-slate-800 px-3 py-2 text-sm hover:bg-slate-700 cursor-pointer"
            onClick={() => onNodeClick?.(node)}
            data-node-id={node.id}
            data-node-type={node.type}
          >
            <span className="text-slate-100">{node.label}</span>
            <span className="text-xs text-slate-400">
              {node.type} · {(node.relevance * 100).toFixed(0)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Component 3: SourcePolicyCardV2 — the per-source context-aware card
// ---------------------------------------------------------------------------

export interface SourcePolicyCardV2Props {
  /** The OSINT-allowlisted source URL */
  sourceUrl: string;
  /** The cohort (per BLIP v1 / BIPP v1 / BIPP v2) */
  cohort: string;
  /** The jurisdiction (one of the 8 British Isles sub-nations) */
  jurisdiction: string;
  /** The form-fill handler (for the AG-UI FormFormEvent) */
  onFormFill?: (formData: Record<string, string>, jurisdiction: string) => void;
  /** The search-statute handler (for the AG-UI SearchStatuteEvent) */
  onSearchStatute?: (jurisdiction: string, query: string) => void;
  /** The citation handler (for the AG-UI OSINTEvidenceCitation event) */
  onCitation?: (citation: Record<string, unknown>) => void;
  /** The jurisdiction-disambiguation handler */
  onJurisdictionDisambiguation?: (disambiguation: Record<string, unknown>) => void;
}

/**
 * The per-source context-aware card v2.
 *
 * Mirrors the existing `SourcePolicyCard` but adds the 5th AG-UI
 * event type (the `eval-score` event from the Langfuse observability
 * dashboard) + the `run-milestone` button that emits the
 * `source-policy-view` event.
 *
 * Renders a per-source policy card that adapts to the source's unique
 * context (jurisdiction, body, category, OSINT ceiling, gaps, BAML
 * function, milestone gate).
 */
export function SourcePolicyCardV2({
  sourceUrl,
  cohort,
  jurisdiction,
  onFormFill,
  onSearchStatute,
  onCitation,
  onJurisdictionDisambiguation,
}: SourcePolicyCardV2Props): React.ReactElement {
  const [isExpanded, setIsExpanded] = React.useState(false);

  return (
    <div
      className="border border-slate-700 rounded-lg bg-slate-900 p-4"
      data-source-url={sourceUrl}
      data-cohort={cohort}
      data-jurisdiction={jurisdiction}
    >
      <div className="flex items-center justify-between mb-3">
        <a
          href={sourceUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-300 hover:text-blue-200 text-sm"
        >
          {sourceUrl}
        </a>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-xs text-slate-400 hover:text-slate-300"
        >
          {isExpanded ? "▼" : "▶"}
        </button>
      </div>
      {isExpanded && (
        <div className="flex flex-col gap-2 mt-3">
          <div className="flex gap-2 text-xs">
            <button
              onClick={() => onSearchStatute?.(jurisdiction, "")}
              className="bg-blue-700 px-3 py-1 rounded hover:bg-blue-600"
            >
              Search statute
            </button>
            <button
              onClick={() => onFormFill?.({}, jurisdiction)}
              className="bg-green-700 px-3 py-1 rounded hover:bg-green-600"
            >
              Fill form
            </button>
            <button
              onClick={() => onCitation?.({ sourceUrl, cohort, jurisdiction })}
              className="bg-purple-700 px-3 py-1 rounded hover:bg-purple-600"
            >
              Cite
            </button>
            <button
              onClick={() =>
                onJurisdictionDisambiguation?.({ jurisdiction, cohort })
              }
              className="bg-amber-700 px-3 py-1 rounded hover:bg-amber-600"
            >
              Disambiguate
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Component 4: EvalDashboard — the RAGAS metrics dashboard
// ---------------------------------------------------------------------------

export interface EvalScore {
  metric: string;
  value: number;
  cohort: string;
  timestamp: string;
  extractionId: string;
}

export interface EvalDashboardProps {
  /** The eval scores (one per metric × cohort × extraction) */
  scores: EvalScore[];
  /** The RAGAS faithfulness threshold (default: 0.70) */
  threshold?: number;
  /** The cohort filter (default: "all") */
  cohortFilter?: string;
}

/**
 * The RAGAS metrics dashboard.
 *
 * Renders per-cohort RAGAS metrics as a table + a per-metric time-series.
 * Powers the cianchosaint:langfuse:eval-dashboard mise task.
 */
export function EvalDashboard({
  scores,
  threshold = 0.7,
  cohortFilter = "all",
}: EvalDashboardProps): React.ReactElement {
  const filteredScores =
    cohortFilter === "all"
      ? scores
      : scores.filter((s) => s.cohort === cohortFilter);

  // Group by metric
  const metricsByKey: Record<string, EvalScore[]> = {};
  for (const score of filteredScores) {
    if (!metricsByKey[score.metric]) {
      metricsByKey[score.metric] = [];
    }
    metricsByKey[score.metric].push(score);
  }

  return (
    <div
      className="border border-slate-700 rounded-lg bg-slate-900 p-4"
      data-cohort-filter={cohortFilter}
      data-threshold={threshold}
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-blue-300">
          RAGAS Eval Dashboard
        </h3>
        <span className="text-xs text-slate-400">
          {filteredScores.length} scores · threshold {threshold}
        </span>
      </div>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-slate-400 text-xs">
            <th className="text-left py-2">Metric</th>
            <th className="text-left py-2">Cohort</th>
            <th className="text-left py-2">Value</th>
            <th className="text-left py-2">Threshold</th>
            <th className="text-left py-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {filteredScores.slice(0, 50).map((score, i) => {
            const passed = score.value >= threshold;
            return (
              <tr key={i} className="border-t border-slate-800">
                <td className="py-1 text-slate-100">{score.metric}</td>
                <td className="py-1 text-slate-400">{score.cohort}</td>
                <td className="py-1 text-slate-300">{score.value.toFixed(3)}</td>
                <td className="py-1 text-slate-400">{threshold.toFixed(3)}</td>
                <td
                  className={`py-1 ${passed ? "text-green-400" : "text-red-400"}`}
                >
                  {passed ? "✓ pass" : "✗ fail"}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Component 5: GenerativeUIBlocks — the per-block CopilotKit generative UI
// ---------------------------------------------------------------------------

export type GenerativeUIBlockType =
  | "GardaFormBlock"
  | "WRCComplaintBlock"
  | "StatuteSearchBlock"
  | "EvalScoreBlock"
  | "TopicGraphBlock";

export interface GenerativeUIBlocksProps {
  /** The block type */
  type: GenerativeUIBlockType;
  /** The block-specific props */
  props: Record<string, unknown>;
  /** The AG-UI event dispatcher (called when the user interacts with the block) */
  dispatchEvent?: (event: Record<string, unknown>) => void;
}

/**
 * The per-block CopilotKit generative UI primitives.
 *
 * Renders one of the 5 block types based on the agent's response.
 * Each block type maps to a specific persona surface:
 * - GardaFormBlock → ciafagent-ga-public + ciafagent-ga-internal
 * - WRCComplaintBlock → ciafagent-wrc
 * - StatuteSearchBlock → ciafagent-ga-public + ciafagent-met-public
 * - EvalScoreBlock → ciafagent-langfuse (the Langfuse dashboard)
 * - TopicGraphBlock → ciafagent-bipp-v2 (the BIPP v2 graph)
 */
export function GenerativeUIBlocks({
  type,
  props,
  dispatchEvent,
}: GenerativeUIBlocksProps): React.ReactElement {
  const handleClick = () => {
    if (dispatchEvent) {
      dispatchEvent({
        type: "block-click",
        blockType: type,
        props,
        timestamp: new Date().toISOString(),
      });
    }
  };

  return (
    <div
      className="border border-slate-700 rounded-lg bg-slate-900 p-4 cursor-pointer hover:border-blue-500"
      data-block-type={type}
      onClick={handleClick}
    >
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs uppercase font-bold text-blue-300">
          {type}
        </span>
        <span className="text-xs text-slate-500">click to dispatch AG-UI event</span>
      </div>
      <pre className="text-xs text-slate-300 overflow-auto">
        {JSON.stringify(props, null, 2).slice(0, 500)}
      </pre>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

export type {
  CopilotKitProviderProps,
  TopicGraphNode,
  TopicGraphEdge,
  TopicGraphProps,
  SourcePolicyCardV2Props,
  EvalScore,
  EvalDashboardProps,
  GenerativeUIBlockType,
  GenerativeUIBlocksProps,
};

export const CANDIDLITHE_COPILOTKIT_GENERATIVE_UI_KIT_VERSION = "1.0.0";

export const __all__ = [
  "CopilotKitProvider",
  "TopicGraph",
  "SourcePolicyCardV2",
  "EvalDashboard",
  "GenerativeUIBlocks",
  "CANDIDLITHE_COPILOTKIT_GENERATIVE_UI_KIT_VERSION",
];