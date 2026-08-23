/**
 * CIANCHOSAINT wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/cianchosaint-repo-bootstrap-v2/specs/cianchosaint-bootstrap-v2/spec.md).
 * Migrated to cianchosaint: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import * as React from "react";
import ReactDOM from "react-dom/client";
import { createRouter, createRoute, createRootRoute, RouterProvider, Outlet, Link } from "@tanstack/react-router";
import { CopilotKit } from "@copilotkit/react-core/v2";
import { ProviderChainBadge } from "./components/ProviderChainBadge";
import "./styles/app.css";
import * as IndexRoute from "./routes/index";
import * as ChatRoute from "./routes/chat";
import * as PolicingBoardRoute from "./routes/policing-board";
import * as CircularsRoute from "./routes/circulars";
import * as TrainingRoute from "./routes/training";

const rootRoute = createRootRoute({
  component: () => (
    <CopilotKit runtimeUrl="/api/copilotkit" agent="psni_root_agent">
      <div className="h-screen w-screen flex flex-col bg-slate-950 text-slate-100">
        <header className="h-14 bg-emerald-950 border-b border-emerald-800 flex items-center px-4 justify-between shrink-0">
          <div className="flex items-center gap-3"><Link to="/" className="w-8 h-8 rounded-md bg-emerald-700 flex items-center justify-center font-bold text-white text-sm">PSNI</Link><div><Link to="/" className="font-bold text-lg text-emerald-300">PSNI — Internal</Link><span className="block text-xs text-red-400">⚠ INTERNAL ONLY</span></div></div>
          <nav className="flex items-center gap-4 text-sm"><Link to="/chat" className="hover:text-emerald-300">Chat</Link><Link to="/policing-board" className="hover:text-emerald-300">Policing Board</Link><Link to="/circulars" className="hover:text-emerald-300">Circulars</Link><Link to="/training" className="hover:text-emerald-300">Training</Link></nav>
        </header>
        <main className="flex-1 overflow-y-auto"><Outlet /></main>
        <ProviderChainBadge rootAgent="psni_root_agent" jurisdiction="psni" />
      </div>
    </CopilotKit>
  ),
});

const indexRoute = createRoute({ getParentRoute: () => rootRoute, path: "/", component: IndexRoute.default || IndexRoute.Route?.component || (() => <div>Index</div>) });
const chatRoute = createRoute({ getParentRoute: () => rootRoute, path: "/chat", component: ChatRoute.default || ChatRoute.Route?.component || (() => <div>Chat</div>) });
const pbRoute = createRoute({ getParentRoute: () => rootRoute, path: "/policing-board", component: PolicingBoardRoute.default || PolicingBoardRoute.Route?.component || (() => <div>Policing Board</div>) });
const circRoute = createRoute({ getParentRoute: () => rootRoute, path: "/circulars", component: CircularsRoute.default || CircularsRoute.Route?.component || (() => <div>Circulars</div>) });
const trainRoute = createRoute({ getParentRoute: () => rootRoute, path: "/training", component: TrainingRoute.default || TrainingRoute.Route?.component || (() => <div>Training</div>) });

const routeTree = rootRoute.addChildren([indexRoute, chatRoute, pbRoute, circRoute, trainRoute]);
const router = createRouter({ routeTree });
declare module "@tanstack/react-router" { interface Register { router: typeof router; } }
const root = document.getElementById("root")!;
ReactDOM.createRoot(root).render(<React.StrictMode><RouterProvider router={router} /></React.StrictMode>);
