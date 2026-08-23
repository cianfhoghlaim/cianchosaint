/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
// apps/web/src/main.tsx — ciafagent-ga-internal SPA entry point
// INTERNAL — Garda network only. Cross-references PULSE schema.

import * as React from "react";
import ReactDOM from "react-dom/client";
import {
  createRouter, createRoute, createRootRoute, RouterProvider, Outlet, Link,
} from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { CopilotKit } from "@copilotkit/react-core/v2";
import { ProviderChainBadge } from "./components/ProviderChainBadge";

import "./styles/app.css";

import * as IndexRoute from "./routes/index";
import * as ChatRoute from "./routes/chat";
import * as PulseRoute from "./routes/pulse";
import * as CircularsRoute from "./routes/circulars";
import * as TrainingRoute from "./routes/training";

const rootRoute = createRootRoute({
  component: () => (
    <CopilotKit runtimeUrl="/api/copilotkit" agent="ga_root_agent">
      <div className="h-screen w-screen flex flex-col bg-slate-950 text-slate-100 font-sans">
        <header className="h-14 bg-slate-900 border-b border-blue-800 flex items-center px-4 justify-between shrink-0">
          <div className="flex items-center gap-3">
            <Link to="/" className="w-8 h-8 rounded-md bg-blue-700 flex items-center justify-center font-bold text-white text-sm">GA</Link>
            <div>
              <Link to="/" className="font-bold text-lg text-blue-300">An Garda Síochána — Internal</Link>
              <span className="block text-xs text-red-400">⚠ INTERNAL ONLY · RESTRICTED ACCESS</span>
            </div>
          </div>
          <nav className="flex items-center gap-4 text-sm">
            <Link to="/chat" className="text-slate-300 hover:text-blue-300">Chat</Link>
            <Link to="/pulse" className="text-slate-300 hover:text-blue-300">PULSE</Link>
            <Link to="/circulars" className="text-slate-300 hover:text-blue-300">Circulars</Link>
            <Link to="/training" className="text-slate-300 hover:text-blue-300">Training</Link>
          </nav>
        </header>
        <main className="flex-1 overflow-y-auto"><Outlet /></main>
        <ProviderChainBadge rootAgent="ga_root_agent" jurisdiction="ga" />
        {import.meta.env.DEV && <TanStackRouterDevtools position="bottom-right" />}
      </div>
    </CopilotKit>
  ),
});

const indexRoute = createRoute({ getParentRoute: () => rootRoute, path: "/", component: IndexRoute.default || IndexRoute.Route?.component || (() => <div>Index</div>) });
const chatRoute = createRoute({ getParentRoute: () => rootRoute, path: "/chat", component: ChatRoute.default || ChatRoute.Route?.component || (() => <div>Chat</div>) });
const pulseRoute = createRoute({ getParentRoute: () => rootRoute, path: "/pulse", component: PulseRoute.default || PulseRoute.Route?.component || (() => <div>PULSE</div>) });
const circularsRoute = createRoute({ getParentRoute: () => rootRoute, path: "/circulars", component: CircularsRoute.default || CircularsRoute.Route?.component || (() => <div>Circulars</div>) });
const trainingRoute = createRoute({ getParentRoute: () => rootRoute, path: "/training", component: TrainingRoute.default || TrainingRoute.Route?.component || (() => <div>Training</div>) });

const routeTree = rootRoute.addChildren([indexRoute, chatRoute, pulseRoute, circularsRoute, trainingRoute]);
const router = createRouter({ routeTree });

declare module "@tanstack/react-router" { interface Register { router: typeof router; } }

const root = document.getElementById("root")!;
ReactDOM.createRoot(root).render(<React.StrictMode><RouterProvider router={router} /></React.StrictMode>);
