/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef operation-catalog route.
 *
 * Wholesale source: hmgcc/CyberChef/ (Apache 2.0).
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import { createFileRoute } from "@tanstack/react-router";

const WRAPPED_OPERATIONS: string[] = [
  "From_Base64",
  "To_Base64",
  "From_Hex",
  "To_Hex",
  "URL_Decode",
  "URL_Encode",
  "HTML_Encode",
  "HTML_Decode",
  "SHA2",
  "SHA3",
  "MD5",
  "AES_Decrypt",
  "AES_Encrypt",
  "XKCD_Extract_IPv6",
  "Extract_IPv6_Addresses",
  "Parse_Certificate",
  "JSON_Beautify",
  "JSON_Minify",
  "XML_Beautify",
  "CSV_to_JSON",
  "Regular_expression",
  "Search_Replace",
  "Split",
  "Merge",
  "Sort",
  "Unique",
  "Reverse",
];

export const Route = createFileRoute("/operation-catalog")({
  component: () => (
    <div className="max-w-4xl mx-auto p-8 text-slate-200">
      <h1 className="text-2xl font-bold text-cyan-300 mb-4">
        CyberChef Operation Catalog
      </h1>
      <p className="text-slate-400 text-sm mb-4">
        {WRAPPED_OPERATIONS.length} operations (out of 300+ in upstream
        GCHQ CyberChef, Apache 2.0). Mirrors
        <code> CyberChefRecipePipeline.CYBERCHEF_OPERATIONS </code>.
      </p>
      <ul className="grid grid-cols-3 gap-2 text-sm">
        {WRAPPED_OPERATIONS.map((op) => (
          <li
            key={op}
            className="bg-cyan-950 border border-cyan-900 rounded px-3 py-2 font-mono text-cyan-200"
          >
            {op}
          </li>
        ))}
      </ul>
    </div>
  ),
});
