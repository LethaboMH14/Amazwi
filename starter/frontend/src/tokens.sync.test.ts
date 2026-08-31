import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

// src/tokens.css is a copy of 04_assets/themes/tokens.css, kept here because
// Vite's dev server does not reliably serve CSS imported from outside src/.
// This test fails the suite the moment the two drift apart -- re-copy from
// the canonical file, never hand-edit the copy in src/.
// Resolved from process.cwd() (the package root, starter/frontend, when run
// via `npm test` from here) rather than import.meta.url -- Vitest's module
// transform does not always yield a real file:// URL for the latter.
describe("tokens.css sync", () => {
  it("matches the canonical 04_assets/themes/tokens.css byte-for-byte", () => {
    const canonical = readFileSync(
      resolve(process.cwd(), "../../04_assets/themes/tokens.css"),
      "utf8"
    );
    const copy = readFileSync(resolve(process.cwd(), "src/tokens.css"), "utf8");
    expect(copy).toBe(canonical);
  });
});
