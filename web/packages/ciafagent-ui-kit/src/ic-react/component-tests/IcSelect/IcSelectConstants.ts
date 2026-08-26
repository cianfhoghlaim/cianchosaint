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
export const IC_SELECT = "ic-select";
export const IC_INPUT_CONTAINER = "ic-input-component-container";
export const IC_MENU_LI = "ic-menu ul li";
export const IC_MENU_UL = "ic-menu ul";
export const SC_IC_MENU_TYPOGRAPHY = ".sc-ic-menu ic-typography";
export const DISABLED_OPTION_MENU = "option disabled-option sc-ic-menu";
export const IC_TYPOGRAPHY = "ic-typography";
export const ID_CLEAR_BUTTON = "#clear-button";
export const ARIA_SELECTED = "aria-selected";
export const SELECT_INPUT = ".select-input";

export const TYPE_DOWN_ARROW = "{downArrow}";
export const TYPE_UP_ARROW = "{upArrow}";
export const TYPE_ENTER = "{enter}";
export const TYPE_BACKSPACE = "{backspace}";
export const DATA_VALUE_CAPPUCCINO = '[data-value="cappuccino"]';
export const DATA_VALUE_ESPRESSO = "[data-value='espresso']";
export const DATA_VALUE_CAP = '[data-value="Cap"]';
export const DATA_VALUE_AMERICANO = '[data-value="americano"]';
export const DATA_LABEL_CAPPUCCINO = '[data-label="Cappuccino"]';
export const DATA_LABEL_ESPRESSO = '[data-label="Espresso"]';
export const INPUT_TYPE_HIDDEN = "input[type='hidden']";
export const NO_RESULTS_FOUND = "No results found";
export const RETRY_BUTTON = "#retry-button";
export const LOADING_MESSAGE = "Loading...";
export const CHECK_ICON_CLASS = "check-icon";

export const COFFEE_EXAMPLE = "Café au lait";
export const OPTION_SELECT_STUB = "@icOptionSelect";
export const OPTION_DESELECT_STUB = "@icOptionDeselect";
export const OPTION_GROUP_TITLE = "option-group-title";
export const MENU_SCROLL_CLASS = "menu-scroll";
