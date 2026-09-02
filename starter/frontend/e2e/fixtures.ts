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
      // /impact and /ops must be stubbed with contract-shaped payloads, not
      // a bare {ok:true}. Both routes map over arrays (`impact.nodes`,
      // `ops.proposals`), so a wrong shape throws during render, React
      // unmounts the whole tree, and the gates then report "0 <main>
      // elements" — a harness artefact that looks exactly like a real
      // landmark failure. Keep these in sync with api/contracts.ts.
      if (path.endsWith("/api/impact")) {
        return json({
          verified_total: 1284,
          languages_active: 3,
          missions_completed: 2,
          geography_available: true,
          suppressed_cell_count: 4,
          generated_at: "2026-09-02T09:00:00Z",
          nodes: [
            {
              id: "node-1",
              language: "zul",
              province_code: "KZN",
              campaign: "Healthcare isiZulu",
              verified_count_band: "50-99",
              coverage_percent: 62,
              model_gap_percent: 31,
              updated_at: "2026-09-02T09:00:00Z",
            },
            {
              id: "node-2",
              language: "tsn",
              province_code: "NW",
              campaign: "Banking Setswana",
              verified_count_band: "20-49",
              coverage_percent: 28,
              // null exercises the "Model evidence unavailable" branch
              // rather than letting the UI infer a number it does not have.
              model_gap_percent: null,
              updated_at: "2026-09-02T09:00:00Z",
            },
          ],
        });
      }
      if (path.endsWith("/api/ops")) {
        return json({
          principal_kind: "mtn_operator",
          // Must be exactly OPS_ROLE from OpsRoute.tsx. Any other string
          // renders the "you do not have access" state, which has no
          // interactive controls at all — the keyboard gate then fails
          // for a stub reason rather than a real accessibility one.
          roles: ["MTN_LANGUAGE_OPS"],
          display_name: "MTN Language Ops",
          confirmation_text: "AUTHORISE",
          readiness: [
            { label: "Verified clips", value: "1284", detail: "Peer-verified only", available: true },
            { label: "Model evidence", value: null, detail: "No promoted model yet", available: false },
          ],
          gaps: [
            { language: "zul", verified_contributions: 812 },
            { language: "tsn", verified_contributions: 472 },
          ],
          proposals: [
            {
              id: "proposal-1",
              language: "tsn",
              province_code: "NW",
              domain: "Banking",
              rationale: "Lowest verified coverage of the active campaigns.",
              target_verified_clips: 500,
              fixed_reward_cents: 250,
              budget_cents: 125000,
              state: "PROPOSED",
              authorised_by: null,
            },
          ],
        });
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
  { name: "impact", path: "/impact" },
  { name: "ops", path: "/ops" },
];
