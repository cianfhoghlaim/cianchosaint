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
import React, { useEffect, useRef, FC } from "react";
import { IcToast, IcButton, IcToastRegion, SlottedSVG, IcLink } from "../..";
import { IcStatusVariants } from "@ukic/web-components";

export const ToastTypes: FC<{ variant: IcStatusVariants }> = ({ variant }) => {
  const toastRegionEl = useRef<any>(null);
  const toastEl = useRef<any>(null);
  const handleClick = () => {
    toastRegionEl.current.openToast = toastEl.current;
  };
  return (
    <>
      <IcButton onClick={handleClick}>Display toast</IcButton>
      <IcToastRegion ref={toastRegionEl}>
        <IcToast
          heading="Your coffee is ready"
          ref={toastEl}
          message="Please dismiss and collect"
          variant={variant}
        />
      </IcToastRegion>
    </>
  );
};

export const SimpleAutoDismissToast = () => {
  const toastRegionEl = useRef<any>(null);
  const toastEl = useRef<any>(null);
  const handleClick = () => {
    toastRegionEl.current.openToast = toastEl.current;
  };
  return (
    <>
      <IcButton onClick={handleClick}>Display toast</IcButton>
      <IcToastRegion ref={toastRegionEl}>
        <IcToast
          heading="Your coffee is ready"
          ref={toastEl}
          message="Please dismiss and collect"
          variant="success"
          dismissMode="automatic"
          autoDismissTimeout={100}
        />
      </IcToastRegion>
    </>
  );
};

export const SlottedActionToast = () => {
  const toastRegionEl = useRef<any>(null);
  const toastEl = useRef<any>(null);
  const handleClick = () => {
    toastRegionEl.current.openToast = toastEl.current;
  };
  return (
    <>
      <IcButton id="open-toast-btn" onClick={handleClick}>
        Display toast
      </IcButton>
      <IcToastRegion ref={toastRegionEl}>
        <IcToast
          heading="Your coffee is ready"
          ref={toastEl}
          message="Please dismiss and collect"
          variant="success"
        >
          <IcButton id="test-button" slot="action">
            Test
          </IcButton>
        </IcToast>
      </IcToastRegion>
    </>
  );
};

export const SlottedLinkToast = () => {
  const toastRegionEl = useRef<any>(null);
  const toastEl = useRef<any>(null);
  const handleClick = () => {
    toastRegionEl.current.openToast = toastEl.current;
  };
  return (
    <>
      <IcButton id="open-toast-btn" onClick={handleClick}>
        Display toast
      </IcButton>
      <IcToastRegion ref={toastRegionEl}>
        <IcToast
          heading="Your coffee is ready"
          ref={toastEl}
          message="Please dismiss and collect"
          variant="success"
        >
          <IcLink href="/" slot="action" theme="dark" monochrome={true}>
            Test
          </IcLink>
        </IcToast>
      </IcToastRegion>
    </>
  );
};

export const SlottedActionAutoDismissToast = () => {
  const toastRegionEl = useRef<any>(null);
  const toastEl = useRef<any>(null);
  const handleClick = () => {
    toastRegionEl.current.openToast = toastEl.current;
  };
  return (
    <>
      <IcButton id="open-toast-btn" onClick={handleClick}>
        Display toast
      </IcButton>
      <IcToastRegion ref={toastRegionEl}>
        <IcToast
          heading="Your coffee is ready"
          ref={toastEl}
          message="Please dismiss and collect"
          variant="success"
          dismissMode="automatic"
        >
          <IcButton id="test-button" slot="action">
            Test
          </IcButton>
        </IcToast>
      </IcToastRegion>
    </>
  );
};

export const SlottedIconToast = () => {
  const toastRegionEl = useRef<any>(null);
  const toastEl = useRef<any>(null);
  const handleClick = () => {
    toastRegionEl.current.openToast = toastEl.current;
  };
  return (
    <>
      <IcButton onClick={handleClick}>Display toast</IcButton>
      <IcToastRegion ref={toastRegionEl}>
        <IcToast
          heading="Your coffee is ready"
          ref={toastEl}
          message="Please dismiss and collect"
        >
          <SlottedSVG
            slot="neutral-icon"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M8.79502 15.875L4.62502 11.705L3.20502 13.115L8.79502 18.705L20.795 6.70501L19.385 5.29501L8.79502 15.875Z" />
          </SlottedSVG>
        </IcToast>
      </IcToastRegion>
    </>
  );
};

export const HeadingOnlyToast = () => {
  const toastRegionEl = useRef<any>(null);
  const toastEl = useRef<any>(null);
  const handleClick = () => {
    toastRegionEl.current.openToast = toastEl.current;
  };
  return (
    <>
      <IcButton onClick={handleClick}>Display toast</IcButton>
      <IcToastRegion ref={toastRegionEl}>
        <IcToast heading="Your coffee is ready" ref={toastEl} />
      </IcToastRegion>
    </>
  );
};

export const MultilineMessageToast = () => {
  const toastRegionEl = useRef<any>(null);
  const toastEl = useRef<any>(null);
  const handleClick = () => {
    toastRegionEl.current.openToast = toastEl.current;
  };
  return (
    <>
      <IcButton onClick={handleClick}>Display toast</IcButton>
      <IcToastRegion ref={toastRegionEl}>
        <IcToast
          heading="Your coffee is ready"
          ref={toastEl}
          message="Please dismiss and come to collect your delicious coffee from the barista right away before it gets cold. Don't delay! We wouldn't want you to lose out on your fantastic coffee now would we?"
        />
      </IcToastRegion>
    </>
  );
};

export const DismissAriaLabelToast = () => {
  const toastRegionEl = useRef<any>(null);
  const toastEl = useRef<any>(null);
  const handleClick = () => {
    toastRegionEl.current.openToast = toastEl.current;
  };
  return (
    <>
      <IcButton onClick={handleClick}>Display toast</IcButton>
      <IcToastRegion ref={toastRegionEl}>
        <IcToast
          heading="Your coffee is ready"
          ref={toastEl}
          message="Please dismiss and collect"
          variant="neutral"
          dismissButtonAriaLabel="dismiss me"
        />
      </IcToastRegion>
    </>
  );
};

export const AutoLoadToast = (): JSX.Element => {
  const toastRegionEl = useRef<HTMLIcToastRegionElement>(null);
  const shareToastEl = useRef<HTMLIcToastElement>(null);

  useEffect(() => {
    if (toastRegionEl.current && shareToastEl.current) {
      toastRegionEl.current.openToast = shareToastEl.current;
    }
  }, []);

  return (
    <IcToastRegion ref={toastRegionEl}>
      <IcToast heading="My toast heading" ref={shareToastEl} />
    </IcToastRegion>
  );
};
