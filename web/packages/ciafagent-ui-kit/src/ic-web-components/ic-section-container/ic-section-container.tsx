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
import { Component, Prop, Host, h } from "@stencil/core";
import { IcAlignment } from "../../utils/types";

@Component({
  tag: "ic-section-container",
  styleUrl: "ic-section-container.css",
  shadow: true,
})
export class SectionContainer {
  /**
   * The alignment of the container.
   */
  @Prop() aligned?: IcAlignment = "left";

  /**
   * If `true`, the standard vertical padding from the container will be removed.
   */
  @Prop() fullHeight?: boolean = false;

  render() {
    const { aligned, fullHeight } = this;
    return (
      <Host
        class={{
          ["aligned-left"]: aligned === "left" || aligned === null,
          ["aligned-center"]: aligned === "center",
          ["aligned-full-width"]: aligned === "full-width",
          ["no-vertical-padding"]: !!fullHeight,
        }}
      >
        <slot></slot>
      </Host>
    );
  }
}
