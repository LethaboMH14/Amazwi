import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: false,
    setupFiles: ["./src/test-setup.ts"],
    // Vitest owns src/ only. e2e/ holds Playwright specs, which throw
    // "Playwright Test did not expect test.describe() to be called here"
    // when a second runner tries to collect them. Run those with
    // `npm run test:e2e`.
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
  },
});
