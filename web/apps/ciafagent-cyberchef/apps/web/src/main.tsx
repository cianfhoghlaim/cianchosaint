/**
 * CIANCHOSAINT new-build: ciafagent-cyberchef web app entry.
 *
 * Wholesale pattern: mirrors ciafagent-psni-internal/apps/web/src/main.tsx.
 *
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
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
import { CopilotKit } from "@copilotkit/react-core/v2";
import { ProviderChainBadge } from "./components/ProviderChainBadge";
import "./styles/app.css";

import * as IndexRoute from "./routes/index";
import * as ChatRoute from "./routes/chat";
import * as RecipesRoute from "./routes/recipes";
import * as CatalogRoute from "./routes/operation-catalog";
import * as ExecutionsRoute from "./routes/executions";

const rootRoute = createRootRoute({
  component: () => (
    <CopilotKit runtimeUrl="/api/copilotkit" agent="cyberchef_root_agent">
      <div className="h-screen w-screen flex flex-col bg-slate-950 text-slate-100">
        <header className="h-14 bg-cyan-950 border-b border-cyan-800 flex items-center px-4 justify-between shrink-0">
          <div className="flex items-center gap-3">
            <Link
              to="/"
              className="w-8 h-8 rounded-md bg-cyan-700 flex items-center justify-center font-bold text-white text-sm"
            >
              CC
            </Link>
            <div>
              <Link to="/" className="font-bold text-lg text-cyan-300">
                CyberChef — Internal
              </Link>
              <span className="block text-xs text-red-400">
                UK PUBLIC-SECTOR ANALYST ONLY
              </span>
            </div>
          </div>
          <nav className="flex items-center gap-4 text-sm">
            <Link to="/chat" className="hover:text-cyan-300">Chat</Link>
            <Link to="/recipes" className="hover:text-cyan-300">Recipes</Link>
            <Link to="/operation-catalog" className="hover:text-cyan-300">Operations</Link>
            <Link to="/executions" className="hover:text-cyan-300">Executions</Link>
          </nav>
        </header>
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
        <ProviderChainBadge
          rootAgent="cyberchef_root_agent"
          jurisdiction="uk"
        />
      </div>
    </CopilotKit>
  ),
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component:
    IndexRoute.default ||
    IndexRoute.Route?.component ||
    (() => <div>Index</div>),
});
const chatRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/chat",
  component:
    ChatRoute.default ||
    ChatRoute.Route?.component ||
    (() => <div>Chat</div>),
});
const recipesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/recipes",
  component:
    RecipesRoute.default ||
    RecipesRoute.Route?.component ||
    (() => <div>Recipes</div>),
});
const catalogRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/operation-catalog",
  component:
    CatalogRoute.default ||
    CatalogRoute.Route?.component ||
    (() => <div>Operation Catalog</div>),
});
const executionsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/executions",
  component:
    ExecutionsRoute.default ||
    ExecutionsRoute.Route?.component ||
    (() => <div>Executions</div>),
});

const routeTree = rootRoute.addChildren([
  indexRoute,
  chatRoute,
  recipesRoute,
  catalogRoute,
  executionsRoute,
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
