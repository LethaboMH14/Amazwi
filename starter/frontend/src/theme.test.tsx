import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { ThemeControl, ThemeProvider, isNdebeleSeason, useTheme } from "./theme";

describe("isNdebeleSeason", () => {
  it("is true in September regardless of query string", () => {
    expect(isNdebeleSeason(new Date(2026, 8, 15))).toBe(true); // month index 8 = September
  });

  it("is false outside September with no override query param", () => {
    expect(isNdebeleSeason(new Date(2026, 7, 15))).toBe(false); // August
    expect(isNdebeleSeason(new Date(2026, 9, 15))).toBe(false); // October
  });

  it("is true outside September when ?season=heritage is present", () => {
    expect(isNdebeleSeason(new Date(2026, 0, 1), "?season=heritage")).toBe(true);
  });

  it("ignores an unrelated or wrong-value season query param outside September", () => {
    expect(isNdebeleSeason(new Date(2026, 0, 1), "?season=other")).toBe(false);
    expect(isNdebeleSeason(new Date(2026, 0, 1), "?other=heritage")).toBe(false);
  });

  it("is true on both the first and last day of September", () => {
    expect(isNdebeleSeason(new Date(2026, 8, 1))).toBe(true);
    expect(isNdebeleSeason(new Date(2026, 8, 30))).toBe(true);
  });
});

function ThemeProbe() {
  const { theme } = useTheme();
  return <span data-testid="theme-value">{theme}</span>;
}

describe("ThemeProvider / ThemeControl", () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.removeAttribute("data-theme");
  });

  it("defaults to daylight when nothing is saved", () => {
    // Changed 3 Sep 2026: Signal Daylight is now the Figma light
    // fintech direction and the product's default face. Midnight is
    // still selectable and still the dark palette.
    render(
      <ThemeProvider>
        <ThemeProbe />
      </ThemeProvider>,
    );
    expect(screen.getByTestId("theme-value").textContent).toBe("daylight");
    expect(document.documentElement.dataset.theme).toBe("daylight");
  });

  it("restores a previously saved daylight theme", () => {
    localStorage.setItem("amazwi.theme", "daylight");
    render(
      <ThemeProvider>
        <ThemeProbe />
      </ThemeProvider>,
    );
    expect(screen.getByTestId("theme-value").textContent).toBe("daylight");
  });

  it("switching the theme control updates context, the DOM attribute, and persists to localStorage", () => {
    render(
      <ThemeProvider>
        <ThemeControl />
        <ThemeProbe />
      </ThemeProvider>,
    );
    fireEvent.change(screen.getByLabelText(/theme/i), { target: { value: "daylight" } });
    expect(screen.getByTestId("theme-value").textContent).toBe("daylight");
    expect(document.documentElement.dataset.theme).toBe("daylight");
    expect(localStorage.getItem("amazwi.theme")).toBe("daylight");
  });

  it("offers both Midnight Shweshwe and Signal Daylight as first-class options", () => {
    render(
      <ThemeProvider>
        <ThemeControl />
      </ThemeProvider>,
    );
    const select = screen.getByLabelText(/theme/i) as HTMLSelectElement;
    const optionValues = Array.from(select.options).map((o) => o.value);
    expect(optionValues).toContain("midnight");
    expect(optionValues).toContain("daylight");
  });
});
