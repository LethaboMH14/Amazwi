import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import fs from "node:fs";
import path from "node:path";

const identityHeaders = {
  ...(process.env.VITE_USER_ID ? { "X-User-ID": process.env.VITE_USER_ID } : {}),
  ...(process.env.VITE_PROVIDER_SUBJECT ? { "X-Provider-Subject": process.env.VITE_PROVIDER_SUBJECT } : {}),
};

// mediaDevices.getUserMedia() does not exist at all in a browser's `window`
// object outside a secure context. A LAN IP over plain HTTP is not secure,
// so on a phone the mic button threw "Cannot read properties of undefined
// (reading 'getUserMedia')" -- not a permission prompt, the API was simply
// absent. Self-signed HTTPS makes the origin secure; the phone accepts one
// standard "connection not private" warning (self-signed, expected for a
// local demo) and getUserMedia becomes available. Certs are demo-only,
// 3-day expiry, gitignored -- generate with:
//   openssl req -x509 -newkey rsa:2048 -keyout .certs/key.pem \
//     -out .certs/cert.pem -days 3 -nodes -config .certs/san.cnf
const certDir = path.resolve(__dirname, ".certs");
const httpsConfig =
  fs.existsSync(path.join(certDir, "key.pem")) && fs.existsSync(path.join(certDir, "cert.pem"))
    ? {
        key: fs.readFileSync(path.join(certDir, "key.pem")),
        cert: fs.readFileSync(path.join(certDir, "cert.pem")),
      }
    : undefined;

export default defineConfig({
  plugins: [react()],
  server: {
    port: process.env.PORT ? Number(process.env.PORT) : 5173,
    https: httpsConfig,
    // Keep the browser calling the same `/api/*` contract in dev and deploy.
    // Override when the backend is not running on the local default port.
    proxy: {
      "/api": {
        target: process.env.API_PROXY_TARGET || "http://127.0.0.1:8000",
        changeOrigin: true,
        // Every backend router is mounted at its bare path (/consents,
        // /contributions, ...) with no /api prefix -- confirmed by every
        // backend test calling routes that way. Only /health is dual-
        // registered under both. Without this rewrite, every real API
        // call the client makes 404s; only /api/health happened to work,
        // which is why this was invisible until an actual browser walk.
        // (Found and fixed independently on both Sbu's and Codex's side
        // within minutes of each other -- same bug, same diagnosis.)
        rewrite: (path) => path.replace(/^\/api/, ""),
        // Browser media elements cannot attach headers. Each demo device
        // runs its own proxy process with its own seeded identity.
        headers: identityHeaders,
      },
    },
  },
});
