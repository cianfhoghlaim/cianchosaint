// BAML extraction schema for the BIOD v1 narrative deep-dive.
//
// Per openspec/changes/cianchosaint-narrative-deep-dive-v1/specs/cianchosaint-narrative-deep-dive/spec.md,
// Requirement: The NarrativeContext BAML extraction.
//
// Mirrors cianfhoghlaim's agent-valley-archive archive/agent.py::VESPER's narrative arc:
// "Why this visitor cares about the object they brought, what they have
// already tried to fix it, and what they are or are not willing to do about it."
//
// Routes through the 4-tier client chain (Primary → Fallback → Emergency →
// LastResort) declared in baml_src/clients.baml per cianchosaint-bootstrap-v2 spec.
//
// Licence: BUSL-1.1 (per LICENSE.md)

class NarrativeContext {
  subject_name string
  narrative_summary string
  opening_question string
  constraints string[]
  closed_topics string[]
}

function ExtractNarrativeContext(input: string) -> NarrativeContext {
  client Primary
  resolver "langfuse"
  resolver_args { prompt_name "extract_narrative_context" }
  prompt #"
    { _.role("user") }
    You are the canonical BIOD v1 narrative analyst.
    Given the input dossier text, extract a NarrativeContext record with:
    - subject_name: the politician / entity under investigation
    - narrative_summary: a 2-3 sentence synthesis of who they are
    - opening_question: the question that started the visit
    - constraints: what the analyst will/won't do (durable only)
    - closed_topics: topics that should NOT be persisted (per the policy boundary)

    Be conservative — only return data explicitly present in the input.

    Input dossier text:
    { input }
  "#
}
