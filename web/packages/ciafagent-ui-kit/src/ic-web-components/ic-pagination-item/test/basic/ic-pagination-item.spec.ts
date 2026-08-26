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
import { PaginationItem } from "../../ic-pagination-item";
import { newSpecPage } from "@stencil/core/testing";

describe("ic-pagination-item", () => {
  it("should render default pagination item", async () => {
    const page = await newSpecPage({
      components: [PaginationItem],
      html: `<ic-pagination-item page=1></ic-pagination-item>`,
    });

    expect(page.root).toMatchSnapshot("render default pagination item");
  });

  it("should render with custom label", async () => {
    const page = await newSpecPage({
      components: [PaginationItem],
      html: `<ic-pagination-item page=1 label="screen"></ic-pagination-item>`,
    });

    expect(page.root).toMatchSnapshot("render with custom label");
  });

  it("should render with dark appearance", async () => {
    const page = await newSpecPage({
      components: [PaginationItem],
      html: `<ic-pagination-item page=1 type="page" appearance="dark"></ic-pagination-item>`,
    });

    expect(page.root).toMatchSnapshot("render with dark appearance");
  });

  it("should render with light appearance", async () => {
    const page = await newSpecPage({
      components: [PaginationItem],
      html: `<ic-pagination-item page=1 type="page" appearance="light"></ic-pagination-item>`,
    });

    expect(page.root).toMatchSnapshot("render with light appearance");
  });

  it("should render as selected item", async () => {
    const page = await newSpecPage({
      components: [PaginationItem],
      html: `<ic-pagination-item page=1 type="page" selected></ic-pagination-item>`,
    });

    expect(page.root).toMatchSnapshot("render as selected item");
  });

  it("should render disabled", async () => {
    const page = await newSpecPage({
      components: [PaginationItem],
      html: `<ic-pagination-item page=1 type="page" disabled></ic-pagination-item>`,
    });

    expect(page.root).toMatchSnapshot("render disabled");

    page.root?.setAttribute("disabled", "false");

    await page.waitForChanges();
    expect(page.root).toMatchSnapshot("disabled-removed");
  });

  it("should render as ellipsis type", async () => {
    const page = await newSpecPage({
      components: [PaginationItem],
      html: `<ic-pagination-item page=1 type="ellipsis"></ic-pagination-item>`,
    });

    expect(page.root).toMatchSnapshot("render as ellipsis type");
  });

  it("should render disabled ellipsis type", async () => {
    const page = await newSpecPage({
      components: [PaginationItem],
      html: `<ic-pagination-item page=1 type="ellipsis" disabled></ic-pagination-item>`,
    });

    expect(page.root).toMatchSnapshot("render disabled ellipsis type");
  });

  it("should test paginationItemClick event", async () => {
    const page = await newSpecPage({
      components: [PaginationItem],
      html: `<ic-pagination-item page=1></ic-pagination-item>`,
    });

    const eventSpy = jest.fn();

    document.addEventListener("paginationItemClick", eventSpy);

    page.rootInstance.handleClick();

    await page.waitForChanges();

    expect(eventSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        detail: expect.objectContaining({
          page: 1,
        }),
      })
    );
  });
});
