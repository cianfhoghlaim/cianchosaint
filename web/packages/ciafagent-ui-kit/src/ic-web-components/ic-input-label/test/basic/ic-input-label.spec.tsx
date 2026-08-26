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
import { InputLabel } from "../../ic-input-label";
import { newSpecPage } from "@stencil/core/testing";

describe("ic-input-label", () => {
  it("should render", async () => {
    const page = await newSpecPage({
      components: [InputLabel],
      html: `<ic-input-label for="test-input-id" label="Test label"></ic-input-label>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render required variant", async () => {
    const page = await newSpecPage({
      components: [InputLabel],
      html: `<ic-input-label for="test-input-id" label="Test label" required=true></ic-input-label>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render disabled variant", async () => {
    const page = await newSpecPage({
      components: [InputLabel],
      html: `<ic-input-label for="test-input-id" label="Test label" required=true disabled=true></ic-input-label>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render readonly variant", async () => {
    const page = await newSpecPage({
      components: [InputLabel],
      html: `<ic-input-label for="test-input-id" label="Test label" required=true readonly=true></ic-input-label>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render error variant", async () => {
    const page = await newSpecPage({
      components: [InputLabel],
      html: `<ic-input-label for="test-input-id" label="Test label" status="error"></ic-input-label>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with helpertext", async () => {
    const page = await newSpecPage({
      components: [InputLabel],
      html: `<ic-input-label for="test-input-id" label="Test label" required=true helper-text="Some helper text"></ic-input-label>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with label text not wrapped in label tag", async () => {
    const page = await newSpecPage({
      components: [InputLabel],
      html: `<ic-input-label label="Test label" required=true helper-text="Some helper text" use-label-tag=false></ic-input-label>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should remove label but keep helpertext", async () => {
    const page = await newSpecPage({
      components: [InputLabel],
      html: `<ic-input-label for="test-input-id" label="Test label" hide-label='true' helper-text="Some helper text"></ic-input-label>`,
    });

    expect(page.root).toEqualHtml(`
    <ic-input-label class="with-helper" for="test-input-id" helper-text="Some helper text" hide-label="true" label="Test label">
      <ic-typography class="helpertext helpertext-normal" variant="caption">
        <span id="test-input-id-helper-text">
          Some helper text
        </span>
      </ic-typography>
    </ic-input-label>
    `);
  });

  it("should remove helpertext but keep label", async () => {
    const page = await newSpecPage({
      components: [InputLabel],
      html: `<ic-input-label for="test-input-id" label="Test label" helper-text=""></ic-input-label>`,
    });

    expect(page.root).toEqualHtml(`
      <ic-input-label for="test-input-id" helper-text="" label="Test label">
        <ic-typography variant="label">
          <label htmlfor="test-input-id">
            Test label
          </label>
        </ic-typography>
      </ic-input-label>
    `);
  });

  it("should correctly detect if a helper text slot is used", async () => {
    const page = await newSpecPage({
      components: [InputLabel],
      html: `<ic-input-label for="test-input-id" label="Test label"></ic-input-label>`,
    });

    const mockSlot = {
      assignedElements: jest
        .fn()
        .mockReturnValue([document.createElement("div")]),
    } as unknown as HTMLSlotElement;

    expect(page.rootInstance.isSlotUsed(mockSlot)).toBe(true);

    const parentMockSlot = {
      assignedElements: jest.fn().mockReturnValue([mockSlot]),
    } as unknown as HTMLSlotElement;

    parentMockSlot.assignedElements = jest.fn().mockReturnValue([mockSlot]);

    expect(page.rootInstance.isSlotUsed(parentMockSlot)).toBe(true);

    mockSlot.assignedElements = jest.fn().mockReturnValue([]);

    expect(page.rootInstance.isSlotUsed(mockSlot)).toBe(false);
  });
});
