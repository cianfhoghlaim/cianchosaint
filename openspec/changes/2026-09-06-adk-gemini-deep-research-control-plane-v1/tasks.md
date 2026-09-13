# Tasks: cianchosaint mirror

## Stage 0 — Pre-flight
- [ ] T0.1 — Confirm the parent change is archived
- [ ] T0.2 — Add the cianchosaint-specific opt-in flag

## Stage 1 — Spec delta
- [ ] T1.1 — Write `openspec/specs/adk-deep-research-control-plane/spec.md` (mirror)
- [ ] T1.2 — Write the change's `specs/adk-deep-research-control-plane/spec.md` delta

## Stage 2 — Routing keywords
- [ ] T2.1 — Add `gemini_deep_research` bucket to `agents/routing_keywords.py`

## Stage 3 — Agent opt-in
- [ ] T3.1 — Add `gemini_deep_research_opted_in` to cianchosaint agent config
- [ ] T3.2 — Modify the root agent to skip registration when opted out

## Stage 4 — DLT + BAML mirrors
- [ ] T4.1 — Copy `dlt_sources/_shared/gemini_deep_research.py` from parent
- [ ] T4.2 — Copy `baml_src/_shared/gemini_deep_research.baml` from parent

## Stage 5 — Validation
- [ ] T5.1 — Run `openspec validate 2026-09-06-adk-gemini-deep-research-control-plane-v1 --strict`
