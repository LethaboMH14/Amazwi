import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const identityHeaders = {
  ...(process.env.VITE_USER_ID ? { "X-User-ID": process.env.VITE_USER_ID } : {}),
  ...(process.env.VITE_PROVIDER_SUBJECT ? { "X-Provider-Subject": process.env.VITE_PROVIDER_SUBJECT } : {}),
};

export default defineConfig({
  plugins: [react()],
  server: {
    port: process.env.PORT ? Number(process.env.PORT) : 5173,
    // Keep the browser calling the same `/api/*` contract in dev and deploy.
    // Override when the backend is not running on the local default port.
    proxy: {
      "/api": {
        target: process.env.API_PROXY_TARGET || "http://127.0.0.1:8000",
        changeOrigin: true,
        // The backend mounts its routes at the ROOT (/consents, /contributions,
        // /assignments, ...), not under /api. Without this rewrite the proxy
        // forwarded /api/consents verbatim and the backend 404'd every single
        // authenticated call.
        //
        // This stayed hidden because the backend also happens to serve
        // /api/health as a special case -- so the one endpoint anyone
        // smoke-tests was the one endpoint that worked, while the whole
        // consent -> record -> verify flow was dead. Found 2 Sep 2026 by
        // clicking Continue on the real Consent screen and reading the
        // network panel: POST /api/consents -> 404.
        //
        // /api/health still resolves correctly after the rewrite (-> /health).
        rewrite: (path) => path.replace(/^\/api/, ""),
        // Browser media elements cannot attach headers. Each demo device
        // runs its own proxy process with its own seeded identity.
        headers: identityHeaders,
      },
    },
  },
});
