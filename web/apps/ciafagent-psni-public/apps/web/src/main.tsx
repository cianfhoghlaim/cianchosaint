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
    <CopilotKit runtimeUrl="/api/copilotkit" agent="psni_root_agent">
      <div className="h-screen w-screen flex flex-col bg-slate-900 text-slate-100">
        <header className="h-14 bg-emerald-950 border-b border-emerald-800 flex items-center px-4 justify-between shrink-0">
          <div className="flex items-center gap-3">
            <Link to="/" className="w-8 h-8 rounded-md bg-emerald-700 flex items-center justify-center font-bold text-white text-sm">PSNI</Link>
            <div><Link to="/" className="font-bold text-lg text-emerald-300">Police Service of Northern Ireland</Link><span className="block text-xs text-slate-500">psni-public.cianchosaint.ie</span></div>
          </div>
          <nav className="flex items-center gap-4 text-sm">
            <Link to="/chat" className="hover:text-emerald-300">Chat</Link>
            <Link to="/form-fill" className="hover:text-emerald-300">Form fill</Link>
            <Link to="/statute-search" className="hover:text-emerald-300">Statute search</Link>
            <Link to="/about" className="hover:text-emerald-300">About</Link>
          </nav>
        </header>
        <main className="flex-1 overflow-y-auto"><Outlet /></main>
        <ProviderChainBadge rootAgent="psni_root_agent" jurisdiction="psni" />
      </div>
    </CopilotKit>
  ),
});

const indexRoute = createRoute({ getParentRoute: () => rootRoute, path: "/", component: () => <><PrivacyDisclaimer jurisdiction="psni" /><IndexRoute.default || IndexRoute.Route?.component || (() => <div>Index</div>)}</> });
const chatRoute = createRoute({ getParentRoute: () => rootRoute, path: "/chat", component: () => <><PrivacyDisclaimer jurisdiction="psni" /><ChatRoute.default || ChatRoute.Route?.component || (() => <div>Chat</div>)}</> });
const formFillRoute = createRoute({ getParentRoute: () => rootRoute, path: "/form-fill", component: () => FormFillRoute.default || FormFillRoute.Route?.component || (() => <div>Form fill</div>) });
const statuteRoute = createRoute({ getParentRoute: () => rootRoute, path: "/statute-search", component: () => StatuteRoute.default || StatuteRoute.Route?.component || (() => <div>Statute search</div>) });
const aboutRoute = createRoute({ getParentRoute: () => rootRoute, path: "/about", component: () => AboutRoute.default || AboutRoute.Route?.component || (() => <div>About</div>) });

const routeTree = rootRoute.addChildren([indexRoute, chatRoute, formFillRoute, statuteRoute, aboutRoute]);
const router = createRouter({ routeTree });
declare module "@tanstack/react-router" { interface Register { router: typeof router; } }
const root = document.getElementById("root")!;
ReactDOM.createRoot(root).render(<React.StrictMode><RouterProvider router={router} /></React.StrictMode>);
