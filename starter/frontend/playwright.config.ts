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
    baseURL: "http://127.0.0.1:5174",
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
    command: "npm run dev -- --port 5174 --strictPort",
    url: "http://127.0.0.1:5174",
    reuseExistingServer: true,
    timeout: 120_000,
  },
});
