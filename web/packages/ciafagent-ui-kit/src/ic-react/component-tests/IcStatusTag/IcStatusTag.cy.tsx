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
/// <reference types='Cypress' />

import { mount } from "cypress/react";
import React from "react";
import {
  Neutral,
  Success,
  Warning,
  Danger,
  AllStatusesSmall,
  AllStatuses,
  AllStatusesLarge,
  StatusTagsWithSentenceCase,
} from "./IcStatusTagTestData";
import { setThresholdBasedOnEnv } from "../../../cypress/utils/helpers";
import "cypress-axe";
import { HAVE_ATTR, HAVE_TEXT, NOT_HAVE_ATTR } from "../utils/constants";

const STATUS_TAG_SELECTOR = "ic-status-tag";
const DEFAULT_TEST_THRESHOLD = 0.017;

describe("IcStatusTag end-to-end, visual regression and a11y tests", () => {
  beforeEach(() => {
    cy.injectAxe();
  });

  afterEach(() => {
    cy.task("generateReport");
  });

  it("should render neutral status tag", () => {
    mount(<Neutral />);

    cy.checkHydrated(STATUS_TAG_SELECTOR);

    cy.get(STATUS_TAG_SELECTOR).eq(0).should(HAVE_ATTR, "label", "Neutral");
    cy.findShadowEl(STATUS_TAG_SELECTOR, "ic-typography")
      .eq(0)
      .should(HAVE_TEXT, "Neutral");

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/neutral",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD + 0.006),
    });
  });

  it("should render success status tag and add role='status' when announced is set to true", () => {
    mount(<Success />);

    cy.checkHydrated(STATUS_TAG_SELECTOR);

    cy.get(STATUS_TAG_SELECTOR).eq(0).should(HAVE_ATTR, "role", "status");
    cy.get(STATUS_TAG_SELECTOR).eq(1).should(NOT_HAVE_ATTR, "role", "status");

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/success",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD),
    });
  });

  it("should render warning status tag", () => {
    mount(<Warning />);

    cy.checkHydrated(STATUS_TAG_SELECTOR);

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/warning",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD + 0.011),
    });
  });

  it("should render danger status tag", () => {
    mount(<Danger />);

    cy.checkHydrated(STATUS_TAG_SELECTOR);

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/danger",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD + 0.008),
    });
  });

  it("should render small status tags", () => {
    mount(<AllStatusesSmall />);

    cy.checkHydrated(STATUS_TAG_SELECTOR);

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/small",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD + 0.026),
    });
  });

  it("should render large status tags", () => {
    mount(<AllStatusesLarge />);

    cy.checkHydrated(STATUS_TAG_SELECTOR);

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/large",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD + 0.026),
    });
  });

  it("should render a status tag with sentence case", () => {
    mount(<StatusTagsWithSentenceCase />);

    cy.checkHydrated(STATUS_TAG_SELECTOR);

    cy.checkA11yWithWait();
    cy.compareSnapshot({
      name: "/sentence-case",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD + 0.01),
    });
  });
});

describe("IcStatusTag visual regression tests in high contrast mode", () => {
  before(() => {
    cy.enableForcedColors();
  });

  after(() => {
    cy.disableForcedColors();
  });

  afterEach(() => {
    cy.task("generateReport");
  });

  it("should render all status tags in high contrast mode", () => {
    mount(<AllStatuses />);

    cy.checkHydrated(STATUS_TAG_SELECTOR);

    cy.compareSnapshot({
      name: "/high-contrast",
      testThreshold: setThresholdBasedOnEnv(DEFAULT_TEST_THRESHOLD + 0.024),
    });
  });
});
