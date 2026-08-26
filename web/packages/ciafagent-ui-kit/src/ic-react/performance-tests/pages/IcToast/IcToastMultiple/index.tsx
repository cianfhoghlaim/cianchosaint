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
// IcToastMultiplePage displays multiple toast components for performance testing of the IcToast component.
import React, { useRef, useEffect } from "react";
import { IcToast, IcToastRegion, IcTheme } from "../../../../components";

type PageProps = {
  theme: "light" | "dark";
};

const IcToastMultiplePage: React.FC<PageProps> = ({ theme }) => {
  const toastRegionEl = useRef<HTMLIcToastRegionElement | null>(null);
  const toastRefs = Array.from({ length: 20 }, () =>
    useRef<HTMLIcToastElement | null>(null)
  );

  const queueIndex = useRef(0);

  useEffect(() => {
    if (toastRegionEl.current && toastRefs[0].current) {
      toastRegionEl.current.openToast = toastRefs[0].current;
    }
  }, [toastRefs]);

  const handleDismiss = () => {
    queueIndex.current += 1;
    if (
      queueIndex.current < toastRefs.length &&
      toastRegionEl.current &&
      toastRefs[queueIndex.current]
    ) {
      toastRefs[queueIndex.current].current.setVisible();
    }
  };

  return (
    <IcTheme id="theme-wrapper" theme={theme}>
      <IcToastRegion ref={toastRegionEl}>
        {toastRefs.map((ref, i) => (
          <IcToast
            key={i}
            heading="Your coffee is ready"
            ref={ref}
            onIcDismiss={() => {
              console.log(`Toast ${i + 1} dismissed`);
              handleDismiss();
            }}
          />
        ))}
      </IcToastRegion>
    </IcTheme>
  );
};

export default IcToastMultiplePage;
