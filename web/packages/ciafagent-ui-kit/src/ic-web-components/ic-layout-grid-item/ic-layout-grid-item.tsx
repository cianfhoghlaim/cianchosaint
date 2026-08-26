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
import { Component, Prop, Host, h, Element, Watch } from "@stencil/core";

@Component({
  tag: "ic-layout-grid-item",
  styleUrl: "ic-layout-grid-item.css",
  shadow: true,
})
export class LayoutGridItem {
  @Element() el: HTMLIcLayoutGridItemElement;

  /**
   * The number of columns the grid item should span.
   */
  @Prop() colSpan?: number = 1;
  @Watch("colSpan")
  watchColSpan(newValue: number) {
    this.el.style.setProperty("--ic-grid-item-col-span", `${newValue}`);
  }

  /**
   * The column the grid item should start at.
   */
  @Prop() colStart?: number = 1;
  @Watch("colStart")
  watchColStart(newValue: number) {
    this.el.style.setProperty("--ic-grid-item-col-start", `${newValue}`);
  }

  /**
   * If `true`, the grid item will be hidden on smaller screens.
   */
  @Prop() hideInMobileMode?: boolean = false;

  /**
   * The number of rows the grid item should span.
   */
  @Prop() rowSpan?: number = 1;
  @Watch("rowSpan")
  watchRowSpan(newValue: number) {
    this.el.style.setProperty("--ic-grid-item-row-span", `${newValue}`);
  }

  /**
   * The row the grid item should start at.
   */
  @Prop() rowStart?: number = 1;
  @Watch("rowStart")
  watchRowStart(newValue: number) {
    this.el.style.setProperty("--ic-grid-item-row-start", `${newValue}`);
  }

  componentWillLoad(): void {
    this.el.style.setProperty("--ic-grid-item-col-start", `${this.colStart}`);
    this.el.style.setProperty("--ic-grid-item-col-span", `${this.colSpan}`);
    this.el.style.setProperty("--ic-grid-item-row-start", `${this.rowStart}`);
    this.el.style.setProperty("--ic-grid-item-row-span", `${this.rowSpan}`);
  }

  render() {
    const { hideInMobileMode } = this;
    return (
      <Host
        class={{
          "ic-layout-grid-hide-in-mobile": !!hideInMobileMode,
        }}
      >
        <slot></slot>
      </Host>
    );
  }
}
