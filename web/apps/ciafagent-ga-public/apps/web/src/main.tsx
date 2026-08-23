/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/web/src/main.tsx — ciafagent-ga-public SPA entry point
// The public-facing An Garda Síochána entry point.

import * as React from "react";
import ReactDOM from "react-dom/client";
import {
  createRouter,
  createRoute,
  createRootRoute,
  RouterProvider,
  Outlet,
  Link,
} from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { CopilotKit } from "@copilotkit/react-core/v2";
import { PrivacyDisclaimer } from "./components/PrivacyDisclaimer";
import { ProviderChainBadge } from "./components/ProviderChainBadge";

import "./styles/app.css";

import * as IndexRoute from "./routes/index";
import * as ChatRoute from "./routes/chat";
import * as FormFillRoute from "./routes/form-fill";
import * as StatuteRoute from "./routes/statute-search";
import * as AboutRoute from "./routes/about";

const rootRoute = createRootRoute({
  component: () => (
    <CopilotKit
      runtimeUrl="/api/copilotkit"
      agent="ga_root_agent"
    >
      <div className="h-screen w-screen flex flex-col bg-slate-900 text-slate-100 font-sans">
        <header className="h-14 bg-slate-950 border-b border-slate-800 flex items-center px-4 justify-between shrink-0">
          <div className="flex items-center gap-3">
            <Link to="/" className="w-8 h-8 rounded-md bg-emerald-600 flex items-center justify-center font-bold text-white text-sm">
              GA
            </Link>
            <div>
              <Link to="/" className="font-bold text-lg tracking-wider text-emerald-400">
                An Garda Síochána
              </Link>
              <span className="block text-xs text-slate-500">
                Public citizen portal · ga-public.cianchosaint.ie
              </span>
            </div>
          </div>
          <nav className="flex items-center gap-4 text-sm">
            <Link to="/chat" className="text-slate-300 hover:text-emerald-400">Chat</Link>
            <Link to="/form-fill" className="text-slate-300 hover:text-emerald-400">Form fill</Link>
            <Link to="/statute-search" className="text-slate-300 hover:text-emerald-400">Statute search</Link>
            <Link to="/about" className="text-slate-300 hover:text-emerald-400">About</Link>
          </nav>
        </header>
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
        <ProviderChainBadge rootAgent="ga_root_agent" jurisdiction="ga" />
        {import.meta.env.DEV && <TanStackRouterDevtools position="bottom-right" />}
      </div>
    </CopilotKit>
  ),
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: () => (
    <>
      <PrivacyDisclaimer jurisdiction="ga" />
      <IndexRoute.default || IndexRoute.Route?.component || (() => <div>Index</div>)}
    </>
  ),
});

const chatRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/chat",
  component: () => (
    <>
      <PrivacyDisclaimer jurisdiction="ga" />
      <ChatRoute.default || ChatRoute.Route?.component || (() => <div>Chat</div>)}
    </>
  ),
});

const formFillRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/form-fill",
  component: () => FormFillRoute.default || FormFillRoute.Route?.component || (() => <div>Form fill</div>),
});

const statuteRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/statute-search",
  component: () => StatuteRoute.default || StatuteRoute.Route?.component || (() => <div>Statute search</div>),
});

const aboutRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/about",
  component: () => AboutRoute.default || AboutRoute.Route?.component || (() => <div>About</div>),
});

const routeTree = rootRoute.addChildren([
  indexRoute,
  chatRoute,
  formFillRoute,
  statuteRoute,
  aboutRoute,
]);

const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

const root = document.getElementById("root")!;
ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);
