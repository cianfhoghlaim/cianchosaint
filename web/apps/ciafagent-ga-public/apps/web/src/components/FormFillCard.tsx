/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// components/FormFillCard.tsx — non-emergency form filling UI

import * as React from "react";
import { useProviderChain } from "../hooks/useProviderChain";

interface FormFillCardProps {
  jurisdiction: "ga" | "met" | "psni";
}

interface FormField {
  name: string;
  label: string;
  type: "text" | "email" | "date" | "textarea" | "select";
  required: boolean;
  options?: string[];
  value: string;
}

interface FormDefinition {
  formType: string;
  title: string;
  description: string;
  fields: Array<Omit<FormField, "value">>;
}

export function FormFillCard({ jurisdiction }: FormFillCardProps) {
  const [formType, setFormType] = React.useState<string>("");
  const [fields, setFields] = React.useState<FormField[]>([]);
  const [submitted, setSubmitted] = React.useState(false);
  const { providerTier } = useProviderChain();

  const availableForms: FormDefinition[] = React.useMemo(() => {
    if (jurisdiction === "ga") {
      return [
        {
          formType: "lost_property",
          title: "Lost property report",
          description: "Report lost property to the Gardaí.",
          fields: [
            { name: "name", label: "Your name", type: "text", required: true },
            { name: "email", label: "Email", type: "email", required: true },
            { name: "item", label: "Item description", type: "textarea", required: true },
            { name: "date_lost", label: "Date lost", type: "date", required: true },
            { name: "station", label: "Preferred Garda station", type: "select", required: false, options: ["Dublin", "Cork", "Galway", "Limerick", "Other"] },
          ],
        },
        {
          formType: "minor_crime",
          title: "Minor crime report (non-emergency)",
          description: "Report a non-emergency minor crime (theft, damage).",
          fields: [
            { name: "name", label: "Your name", type: "text", required: true },
            { name: "email", label: "Email", type: "email", required: true },
            { name: "incident_date", label: "Date of incident", type: "date", required: true },
            { name: "location", label: "Location", type: "text", required: true },
            { name: "description", label: "Description", type: "textarea", required: true },
          ],
        },
      ];
    }
    return [];
  }, [jurisdiction]);

  const handleFormTypeChange = (t: string) => {
    setFormType(t);
    const form = availableForms.find((f) => f.formType === t);
    if (form) {
      setFields(form.fields.map((f) => ({ ...f, value: "" })));
    }
  };

  const updateField = (name: string, value: string) => {
    setFields((fs) => fs.map((f) => (f.name === name ? { ...f, value } : f)));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = Object.fromEntries(fields.map((f) => [f.name, f.value]));
    // POST to the api gateway via /api/form-fill
    await fetch("/api/form-fill", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ formType, jurisdiction, payload, providerTier }),
    });
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div className="max-w-2xl mx-auto p-8">
        <div className="bg-emerald-900 border border-emerald-700 rounded-lg p-6">
          <h2 className="font-bold text-emerald-300 mb-2">Form submitted</h2>
          <p className="text-emerald-200 text-sm">
            Your {formType.replace("_", " ")} report has been received. You will receive a
            confirmation email within 24 hours.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-8 flex flex-col gap-6">
      <h1 className="text-3xl font-bold text-emerald-400">Non-emergency form filling</h1>
      <div>
        <label className="block text-sm text-slate-300 mb-2">Form type</label>
        <select
          value={formType}
          onChange={(e) => handleFormTypeChange(e.target.value)}
          className="w-full bg-slate-800 text-slate-100 rounded px-3 py-2 text-sm"
        >
          <option value="">Select a form…</option>
          {availableForms.map((f) => (
            <option key={f.formType} value={f.formType}>
              {f.title}
            </option>
          ))}
        </select>
      </div>
      {formType && (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {fields.map((f) => (
            <div key={f.name}>
              <label className="block text-sm text-slate-300 mb-1">
                {f.label}{f.required && <span className="text-red-400"> *</span>}
              </label>
              {f.type === "textarea" ? (
                <textarea
                  value={f.value}
                  onChange={(e) => updateField(f.name, e.target.value)}
                  required={f.required}
                  className="w-full bg-slate-800 text-slate-100 rounded px-3 py-2 text-sm"
                />
              ) : f.type === "select" ? (
                <select
                  value={f.value}
                  onChange={(e) => updateField(f.name, e.target.value)}
                  required={f.required}
                  className="w-full bg-slate-800 text-slate-100 rounded px-3 py-2 text-sm"
                >
                  <option value="">Select…</option>
                  {f.options?.map((o) => (
                    <option key={o} value={o}>{o}</option>
                  ))}
                </select>
              ) : (
                <input
                  type={f.type}
                  value={f.value}
                  onChange={(e) => updateField(f.name, e.target.value)}
                  required={f.required}
                  className="w-full bg-slate-800 text-slate-100 rounded px-3 py-2 text-sm"
                />
              )}
            </div>
          ))}
          <button
            type="submit"
            className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded text-sm"
          >
            Submit
          </button>
        </form>
      )}
    </div>
  );
}
