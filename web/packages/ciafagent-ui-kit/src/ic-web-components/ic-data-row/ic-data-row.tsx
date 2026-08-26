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
import { Component, Element, Host, Prop, h, State } from "@stencil/core";
import {
  checkResizeObserver,
  DEVICE_SIZES,
  getCurrentDeviceSize,
  isSlotUsed,
  slotHasContent,
} from "../../utils/helpers";
import { IcSizesNoLarge, IcThemeMode } from "../../utils/types";

/**
 * @slot label - Content will be rendered in the leftmost cell.
 * @slot value - Content will be rendered to the right of the label.
 * @slot end-component - Content will be displayed in the rightmost cell.
 */
@Component({
  tag: "ic-data-row",
  styleUrl: "ic-data-row.css",
  shadow: true,
})
export class DataRow {
  private hasEndComponent: boolean = false;
  private resizeObserver: ResizeObserver | null = null;

  @Element() el: HTMLIcDataRowElement;

  @State() deviceSize: number = DEVICE_SIZES.XL;
  @State() listSize: "xl" | "m" | "xs";

  /**
   * The label in the leftmost cell of the row.
   */
  @Prop() label?: string;

  /**
   * The size of the data row component.
   */
  @Prop() size?: IcSizesNoLarge = "medium";

  /**
   * Sets the theme color to the dark or light theme color. "inherit" will set the color based on the system settings or ic-theme component.
   */
  @Prop() theme?: IcThemeMode = "inherit";

  /**
   * The value of the middle (right if no end-component supplied) cell of the row.
   */
  @Prop() value?: string;

  disconnectedCallback(): void {
    this.resizeObserver?.disconnect();
  }

  componentWillLoad(): void {
    this.deviceSize = getCurrentDeviceSize();
    this.hasEndComponent = slotHasContent(this.el, "end-component");
    this.checkLabelAbove();
  }

  componentDidLoad(): void {
    checkResizeObserver(this.runResizeObserver);
    if (this.hasEndComponent) this.labelEndComponent();
  }

  private runResizeObserver = () => {
    this.resizeObserver = new ResizeObserver(() => {
      this.checkLabelAbove();
    });

    this.resizeObserver.observe(this.el);
  };

  private checkLabelAbove() {
    const row = this.el.shadowRoot?.querySelector(".data");
    if (row) {
      const rowSize = row?.clientWidth + 46;
      if (rowSize) {
        this.listSize =
          rowSize < DEVICE_SIZES.S
            ? "xs"
            : rowSize < DEVICE_SIZES.M
            ? "m"
            : "xl";
      }
    }
  }

  private renderCellContent = (cell: "label" | "value") => {
    const isValue = cell === "value";
    return (
      <div class={cell}>
        {isSlotUsed(this.el, cell) ? (
          <slot name={cell}></slot>
        ) : (
          <ic-typography
            variant={
              isValue
                ? "body"
                : this.listSize === "xs"
                ? "label"
                : "subtitle-large"
            }
          >
            {isValue ? this.value : this.label}
          </ic-typography>
        )}
      </div>
    );
  };

  private labelEndComponent(): void {
    this.el.shadowRoot
      ?.querySelectorAll("slot[name=end-component]")
      .forEach((child) =>
        child.setAttribute("aria-label", `for ${this.label} row`)
      );
  }

  render() {
    const {
      el,
      listSize,
      hasEndComponent,
      label,
      renderCellContent,
      size,
      theme,
      value,
    } = this;

    return (
      <Host
        class={{
          ["ic-data-row-small"]: size === "small",
          ["breakpoint-medium"]: listSize === "m",
          ["breakpoint-xs"]: listSize === "xs",
          [`ic-theme-${theme}`]: theme !== "inherit",
        }}
        role="listitem"
      >
        <div class="data">
          <div class="text-cells">
            {(isSlotUsed(el, "label") || label) && renderCellContent("label")}
            {(isSlotUsed(el, "value") || value) && renderCellContent("value")}
          </div>
          {hasEndComponent && (
            <div class="end-component">
              <slot name="end-component"></slot>
            </div>
          )}
        </div>
        <div class="divider" />
      </Host>
    );
  }
}
