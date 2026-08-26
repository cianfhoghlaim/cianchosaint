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
  Event,
  EventEmitter,
  Host,
  Prop,
  h,
} from "@stencil/core";
import { IcThemeMode } from "../../utils/types";

@Component({
  tag: "ic-tab-panel",
  styleUrl: "ic-tab-panel.css",
  shadow: true,
})
export class TabPanel {
  @Element() el: HTMLIcTabPanelElement;

  /**
   * @internal If `true`, the tab panel will be displayed.
   */
  @Prop() active: boolean = false;

  /**
   * @internal Determines whether black variant of the tabs should be displayed.
   */
  @Prop() monochrome?: boolean = false;

  /**
   * @internal The shared ID that links the panel and tab.
   */
  @Prop({ reflect: true }) panelId?: string;

  /**
   * @internal The shared ID of the currently selected tab.
   */
  @Prop() selectedTab?: string;

  /**
   * @internal The position of the tab panel inside the tabs array in context.
   */
  @Prop({ reflect: true }) tabPosition?: number;

  /** @internal Determines whether the light or dark variant of the tabs should be displayed. */
  @Prop() theme?: IcThemeMode = "inherit";

  /**
   * @internal Emitted when a tab panel is dynamically created.
   */
  @Event() tabPanelCreated: EventEmitter<HTMLIcTabPanelElement>;

  /**
   * @internal Emitted when a tab panel is unmounted.
   */
  @Event() tabPanelRemoved: EventEmitter<void>;

  connectedCallback(): void {
    this.tabPanelCreated.emit(this.el);
  }

  render() {
    const { active, theme } = this;
    return (
      <Host
        class={{
          [`ic-theme-${theme}`]: theme !== "inherit",
          "ic-tab-panel-hidden": !active,
        }}
        role="tabpanel"
        aria-hidden={`${!active}`}
      >
        <div>
          <slot></slot>
        </div>
      </Host>
    );
  }
}
