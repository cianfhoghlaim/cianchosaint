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
import { Component, Element, Host, h, Prop } from "@stencil/core";
import { isPropDefined } from "../../utils/helpers";

@Component({
  tag: "ic-menu-group",
  styleUrl: "ic-menu-group.css",
  shadow: true,
})
export class MenuGroup {
  @Element() el: HTMLIcMenuGroupElement;
  /**
   * The label to display as the title of the menu group.
   */
  @Prop() label?: string;

  render() {
    const parentMenu = this.el.closest("ic-popover-menu");

    return (
      <Host role="group" aria-label={this.label !== null ? this.label : ""}>
        {isPropDefined(this.label) && (
          <ic-typography variant="subtitle-small">{this.label}</ic-typography>
        )}
        <span class="menu-items-wrapper">
          <slot></slot>
        </span>
        {/* The line under the menu group is added on all menu groups except in the case that the menu group is the last item in the popover menu */}
        {this.el !== parentMenu?.querySelector("ic-menu-group:last-child") && (
          <hr />
        )}
      </Host>
    );
  }
}
