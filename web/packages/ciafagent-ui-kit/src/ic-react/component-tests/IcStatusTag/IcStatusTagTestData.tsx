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
import React from "react";
import { IcStatusTag } from "../../components";

export const Neutral = () => {
  return (
    <div style={{ padding: "10px" }}>
      <IcStatusTag label="Neutral" />
      <IcStatusTag label="Neutral" variant="outlined" />
    </div>
  );
};

export const Success = () => {
  return (
    <div style={{ padding: "10px" }}>
      <IcStatusTag label="Success" status="success" announced={true} />
      <IcStatusTag label="Success" status="success" variant="outlined" />
    </div>
  );
};

export const Warning = () => {
  return (
    <div style={{ padding: "10px" }}>
      <IcStatusTag label="Warning" status="warning" />
      <IcStatusTag label="Warning" status="warning" variant="outlined" />
    </div>
  );
};

export const Danger = () => {
  return (
    <div style={{ padding: "10px" }}>
      <IcStatusTag label="Danger" status="danger" />
      <IcStatusTag label="Danger" status="danger" variant="outlined" />
    </div>
  );
};

export const AllStatuses = () => {
  return (
    <div style={{ padding: "10px" }}>
      <IcStatusTag label="Neutral" status="neutral" />
      <IcStatusTag label="Neutral" status="neutral" variant="outlined" />
      <IcStatusTag label="Success" status="success" />
      <IcStatusTag label="Success" status="success" variant="outlined" />
      <IcStatusTag label="Warning" status="warning" />
      <IcStatusTag label="Warning" status="warning" variant="outlined" />
      <IcStatusTag label="Error" status="danger" />
      <IcStatusTag label="Error" status="danger" variant="outlined" />
    </div>
  );
};

export const AllStatusesSmall = () => {
  return (
    <div style={{ padding: "10px" }}>
      <IcStatusTag label="Neutral" status="neutral" size="small" />
      <IcStatusTag
        label="Neutral"
        status="neutral"
        variant="outlined"
        size="small"
      />
      <IcStatusTag label="Success" status="success" size="small" />
      <IcStatusTag
        label="Success"
        status="success"
        variant="outlined"
        size="small"
      />
      <IcStatusTag label="Warning" status="warning" size="small" />
      <IcStatusTag
        label="Warning"
        status="warning"
        variant="outlined"
        size="small"
      />
      <IcStatusTag label="Error" status="danger" size="small" />
      <IcStatusTag
        label="Error"
        status="danger"
        variant="outlined"
        size="small"
      />
    </div>
  );
};

export const AllStatusesLarge = () => {
  return (
    <div style={{ padding: "10px" }}>
      <IcStatusTag label="Neutral" status="neutral" size="large" />
      <IcStatusTag
        label="Neutral"
        status="neutral"
        variant="outlined"
        size="large"
      />
      <IcStatusTag label="Success" status="success" size="large" />
      <IcStatusTag
        label="Success"
        status="success"
        variant="outlined"
        size="large"
      />
      <IcStatusTag label="Warning" status="warning" size="large" />
      <IcStatusTag
        label="Warning"
        status="warning"
        variant="outlined"
        size="large"
      />
      <IcStatusTag label="Error" status="danger" size="large" />
      <IcStatusTag
        label="Error"
        status="danger"
        variant="outlined"
        size="large"
      />
    </div>
  );
};

export const StatusTagsWithSentenceCase = () => {
  return (
    <div style={{ padding: "10px" }}>
      <IcStatusTag label="Neutral status tag" uppercase={false} />
      <IcStatusTag label="neutral" variant="outlined" uppercase={false} />
    </div>
  );
};
