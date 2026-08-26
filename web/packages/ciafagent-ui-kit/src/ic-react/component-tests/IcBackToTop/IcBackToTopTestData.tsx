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
import React from "react";
import { IcBackToTop } from "../../components";
import {
  IcBackToTopPositions,
  IcBackToTopVariants,
  IcThemeMode,
} from "@ukic/web-components";

export const BackToTop = (props: {
  variant?: IcBackToTopVariants;
  theme: IcThemeMode;
  position?: IcBackToTopPositions;
}) => {
  const { variant, theme, position } = props;

  return (
    <div style={{ height: "120vh" }}>
      <div id="topEl" style={{ position: "absolute", top: "0", width: "100%" }}>
        Top of screen
      </div>
      <IcBackToTop
        target="topEl"
        variant={variant}
        theme={theme}
        position={position == undefined ? "right" : position}
      />
    </div>
  );
};
