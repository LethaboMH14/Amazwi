import { defineConfig, devices } from "@playwright/test";

/**
 * Plan 03 Task 11 gate harness.
 *
 * Chromium projects at 320/360/390/430/480 CSS px — the real low-end Android
 * band AMAZWI targets. These run against the actual Vite dev server, not a
 * static snapshot, so what is measured is what a phone would render.
 *
 * The backend is NOT required: every spec stubs `/api/**` itself, so these
 * gates stay deterministic and runnable without Postgres.
 */
const widths = [320, 360, 390, 430, 480];

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  workers: 1,
  reporter: [["list"]],
  timeout: 30_000,
  use: {
    baseURL: "http://127.0.0.1:5199",
    trace: "off",
  },
  projects: widths.map((width) => ({
    name: `chromium-${width}`,
    use: {
      ...devices["Desktop Chrome"],
      viewport: { width, height: 844 },
    },
  })),
  webServer: {
    // Invoke Vite's bin through node directly: on Windows the `npm run dev`
    // shim fails to spawn under Playwright ("The system cannot execute the
    // specified program"). `--host 127.0.0.1` is required because Vite's
    // default bind is IPv6 `::1` only, so a 127.0.0.1 readiness probe never
    // resolves and the webServer wait times out at 120s.
    command: "node node_modules/vite/bin/vite.js --port 5199 --strictPort --host 127.0.0.1",
    url: "http://127.0.0.1:5199",
    // MUST stay false. With `true` and a stray dev server on the port, Playwright
    // silently attaches to whatever is listening and the whole suite measures the
    // wrong application. That is exactly what happened on 2026-09-02: 15 gate
    // failures were captured against an unrelated project's page, not AMAZWI.
    reuseExistingServer: false,
    timeout: 120_000,
  },
});
