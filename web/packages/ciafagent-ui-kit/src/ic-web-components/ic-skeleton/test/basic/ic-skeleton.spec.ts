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
import { Skeleton } from "../../ic-skeleton";

beforeAll(() => {
  jest.spyOn(console, "warn").mockImplementation(jest.fn());
});

describe("ic-skeleton", () => {
  it("should render with default height and width", async () => {
    const page = await newSpecPage({
      components: [Skeleton],
      html: `<ic-skeleton></ic-skeleton>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with supplied height", async () => {
    const page = await newSpecPage({
      components: [Skeleton],
      html: `<ic-skeleton style="height: 100px;"></ic-skeleton>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with supplied width", async () => {
    const page = await newSpecPage({
      components: [Skeleton],
      html: `<ic-skeleton style="width: 300px;"></ic-skeleton>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with supplied height and width", async () => {
    const page = await newSpecPage({
      components: [Skeleton],
      html: `<ic-skeleton style="height: 100px; width: 300px;"></ic-skeleton>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with supplied height and width in props", async () => {
    const page = await newSpecPage({
      components: [Skeleton],
      html: `<ic-skeleton height="100px" width="300px"></ic-skeleton>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render circular variant", async () => {
    const page = await newSpecPage({
      components: [Skeleton],
      html: `<ic-skeleton variant="circle"></ic-skeleton>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render circular variant with height", async () => {
    const page = await newSpecPage({
      components: [Skeleton],
      html: `<ic-skeleton variant="circle" height="150px"></ic-skeleton>`,
    });

    page.rootInstance.width = "150px";

    expect(page.root).toMatchSnapshot();
  });

  it("should render circular variant with width", async () => {
    const page = await newSpecPage({
      components: [Skeleton],
      html: `<ic-skeleton variant="circle" width="150px"></ic-skeleton>`,
    });

    page.rootInstance.height = "150px";

    expect(page.root).toMatchSnapshot();
  });

  it("should render text variant", async () => {
    const page = await newSpecPage({
      components: [Skeleton],
      html: `<ic-skeleton variant="text"><ic-typography>Test</ic-typography></ic-skeleton>`,
    });

    expect(page.root).toMatchSnapshot();
  });
});
