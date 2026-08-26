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
/* eslint-disable react/jsx-no-bind */
/// <reference types="Cypress" />

import { mount } from "cypress/react";
import React from "react";
import { IcSectionContainer, IcButton } from "../../components";
import { setThresholdBasedOnEnv } from "../../../cypress/utils/helpers";

const DEFAULT_TEST_THRESHOLD = 0.009;
const SECTION_CONTAINER_SELECTOR = "ic-section-container";

describe("IcSectionContainer visual regression and a11y tests", () => {
  beforeEach(() => {
    cy.viewport(1024, 750);
    cy.injectAxe();
  });

  afterEach(() => {
    cy.task("generateReport");
  });

  it("should render default left aligned section container", () => {
    mount(
      <IcSectionContainer style={{ border: "1px solid black" }}>
        <main>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <IcButton>Start</IcButton>
            <IcButton>End</IcButton>
          </div>
        </main>
      </IcSectionContainer>
    );

    cy.checkHydrated(SECTION_CONTAINER_SELECTOR);

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/left-aligned",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD),
    });
  });

  it("should render center aligned section container", () => {
    mount(
      <IcSectionContainer
        aligned="center"
        style={{ border: "1px solid black" }}
      >
        <main>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <IcButton>Start</IcButton>
            <IcButton>End</IcButton>
          </div>
        </main>
      </IcSectionContainer>
    );

    cy.checkHydrated(SECTION_CONTAINER_SELECTOR);

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/center-aligned",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD),
    });
  });

  it("should render full width section container", () => {
    mount(
      <IcSectionContainer
        aligned="full-width"
        style={{ border: "1px solid black" }}
      >
        <main>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <IcButton>Start</IcButton>
            <IcButton>End</IcButton>
          </div>
        </main>
      </IcSectionContainer>
    );

    cy.checkHydrated(SECTION_CONTAINER_SELECTOR);

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/full-width",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD),
    });
  });

  it("should render full width section container", () => {
    mount(
      <IcSectionContainer
        aligned="full-width"
        fullHeight="true"
        style={{ border: "1px solid black" }}
      >
        <main>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <IcButton>Start</IcButton>
            <IcButton>End</IcButton>
          </div>
        </main>
      </IcSectionContainer>
    );

    cy.checkHydrated(SECTION_CONTAINER_SELECTOR);

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/full-height",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD),
    });
  });
});
