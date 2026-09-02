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
        // FastAPI mounts API routers at /consents, /contributions, etc.;
        // strip the frontend-only /api prefix before forwarding.
        rewrite: (path) => path.replace(/^\/api/, ""),
        // Browser media elements cannot attach headers. Each demo device
        // runs its own proxy process with its own seeded identity.
        headers: identityHeaders,
      },
    },
  },
});
