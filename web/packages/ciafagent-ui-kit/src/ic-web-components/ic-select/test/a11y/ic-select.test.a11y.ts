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
import { fixture } from "@open-wc/testing-helpers";
import { axe } from "jest-axe";
// Unable to import from @ukic/web-components
import { checkShadowElementRendersCorrectly } from "../../../../utils/testa11y.helpers";

describe("ic-select", () => {
  it("passes accessibility", async () => {
    const el = await fixture(
      `<ic-select 
    placeholder="Select an option..." 
    label="What is your favourite coffee?"
  ></ic-select>
  <script>
     const select = document.querySelector("ic-select");
     let option = "Cappuccino";
     select.options = [
       { label: "Espresso", value: "espresso" },
       { label: "Double Espresso", value: "doubleespresso" },
       { label: "Flat White", value: "flatwhite" },
       { label: "Cappuccino", value: "cappuccino" },
       { label: "Americano", value: "americano" },
       { label: "Mocha", value: "mocha" },
     ];
     select.addEventListener("icChange", function (event) {
       console.log(event.detail.value);
     });
   </script>`
    );
    checkShadowElementRendersCorrectly(el);
    expect(await axe(el)).toHaveNoViolations();
  });
});

describe("ic-select-searchable", () => {
  it("passes accessibility", async () => {
    const el = await fixture(
      `<ic-select 
    placeholder="Select an option…"
    label="What is your favourite coffee?" 
    searchable="true"
  ></ic-select>
   <script>
     const select = document.querySelector("ic-select");
     let option = "Cappuccino";
     select.options = [
       { label: "Cappuccino", value: "Cap" },
       { label: "Latte", value: "Lat" },
       { label: "Americano", value: "Ame" },
       { label: "Flat white", value: "Fla" },
       { label: "Mocha", value: "Moc" },
       { label: "Macchiato", value: "Mac" },
       { label: "Café au lait", value: "Caf" },
       { label: "Espresso", value: "Esp" },
       { label: "Cortado", value: "Cor" },
       { label: "Latte macchiato", value: "Lam" },
     ];
     select.addEventListener("icChange", function (event) {
       console.log(event.detail.value);
     });
   </script>`
    );
    checkShadowElementRendersCorrectly(el);
    expect(await axe(el)).toHaveNoViolations();
  });
});
