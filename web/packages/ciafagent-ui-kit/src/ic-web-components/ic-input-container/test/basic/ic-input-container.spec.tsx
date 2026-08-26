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
import { InputContainer } from "../../ic-input-container";
import { newSpecPage } from "@stencil/core/testing";

describe("ic-input-container", () => {
  it("should render", async () => {
    const page = await newSpecPage({
      components: [InputContainer],
      html: `<ic-input-container></ic-input-container>`,
    });

    expect(page.root).toEqualHtml(`
    <ic-input-container>
      <div class="component-container"></div>
    </ic-input-container>
    `);
  });

  it("should render disabled", async () => {
    const page = await newSpecPage({
      components: [InputContainer],
      html: `<ic-input-container disabled=true></ic-input-container>`,
    });

    expect(page.root).toEqualHtml(`
      <ic-input-container disabled="true">
        <div class="component-container disabled"></div>
      </ic-input-container>
    `);
  });

  it("should render readonly", async () => {
    const page = await newSpecPage({
      components: [InputContainer],
      html: `<ic-input-container readonly=true></ic-input-container>`,
    });

    expect(page.root).toEqualHtml(`
      <ic-input-container readonly="true">
        <div class="component-container readonly"></div>
      </ic-input-container>
    `);
  });
});
