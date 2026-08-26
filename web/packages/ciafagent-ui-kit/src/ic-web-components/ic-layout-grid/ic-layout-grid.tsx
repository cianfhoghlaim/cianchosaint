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
import { IcAlignment } from "../../utils/types";
import { IcGridBreakpoints, IcGridType } from "./ic-layout-grid.types";

@Component({
  tag: "ic-layout-grid",
  styleUrl: "ic-layout-grid.css",
  shadow: true,
})
export class LayoutGrid {
  private COL_WIDTH_CSS_PROP = "--ic-layout-grid-col-width";

  @Element() el: HTMLIcLayoutGridElement;

  /**
   * The alignment of the grid.
   */
  @Prop() aligned?: IcAlignment = "left";

  /**
   * The number of columns in the grid.
   * This can be a number or an object specifying different values for each breakpoint.
   */
  @Prop() columns?: IcGridBreakpoints;
  @Watch("columns")
  watchColumns() {
    this.getColumns();
  }

  /**
   * The default column span for grid items.
   */
  @Prop() defaultColSpan?: IcGridBreakpoints = 1;
  @Watch("defaultColSpan")
  watchDefaultColSpan() {
    this.getColSpan();
  }

  /**
   * The default column width for grid items.
   * This is used when the grid type is set to "fixed".
   */
  @Prop() defaultColWidth?: string = "64px";
  @Watch("defaultColWidth")
  watchDefaultColWidth(newValue: string) {
    if (this.type === "fixed") {
      this.el.style.setProperty(this.COL_WIDTH_CSS_PROP, newValue);
    }
  }

  /**
   * The default row span for grid items.
   */
  @Prop() defaultRowSpan?: number = 1;
  @Watch("defaultRowSpan")
  watchDefaultRowSpan(newValue: number) {
    this.el.style.setProperty("--ic-layout-grid-row-span", `${newValue}`);
  }

  /**
   * If `true`, the standard vertical padding from the grid will be removed.
   */
  @Prop() fullHeight?: boolean = false;

  /**
   * The space between grid items, in multiples of the base spacing unit (`var(--ic-space-xs)`).
   */
  @Prop() gridSpacing?: number = 2;
  @Watch("gridSpacing")
  watchGridSpacing() {
    this.getGridSpacing();
  }

  /**
   * The number of rows in the grid.
   */
  @Prop() rows?: number = 1;
  @Watch("rows")
  watchRows(newValue: number) {
    this.el.style.setProperty("--ic-layout-grid-rows", `${newValue}`);
  }

  /**
   * The layout type of the grid.
   */
  @Prop() type: IcGridType = "fixed";
  @Watch("type")
  watchType(newValue: IcGridType) {
    this.getColumns();
    if (newValue === "fixed" && this.defaultColWidth) {
      this.el.style.setProperty(this.COL_WIDTH_CSS_PROP, this.defaultColWidth);
    } else {
      this.el.style.removeProperty(this.COL_WIDTH_CSS_PROP);
    }
  }

  componentWillLoad(): void {
    if (this.columns === undefined) {
      if (this.type === "fixed") {
        this.columns = 12;
      } else if (this.type === "fluid") {
        this.columns = {
          xs: 2,
          sm: 4,
          md: 8,
          lg: 12,
          xl: 12,
        };
      }
    }
    this.getColumns();
    this.getColSpan();
    this.getGridSpacing();
    if (this.type === "fixed" && this.defaultColWidth) {
      this.el.style.setProperty(this.COL_WIDTH_CSS_PROP, this.defaultColWidth);
    }
    if (this.rows) {
      this.el.style.setProperty("--ic-layout-grid-rows", `${this.rows}`);
      this.el.style.setProperty(
        "--ic-layout-grid-row-span",
        `${this.defaultRowSpan}`
      );
    }
  }

  private getColumns = () => {
    if (typeof this.columns === "number") {
      this.el.style.setProperty(
        "--ic-layout-grid-columns",
        this.columns.toString()
      );
    } else if (typeof this.columns === "object") {
      Object.entries(this.columns).forEach(([breakpoint, value]) => {
        if (value !== undefined) {
          this.el.style.setProperty(
            `--ic-layout-grid-columns-${breakpoint}`,
            value.toString()
          );
        }
      });
    }
  };

  private getColSpan = () => {
    if (this.defaultColSpan !== undefined) {
      if (typeof this.defaultColSpan === "number") {
        (Array.from(this.el.children) as HTMLElement[]).forEach((child) => {
          child.style.setProperty(
            "--ic-layout-grid-col-span",
            `${this.defaultColSpan}`
          );
        });
      } else if (typeof this.defaultColSpan === "object") {
        Object.entries(this.defaultColSpan).forEach(([breakpoint, value]) => {
          if (value !== undefined) {
            this.el.style.setProperty(
              `--ic-layout-grid-col-span-${breakpoint}`,
              value.toString()
            );
          }
        });
      }
    }
  };

  private getGridSpacing = () => {
    this.el.style.setProperty(
      "--ic-layout-grid-spacing",
      `calc(var(--ic-space-xs) * ${this.gridSpacing})`
    );
  };

  render() {
    const { aligned, fullHeight } = this;

    return (
      <Host
        class={{
          [`ic-layout-grid-aligned-${aligned}`]: true,
          ["ic-layout-grid-no-vertical-padding"]: !!fullHeight,
        }}
      >
        <slot></slot>
      </Host>
    );
  }
}
