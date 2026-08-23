/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import type { Config } from "typescript";
export const tsConfigBase: Config = { compilerOptions: { target: "ES2022", lib: ["ES2022"], module: "ESNext", moduleResolution: "Bundler", noEmit: true, strict: true, skipLibCheck: true } };
export const APP_NAME = "ciafagent-api";
export const PORT = 8794;
export const RATE_LIMIT_PER_MIN = 600;
