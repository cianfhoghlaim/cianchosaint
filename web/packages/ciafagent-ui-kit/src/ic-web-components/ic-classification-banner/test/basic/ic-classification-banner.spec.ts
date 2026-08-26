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
import { ClassificationBanner } from "../../ic-classification-banner";

describe("ic-classification-banner component", () => {
  it("should render with default classification text when no classification set", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with official classification text", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification="official"></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with official sensitive classification text", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification="official-sensitive"></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with secret classification text", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification="secret"></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with top secret classification text", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification="top-secret"></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with up to before classification", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification="official" up-to=true></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with a different country when supplied", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification="official" country="us"></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it('should render with no country when supplied ""', async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification="official" country=""></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render default banner if no props are passed", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render default banner if props with empty strings are passed", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification="" country="" additionalSelectors=""></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render default banner if props with undefined are passed", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification=${undefined} country=${undefined} additionalSelectors=${undefined}></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with additional selectors after classification when supplied", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification="official" additional-selectors="ukic"></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });

  it("should render with custom classification text only if supplied", async () => {
    const page = await newSpecPage({
      components: [ClassificationBanner],
      html: `<ic-classification-banner classification="official" custom-classification-text="Custom classification text" additional-selectors="ukic" up-to=true country="uk"></ic-classification-banner>`,
    });

    expect(page.root).toMatchSnapshot();
  });
});
