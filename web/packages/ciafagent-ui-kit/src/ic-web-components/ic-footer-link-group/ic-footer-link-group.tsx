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
import {
  Component,
  Host,
  Element,
  Listen,
  Prop,
  h,
  State,
} from "@stencil/core";
import {
  DEVICE_SIZES,
  getBrandForegroundAppearance,
  onComponentRequiredPropUndefined,
} from "../../utils/helpers";
import {
  IcBrand,
  IcBrandForeground,
  IcBrandForegroundNoDefault,
} from "../../utils/types";

@Component({
  tag: "ic-footer-link-group",
  styleUrl: "ic-footer-link-group.css",
  shadow: {
    delegatesFocus: true,
  },
})
export class FooterLinkGroup {
  @Element() el: HTMLIcFooterLinkGroupElement;

  @State() expanded: boolean = false;
  @State() deviceSize: number = DEVICE_SIZES.XL;
  @State() dropdownIconStyle: IcBrandForegroundNoDefault | IcBrandForeground =
    getBrandForegroundAppearance();
  @State() small: boolean = false;

  /**
   * The title of the link group to be displayed.
   */
  @Prop() label!: string;

  componentWillLoad(): void {
    this.small = this.isSmall(this.el);
  }

  componentDidLoad(): void {
    onComponentRequiredPropUndefined(
      [{ prop: this.label, propName: "label" }],
      "Footer Link Group"
    );
  }

  @Listen("footerResized", { target: "document" })
  footerResizeHandler(): void {
    this.small = this.isSmall(this.el);
  }

  @Listen("brandChange", { target: "document" })
  footerBrandChangeHandler(ev: CustomEvent<IcBrand>): void {
    this.dropdownIconStyle = ev.detail.mode;
  }

  private isSmall(e: HTMLElement): boolean {
    if (e.parentElement !== null) {
      if (e.parentElement.classList.contains("ic-footer")) {
        return e.parentElement.classList.contains("ic-footer-small");
      } else {
        return this.isSmall(e.parentElement);
      }
    } else {
      return false;
    }
  }

  private handleKeydown = (event: KeyboardEvent): void => {
    if (event.key === " " || event.key === "Enter") {
      this.toggleExpanded();
    }
  };

  private toggleExpanded = (): void => {
    this.expanded = !this.expanded;
  };

  render() {
    const { small, label } = this;

    return !small ? (
      <Host
        class={{
          ["footer-link-group footer-link-group-sparse"]: true,
          [`footer-link-group-${this.dropdownIconStyle}`]: true,
        }}
        role="listitem"
      >
        <div class="footer-link-label">
          <ic-typography variant="subtitle-small">{label}</ic-typography>
        </div>
        <div class="footer-link-group-links" role="list">
          <slot />
        </div>
      </Host>
    ) : (
      <Host
        class={{
          ["footer-link-group footer-link-group-small"]: true,
          [`footer-link-group-${this.dropdownIconStyle}`]: true,
        }}
        onClick={this.toggleExpanded}
        onKeydown={this.handleKeydown}
        aria-expanded={this.expanded}
        role="listitem"
      >
        <ic-section-container tabindex="0" fullHeight={true}>
          <div class="footer-link-group-header">
            <div class="footer-link-label">
              <ic-typography variant="label">{label}</ic-typography>
            </div>
            {this.expanded ? (
              <svg
                class="footer-link-group-toggle"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
                role="img"
                width="1em"
                height="1em"
                preserveAspectRatio="xMidYMid meet"
                viewBox="0 0 1200 1200"
              >
                <path
                  fill="currentColor"
                  d="M600.002 210.605L421.285 389.336L0 810.559l178.721 178.836l421.281-421.341l421.281 421.341L1200 810.559L778.733 389.336L600.002 210.605z"
                />
              </svg>
            ) : (
              <svg
                class="footer-link-group-toggle"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
                role="img"
                width="1em"
                height="1em"
                preserveAspectRatio="xMidYMid meet"
                viewBox="0 0 1200 1200"
              >
                <g transform="translate(0 1200) scale(1 -1)">
                  <path
                    fill="currentColor"
                    d="M600.002 210.605L421.285 389.336L0 810.559l178.721 178.836l421.281-421.341l421.281 421.341L1200 810.559L778.733 389.336L600.002 210.605z"
                  />
                </g>
              </svg>
            )}
          </div>
          {this.expanded && (
            <div class="footer-link-group-links" role="list">
              <slot />
            </div>
          )}
        </ic-section-container>
      </Host>
    );
  }
}
