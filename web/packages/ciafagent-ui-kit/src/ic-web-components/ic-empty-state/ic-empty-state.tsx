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
import { h, Component, Host, Prop, Element } from "@stencil/core";

import { IcEmptyStateAlignment } from "./ic-empty-state.types";
import {
  isSlotUsed,
  onComponentRequiredPropUndefined,
  renderDynamicChildSlots,
} from "../../utils/helpers";
import { IcSizes, IcThemeMode } from "../../utils/types";

/**
 * @slot image - Content is placed at the top above all other content.
 * @slot actions - Content is placed at the bottom below all other content.
 * @slot heading - Content will be rendered in place of the heading prop.
 * @slot subheading - Content will be rendered in place of the subheading prop.
 * @slot body - Content will be rendered in place of the body prop.
 */
@Component({
  tag: "ic-empty-state",
  styleUrl: "ic-empty-state.css",
  shadow: true,
})
export class EmptyState {
  private hostMutationObserver: MutationObserver | null = null;

  @Element() el: HTMLIcEmptyStateElement;

  /**
   * The alignment of the empty state container.
   */
  @Prop() aligned?: IcEmptyStateAlignment = "left";

  /**
   * The body text rendered in the empty state container.
   */
  @Prop() body?: string;

  /**
   * The number of lines of body text to display before truncating.
   */
  @Prop() maxLines?: number;

  /**
   * The title rendered in the empty state container.
   */
  @Prop() heading?: string;

  /**
   * The size of the image or icon used in the image slot.
   */
  @Prop() imageSize?: IcSizes = "medium";

  /**
   * The subtitle rendered in the empty state container.
   */
  @Prop() subheading?: string;

  /**
   * Sets the theme color to the dark or light theme color. "inherit" will set the color based on the system settings or ic-theme component.
   */
  @Prop() theme?: IcThemeMode = "inherit";

  disconnectedCallback(): void {
    this.hostMutationObserver?.disconnect();
  }

  componentDidLoad(): void {
    !isSlotUsed(this.el, "heading") &&
      onComponentRequiredPropUndefined(
        [{ prop: this.heading, propName: "heading" }],
        "Empty State"
      );

    this.hostMutationObserver = new MutationObserver((mutationList) =>
      renderDynamicChildSlots(mutationList, ["image", "actions"], this)
    );
    this.hostMutationObserver.observe(this.el, {
      childList: true,
    });
  }

  render() {
    const { aligned, body, maxLines, heading, imageSize, subheading, theme } =
      this;
    return (
      <Host
        class={{
          [`ic-empty-state-${aligned}`]: true,
          [`image-${imageSize}`]: isSlotUsed(this.el, "image"),
          [`ic-theme-${theme}`]: theme !== "inherit",
        }}
      >
        {isSlotUsed(this.el, "image") && <slot name="image"></slot>}
        <div>
          <slot name="heading">
            <ic-typography variant="h4" class="empty-state-heading">
              {heading}
            </ic-typography>
          </slot>
          <slot name="subheading">
            <ic-typography
              variant="subtitle-small"
              class="empty-state-subheading"
            >
              {subheading}
            </ic-typography>
          </slot>
          <slot name="body">
            <ic-typography maxLines={maxLines} class="empty-state-body">
              {body}
            </ic-typography>
          </slot>
        </div>
        {isSlotUsed(this.el, "actions") && (
          <div class="action-area">
            <slot name="actions" />
          </div>
        )}
      </Host>
    );
  }
}
