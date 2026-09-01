import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

// vitest.config.ts sets globals: false, so @testing-library/react's automatic
// per-test cleanup (which relies on detecting a global afterEach) never
// registers. Without this, DOM nodes from one render leak into the next test
// in the same file -- invisible until a file renders more than once.
afterEach(() => {
  cleanup();
});
