/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// Internal FormFillCard — for Garda internal forms (incident reports, member admin)
import * as React from "react";

interface FormFillCardProps {
  jurisdiction: "ga";
}

export function FormFillCard({ jurisdiction }: FormFillCardProps) {
  const [formType, setFormType] = React.useState<string>("");
  const [_fields, _setFields] = React.useState<Record<string, string>>({});

  const forms = [
    { id: "incident_report", label: "Incident report (internal)" },
    { id: "member_admin", label: "Member admin form" },
    { id: "evidence_log", label: "Evidence log entry" },
  ];

  return (
    <div className="max-w-2xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-blue-300">Internal form filling</h1>
      <div className="bg-slate-900 border border-blue-900 rounded p-6">
        <label className="block text-sm text-slate-300 mb-2">Form type</label>
        <select value={formType} onChange={(e) => setFormType(e.target.value)} className="w-full bg-slate-800 text-slate-100 rounded px-3 py-2 text-sm">
          <option value="">Select a form…</option>
          {forms.map((f) => <option key={f.id} value={f.id}>{f.label}</option>)}
        </select>
        {formType && (
          <p className="text-slate-400 text-sm mt-3">
            Form {formType} selected. The full form will render dynamically.
          </p>
        )}
        <p className="text-xs text-slate-500 mt-3">Jurisdiction: {jurisdiction}</p>
      </div>
    </div>
  );
}
