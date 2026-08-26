/**
 * CIANCHOSAINT wholesale-copy of mi6/ic-ui-kit.
 *
 * Original: mi6/ic-ui-kit (https://github.com/mi6/ic-ui-kit, MIT + OGL-3.0).
 * Wholesale-copied into cianchosaint: 2026-08-26 per
 * openspec/changes/2026-08-26-cianchosaint-ic-ui-kit-integration-v1/
 * specs/cianchosaint-ic-ui-kit-integration/spec.md.
 *
 * Upstream licences (preserved):
 *   - MIT (https://github.com/mi6/ic-ui-kit/blob/main/LICENSE)
 *   - Open Government Licence v3.0 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)
 *
 * Cianchosaint licence:
 *   - BUSL-1.1 v2 (CIANCHOSAINT edition, per LICENSE.md) — British-Isles-only.
 *   - This file is part of the ciafagent UI kit that wraps the IC Design System
 *     for British-Isles defence / policing / intelligence-oversight analysts.
 *
 * Namespace: cianchosaint (every reference is renamed from the upstream
 * `ukic` / `@ukic` package scope to the `cianchosaint` workspace scope
 * during build via the cianchosaint @ukic/* package aliases).
 */
// Compatible with IcMenuOption, but stricter
export type IcSelectOption =
  | IcSelectOptionBase
  | IcSelectOptionGroup
  | IcSelectOptionLoading
  | IcSelectOptionTimedOut;

type IcSelectOptionElement = {
  component: any;
  ariaLabel: string;
};

export type IcSelectOptionBase = {
  label: string;
  value: string;
  description?: string;
  disabled?: boolean;
  recommended?: boolean;
  icon?: string;
  hideLabel?: boolean;
  htmlProps?: Record<string, string>;
  element?: IcSelectOptionElement;
};

export type IcSelectOptionGroup = {
  label: string;
  children: IcSelectOptionBase[];
};

type IcSelectOptionLoading = {
  label: string;
  value: "";
  loading: true;
};

type IcSelectOptionTimedOut = {
  label: string;
  value: "";
  timedOut: true;
};

export type IcSelectOptionFlat = {
  label: string;
  value: string;
  description?: string;
  disabled?: boolean;
  recommended?: boolean;
  icon?: string;
  hideLabel?: boolean;
  htmlProps?: Record<string, string>;
  element?: IcSelectOptionElement;
  group?: string;
};
