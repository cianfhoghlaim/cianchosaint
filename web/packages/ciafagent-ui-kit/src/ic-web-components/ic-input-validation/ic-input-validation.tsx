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
import { Element, Component, Host, Prop, h, Watch } from "@stencil/core";

import {
  IcAriaLive,
  IcInformationStatus,
  IcInformationStatusOrEmpty,
} from "../../utils/types";
import errorIcon from "../../assets/error-icon.svg";
import successIcon from "../../assets/success-icon.svg";
import warningIcon from "../../assets/warning-icon.svg";

import { getInputValidationTextID, isSlotUsed } from "../../utils/helpers";

const ICON = {
  [IcInformationStatus.Warning]: warningIcon,
  [IcInformationStatus.Error]: errorIcon,
  [IcInformationStatus.Success]: successIcon,
};
const INVISIBLE_CHAR = "\u200B";

/**
 * @slot validation-message-adornment - Content will be placed to the right of the validation message.
 * @slot validation-message - Content will be placed as the validation message.
 */
@Component({
  tag: "ic-input-validation",
  styleUrl: "ic-input-validation.css",
})
export class InputValidation {
  private messageEl!: HTMLSpanElement;

  @Element() el: HTMLIcInputValidationElement;

  /**
   *  The ARIA live mode to apply to the message.
   */
  @Prop() ariaLiveMode?: IcAriaLive = "polite";

  /**
   * The ID of the form element the validation is bound to.
   */
  @Prop() for?: string;

  /**
   *  If `true`, the input validation will fill the width of the container.
   */
  @Prop() fullWidth?: boolean = false;

  /**
   * The validation message to display.
   */
  @Prop() message?: string;
  @Watch("message")
  watchMessageHandler(newValue: string) {
    // Force detectable DOM changes
    // Invisible character used as screen readers can ignore whitespace changes e.g. "" and " "
    this.messageEl.textContent = INVISIBLE_CHAR;
    setTimeout(() => {
      this.messageEl.textContent = newValue;
    }, 200); // Delay to help ensure screen readers detect change
  }

  /**
   * The status of the validation - e.g. 'error' | 'warning' | 'success'.
   */
  @Prop() status?: IcInformationStatusOrEmpty = "";

  componentDidLoad(): void {
    this.messageEl.textContent = INVISIBLE_CHAR;
  }

  render() {
    const { ariaLiveMode, fullWidth, status, message } = this;
    const displayIcon = status !== "" ? ICON[status!] : "";
    return (
      <Host
        class={{
          [`ic-input-validation-${status}`]: status !== "",
          "ic-input-validation-full-width": !!fullWidth,
          "ic-input-validation-with-status": status !== "",
        }}
      >
        {displayIcon !== "" && (
          <span
            class={{
              "status-icon": true,
              [`icon-${status}`]: true,
            }}
            innerHTML={displayIcon}
          />
        )}
        <ic-typography variant="caption" class="statustext">
          <span id={this.for && getInputValidationTextID(this.for)}>
            {isSlotUsed(this.el, "validation-message") ? (
              <slot name="validation-message" />
            ) : (
              message
            )}
          </span>
          {/* Separate aria-live region to avoid flashing due to textContent delay */}
          <span
            ref={(el) => (this.messageEl = el as HTMLSpanElement)}
            class="sr-only"
            aria-live={ariaLiveMode}
          ></span>
        </ic-typography>
        <slot name="validation-message-adornment"></slot>
      </Host>
    );
  }
}
