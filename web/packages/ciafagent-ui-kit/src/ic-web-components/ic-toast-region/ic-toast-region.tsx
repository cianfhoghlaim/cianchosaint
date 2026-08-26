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
import { Component, Element, h, Listen, Prop, Watch } from "@stencil/core";
import { IcFocusableComponents } from "../../utils/types";

@Component({ tag: "ic-toast-region" })
export class ToastRegion {
  private pendingVisibility: HTMLIcToastElement[] = [];
  private previouslyFocused: HTMLElement | null;

  @Element() el: HTMLIcToastRegionElement;

  /**
   * The toast element to be displayed.
   */
  @Prop({ mutable: true }) openToast?: HTMLIcToastElement;
  @Watch("openToast")
  watchOpenToastHandler(newValue: HTMLIcToastElement): void {
    if (this.openToast !== undefined) {
      this.showToast(newValue);
      this.openToast = undefined;
    }
  }

  componentDidLoad(): void {
    if (this.openToast) {
      this.showToast(this.openToast);
      this.openToast = undefined;
    }
  }

  @Listen("icDismiss", { capture: true })
  handleDismissedToast(): void {
    if (this.pendingVisibility.length > 0) {
      this.pendingVisibility[0]
        .setVisible()
        .then((res) => (this.previouslyFocused = res));
      this.pendingVisibility.shift();
    } else {
      if (this.previouslyFocused && "setFocus" in this.previouslyFocused) {
        (this.previouslyFocused as IcFocusableComponents).setFocus();
      } else this.previouslyFocused?.focus();
    }
  }

  private showToast = (toast: HTMLIcToastElement) => {
    const visibleToasts = Array.from(
      document.querySelectorAll("ic-toast")
    ).filter((el) => window.getComputedStyle(el).display !== "none");
    if (visibleToasts.indexOf(toast) === -1 && visibleToasts.length <= 0) {
      toast.setVisible().then((res) => (this.previouslyFocused = res));
    }
    if (visibleToasts.length > 0) this.pendingVisibility.push(toast);
  };

  render() {
    return <slot></slot>;
  }
}
