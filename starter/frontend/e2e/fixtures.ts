import type { Page } from "@playwright/test";

/**
 * Every gate spec stubs the backend itself. These gates are about layout,
 * keyboard and screen-reader semantics; making them depend on a running
 * Postgres-backed API would make them flaky for reasons unrelated to what
 * they measure.
 */
/**
 * Match ONLY real backend calls: pathname starting with `/api/`.
 *
 * The obvious glob `**\/api/**` is wrong and was a real, silent harness bug:
 * it also matches the app's own module `/src/api/client.ts`, so Vite's
 * JavaScript was answered with `application/json`, the module graph failed
 * ("Expected a JavaScript-or-Wasm module script"), React never mounted, and
 * every route rendered an empty <div id="root">. The reflow, touch-target and
 * axe gates then "passed" vacuously against a blank page while the landmark
 * and keyboard gates failed for a reason that had nothing to do with the UI.
 */
export async function stubApi(page: Page) {
  await page.route(
    (url) => url.pathname.startsWith("/api/"),
    async (route) => {
    const path = new URL(route.request().url()).pathname;
    const json = (body: unknown) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(body) });

    if (path.endsWith("/api/health")) return json({ status: "ok", provider_mode: "sandbox" });
    if (path.includes("/assignments")) {
      return json({
        id: "assignment-1",
        prompt_text: "Sawubona — say the greeting you heard",
        audio_playback_url: "/silence.wav",
      });
    }
    if (path.includes("/result")) {
      return json({ outcome: "Understood by peers", reward_minor: 250, currency: "ZAR" });
    }
      return json({ ok: true });
    },
  );
}

export const ROUTES = [
  { name: "home", path: "/" },
  { name: "consent", path: "/consent" },
  { name: "recording", path: "/record/contribution-1" },
  { name: "verification", path: "/verify?contributionId=contribution-1" },
  { name: "result", path: "/result/contribution-1" },
];
