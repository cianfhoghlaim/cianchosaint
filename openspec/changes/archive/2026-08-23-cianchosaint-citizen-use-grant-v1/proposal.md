# Change: cianchosaint-citizen-use-grant-v1

## Why

The `LICENSE.md` Additional Use Grant covers production use by
British Isles public-sector bodies (Ireland / UK / Crown Dependencies).
Members of the public using cianchosaint for personal interaction
with their own government's services do NOT fall under the Additional
Use Grant as drafted.

The `cianchosaint-self-hosted-citizen` spec already exists and
provides the technical capability (Docker Compose bundle + Locket
sidecar + private Pangolin resource + per-tenant Infisical read-only
token). But the spec is explicit:

> "Until that change [the citizen use grant] lands, the self-hosted
> citizen option is **experimental** and licensed under the same grant
> as the rest of the platform."

This change ships the **Natural Person Citizen Grant** — an amendment
to `LICENSE.md` that grants natural persons of the British Isles
(who are not affiliated with the bodies in (a), (b), or (c) of the
Additional Use Grant) the right to use the Licensed Work for
non-commercial personal purposes, including self-hosted deployment.

The grant is conditioned on:

1. The citizen is a natural person.
2. The use is for non-commercial personal purposes only.
3. The prohibition on commercial monetisation in (1) of `LICENSE.md`
   is preserved.
4. No public-facing deployment (the citizen's instance is private).
5. No foreign use (foreign entities are still explicitly banned).

## What changes

- **1 NEW canonical spec**: `cianchosaint-citizen-use-grant` with 2
  ADDED Requirements:
  - Requirement: The Natural Person Citizen Grant amendment to
    `LICENSE.md`
  - Requirement: The grant preserves the prohibition on commercial
    monetisation + foreign use + public-facing deployment

- **1 MODIFIED file**: `LICENSE.md` is extended with a new "NATURAL
  PERSON CITIZEN GRANT" section that grants natural persons of the
  British Isles the right to use the Licensed Work for non-commercial
  personal purposes.

- **1 MODIFIED spec**: `openspec/specs/cianchosaint-self-hosted-citizen/spec.md`
  is updated to reference the citizen use grant amendment.

## Impact

- Affected specs: 1 NEW spec (`cianchosaint-citizen-use-grant/`) +
  1 MODIFIED spec (`cianchosaint-self-hosted-citizen/`).
- Affected code/config: 1 MODIFIED `LICENSE.md` + 1 MODIFIED
  `openspec/specs/cianchosaint-self-hosted-citizen/spec.md`.
- No secret values are written to disk.
- No runtime behaviour changes — the self-hosted citizen option
  continues to work exactly as before; this change grants a legal
  permission to British Isles citizens.

## Out of scope

- The natural-person citizen Docker Compose bundle. Already shipped
  by the `cianchosaint-self-hosted-citizen` spec (the technical
  capability exists; this change grants the legal permission).
- The per-portal credentials for the citizen use case. Covered by
  the existing wholesale-copied Cianfhoghlaim Infisical pattern.
- The natural-person citizen license verification (the citizen's
  eligibility is verified by the Pocket ID organisation membership
  pattern at runtime; this change does not add new verification
  infrastructure).

## Validation criteria

1. `openspec validate cianchosaint-citizen-use-grant-v1 --strict`
   passes (exit code 0).
2. `openspec validate cianchosaint-citizen-use-grant --strict` passes
   (exit code 0).
3. `openspec validate cianchosaint-self-hosted-citizen --strict`
   passes after the spec update.
4. `LICENSE.md` preserves the existing BUSL-1.1 v2 grant structure
   (the Additional Use Grant + the Foreign-Use Gate + the Warrant to
   enforce + the Change Date + the Change License are all preserved
   verbatim).

## Dependencies

`Blocked by: none`
`Blocked by (soft): cianchosaint-self-hosted-citizen` (extends; the
  upstream citizen capability)
`Affected repos: cianchosaint.` (Cianfhoghlaim + leabharlann remain
  completely unchanged — `LICENSE.md` is the load-bearing legal
  document for the cianchosaint repo only; the cianfhoghlaim repo
  has its own `LICENSE.md`.)

## Cross-repo sync

This change touches **ONLY the `cianchosaint` repo**. The Cianfhoghlaim
`LICENSE.md` (at `/Users/cianmacandeisigh/dev/kings_college_galway/LICENSE.md`)
remains **completely unchanged**. See `cross-repo-sync.md` for the
full commit plan.
