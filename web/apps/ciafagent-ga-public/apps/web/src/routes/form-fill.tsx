/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// routes/form-fill.tsx — non-emergency form filling

import { createFileRoute } from "@tanstack/react-router";
import { FormFillCard } from "../components/FormFillCard";

export const Route = createFileRoute("/form-fill")({
  component: FormFillComponent,
});

function FormFillComponent() {
  return <FormFillCard jurisdiction="ga" />;
}
