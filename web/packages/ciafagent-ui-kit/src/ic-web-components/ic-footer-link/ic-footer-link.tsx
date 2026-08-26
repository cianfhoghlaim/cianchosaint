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
  Element,
  Host,
  Listen,
  Prop,
  h,
  State,
} from "@stencil/core";
import {
  DEVICE_SIZES,
  getBrandForegroundAppearance,
} from "../../utils/helpers";
import { IcBrand, IcBrandForeground } from "../../utils/types";

type FooterConfig = { small: boolean; grouped: boolean };

@Component({
  tag: "ic-footer-link",
  styleUrl: "ic-footer-link.css",
  shadow: {
    delegatesFocus: true,
  },
})
export class FooterLink {
  @Element() el: HTMLIcFooterLinkElement;

  @State() deviceSize: number = DEVICE_SIZES.XL;
  @State() footerConfig: FooterConfig = { small: false, grouped: false };
  @State() foregroundColor: IcBrandForeground = getBrandForegroundAppearance();

  /**
   * If `true`, the user can save the linked URL instead of navigating to it.
   */
  @Prop() download?: string | boolean = false;

  /**
   * The URL that the link points to.
   */
  @Prop() href?: string;

  /**
   * The human language of the linked URL.
   */
  @Prop() hreflang?: string;

  /**
   * How much of the referrer to send when following the link.
   */
  @Prop() referrerpolicy?: ReferrerPolicy;

  /**
   * The relationship of the linked URL as space-separated link types.
   */
  @Prop() rel?: string;

  /**
   * The place to display the linked URL, as the name for a browsing context (a tab, window, or iframe).
   */
  @Prop() target?: string;

  componentWillLoad(): void {
    this.footerConfig = this.inferConfig(this.el);
  }

  @Listen("footerResized", { target: "document" })
  footerResizeHandler(): void {
    this.footerConfig = this.inferConfig(this.el);
  }

  @Listen("brandChange", { target: "document" })
  footerBrandChangeHandler(ev: CustomEvent<IcBrand>): void {
    this.foregroundColor = ev.detail.mode;
  }

  private inferConfig(e: HTMLElement): FooterConfig {
    if (e.parentElement !== null) {
      if (e.parentElement.classList.contains("ic-footer")) {
        return {
          small: e.parentElement.classList.contains("ic-footer-small"),
          grouped: e.parentElement.classList.contains("ic-footer-grouped"),
        };
      } else {
        return this.inferConfig(e.parentElement);
      }
    } else {
      return { small: false, grouped: false };
    }
  }

  render() {
    const {
      footerConfig,
      href,
      hreflang,
      referrerpolicy,
      rel,
      target,
      download,
    } = this;
    const { small, grouped } = footerConfig;

    const isLogoLink = !!this.el.closest("div[slot='logo']");

    return (
      <Host
        class={{
          "footer-link": true,
          [`footer-link-${grouped ? "grouped" : "ungrouped"}-${
            small ? "small" : "sparse"
          }`]: true,
          [`footer-link-${this.foregroundColor}`]: true,
          "footer-logo-link": isLogoLink,
        }}
        role="listitem"
      >
        <ic-link
          class="footer-link"
          href={href}
          hreflang={hreflang}
          referrerpolicy={referrerpolicy}
          rel={rel}
          download={download !== false ? download : undefined}
          target={target}
        >
          <slot />
        </ic-link>
      </Host>
    );
  }
}
