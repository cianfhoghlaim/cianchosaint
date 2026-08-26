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
import { Component, Prop, h, Host } from "@stencil/core";
import { IcProtectiveMarkings } from "./ic-classification-banner.types";

const classificationText = {
  default: "protective marking not set",
  official: "official",
  "official-sensitive": "official-sensitive",
  secret: "secret",
  "top-secret": "top secret",
};

@Component({
  tag: "ic-classification-banner",
  styleUrl: "ic-classification-banner.css",
  shadow: true,
})
export class ClassificationBanner {
  /**
   * The additional information that will be displayed after the classification.
   */
  @Prop() additionalSelectors?: string = "";
  /**
   * The classification level to be displayed - also determines the banner and text colour.
   */
  @Prop() classification?: IcProtectiveMarkings = "default";
  /**
   * The optional text that will be displayed before classification to specify relevant country/countries.
   */
  @Prop() country?: string = "uk";
  /**
   * The custom text that will appear on the banner. If set, the `additionalSelectors`, `country` and `upTo` props are ignored.
   */
  @Prop() customClassificationText?: string = "";
  /**
   * If `true`, the banner will appear inline with the page, instead of sticking to the bottom of the page.
   */
  @Prop() inline?: boolean = false;
  /**
   * If `true`, "Up to" will be displayed before the classification and country.
   */
  @Prop() upTo?: boolean = false;

  render() {
    const { inline, upTo } = this;

    // In case of unrecognized props, fallback to default
    let {
      country,
      additionalSelectors,
      classification,
      customClassificationText,
    } = this;
    if (!country) country = "";
    if (!additionalSelectors) additionalSelectors = "";
    if (
      !classification ||
      (classification && !classificationText[classification])
    )
      classification = "default";
    if (!customClassificationText) customClassificationText = "";

    return (
      <Host class={{ ["ic-classification-banner-inline"]: !!inline }}>
        <banner
          aria-label="Protective marking"
          class={{
            ["classification-banner"]: true,
            [`${classification}`]: classification,
          }}
        >
          {classification !== "default" ? (
            <span class="offscreen">
              The protective marking of this page is:{" "}
            </span>
          ) : null}
          <ic-typography variant="caption-uppercase">
            {customClassificationText !== ""
              ? customClassificationText
              : classification === "default"
              ? classificationText[classification]
              : `${upTo ? "up to" : ""} 
               ${country} 
               ${classificationText[classification]} 
               ${additionalSelectors}`}
          </ic-typography>
        </banner>
      </Host>
    );
  }
}
