import { test, expect, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { ROUTES, stubApi } from "./fixtures";

const THEMES = ["midnight", "daylight"] as const;

async function withTheme(page: Page, theme: string) {
  await page.addInitScript((value) => {
    window.localStorage.setItem("amazwi.theme", value);
  }, theme);
}

/**
 * WCAG 1.4.10 Reflow. 200% zoom is emulated by doubling the root font size,
 * which is what an actual text-zoom does to a layout built in relative units.
 * A layout pinned to fixed pixels does not move and therefore overflows —
 * exactly the defect the .dc.html mockups have by construction and that the
 * real frontend was explicitly told not to inherit.
 */
test.describe("reflow", () => {
  for (const route of ROUTES) {
    test(`${route.name} reflows at 200% zoom without horizontal scroll`, async ({ page }) => {
      await stubApi(page);
      await page.goto(route.path);
      await page.evaluate(() => {
        document.documentElement.style.fontSize = "200%";
      });
      await page.waitForTimeout(50);
      const measured = await page.evaluate(() => ({
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
      }));
      expect(measured.scrollWidth).toBeLessThanOrEqual(measured.clientWidth);
    });
  }
});

/**
 * Real Tab presses, not `.focus()`. Chromium only sets :focus-visible from a
 * genuine keyboard interaction, which is precisely why the mockup pass had to
 * re-verify its button conversions this way.
 */
test.describe("keyboard", () => {
  for (const route of ROUTES) {
    test(`${route.name} reaches every interactive control by Tab with a visible focus ring`, async ({ page }) => {
      await stubApi(page);
      await page.goto(route.path);
      await page.waitForTimeout(150);

      const expected = await page.evaluate(() =>
        Array.from(
          document.querySelectorAll<HTMLElement>(
            'a[href], button, input, select, textarea, audio[controls], [tabindex]:not([tabindex="-1"])',
          ),
        ).filter((el) => el.offsetParent !== null || el.tagName === "AUDIO").length,
      );
      expect(expected).toBeGreaterThan(0);

      const seen: string[] = [];
      for (let i = 0; i < expected + 2; i += 1) {
        await page.keyboard.press("Tab");
        const stop = await page.evaluate(() => {
          const el = document.activeElement as HTMLElement | null;
          if (!el || el === document.body) return null;
          return {
            tag: el.tagName,
            focusVisible: el.matches(":focus-visible"),
            outlineWidth: getComputedStyle(el).outlineWidth,
            hiddenAncestor: !!el.closest("[aria-hidden='true']"),
            name:
              el.getAttribute("aria-label") ||
              (el.labels && el.labels.length ? el.labels[0].textContent : "") ||
              el.textContent ||
              "",
          };
        });
        if (!stop) break;
        // Chromium exposes the shadow-DOM <audio> controls as one stop; its
        // internals are UA-provided and are not ours to name or style.
        if (stop.tag === "AUDIO") {
          seen.push(stop.tag);
          continue;
        }
        expect(stop.focusVisible, `${stop.tag} did not report :focus-visible after a real Tab`).toBe(true);
        expect(parseFloat(stop.outlineWidth), `${stop.tag} has no visible focus outline`).toBeGreaterThan(0);
        expect(stop.hiddenAncestor, `focus entered an aria-hidden subtree (${stop.tag})`).toBe(false);
        expect((stop.name || "").trim().length, `${stop.tag} has no accessible name`).toBeGreaterThan(0);
        seen.push(stop.tag);
      }
      expect(seen.length).toBeGreaterThanOrEqual(expected);
    });
  }

  test("the consent primary action activates on Enter, observed in Chromium", async ({ page }) => {
    await stubApi(page);
    await page.goto("/consent");
    const button = page.getByRole("button", { name: /continue/i });
    await button.focus();
    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(/\/$/);
  });

  test("the recording control toggles on Space, observed in Chromium", async ({ page, context }) => {
    await context.grantPermissions([]);
    await stubApi(page);
    await page.goto("/record/contribution-1");
    const button = page.getByRole("button", { name: /start recording/i });
    await expect(button).toBeVisible();
    await button.focus();
    await page.keyboard.press("Space");
    // getUserMedia is denied in this context, so the honest observable outcome
    // is the error region announcing — which still proves the key activated
    // the handler rather than being swallowed.
    await expect(page.getByRole("alert")).toBeVisible({ timeout: 5000 });
  });
});

test.describe("touch targets", () => {
  for (const route of ROUTES) {
    test(`${route.name} controls meet the 44px minimum`, async ({ page }) => {
      await stubApi(page);
      await page.goto(route.path);
      await page.waitForTimeout(150);
      const undersized = await page.evaluate(() =>
        Array.from(document.querySelectorAll<HTMLElement>("button, a[href], select"))
          .filter((el) => el.offsetParent !== null)
          .map((el) => {
            const r = el.getBoundingClientRect();
            return { text: (el.textContent || "").trim().slice(0, 40), w: Math.round(r.width), h: Math.round(r.height) };
          })
          .filter((m) => m.h < 44 || m.w < 44),
      );
      expect(undersized, JSON.stringify(undersized)).toEqual([]);
    });
  }
});

test.describe("axe", () => {
  for (const theme of THEMES) {
    for (const route of ROUTES) {
      test(`${route.name} has no serious or critical axe violations in ${theme}`, async ({ page }) => {
        await withTheme(page, theme);
        await stubApi(page);
        await page.goto(route.path);
        await page.waitForTimeout(200);
        const results = await new AxeBuilder({ page })
          .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
          .analyze();
        const blocking = results.violations.filter(
          (v) => v.impact === "serious" || v.impact === "critical",
        );
        expect(
          blocking.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(" ")).join(", ")}`),
        ).toEqual([]);
      });
    }
  }
});

test.describe("screen-reader semantics", () => {
  test("the status announcer regions carry the documented live contract", async ({ page }) => {
    await stubApi(page);
    await page.goto("/verify?contributionId=contribution-1");
    await page.waitForTimeout(300);
    const regions = await page.evaluate(() =>
      Array.from(document.querySelectorAll("[aria-live]")).map((el) => ({
        live: el.getAttribute("aria-live"),
        atomic: el.getAttribute("aria-atomic"),
      })),
    );
    expect(regions.some((r) => r.live === "polite")).toBe(true);
    expect(regions.some((r) => r.live === "assertive")).toBe(true);
  });

  test("every route exposes a labelled main landmark", async ({ page }) => {
    for (const route of ROUTES) {
      await stubApi(page);
      await page.goto(route.path);
      const labelled = await page.evaluate(() => {
        const main = document.querySelector("main");
        if (!main) return false;
        const id = main.getAttribute("aria-labelledby");
        return !!(main.getAttribute("aria-label") || (id && document.getElementById(id)));
      });
      expect(labelled, `${route.name} main is not labelled`).toBe(true);
    }
  });
});
