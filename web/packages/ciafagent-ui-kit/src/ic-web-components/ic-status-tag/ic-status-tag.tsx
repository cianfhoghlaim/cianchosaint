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
import { Component, Host, h, Prop } from "@stencil/core";
import { onComponentRequiredPropUndefined } from "../../utils/helpers";
import { IcStatusTagStatuses } from "./ic-status-tag.types";
import { IcEmphasisType, IcSizes } from "../../utils/types";

@Component({
  tag: "ic-status-tag",
  styleUrl: "ic-status-tag.css",
  shadow: true,
})
export class StatusTag {
  /**
   * If `true`, role='status' is added to the component and it will act as an 'aria-live' region.
   * Screen readers will announce changes to the `label`, but not the initial value.
   */
  @Prop() announced?: boolean = false;

  /**
   * The content rendered within the status tag.
   */
  @Prop() label!: string;

  /**
   * The size of the status tag component.
   */
  @Prop() size?: IcSizes = "medium";

  /**
   * The colour of the status tag.
   */
  @Prop() status?: IcStatusTagStatuses = "neutral";

  /**
   * Sets the theme color to the dark or light theme color. "inherit" will set the color based on the system settings or ic-theme component.
   */
  @Prop() theme?: "dark" | "light" | "inherit" = "inherit";

  /**
   * The letter case of the status tag's label.
   */
  @Prop() uppercase?: boolean = true;

  /**
   * The emphasis of the status tag.
   */
  @Prop() variant?: IcEmphasisType = "filled";

  componentDidLoad(): void {
    onComponentRequiredPropUndefined(
      [{ prop: this.label, propName: "label" }],
      "Status Tag"
    );
  }

  render() {
    const { label, status, variant, size, announced, theme, uppercase } = this;
    return (
      <Host
        class={{ [`ic-theme-${theme}`]: theme !== "inherit" }}
        role={announced ? "status" : null}
        aria-label="Status"
      >
        <strong
          class={{
            ["tag"]: true,
            [`${variant}-${status}`]: true,
            ["outlined"]: variant === "outlined",
            [`${size}`]: true,
          }}
        >
          <ic-typography
            variant={uppercase ? "label-uppercase" : "label"}
            apply-vertical-margins={false}
          >
            <span>{label}</span>
          </ic-typography>
        </strong>
      </Host>
    );
  }
}
