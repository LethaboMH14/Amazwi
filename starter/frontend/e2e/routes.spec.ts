import { test, expect } from "@playwright/test";
import { ROUTES, stubApi } from "./fixtures";

test.describe("routes render on a narrow viewport", () => {
  for (const route of ROUTES) {
    test(`${route.name} renders a single main landmark and one h1`, async ({ page }) => {
      await stubApi(page);
      await page.goto(route.path);
      await expect(page.locator("main")).toHaveCount(1);
      await expect(page.locator("h1")).toHaveCount(1);
      await expect(page.locator("h1")).toBeVisible();
    });

    test(`${route.name} has no horizontal overflow at the project viewport`, async ({ page }) => {
      await stubApi(page);
      await page.goto(route.path);
      const overflow = await page.evaluate(() => ({
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
      }));
      expect(overflow.scrollWidth).toBeLessThanOrEqual(overflow.clientWidth);
    });
  }
});
