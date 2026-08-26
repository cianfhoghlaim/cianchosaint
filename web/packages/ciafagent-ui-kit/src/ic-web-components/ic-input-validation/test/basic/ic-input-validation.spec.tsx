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
import { newSpecPage } from "@stencil/core/testing";
import { InputValidation } from "../../ic-input-validation";
import { waitForTimeout } from "../../../../testspec.setup";

describe("ic-input-validation", () => {
  it("should render", async () => {
    const page = await newSpecPage({
      components: [InputValidation],
      html: `<ic-input-validation for="test-id" message="validation message"></ic-input-validation>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with success status", async () => {
    const page = await newSpecPage({
      components: [InputValidation],
      html: `<ic-input-validation for="test-id" message="validation message" status="success"></ic-input-validation>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with warning status", async () => {
    const page = await newSpecPage({
      components: [InputValidation],
      html: `<ic-input-validation for="test-id" message="validation message" status="warning"></ic-input-validation>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with error status", async () => {
    const page = await newSpecPage({
      components: [InputValidation],
      html: `<ic-input-validation for="test-id" message="validation message" status="error"></ic-input-validation>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with full width", async () => {
    const page = await newSpecPage({
      components: [InputValidation],
      html: `<ic-input-validation for="test-id" message="validation message" full-width=true></ic-input-validation>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should update the text content of the aria-live region", async () => {
    const page = await newSpecPage({
      components: [InputValidation],
      html: `<ic-input-validation for="test-id" message="validation message"></ic-input-validation>`,
    });

    page.rootInstance.message = "new validation message";

    await waitForTimeout(300);
    expect(page.root).toMatchSnapshot();
  });
});
