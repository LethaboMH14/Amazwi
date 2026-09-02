import { describe, expect, it } from "vitest";
import { formatMinor } from "./money";

// en-ZA formats with a COMMA decimal separator and a space after the symbol:
// 200 minor ZAR renders as "R 2,00", not "R2.00". That is correct for South
// Africa, so these assertions are separator-agnostic rather than forcing a
// US-style dot the product should not be showing.
const digits = (s: string) => s.replace(/[^\d]/g, "");

describe("formatMinor", () => {
  it("renders the demo reward as 2 rand 00, not 200", () => {
    // The exact bug this exists to prevent: the receipt showed "200 ZAR" for
    // a reward the plan publishes as R2.00 -- a 100x overstatement on the
    // screen the pitch relies on to be financially truthful.
    const out = formatMinor(200, "ZAR");
    expect(digits(out)).toBe("200");        // 2 . 0 0
    expect(out).toMatch(/2[.,]00/);
    expect(out).toMatch(/^R/);
  });

  it("always shows two decimal places", () => {
    expect(formatMinor(0, "ZAR")).toMatch(/0[.,]00/);
    expect(formatMinor(1050, "ZAR")).toMatch(/10[.,]50/);
  });

  it("handles a single cent without rounding it away", () => {
    expect(formatMinor(1, "ZAR")).toMatch(/0[.,]01/);
  });

  it("falls back to a readable string rather than throwing on a bad currency code", () => {
    // A receipt must never blow up over an unexpected currency code.
    expect(formatMinor(200, "NOT_A_CODE")).toBe("2.00 NOT_A_CODE");
  });
});
