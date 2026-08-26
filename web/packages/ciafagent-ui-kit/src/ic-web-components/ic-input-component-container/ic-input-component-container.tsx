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
import { Component, Element, Host, Prop, Watch, h } from "@stencil/core";

import {
  IcInformationStatus,
  IcInformationStatusOrEmpty,
  IcSizes,
} from "../../utils/types";
import successIcon from "../../assets/success-icon.svg";
import {
  removeDisabledFalse,
  renderDynamicChildSlots,
  slotHasContent,
} from "../../utils/helpers";

/**
 * @slot left-icon - Content will be placed to the left of the input.
 */
@Component({
  tag: "ic-input-component-container",
  styleUrl: "ic-input-component-container.css",
})
export class InputComponentContainer {
  private hostMutationObserver: MutationObserver;
  @Element() el: HTMLIcInputComponentContainerElement;

  /**
   *  If `true`, the disabled state will be set.
   */
  @Prop() disabled?: boolean = false;
  @Watch("disabled")
  watchDisabledHandler(): void {
    removeDisabledFalse(this.disabled, this.el);
  }

  /**
   *  If `true`, the input component container will fill the width of the container it is in.
   */
  @Prop() fullWidth?: boolean = false;

  /**
   *  If `true`, the input component container will allow for multiple lines.
   */
  @Prop() multiLine?: boolean = false;

  /**
   *  If `true`, the readonly state will be set.
   */
  @Prop() readonly?: boolean = false;

  /**
   * The size of the input component container component.
   */
  @Prop() size?: IcSizes = "medium";

  /**
   *  If `true`, the validation will display inline.
   */
  @Prop() validationInline?: boolean = false;

  /**
   * The validation status of the input component container - e.g. 'error' | 'warning' | 'success'.
   */
  @Prop() validationStatus?: IcInformationStatusOrEmpty = "";

  componentWillLoad(): void {
    removeDisabledFalse(this.disabled, this.el);
  }

  componentDidLoad(): void {
    this.hostMutationObserver = new MutationObserver((mutationList) =>
      renderDynamicChildSlots(mutationList, "left-icon", this)
    );
    this.hostMutationObserver.observe(this.el, { childList: true });
  }

  render() {
    const {
      size,
      validationStatus,
      disabled,
      readonly,
      multiLine,
      fullWidth,
      validationInline,
    } = this;

    return (
      <Host
        class={{
          [`ic-input-component-container-${size}`]: true,
          [`ic-input-component-container-${validationStatus}`]:
            validationStatus !== "" && !disabled && !readonly,
          "ic-input-component-container-disabled": !!disabled,
          "ic-input-component-container-readonly": !!readonly,
          "ic-input-component-container-multiline": !!multiLine,
          "ic-input-component-container-full-width": !!fullWidth,
        }}
        aria-disabled={disabled ? "true" : null}
      >
        <div class="focus-indicator">
          {slotHasContent(this.el, "left-icon") && (
            <div class="icon-container">
              <slot name="left-icon" />
            </div>
          )}
          <slot></slot>

          {validationInline &&
            validationStatus === IcInformationStatus.Success && (
              <span class="inline-success" innerHTML={successIcon} />
            )}
        </div>
      </Host>
    );
  }
}
