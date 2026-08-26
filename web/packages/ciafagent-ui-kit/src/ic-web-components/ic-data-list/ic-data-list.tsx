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
import { IcSizesNoLarge, IcThemeMode } from "../../utils/types";

/**
 * @slot heading - Content will be placed at the top of the data list.
 */
@Component({
  tag: "ic-data-list",
  styleUrl: "ic-data-list.css",
  shadow: true,
})
export class DataList {
  @Element() el: HTMLIcDataListElement;

  /**
   * The title for the data list.
   */
  @Prop() heading?: string;

  /**
   * The size of the data list component.
   */
  @Prop() size?: IcSizesNoLarge = "medium";

  /**
   * Sets the theme color to the dark or light theme color. "inherit" will set the color based on the system settings or ic-theme component.
   */
  @Prop() theme?: IcThemeMode = "inherit";

  render() {
    const { el, heading, size, theme } = this;

    if (size === "small") {
      Array.from(el.children).forEach((child) =>
        child.setAttribute("size", "small")
      );
    }

    const hasHeading = heading || el.querySelector('[slot="heading"]');

    return (
      <Host
        class={{
          "ic-data-list-small": size === "small",
          [`ic-theme-${theme}`]: theme !== "inherit",
        }}
      >
        <div class="heading" id="data-list-heading">
          <slot name="heading">
            <ic-typography variant="h3">{heading}</ic-typography>
          </slot>
        </div>
        <div class={{ divider: true, "divider-no-heading": !hasHeading }} />
        <ul aria-labelledby="data-list-heading" class="rows">
          <slot></slot>
        </ul>
      </Host>
    );
  }
}
