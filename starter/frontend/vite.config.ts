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
//
// Only the SPEAKER device needs this. Verifier devices play audio and type an
// answer -- neither needs a secure context -- so forcing a self-signed cert on
// them just adds a "connection is not private" click to every verifier laptop
// mid-demo for no benefit. Set AMAZWI_NO_HTTPS=true on those instances.
// AMAZWI_NO_HTTPS=true forces plain HTTP even when certs exist (flag
// already present below). The phone needs HTTPS for getUserMedia, but
// a self-signed cert is a click-through wall for anything that cannot
// accept it. Run the phone instance with certs and a second desktop
// instance with AMAZWI_NO_HTTPS=true, rather than choosing one.
const certDir = path.resolve(__dirname, ".certs");
const httpsConfig =
  process.env.AMAZWI_NO_HTTPS === "true"
    ? undefined
    : fs.existsSync(path.join(certDir, "key.pem")) && fs.existsSync(path.join(certDir, "cert.pem"))
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
      // Audio playback is NOT under /api. The backend returns a playback
      // URL of `/private-audio/play/<token>` and the verifier screen puts
      // that straight into an <audio src>. With only an /api rule, Vite
      // served its own SPA index for that path -- 1378 bytes of text/html
      // where audio/webm was expected -- so every verifier device showed a
      // player that could never play anything, on every laptop, silently.
      //
      // A <audio> element cannot attach headers, which is the whole reason
      // the proxy injects this device's seeded identity. Without that the
      // backend correctly answers 401: the playback token is audience-bound
      // and it re-checks consent at fetch time.
      "/private-audio": {
        target: process.env.API_PROXY_TARGET || "http://127.0.0.1:8000",
        changeOrigin: true,
        headers: identityHeaders,
      },
      "/api": {
        target: process.env.API_PROXY_TARGET || "http://127.0.0.1:8000",
        changeOrigin: true,
        // Every backend router is mounted at its bare path (/consents,
        // /contributions, /assignments, /impact, /ops) with no /api prefix --
        // confirmed by every backend test calling routes that way. Only
        // /health is dual-registered under both. Without this rewrite, every
        // real API call the client makes 404s; only /api/health happened to
        // work, which is why this was invisible until an actual browser walk.
        //
        // The UI symptom was simply that Continue did nothing -- no error, no
        // navigation -- because the 404 was swallowed before it could route.
        // Confirmed by clicking Continue on the real Consent screen and
        // reading the network panel: POST /api/consents -> 404, while a
        // direct POST /consents with the seeded speaker's headers -> 201.
        //
        // /api/health still resolves correctly after the rewrite (-> /health).
        //
        // Found and fixed independently on Lethabo's, Sbu's and Codex's sides
        // within minutes of each other -- same bug, same diagnosis, three
        // separate browser walks. Comments merged rather than one overwriting
        // the others.
        rewrite: (path) => path.replace(/^\/api/, ""),
        // Browser media elements cannot attach headers. Each demo device
        // runs its own proxy process with its own seeded identity.
        headers: identityHeaders,
      },
    },
  },
});
