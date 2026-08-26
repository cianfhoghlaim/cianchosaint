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
import { Component, Element, h, Host, Method, Prop } from "@stencil/core";
import { IcThemeMode } from "../../utils/types";

@Component({
  tag: "ic-skip-link",
  styleUrl: "ic-skip-link.css",
  shadow: true,
})
export class SkipLink {
  private linkEl?: HTMLIcLinkElement;

  @Element() el: HTMLIcSkipLinkElement;

  /**
   * If `true`, the skip link will fill the width of the page.
   */
  @Prop() fullWidth: boolean = false;

  /**
   * If `true`, the skip link will appear inline with surrounding page content when focused.
   */
  @Prop() inline: boolean = false;

  /**
   * The label displayed when the skip link is focused.
   */
  @Prop() label: string = "Skip to main content";

  /**
   * If `true`, the skip link will display as black in the light theme, and white in the dark theme.
   */
  @Prop() monochrome: boolean = false;

  /**
   * The target ID for the element which should receive focus when triggering the skip link.
   */
  @Prop() target!: string;

  /**
   * Sets the theme color to the dark or light theme color. `inherit` will set the color based on the system settings or ic-theme component.
   */
  @Prop() theme: IcThemeMode = "inherit";

  /**
   * If `true`, the background will be hidden.
   */
  @Prop() transparentBackground: boolean = false;

  /**
   * Sets focus on the element.
   */
  @Method()
  async setFocus(): Promise<void> {
    if (this.linkEl) this.linkEl.setFocus();
  }

  render() {
    const {
      fullWidth,
      inline,
      label,
      monochrome,
      target,
      theme,
      transparentBackground,
    } = this;

    return (
      <Host
        class={{
          [`ic-theme-${theme}`]: theme !== "inherit",
        }}
      >
        <ic-link
          class={{
            "display-top": !inline,
            "full-width": !!fullWidth,
            "show-background": !transparentBackground,
            inline: !!inline,
          }}
          href={`#${target}`}
          monochrome={monochrome}
          theme={theme}
          ref={(el) => (this.linkEl = el)}
        >
          {label}
        </ic-link>
      </Host>
    );
  }
}
