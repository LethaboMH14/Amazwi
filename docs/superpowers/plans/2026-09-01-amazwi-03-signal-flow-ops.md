# AMAZWI Signal Flow and Language Ops Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Stages 7–8 as a responsive Signal Flow React application with authoritative peer truth shown before advisory AI, equal Midnight Shweshwe and Signal Daylight themes, aggregate Coverage Constellation, and human-authorised MTN Language Ops.

**Architecture:** Restructure the small frontend into focused `api`, `app`, `components`, `features`, and `styles` modules while preserving the Stage 1–6 API authority boundaries. Use CSS and the Web Animations API for event-bound motion, Playwright for route/accessibility/visual checks, and a read-only Figma export gate that compares only when fresh export evidence from file `JPZuFmbhRh9fhkgBLxRymq` exists. Add aggregate impact and mission-proposal backend services whose proposals cannot launch themselves; only an authenticated MTN operator can authorise a mission, with an audit event and idempotent state transition.

**Tech Stack:** React 18, TypeScript 5.5, React Router 7, Vite 5, Vitest 2, Testing Library, Playwright 1.55, CSS Custom Properties, CSS Container Queries, Web Animations API, axe-core 4.10, FastAPI, Pydantic, SQLAlchemy 2, Alembic, PostgreSQL 16, pytest.

## Global Constraints

- All constraints in `2026-09-01-amazwi-governed-intelligence-program.md` apply.
- Implement routes `/`, `/consent`, `/record/:contributionId`, `/verify`, `/result/:contributionId`, `/receipt/:contributionId`, `/impact`, and `/ops`.
- Peer verification is authoritative and must render before any advisory AI output.
- AI-disabled, AI-pending, and AI-failed states preserve the complete peer decision, reward, receipt, and wallet path.
- Midnight Shweshwe and Signal Daylight are equal first-class themes with identical functionality and automated coverage.
- Ndebele is seasonal only, enabled from 1–30 September or through the explicit local demo override `?season=heritage`; it is never the default and never a full-body pattern wall.
- Signal Flow uses 24–32px feature-card radii, 18–24px nested-surface radii, layered surfaces, controlled overlap, subtle grain, spectral glow, masked textile micro-patterns, Archivo typography, and waveform identity.
- CSS/WAAPI implements motion. Do not add a React motion library in this plan.
- Motion is event-bound and finite except for the live recorder. Reduced motion uses short opacity changes, a slower level meter, no morph, no ripple, and a static success glyph.
- Coverage is aggregate only. Never expose raw audio, exact location, or named contributors.
- The South Africa map is flat with aggregate province pins and a ripple on change. Do not build a 3D map.
- Do not implement a chance wheel, spin-to-win action, random cash result, or any visual implying random payout.
- Mission proposals are advisory. Only a human with `MTN_LANGUAGE_OPS` role can authorise a proposed mission.
- Fixed campaign reward and budget values come from persisted campaign rules. The UI does not invent or alter them.
- Accessibility acceptance covers 320px, 360px, 390px, 430px, and 480px widths, 200% zoom/reflow, keyboard operation, screen-reader names/status, and reduced motion.
- Visual regression covers Midnight Shweshwe and Signal Daylight. Token drift is checked only against timestamped read-only exports from Figma file `JPZuFmbhRh9fhkgBLxRymq`.
- Never claim Figma parity, pixel parity, or token parity when the export manifest is absent, stale, incomplete, or failed validation. Report `FIGMA_COMPARISON_UNAVAILABLE` instead.
- No Vercel deployment, Vercel configuration, production deployment, Figma mutation, real payment, or campaign launch occurs in this plan.
- TDD is mandatory. Every task begins with a failing test, reaches green, runs its relevant broader suite, and ends in a focused commit.

---

## Mandatory Execution Order

Execute tasks in this dependency order, not numeric-document order: **Task 0 → Task 2 → Task 3 → Task 1 → Tasks 4–13**. Task 2 owns the API types consumed by Task 1, and Task 3 owns the theme provider consumed by `AppShell`. Do not create temporary interfaces, `as any` casts, stub route components, or test-only production branches to bypass this order.

### Task 0: Lock frontend tooling, scripts, and deterministic browser fixtures

**Files:**
- Modify: `starter/frontend/package.json`
- Modify: `starter/frontend/package-lock.json`
- Modify: `starter/frontend/vite.config.ts`
- Create: `starter/frontend/playwright.config.ts`
- Create: `starter/frontend/e2e/support/mockApi.ts`
- Create: `starter/frontend/e2e/tooling.spec.ts`

**Interfaces:**
- Produces scripts `test:unit`, `test:e2e`, `test:a11y`, and `test:visual`.
- Produces a Playwright `webServer` at `http://127.0.0.1:4173` using Vite preview.
- Produces `installMockApi(page, scenario)` where `scenario` is `"golden" | "council-disabled" | "council-failed" | "operator-forbidden"`.
- Pins browser-test dependencies exactly: `@playwright/test@1.55.0`, `@axe-core/playwright@4.10.2`, and `@testing-library/user-event@14.6.1`.

- [ ] **Step 1: Write the failing tooling smoke test**

```ts
// e2e/tooling.spec.ts
import { expect, test } from "@playwright/test";
import { installMockApi } from "./support/mockApi";

test("serves the React shell against deterministic API fixtures", async ({ page }) => {
  await installMockApi(page, "golden");
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "AMAZWI" })).toBeVisible();
  await expect(page.getByText("backend unreachable")).toHaveCount(0);
});
```

- [ ] **Step 2: Install exact dependencies and verify RED**

Run: `cd starter/frontend && npm install --save-dev --save-exact @playwright/test@1.55.0 @axe-core/playwright@4.10.2 @testing-library/user-event@14.6.1`

Set the scripts exactly:

```json
{
  "test": "vitest run",
  "test:unit": "vitest run",
  "test:e2e": "playwright test",
  "test:a11y": "playwright test e2e/accessibility.spec.ts",
  "test:visual": "playwright test e2e/visual.spec.ts"
}
```

Run: `cd starter/frontend && npm run build && npm run test:e2e -- e2e/tooling.spec.ts`
Expected: FAIL because `playwright.config.ts`, `installMockApi`, and the Stage 7 shell do not exist.

- [ ] **Step 3: Add the exact Playwright server configuration**

```ts
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  retries: 0,
  reporter: [["list"]],
  use: {
    baseURL: "http://127.0.0.1:4173",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    video: "off",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: "npm run build && npm run preview -- --host 127.0.0.1 --port 4173",
    url: "http://127.0.0.1:4173",
    reuseExistingServer: false,
    timeout: 120_000,
  },
});
```

Add `server.proxy["/api"] = { target: "http://127.0.0.1:8000", changeOrigin: false }` to `vite.config.ts`; browser fixtures still intercept `/api/**`, while local integrated runs reach FastAPI.

- [ ] **Step 4: Implement deterministic API interception**

`installMockApi` must register one `page.route("**/api/**", handler)` before navigation, dispatch by method plus pathname, and fulfil JSON with `content-type: application/json`. The golden fixture must cover every request used by `/`, `/consent`, `/record/c1`, `/verify`, `/result/c1`, `/receipt/c1`, `/impact`, and `/ops`. Any unmatched request must fulfil status 501 with `{ "code": "UNMOCKED_E2E_REQUEST", "path": pathname, "method": request.method() }`; it must never fall through to the network.

- [ ] **Step 5: Verify GREEN and commit**

Run: `cd starter/frontend && npx playwright install chromium`
Run: `cd starter/frontend && npm run test:e2e -- e2e/tooling.spec.ts`
Expected: PASS with zero real API requests.

```bash
git add starter/frontend/package.json starter/frontend/package-lock.json starter/frontend/vite.config.ts starter/frontend/playwright.config.ts starter/frontend/e2e/support/mockApi.ts starter/frontend/e2e/tooling.spec.ts
git commit -m "UI: lock Stage 7 frontend test tooling"
```

---

## Locked File Structure

### Frontend

- `starter/frontend/src/api/contracts.ts`: frontend DTOs matching Stage 1–8 API responses.
- `starter/frontend/src/api/client.ts`: JSON fetch wrapper, typed errors, and injectable `AmazwiApi` interface.
- `starter/frontend/src/app/AppRouter.tsx`: route objects and route dependency injection.
- `starter/frontend/src/app/AppShell.tsx`: responsive page frame, skip link, theme control, mode label, and floating navigation.
- `starter/frontend/src/app/theme.tsx`: theme state, persistence, system preference, and seasonal Ndebele eligibility.
- `starter/frontend/src/components/SignalCard.tsx`: rounded layered feature/nested surface primitive.
- `starter/frontend/src/components/ProgressRail.tsx`: Kuest-inspired progress/status hierarchy without mascot art.
- `starter/frontend/src/components/PeerTruthStatus.tsx`: authoritative two-peer status.
- `starter/frontend/src/components/CouncilInsight.tsx`: advisory output rendered after peer truth.
- `starter/frontend/src/components/Waveform.tsx`: live and static waveform with reduced-motion behavior.
- `starter/frontend/src/components/SouthAfricaCoverageMap.tsx`: flat aggregate SVG map and province pins.
- `starter/frontend/src/components/StatusAnnouncer.tsx`: polite/assertive live regions.
- `starter/frontend/src/features/home/HomeRoute.tsx`: mission browser and progress overview.
- `starter/frontend/src/features/consent/ConsentRoute.tsx`: scoped consent and separate model-retention opt-in.
- `starter/frontend/src/features/recording/RecordingRoute.tsx`: recording, retry, upload, waiting, and errors.
- `starter/frontend/src/features/verification/VerificationRoute.tsx`: listen, free text, answer lock, referee, and reveal.
- `starter/frontend/src/features/result/ResultRoute.tsx`: authoritative result transition.
- `starter/frontend/src/features/receipt/ReceiptRoute.tsx`: peer truth, reward state, then advisory insight.
- `starter/frontend/src/features/impact/ImpactRoute.tsx`: Coverage Constellation and aggregate progress.
- `starter/frontend/src/features/ops/OpsRoute.tsx`: operator-only readiness, proposals, and human authorisation.
- `starter/frontend/src/styles/tokens.css`: semantic design tokens shared by both first-class themes.
- `starter/frontend/src/styles/themes.css`: Midnight, Daylight, and seasonal Ndebele token values.
- `starter/frontend/src/styles/materials.css`: Signal Flow surfaces, grain, glow, map, and responsive layout.
- `starter/frontend/src/styles/motion.css`: finite motion primitives and reduced-motion overrides.
- `starter/frontend/src/styles/accessibility.css`: focus, reflow, target-size, forced-colors, and screen-reader utilities.
- `starter/frontend/e2e/*.spec.ts`: browser acceptance, accessibility, and visual regression.
- `starter/frontend/scripts/export-figma.mjs`: read-only Figma export command.
- `starter/frontend/scripts/check-figma-evidence.mjs`: export age, screen inventory, and token drift gate.
- `starter/frontend/visual/figma/JPZuFmbhRh9fhkgBLxRymq/`: generated read-only export evidence, never hand-authored.

### Backend

- `starter/backend/app/impact.py`: aggregate coverage calculation with privacy thresholds.
- `starter/backend/app/missions.py`: proposal generation, authorisation, and audit transition.
- `starter/backend/app/routes/impact.py`: aggregate coverage endpoint.
- `starter/backend/app/routes/ops.py`: authorised MTN Language Ops endpoints.
- `starter/backend/app/api_types.py`: Stage 8 impact, proposal, authorisation, and readiness DTOs.
- `starter/backend/app/models.py`: `MissionProposal` and `MissionAuthorisation` records.
- `starter/backend/alembic/versions/e0f1a2b3c4d5_language_ops.py`: Stage 8 schema migration.

---

### Task 1: Restructure the React shell and lock all routes

**Files:**
- Create: `starter/frontend/src/app/AppRouter.tsx`
- Create: `starter/frontend/src/app/AppShell.tsx`
- Create: `starter/frontend/src/app/AppRouter.test.tsx`
- Move: `starter/frontend/src/HomeRoute.tsx` to `starter/frontend/src/features/home/HomeRoute.tsx`
- Move: `starter/frontend/src/ModeLabel.tsx` to `starter/frontend/src/components/ModeLabel.tsx`
- Move: `starter/frontend/src/ModeLabel.test.tsx` to `starter/frontend/src/components/ModeLabel.test.tsx`
- Move: `starter/frontend/src/hostBridge.ts` to `starter/frontend/src/app/hostBridge.ts`
- Move: `starter/frontend/src/hostBridge.test.ts` to `starter/frontend/src/app/hostBridge.test.ts`
- Modify: `starter/frontend/src/App.tsx`
- Modify: `starter/frontend/src/main.tsx`

**Interfaces:**
- Produces: `createAppRouter(api: AmazwiApi, initialEntries?: string[]): Router`.
- Produces: `AppShell` with `<main id="main-content">` and route outlet.
- Produces exact paths `/`, `/consent`, `/record/:contributionId`, `/verify`, `/result/:contributionId`, `/receipt/:contributionId`, `/impact`, `/ops`.
- Consumes: `AmazwiApi` from Task 2; use a temporary typed import until Task 2 lands.

- [ ] **Step 1: Write the failing route inventory test**

```tsx
import { render, screen } from "@testing-library/react";
import { RouterProvider } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { createAppRouter } from "./AppRouter";
import { fakeApi } from "../test/fakeApi";

const cases = [
  ["/", "Home"],
  ["/consent", "Consent"],
  ["/record/11111111-1111-1111-1111-111111111111", "Record"],
  ["/verify", "Verify"],
  ["/result/11111111-1111-1111-1111-111111111111", "Result"],
  ["/receipt/11111111-1111-1111-1111-111111111111", "Receipt"],
  ["/impact", "Impact"],
  ["/ops", "MTN Language Ops"],
] as const;

describe("application routes", () => {
  it.each(cases)("renders %s", async (path, heading) => {
    render(<RouterProvider router={createAppRouter(fakeApi, [path])} />);
    expect(await screen.findByRole("heading", { name: heading })).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run the route test and verify failure**

Run: `cd starter/frontend && npm test -- src/app/AppRouter.test.tsx`
Expected: FAIL because `AppRouter`, feature routes, and `fakeApi` do not exist.

- [ ] **Step 3: Create the router and shell**

```tsx
// src/app/AppRouter.tsx
import { createBrowserRouter, createMemoryRouter, type RouteObject } from "react-router-dom";
import type { AmazwiApi } from "../api/client";
import { AppShell } from "./AppShell";
import { ConsentRoute } from "../features/consent/ConsentRoute";
import { HomeRoute } from "../features/home/HomeRoute";
import { ImpactRoute } from "../features/impact/ImpactRoute";
import { OpsRoute } from "../features/ops/OpsRoute";
import { RecordingRoute } from "../features/recording/RecordingRoute";
import { ReceiptRoute } from "../features/receipt/ReceiptRoute";
import { ResultRoute } from "../features/result/ResultRoute";
import { VerificationRoute } from "../features/verification/VerificationRoute";

function routes(api: AmazwiApi): RouteObject[] {
  return [{
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <HomeRoute api={api} /> },
      { path: "consent", element: <ConsentRoute api={api} /> },
      { path: "record/:contributionId", element: <RecordingRoute api={api} /> },
      { path: "verify", element: <VerificationRoute api={api} /> },
      { path: "result/:contributionId", element: <ResultRoute api={api} /> },
      { path: "receipt/:contributionId", element: <ReceiptRoute api={api} /> },
      { path: "impact", element: <ImpactRoute api={api} /> },
      { path: "ops", element: <OpsRoute api={api} /> },
    ],
  }];
}

export function createAppRouter(api: AmazwiApi, initialEntries?: string[]) {
  return initialEntries
    ? createMemoryRouter(routes(api), { initialEntries })
    : createBrowserRouter(routes(api));
}
```

```tsx
// src/app/AppShell.tsx
import { NavLink, Outlet } from "react-router-dom";
import { ModeLabel } from "../components/ModeLabel";
import { ThemeControl, ThemeProvider } from "./theme";

export function AppShell() {
  return (
    <ThemeProvider>
      <a className="skip-link" href="#main-content">Skip to main content</a>
      <div className="app-shell grain">
        <header className="app-header">
          <NavLink className="wordmark" to="/" aria-label="AMAZWI home">AMAZWI</NavLink>
          <div className="header-actions"><ThemeControl /><ModeLabel mode="standalone" /></div>
        </header>
        <main id="main-content" tabIndex={-1}><Outlet /></main>
        <nav className="floating-nav" aria-label="Primary">
          <NavLink to="/">Home</NavLink>
          <NavLink to="/verify">Verify</NavLink>
          <NavLink to="/impact">Impact</NavLink>
          <NavLink to="/ops">Ops</NavLink>
        </nav>
      </div>
    </ThemeProvider>
  );
}
```

- [ ] **Step 4: Make `App.tsx` and `main.tsx` composition-only**

```tsx
// src/App.tsx
import { RouterProvider } from "react-router-dom";
import { api } from "./api/client";
import { createAppRouter } from "./app/AppRouter";

const router = createAppRouter(api);
export default function App() { return <RouterProvider router={router} />; }
```

Import `styles/tokens.css`, `styles/themes.css`, `styles/materials.css`, `styles/motion.css`, and `styles/accessibility.css` from `main.tsx` in that order.

- [ ] **Step 5: Run route, existing unit, and build checks**

Run: `cd starter/frontend && npm test -- src/app/AppRouter.test.tsx src/app/hostBridge.test.ts src/components/ModeLabel.test.tsx`
Run: `cd starter/frontend && npm run build`
Expected: all routes render, moved tests pass, and TypeScript finds no imports from the old root locations.

- [ ] **Step 6: Commit**

```bash
git add starter/frontend/src/App.tsx starter/frontend/src/main.tsx starter/frontend/src/app starter/frontend/src/components starter/frontend/src/features
git commit -m "UI: restructure app shell and lock Signal Flow routes"
```

---

### Task 2: Lock typed API contracts and visible failure mapping

**Files:**
- Modify: `starter/frontend/src/api/contracts.ts`
- Modify: `starter/frontend/src/api/client.ts`
- Create: `starter/frontend/src/api/client.test.ts`
- Create: `starter/frontend/src/test/fakeApi.ts`

**Interfaces:**
- Produces: `AmazwiApi` with exact consent, private-audio, peer, receipt, impact, and Ops methods shown below.
- Produces: `ApiError` with stable `status`, `code`, and `details`.
- Produces DTO discriminants `PeerDecision`, `CouncilState`, `PaymentState`, `MissionProposalState`.

- [ ] **Step 1: Write failing API error and receipt-order contract tests**

```ts
import { describe, expect, it, vi } from "vitest";
import { apiRequest, ApiError } from "./client";

describe("apiRequest", () => {
  it("preserves stable server error codes", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(
      JSON.stringify({ code: "CONSENT_REQUIRED", scope: "RECORD_PROCESS_ROUND" }),
      { status: 403, headers: { "content-type": "application/json" } },
    )));
    await expect(apiRequest("/consents/me")).rejects.toEqual(
      new ApiError(403, "CONSENT_REQUIRED", { scope: "RECORD_PROCESS_ROUND" }),
    );
  });
});
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/frontend && npm test -- src/api/client.test.ts`
Expected: FAIL because Stage 7–8 contracts and normalized error details do not exist.

- [ ] **Step 3: Define exact DTOs**

```ts
export type ThemeName = "midnight" | "daylight" | "ndebele";
export type ConsentScope = "RECORD_PROCESS_ROUND" | "ASSIGNED_VERIFIER_PLAYBACK" | "RETAIN_MODEL_DEVELOPMENT" | "PUBLIC_AUDIO_ATTRIBUTION";
export type PeerDecision = "PENDING" | "CORPUS_ELIGIBLE" | "PLAYED" | "VOIDED" | "REVIEW_REQUIRED" | "UNVALIDATED" | "EXPIRED";
export type CouncilState = "DISABLED" | "PENDING" | "READY" | "FAILED";
export type PaymentState = "NOT_ELIGIBLE" | "CREDITED" | "SENT_FOR_PAYMENT" | "PAID" | "FAILED";
export type MissionProposalState = "PROPOSED" | "AUTHORISED" | "REJECTED";

export interface ConsentStateDto { scope: ConsentScope; version: string; grantedAt: string; revokedAt: string | null }
export interface AssignmentDto { id: string; contributionId: string; language: "zu" | "tn"; answerLocked: boolean; playbackExpiresAt: string | null }

export interface ReceiptDto {
  contributionId: string;
  peerDecision: PeerDecision;
  verifierCount: number;
  peerResolvedAt: string | null;
  rewardAmountCents: number | null;
  paymentState: PaymentState;
  council: {
    state: CouncilState;
    headline: string | null;
    explanation: string | null;
    modelVersion: string | null;
  };
}

export interface CoverageNodeDto {
  id: string;
  language: "zu" | "tn";
  provinceCode: "EC" | "FS" | "GP" | "KZN" | "LP" | "MP" | "NC" | "NW" | "WC";
  domain: "support" | "sales" | "self_service" | "code_switch";
  verifiedCountBand: "5-19" | "20-49" | "50-99" | "100+";
  coveragePercent: number;
  modelGapPercent: number | null;
  updatedAt: string;
}

export interface ImpactDto {
  verifiedTotal: number;
  languagesActive: number;
  missionsCompleted: number;
  nodes: CoverageNodeDto[];
}

export interface MissionProposalDto {
  id: string;
  language: "zu" | "tn";
  provinceCode: CoverageNodeDto["provinceCode"];
  domain: CoverageNodeDto["domain"];
  rationale: string;
  targetVerifiedClips: number;
  fixedRewardCents: number;
  budgetCents: number;
  state: MissionProposalState;
  proposedByJobId: string;
  authorisedBy: string | null;
  authorisedAt: string | null;
}

export interface OpsDto {
  operator: { id: string; displayName: string; roles: string[] };
  readiness: Array<{ language: "zu" | "tn"; domain: CoverageNodeDto["domain"]; peerCoveragePercent: number; modelReady: boolean; evidenceLabel: string }>;
  proposals: MissionProposalDto[];
}
```

- [ ] **Step 4: Implement the injectable API interface**

```ts
export interface AmazwiApi {
  getHome(): Promise<{ xp: number; level: number; nextLevelXp: number; missions: MissionProposalDto[] }>;
  getConsents(): Promise<ConsentStateDto[]>;
  grantConsent(request: { version: "2026-09-01"; scopes: ConsentScope[] }): Promise<ConsentStateDto[]>;
  createContribution(cardId: string): Promise<{ id: string; rewardAmountCents: number; rewardRuleVersion: string }>;
  beginAudioUpload(contributionId: string): Promise<{ audioObjectId: string; uploadPath: string }>;
  uploadPrivateAudio(uploadPath: string, body: Blob): Promise<void>;
  finaliseAudio(contributionId: string, request: { sha256: string; mimeType: "audio/webm" | "audio/ogg" | "audio/wav"; codec: string; durationMs: number; byteLength: number }): Promise<{ contributionId: string; state: "RECORDED" }>;
  getAssignment(): Promise<AssignmentDto | null>;
  getPlayback(assignmentId: string): Promise<{ url: string; expiresAt: string }>;
  submitAnswer(assignmentId: string, request: { rawAnswer: string }): Promise<{ answerLocked: true }>;
  submitReferee(assignmentId: string, request: { violation: "YES" | "NO" }): Promise<{ revealed: true; contributionId: string }>;
  getResult(contributionId: string): Promise<ReceiptDto>;
  getReceipt(contributionId: string): Promise<ReceiptDto>;
  getImpact(): Promise<ImpactDto>;
  getOps(): Promise<OpsDto>;
  authoriseMission(id: string, idempotencyKey: string): Promise<MissionProposalDto>;
}
```

Map methods exactly to `GET /consents/me`, `POST /consents`, `POST /contributions` with only `card_id`, `POST /contributions/{id}/audio/uploads`, `PUT /private-audio/uploads/{audioObjectId}`, `POST /contributions/{id}/audio/finalise`, `GET /assignments/next`, `POST /assignments/{id}/playback`, `POST /assignments/{id}/answer`, `POST /assignments/{id}/referee`, `GET /contributions/{id}/result`, `GET /contributions/{id}/receipt`, `GET /impact`, `GET /ops`, and `POST /ops/missions/{id}/authorise`. Browser methods never send a user, speaker, verifier, campaign, reward amount or reward-rule version to select authority. `authoriseMission` sends only an empty body plus `Idempotency-Key`; it never accepts reward or budget values from the browser.

- [ ] **Step 5: Run API and frontend suites**

Run: `cd starter/frontend && npm test -- src/api/client.test.ts src/app/AppRouter.test.tsx`
Expected: PASS with `fakeApi` implementing every method and no `as any` cast.

- [ ] **Step 6: Commit**

```bash
git add starter/frontend/src/api starter/frontend/src/test/fakeApi.ts
git commit -m "UI: lock typed Stage 7 and Stage 8 API contracts"
```

---

### Task 3: Implement equal themes and seasonal Ndebele eligibility

**Files:**
- Create: `starter/frontend/src/app/theme.tsx`
- Create: `starter/frontend/src/app/theme.test.tsx`
- Create: `starter/frontend/src/styles/tokens.css`
- Create: `starter/frontend/src/styles/themes.css`
- Create: `starter/frontend/src/styles/materials.css`
- Remove: `starter/frontend/src/tokens.css`
- Modify: `starter/frontend/src/tokens.sync.test.ts`

**Interfaces:**
- Produces: `isNdebeleSeason(date: Date, search: string) -> boolean`.
- Produces: `ThemeProvider`, `useTheme()`, and `ThemeControl`.
- Sets `document.documentElement.dataset.theme` to `midnight`, `daylight`, or eligible `ndebele`.
- Persists only `midnight` or `daylight` in `localStorage["amazwi.theme"]`; the seasonal override is session-scoped.

- [ ] **Step 1: Write failing eligibility and theme-equivalence tests**

```tsx
import { describe, expect, it } from "vitest";
import { isNdebeleSeason } from "./theme";

it("enables Ndebele only in September or with the heritage demo override", () => {
  expect(isNdebeleSeason(new Date("2026-09-15T12:00:00Z"), "")).toBe(true);
  expect(isNdebeleSeason(new Date("2026-10-01T00:00:00Z"), "")).toBe(false);
  expect(isNdebeleSeason(new Date("2026-10-01T00:00:00Z"), "?season=heritage")).toBe(true);
});
```

Update `tokens.sync.test.ts` to parse the required semantic variables and assert both `[data-theme="midnight"]` and `[data-theme="daylight"]` define the same names: `--ground`, `--ground-deep`, `--surface-1`, `--surface-2`, `--text`, `--text-dim`, `--border`, `--focus`, `--shadow`, `--texture-opacity`.

Add a failing material-contract assertion that `materials.css` contains `.signal-card`, `.signal-card::before`, `.signal-stack`, `.wave-spine`, and `.textile-mask`, and that feature/nested radii resolve to `28px` and `20px`. This is the automated guard for rounded flowing layers, controlled overlap, grain/glow, and restrained masked textile accents.

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/frontend && npm test -- src/app/theme.test.tsx src/tokens.sync.test.ts`
Expected: FAIL because the new theme module and semantic theme files do not exist.

- [ ] **Step 3: Define invariant and semantic tokens**

```css
/* styles/tokens.css */
:root {
  --voice-1: #ff5a36;
  --voice-2: #e8267f;
  --voice-grad: linear-gradient(96deg, var(--voice-1), var(--voice-2));
  --rand: #ffcb05;
  --understood: #1f8a54;
  --missed: #8a6a1f;
  --danger: #c0341a;
  --calm: #4c6fa5;
  --aqua: #39d6c5;
  --font: "Archivo Variable", Archivo, system-ui, sans-serif;
  --radius-feature: 28px;
  --radius-nested: 20px;
  --radius-control: 16px;
  --space-1: .25rem;
  --space-2: .5rem;
  --space-3: .75rem;
  --space-4: 1rem;
  --space-5: 1.5rem;
  --space-6: 2rem;
  --press-ms: 140ms;
  --entry-ms: 260ms;
  --morph-ms: 380ms;
  --ripple-ms: 500ms;
  --celebrate-ms: 650ms;
  --ease-signal: cubic-bezier(.2, 0, 0, 1);
}
```

```css
/* styles/themes.css */
[data-theme="midnight"] {
  color-scheme: dark;
  --ground: #0c1123; --ground-deep: #080c1a; --surface-1: #161b2e; --surface-2: #202740;
  --text: #eaf0fa; --text-dim: #9eabc2; --border: rgb(168 196 232 / 18%);
  --focus: #39d6c5; --shadow: rgb(0 0 0 / 42%); --texture-opacity: .26;
}
[data-theme="daylight"] {
  color-scheme: light;
  --ground: #fff8ef; --ground-deep: #f3e9dc; --surface-1: #ffffff; --surface-2: #f8f1e8;
  --text: #211a24; --text-dim: #665d6b; --border: #ddcfc3;
  --focus: #176f68; --shadow: rgb(73 45 22 / 16%); --texture-opacity: .12;
}
[data-theme="ndebele"] {
  color-scheme: dark;
  --ground: #0b0908; --ground-deep: #000; --surface-1: #17120f; --surface-2: #241b16;
  --text: #f4efe6; --text-dim: #b5aa9b; --border: #55483e;
  --focus: #e8b22a; --shadow: rgb(0 0 0 / 48%); --texture-opacity: .08;
}
```

Ndebele accents apply only to `.seasonal-divider`, `.seasonal-border`, and `.seasonal-badge`; body backgrounds remain solid Signal Flow material.

Implement the material selectors exactly: `.signal-card` uses `border-radius: var(--radius-feature)`, two layered radial/linear gradients, `box-shadow: 0 24px 70px var(--shadow)`, and `overflow: clip`; `.signal-card::before` supplies non-interactive grain at `opacity: var(--texture-opacity)`; `.signal-stack > * + *` overlaps by `margin-block-start: -0.5rem`; `.wave-spine` is a masked coral→pink→aqua line; `.textile-mask` is limited to `max-block-size: 2.5rem` with `pointer-events: none`. No route may apply a textile image to `body` or `.app-shell`.

- [ ] **Step 4: Implement theme selection**

`ThemeControl` renders a labelled native `<select>` containing Midnight Shweshwe and Signal Daylight always, and Ndebele only when `isNdebeleSeason` is true. The default is system light preference mapped to Daylight, otherwise Midnight. Both first-class themes must expose the same route and control tree.

- [ ] **Step 5: Run theme tests and build**

Run: `cd starter/frontend && npm test -- src/app/theme.test.tsx src/tokens.sync.test.ts`
Run: `cd starter/frontend && npm run build`
Expected: PASS; no production import references `src/tokens.css`.

- [ ] **Step 6: Commit**

```bash
git add starter/frontend/src/app/theme.tsx starter/frontend/src/app/theme.test.tsx starter/frontend/src/styles starter/frontend/src/tokens.sync.test.ts starter/frontend/src/tokens.css
git commit -m "UI: add equal Midnight and Daylight themes"
```

---

### Task 4: Build Signal Flow primitives and finite CSS/WAAPI motion

**Files:**
- Create: `starter/frontend/src/components/SignalCard.tsx`
- Create: `starter/frontend/src/components/ProgressRail.tsx`
- Create: `starter/frontend/src/components/PeerTruthStatus.tsx`
- Create: `starter/frontend/src/components/CouncilInsight.tsx`
- Create: `starter/frontend/src/components/Waveform.tsx`
- Create: `starter/frontend/src/components/StatusAnnouncer.tsx`
- Create: `starter/frontend/src/components/signal-flow.test.tsx`
- Create: `starter/frontend/src/app/useSignalMotion.ts`
- Create: `starter/frontend/src/app/useSignalMotion.test.ts`
- Create: `starter/frontend/src/styles/motion.css`

**Interfaces:**
- Produces: `animateSignal(element, kind, reduced) -> Animation | null`, where `kind` is `press | enter | waveformFold | peerConnect | receiptRise | mapRipple | celebrate`.
- `PeerTruthStatus` consumes `peerDecision` and `verifierCount` only.
- `CouncilInsight` consumes Council state and must be mounted after `PeerTruthStatus` in receipt DOM order.

- [ ] **Step 1: Write failing semantic and reduced-motion tests**

```tsx
it("renders peer authority before advisory AI", () => {
  render(<>
    <PeerTruthStatus decision="CORPUS_ELIGIBLE" verifierCount={2} />
    <CouncilInsight state="READY" headline="Model blind spot" explanation="Peers understood a code-switch the current model missed." />
  </>);
  const truth = screen.getByRole("status", { name: /peer verification/i });
  const advisory = screen.getByRole("complementary", { name: /advisory ai/i });
  expect(truth.compareDocumentPosition(advisory) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  expect(advisory).toHaveTextContent("Advisory");
});
```

```ts
it("does not start WAAPI motion when reduced motion is active", () => {
  const element = document.createElement("div");
  element.animate = vi.fn();
  expect(animateSignal(element, "mapRipple", true)).toBeNull();
  expect(element.animate).not.toHaveBeenCalled();
});
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/frontend && npm test -- src/components/signal-flow.test.tsx src/app/useSignalMotion.test.ts`
Expected: FAIL because primitives and motion functions do not exist.

- [ ] **Step 3: Implement exact motion table**

```ts
const motion = {
  press: { keyframes: [{ transform: "scale(1)" }, { transform: "scale(.97)" }, { transform: "scale(1)" }], duration: 140 },
  enter: { keyframes: [{ opacity: 0, transform: "translateY(12px)" }, { opacity: 1, transform: "translateY(0)" }], duration: 260 },
  waveformFold: { keyframes: [{ transform: "scaleX(1)" }, { transform: "scaleX(.22)" }], duration: 380 },
  peerConnect: { keyframes: [{ opacity: .35, transform: "scaleX(0)" }, { opacity: 1, transform: "scaleX(1)" }], duration: 260 },
  receiptRise: { keyframes: [{ opacity: 0, transform: "translateY(20px)" }, { opacity: 1, transform: "translateY(0)" }], duration: 300 },
  mapRipple: { keyframes: [{ opacity: .55, transform: "scale(.4)" }, { opacity: 0, transform: "scale(1.6)" }], duration: 500 },
  celebrate: { keyframes: [{ opacity: 0, transform: "translateY(8px) scale(.9)" }, { opacity: 1, transform: "translateY(0) scale(1)" }], duration: 650 },
} as const;

export function animateSignal(element: HTMLElement, kind: keyof typeof motion, reduced: boolean): Animation | null {
  if (reduced) return null;
  const spec = motion[kind];
  return element.animate(spec.keyframes, { duration: spec.duration, easing: "cubic-bezier(.2,0,0,1)", fill: "both" });
}
```

- [ ] **Step 4: Implement primitives with semantic HTML**

`SignalCard` renders `<section>` or `<article>` selected by an `as` prop. `ProgressRail` uses `<progress max={nextLevelXp} value={xp}>` and visible `Level {level}` text. `PeerTruthStatus` uses `role="status"`, labels `Confirmed by 2 proficient peers`, and never mentions AI. `CouncilInsight` uses `<aside aria-label="Advisory AI">` and starts with a visible `Advisory` badge. `StatusAnnouncer` exposes one `aria-live="polite"` region and one `aria-live="assertive"` error region.

- [ ] **Step 5: Add reduced-motion CSS**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; animation-duration: 1ms !important; animation-iteration-count: 1 !important; transition-duration: 1ms !important; }
  .waveform__bar { transition: block-size 600ms linear !important; }
  .map-ripple, .reward-confetti { display: none !important; }
  .success-glyph { transform: none !important; opacity: 1 !important; }
}
```

- [ ] **Step 6: Run primitive tests and commit**

Run: `cd starter/frontend && npm test -- src/components/signal-flow.test.tsx src/app/useSignalMotion.test.ts`

```bash
git add starter/frontend/src/components starter/frontend/src/app/useSignalMotion.ts starter/frontend/src/app/useSignalMotion.test.ts starter/frontend/src/styles/motion.css
git commit -m "UI: add Signal Flow primitives and reduced motion"
```

---

### Task 5: Implement the home, consent, record, verify, and result routes

**Files:**
- Modify: `starter/frontend/src/features/home/HomeRoute.tsx`
- Modify: `starter/frontend/src/features/consent/ConsentRoute.tsx`
- Modify: `starter/frontend/src/features/recording/RecordingRoute.tsx`
- Modify: `starter/frontend/src/features/verification/VerificationRoute.tsx`
- Create: `starter/frontend/src/features/result/ResultRoute.tsx`
- Create: `starter/frontend/src/features/golden-path.test.tsx`

**Interfaces:**
- Home consumes `getHome()`, uses `ProgressRail` for Kuest-inspired status hierarchy, calls `createContribution(cardId)` for the authenticated user, then navigates to the returned `/record/:contributionId`.
- Consent grants `RECORD_PROCESS_ROUND` and `ASSIGNED_VERIFIER_PLAYBACK`; `RETAIN_MODEL_DEVELOPMENT` is a separate unchecked-by-default control.
- Recording keeps raw audio in memory only and uses the Stage 1 upload/finalise API.
- Verification locks free text before violation reveal and never shows AI output.
- Result polls authoritative peer state, then links to `/receipt/:contributionId`.

- [ ] **Step 1: Write the failing golden-path ordering test**

```tsx
it("moves from separate consent through authoritative result without AI judging the user", async () => {
  const user = userEvent.setup();
  render(<RouterProvider router={createAppRouter(fakeApi, ["/consent"])} />);
  expect(screen.getByRole("checkbox", { name: /improve language models/i })).not.toBeChecked();
  await user.click(screen.getByRole("button", { name: /continue/i }));
  expect(fakeApi.grantConsent).toHaveBeenCalledWith([
    "RECORD_PROCESS_ROUND",
    "ASSIGNED_VERIFIER_PLAYBACK",
  ]);
  expect(screen.queryByText(/ai score|model confidence/i)).not.toBeInTheDocument();
});
```

Create these exact failing tests in the listed route test files before implementation:

```tsx
it("keeps the captured Blob in memory and retries the same failed upload", async () => {
  api.uploadPrivateAudio.mockRejectedValueOnce(new ApiError(503, "AUDIO_UNAVAILABLE", {}));
  render(<RecordingRoute api={api} contributionId="c1" media={fakeMedia(blob)} />);
  await user.click(screen.getByRole("button", { name: "Submit recording" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("Try upload again");
  await user.click(screen.getByRole("button", { name: "Try upload again" }));
  expect(api.uploadPrivateAudio).toHaveBeenNthCalledWith(2, expect.any(String), blob);
});

it("creates the contribution server-side before opening the recorder", async () => {
  api.createContribution.mockResolvedValue({ id: "c1", rewardAmountCents: 200, rewardRuleVersion: "speaker-v1" });
  render(<HomeRoute api={api} />);
  await user.click(await screen.findByRole("button", { name: /start mission/i }));
  expect(api.createContribution).toHaveBeenCalledWith("card-1");
  expect(location.pathname).toBe("/record/c1");
});

it("refreshes an expired assignment-bound playback URL", async () => {
  api.getPlayback.mockRejectedValueOnce(new ApiError(410, "AUDIO_UNAVAILABLE", {}));
  render(<VerificationRoute api={api} />);
  await user.click(await screen.findByRole("button", { name: "Get a new playback link" }));
  expect(api.getPlayback).toHaveBeenCalledTimes(2);
});

it("locks free text before the separate violation vote and reveal", async () => {
  render(<VerificationRoute api={api} />);
  await user.type(await screen.findByLabelText("What did you hear?"), "ke a leboga");
  await user.click(screen.getByRole("button", { name: "Lock answer" }));
  expect(screen.getByLabelText("What did you hear?")).toBeDisabled();
  expect(screen.getByRole("group", { name: "Banned-word violation" })).toBeVisible();
  expect(screen.queryByText(/advisory ai|model confidence/i)).not.toBeInTheDocument();
});

it("renders UNVALIDATED expiry without peer or AI success language", async () => {
  api.getResult.mockResolvedValue(receipt({ peerDecision: "UNVALIDATED", verifierCount: 1 }));
  render(<ResultRoute api={api} contributionId="c1" />);
  expect(await screen.findByText("Not enough proficient peer answers before expiry")).toBeVisible();
  expect(screen.queryByText(/confirmed|model blind spot/i)).not.toBeInTheDocument();
});
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/frontend && npm test -- src/features/golden-path.test.tsx`
Expected: FAIL because Signal Flow route implementations and recovery states are incomplete.

- [ ] **Step 3: Implement the Kuest-inspired home hierarchy**

Render one progress rail, then mission cards with one mission accent each. Accents encode mission mode, not payout. On start, call `createContribution(cardId)` and use only the returned contribution ID and persisted reward display fields; the browser never supplies speaker or reward configuration. Show fixed reward copy only when returned by the API. Do not render mascot art, a leaderboard of personal earnings, or a reward wheel.

- [ ] **Step 4: Implement consent, recording, verification, and result state machines**

Use explicit discriminated states:

```ts
type RecordingState =
  | { kind: "ready" }
  | { kind: "recording"; startedAt: number }
  | { kind: "review"; blob: Blob; durationMs: number }
  | { kind: "uploading"; progress: number }
  | { kind: "submitted"; contributionId: string }
  | { kind: "error"; code: "MIC_DENIED" | "UPLOAD_FAILED" | "AUDIO_INVALID"; message: string };
```

Map errors to actionable copy: mic denied includes `Open browser settings`; upload failure includes `Try upload again`; expired playback requests a new authorised URL; no assignment offers `Check again`; no error action is disabled by motion.

- [ ] **Step 5: Run route tests and build**

Run: `cd starter/frontend && npm test -- src/features/golden-path.test.tsx src/features/consent src/features/recording src/features/verification src/features/result`
Run: `cd starter/frontend && npm run build`
Expected: PASS with no AI component imported by consent, recording, verification, or result modules.

- [ ] **Step 6: Commit**

```bash
git add starter/frontend/src/features/home starter/frontend/src/features/consent starter/frontend/src/features/recording starter/frontend/src/features/verification starter/frontend/src/features/result
git commit -m "UI: deliver Signal Flow peer golden path"
```

---

### Task 6: Implement the peer-truth-first receipt and advisory failure isolation

**Files:**
- Modify: `starter/frontend/src/features/receipt/ReceiptRoute.tsx`
- Create: `starter/frontend/src/features/receipt/ReceiptRoute.test.tsx`
- Modify: `starter/frontend/src/components/PeerTruthStatus.tsx`
- Modify: `starter/frontend/src/components/CouncilInsight.tsx`

**Interfaces:**
- Receipt DOM order is heading → peer truth → reward/payment state → advisory Council.
- `CouncilState.DISABLED`, `PENDING`, and `FAILED` never hide or downgrade peer truth or reward.
- Payment copy maps exactly: `CREDITED` → `Credited to your AMAZWI balance`; `SENT_FOR_PAYMENT` → `Sent for payment`; `PAID` → `Paid`; `FAILED` → `Payment needs attention`.

- [ ] **Step 1: Write failing authority and payment-language tests**

```tsx
it.each(["DISABLED", "PENDING", "FAILED"] as const)("keeps truth and reward visible when Council is %s", async (state) => {
  fakeApi.getReceipt.mockResolvedValue(receipt({ council: { state, headline: null, explanation: null, modelVersion: null } }));
  render(<RouterProvider router={createAppRouter(fakeApi, ["/receipt/c1"])} />);
  expect(await screen.findByText("Confirmed by 2 proficient peers")).toBeVisible();
  expect(screen.getByText("Credited to your AMAZWI balance")).toBeVisible();
  expect(screen.getByLabelText("Advisory AI")).toHaveTextContent(state === "FAILED" ? "Insight unavailable" : state === "PENDING" ? "Insight pending" : "Insight disabled");
});

it("celebrates once only when a fixed persisted reward becomes CREDITED", async () => {
  fakeApi.getReceipt
    .mockResolvedValueOnce(receipt({ paymentState: "NOT_ELIGIBLE", rewardAmountCents: null }))
    .mockResolvedValueOnce(receipt({ paymentState: "CREDITED", rewardAmountCents: 250 }));
  render(<RouterProvider router={createAppRouter(fakeApi, ["/receipt/c1"])} />);
  expect(screen.queryByTestId("reward-celebration")).not.toBeInTheDocument();
  await user.click(await screen.findByRole("button", { name: "Refresh receipt" }));
  expect(screen.getByTestId("reward-celebration")).toHaveTextContent("R 2.50 credited");
  expect(screen.queryByText(/spin|wheel|mystery|try your luck|random/i)).not.toBeInTheDocument();
});
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/frontend && npm test -- src/features/receipt/ReceiptRoute.test.tsx`
Expected: FAIL until receipt ordering and Council fallback states are implemented.

- [ ] **Step 3: Implement the receipt sequence**

```tsx
return (
  <article aria-labelledby="receipt-title" className="receipt signal-stack">
    <h1 id="receipt-title">Receipt</h1>
    <PeerTruthStatus decision={receipt.peerDecision} verifierCount={receipt.verifierCount} />
    <SignalCard as="section" tone="reward" aria-label="Reward status">
      <p className="money">{formatRand(receipt.rewardAmountCents)}</p>
      <p>{paymentCopy[receipt.paymentState]}</p>
    </SignalCard>
    <CouncilInsight {...receipt.council} />
  </article>
);
```

The one-shot celebration runs only when state changes into `CREDITED`; it uses a static success glyph under reduced motion. It contains no wheel, spin label, random number, mystery amount, or re-roll action.

- [ ] **Step 4: Run receipt and full frontend tests**

Run: `cd starter/frontend && npm test -- src/features/receipt/ReceiptRoute.test.tsx src/components/signal-flow.test.tsx`
Run: `cd starter/frontend && npm test`
Expected: PASS for all Council states and payment copy.

- [ ] **Step 5: Commit**

```bash
git add starter/frontend/src/features/receipt starter/frontend/src/components/PeerTruthStatus.tsx starter/frontend/src/components/CouncilInsight.tsx
git commit -m "UI: render peer truth before advisory insight"
```

---

### Task 7: Add aggregate Coverage Constellation backend contracts

**Files:**
- Create: `starter/backend/app/impact.py`
- Create: `starter/backend/app/routes/impact.py`
- Modify: `starter/backend/app/api_types.py`
- Modify: `starter/backend/app/main.py`
- Create: `starter/backend/tests/test_impact.py`
- Create: `starter/backend/tests/test_impact_api.py`

**Interfaces:**
- Produces: `build_coverage(session, now) -> ImpactResponse`.
- API: `GET /impact`.
- Applies a minimum aggregation threshold of 5 peer-verified contributions per province/language/domain cell.
- Returns count bands, not exact small-cell counts; never returns user IDs, contribution IDs, coordinates, audio URLs, or transcripts.

- [ ] **Step 1: Write failing privacy-threshold tests**

```python
def test_coverage_suppresses_cells_below_five(db_session, coverage_factory):
    coverage_factory(language="tn", province="NW", domain="support", count=4)
    response = build_coverage(db_session, NOW)
    assert response.nodes == []


def test_coverage_returns_bands_without_personal_or_audio_fields(db_session, coverage_factory):
    coverage_factory(language="zu", province="KZN", domain="code_switch", count=7)
    node = build_coverage(db_session, NOW).nodes[0].model_dump()
    assert node["verified_count_band"] == "5-19"
    forbidden = {"user_id", "contribution_id", "latitude", "longitude", "audio_url", "transcript"}
    assert forbidden.isdisjoint(node)
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/backend && python -m pytest tests/test_impact.py tests/test_impact_api.py -v`
Expected: collection failure because `app.impact` and the response contracts do not exist.

- [ ] **Step 3: Add exact response contracts**

```python
class CoverageNodeResponse(BaseModel):
    id: str
    language: Literal["zu", "tn"]
    province_code: Literal["EC", "FS", "GP", "KZN", "LP", "MP", "NC", "NW", "WC"]
    domain: Literal["support", "sales", "self_service", "code_switch"]
    verified_count_band: Literal["5-19", "20-49", "50-99", "100+"]
    coverage_percent: int = Field(ge=0, le=100)
    model_gap_percent: int | None = Field(default=None, ge=0, le=100)
    updated_at: datetime

class ImpactResponse(BaseModel):
    verified_total: int = Field(ge=0)
    languages_active: int = Field(ge=0, le=2)
    missions_completed: int = Field(ge=0)
    nodes: list[CoverageNodeResponse]
```

- [ ] **Step 4: Implement deterministic aggregation**

Group only committed `CORPUS_ELIGIBLE` peer decisions. Compute public cells after applying `HAVING count(*) >= 5`. Derive `id` as `{language}:{province}:{domain}`. Map counts to exact bands. Set `model_gap_percent` only from a signed, active model-evaluation record; otherwise return `None` so the UI says `Model evidence unavailable`.

- [ ] **Step 5: Register route, run tests, and commit**

Run: `cd starter/backend && python -m pytest tests/test_impact.py tests/test_impact_api.py tests/test_resolver.py -v`

```bash
git add starter/backend/app/impact.py starter/backend/app/routes/impact.py starter/backend/app/api_types.py starter/backend/app/main.py starter/backend/tests/test_impact.py starter/backend/tests/test_impact_api.py
git commit -m "Ops: add privacy-thresholded coverage API"
```

---

### Task 8: Render the flat South Africa Coverage Constellation

**Files:**
- Create: `starter/frontend/src/components/SouthAfricaCoverageMap.tsx`
- Create: `starter/frontend/src/components/SouthAfricaCoverageMap.test.tsx`
- Create: `starter/frontend/src/features/impact/ImpactRoute.tsx`
- Create: `starter/frontend/src/features/impact/ImpactRoute.test.tsx`
- Modify: `starter/frontend/src/styles/materials.css`

**Interfaces:**
- `SouthAfricaCoverageMap({ nodes, reducedMotion })` renders one flat SVG outline, province labels, aggregate pins, and an accessible list containing the same data.
- Pin radius is based on count band, not personal value: `5-19=6`, `20-49=8`, `50-99=10`, `100+=12` SVG units.
- A node update triggers one 500ms ripple unless reduced motion is active.

- [ ] **Step 1: Write failing flat-map and privacy tests**

```tsx
it("renders a flat aggregate map with an equivalent accessible list", () => {
  render(<SouthAfricaCoverageMap nodes={[coverageNode]} reducedMotion={false} />);
  expect(screen.getByRole("img", { name: /south africa language coverage/i })).toBeVisible();
  expect(screen.getByRole("list", { name: /coverage details/i })).toHaveTextContent("Setswana, North West, support, 5-19 verified contributions");
  expect(document.querySelector("canvas")).toBeNull();
  expect(document.querySelector("[data-render-style='3d']")).toBeNull();
});
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/frontend && npm test -- src/components/SouthAfricaCoverageMap.test.tsx src/features/impact/ImpactRoute.test.tsx`
Expected: FAIL because the map and Impact route do not exist.

- [ ] **Step 3: Implement the fixed SVG geometry and accessible data mirror**

Use a checked-in `viewBox="0 0 320 300"` SVG path for a simplified South Africa outline and fixed province centroids: `EC(232,226)`, `FS(178,174)`, `GP(202,115)`, `KZN(246,174)`, `LP(205,62)`, `MP(248,111)`, `NC(102,154)`, `NW(159,111)`, `WC(80,235)`. Province location is coarse visual layout, not user location. Every pin has `<title>` and the same text in the adjacent list.

- [ ] **Step 4: Implement Impact route status hierarchy**

Render `Verified contributions`, `Languages active`, and `Missions completed` as the three top progress metrics. Then render the map, then domain gap cards. When `modelGapPercent` is null, show `Model evidence unavailable`; do not infer readiness.

- [ ] **Step 5: Run impact tests and commit**

Run: `cd starter/frontend && npm test -- src/components/SouthAfricaCoverageMap.test.tsx src/features/impact/ImpactRoute.test.tsx`

```bash
git add starter/frontend/src/components/SouthAfricaCoverageMap.tsx starter/frontend/src/components/SouthAfricaCoverageMap.test.tsx starter/frontend/src/features/impact starter/frontend/src/styles/materials.css
git commit -m "UI: add flat aggregate Coverage Constellation"
```

---

### Task 9: Add mission proposals and human-only MTN authorisation

**Files:**
- Modify: `starter/backend/app/models.py`
- Create: `starter/backend/alembic/versions/e0f1a2b3c4d5_language_ops.py`
- Create: `starter/backend/app/missions.py`
- Create: `starter/backend/app/routes/ops.py`
- Modify: `starter/backend/app/api_types.py`
- Modify: `starter/backend/app/main.py`
- Create: `starter/backend/tests/test_missions.py`
- Create: `starter/backend/tests/test_ops_api.py`
- Modify: `starter/backend/tests/test_migrations.py`

**Interfaces:**
- Produces: `propose_mission(session, advisory_job_id, language, province_code, domain, rationale, target_verified_clips, fixed_reward_cents, budget_cents) -> MissionProposal`.
- Produces: `authorise_mission(session, proposal_id, operator, idempotency_key, now) -> MissionProposal`.
- API: `GET /ops` for `MTN_LANGUAGE_OPS` operators.
- API: `POST /ops/missions/{proposal_id}/authorise` with `Idempotency-Key`.
- The authorisation request body is empty; budget, target, language, domain, and fixed reward are copied from the persisted proposal.

- [ ] **Step 1: Write failing authority, immutability, and idempotency tests**

```python
def test_advisory_job_cannot_authorise_its_own_proposal(db_session, proposal, advisory_actor):
    with pytest.raises(OperatorAuthorisationRequired):
        authorise_mission(db_session, proposal.id, advisory_actor, "key-1", NOW)


def test_human_operator_authorisation_is_idempotent_and_preserves_terms(db_session, proposal, mtn_operator):
    first = authorise_mission(db_session, proposal.id, mtn_operator, "key-1", NOW)
    second = authorise_mission(db_session, proposal.id, mtn_operator, "key-1", NOW)
    assert first.id == second.id
    assert first.fixed_reward_cents == proposal.fixed_reward_cents
    assert first.budget_cents == proposal.budget_cents
    assert db_session.scalar(select(func.count(MissionAuthorisation.id))) == 1


def test_different_idempotency_key_cannot_reauthorise(db_session, proposal, mtn_operator):
    authorise_mission(db_session, proposal.id, mtn_operator, "key-1", NOW)
    with pytest.raises(MissionAlreadyDecided):
        authorise_mission(db_session, proposal.id, mtn_operator, "key-2", NOW)
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/backend && python -m pytest tests/test_missions.py tests/test_ops_api.py -v`
Expected: collection failure because mission models and services do not exist.

- [ ] **Step 3: Add mission records and migration**

```python
class MissionProposalState(str, enum.Enum):
    PROPOSED = "PROPOSED"
    AUTHORISED = "AUTHORISED"
    REJECTED = "REJECTED"

class MissionProposal(Base):
    __tablename__ = "mission_proposals"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    advisory_job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("advisory_jobs.id"), unique=True, nullable=False)
    language: Mapped[str] = mapped_column(String(2), nullable=False)
    province_code: Mapped[str] = mapped_column(String(3), nullable=False)
    domain: Mapped[str] = mapped_column(String(32), nullable=False)
    rationale: Mapped[str] = mapped_column(String(1000), nullable=False)
    target_verified_clips: Mapped[int] = mapped_column(Integer, nullable=False)
    fixed_reward_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    budget_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    state: Mapped[MissionProposalState] = mapped_column(SAEnum(MissionProposalState, name="missionproposalstate"), nullable=False, default=MissionProposalState.PROPOSED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)

class MissionAuthorisation(Base):
    __tablename__ = "mission_authorisations"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    proposal_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mission_proposals.id"), unique=True, nullable=False)
    operator_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    authorised_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
```

Set `revision = "e0f1a2b3c4d5"` and `down_revision = "d9e0f1a2b3c4"`. Add checks `target_verified_clips > 0`, `fixed_reward_cents > 0`, `budget_cents >= target_verified_clips * fixed_reward_cents`, language in `zu/tn`, and province/domain in the approved vocabularies. Run `alembic heads` before writing the migration and stop with a dependency error if `d9e0f1a2b3c4` is not the single Stage 6 head; do not silently rebase or create a second head.

- [ ] **Step 4: Enforce a real operator principal**

Use the authenticated session principal from Stage 1. `authorise_mission` requires `principal.kind == "HUMAN"` and `"MTN_LANGUAGE_OPS" in principal.roles`. Return 403 `OPERATOR_ROLE_REQUIRED` for other users, 409 `MISSION_ALREADY_DECIDED` for a second decision, and 409 `IDEMPOTENCY_CONFLICT` when a key belongs to another operation. Write `AuditEvent(action="MISSION_AUTHORISED", actor_id=operator.id, subject_id=proposal.id)` in the same transaction.

- [ ] **Step 5: Run schema, API, and mission tests**

Run: `cd starter/backend && python -m pytest tests/test_missions.py tests/test_ops_api.py tests/test_migrations.py -v`
Run: `cd starter/backend && alembic heads`
Expected: tests pass and exactly one Alembic head is printed.

- [ ] **Step 6: Commit**

```bash
git add starter/backend/app/models.py starter/backend/alembic/versions/e0f1a2b3c4d5_language_ops.py starter/backend/app/missions.py starter/backend/app/routes/ops.py starter/backend/app/api_types.py starter/backend/app/main.py starter/backend/tests/test_missions.py starter/backend/tests/test_ops_api.py starter/backend/tests/test_migrations.py
git commit -m "Ops: require human authorisation for mission launch"
```

---

### Task 10: Implement the MTN Language Ops route

**Files:**
- Create: `starter/frontend/src/features/ops/OpsRoute.tsx`
- Create: `starter/frontend/src/features/ops/OpsRoute.test.tsx`
- Modify: `starter/frontend/src/api/client.ts`
- Modify: `starter/frontend/src/styles/materials.css`

**Interfaces:**
- Consumes `GET /ops` and `POST /ops/missions/{id}/authorise`.
- Shows readiness evidence, aggregate gaps, persisted proposal terms, and a human confirmation dialog.
- Never labels a model ready when `modelReady` is false and never labels a mission launched before `AUTHORISED` returns.

- [ ] **Step 1: Write failing operator and authorisation tests**

```tsx
it("requires a human confirmation and sends no mutable mission terms", async () => {
  const user = userEvent.setup();
  render(<RouterProvider router={createAppRouter(fakeApi, ["/ops"])} />);
  await user.click(await screen.findByRole("button", { name: /review mission/i }));
  expect(screen.getByRole("dialog", { name: /authorise mission/i })).toHaveTextContent("R 2.50 fixed reward");
  await user.click(screen.getByRole("button", { name: /^authorise$/i }));
  expect(fakeApi.authoriseMission).toHaveBeenCalledWith("proposal-1", expect.stringMatching(/^ops-/));
});

it("does not render controls without the MTN Language Ops role", async () => {
  fakeApi.getOps.mockResolvedValue(opsDto({ roles: [] }));
  render(<RouterProvider router={createAppRouter(fakeApi, ["/ops"])} />);
  expect(await screen.findByText("You do not have access to MTN Language Ops.")).toBeVisible();
  expect(screen.queryByRole("button", { name: /authorise/i })).not.toBeInTheDocument();
});
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/frontend && npm test -- src/features/ops/OpsRoute.test.tsx`
Expected: FAIL because operator gating and confirmation do not exist.

- [ ] **Step 3: Implement readiness and proposal hierarchy**

Render readiness rows first, with `Peer coverage`, `Model evidence`, and `Evidence label`. Render proposals second with language, province, domain, rationale, target, fixed reward, and budget. The primary button says `Review mission`, not `Launch automatically`.

- [ ] **Step 4: Implement human confirmation and stable result copy**

The dialog title is `Authorise mission`. Its confirmation text states: `You are authorising the persisted mission terms. AMAZWI will not change the fixed reward or budget from this screen.` On success show `Authorised by {displayName}`. On 409 refresh the proposal and show its committed state. On 403 remove controls and announce the access error assertively.

- [ ] **Step 5: Run Ops and frontend suites**

Run: `cd starter/frontend && npm test -- src/features/ops/OpsRoute.test.tsx src/api/client.test.ts`
Run: `cd starter/frontend && npm run build`

- [ ] **Step 6: Commit**

```bash
git add starter/frontend/src/features/ops starter/frontend/src/api/client.ts starter/frontend/src/styles/materials.css
git commit -m "Ops: add human-authorised Language Ops view"
```

---

### Task 11: Add 320–480px, 200% zoom, keyboard, and screen-reader gates

**Files:**
- Modify: `starter/frontend/package.json`
- Modify: `starter/frontend/package-lock.json`
- Create: `starter/frontend/playwright.config.ts`
- Create: `starter/frontend/e2e/accessibility.spec.ts`
- Create: `starter/frontend/e2e/routes.spec.ts`
- Create: `starter/frontend/src/styles/accessibility.css`

**Interfaces:**
- Produces scripts `test:e2e`, `test:a11y`, and `test:visual`.
- Runs Chromium projects at 320, 360, 390, 430, and 480 CSS pixels.
- Uses native keyboard actions and axe-core; does not infer accessibility from static markup inspection alone.

- [ ] **Step 1: Install exact browser-test dependencies and write failing checks**

Run: `cd starter/frontend && npm install --save-dev @playwright/test@1.55.0 @axe-core/playwright@4.10.2`
Run: `cd starter/frontend && npx playwright install chromium`

```ts
const widths = [320, 360, 390, 430, 480];
for (const width of widths) {
  test(`home reflows at ${width}px and 200% zoom`, async ({ page }) => {
    await page.setViewportSize({ width, height: 844 });
    await page.goto("/");
    await page.evaluate(() => { document.documentElement.style.fontSize = "200%"; });
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
  });
}
```

Add keyboard tests that Tab through theme control, primary CTA, and floating navigation; press Enter/Space on native controls; verify focus never enters hidden surfaces. Add axe scans for every required route in Midnight and Daylight with zero serious or critical violations.

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/frontend && npm run test:a11y`
Expected: FAIL until scripts, configuration, reflow CSS, and complete accessible names exist.

- [ ] **Step 3: Add exact accessibility CSS**

```css
html { min-inline-size: 320px; }
body { overflow-x: clip; }
:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
button, input, select, textarea, a { font: inherit; }
button, [role="button"], .floating-nav a { min-block-size: 44px; min-inline-size: 44px; }
.signal-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr)); gap: var(--space-4); }
.app-shell { inline-size: min(100%, 75rem); margin-inline: auto; padding: clamp(.75rem, 3vw, 2rem); padding-block-end: 6rem; }
.sr-only { position: absolute; inline-size: 1px; block-size: 1px; padding: 0; margin: -1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0; }
@media (forced-colors: active) { .signal-card, .floating-nav { border: 1px solid CanvasText; } }
```

Do not set a fixed 390px app width. Use `rem`, `%`, `min()`, `max()`, and `clamp()` for reflow.

- [ ] **Step 4: Run browser accessibility gates**

Run: `cd starter/frontend && npm run test:a11y`
Run: `cd starter/frontend && npm run test:e2e -- e2e/routes.spec.ts`
Expected: all viewport/theme/route combinations pass; keyboard activation is observed in Chromium, not assumed.

- [ ] **Step 5: Commit**

```bash
git add starter/frontend/package.json starter/frontend/package-lock.json starter/frontend/playwright.config.ts starter/frontend/e2e/accessibility.spec.ts starter/frontend/e2e/routes.spec.ts starter/frontend/src/styles/accessibility.css
git commit -m "UI: enforce mobile zoom keyboard and screen reader gates"
```

---

### Task 12: Add visual regression and evidence-gated Figma token drift

**Files:**
- Create: `starter/frontend/e2e/visual.spec.ts`
- Create: `starter/frontend/scripts/export-figma.mjs`
- Create: `starter/frontend/scripts/check-figma-evidence.mjs`
- Create: `starter/frontend/scripts/check-figma-evidence.test.mjs`
- Modify: `starter/frontend/package.json`
- Modify: `starter/frontend/package-lock.json`
- Create: `starter/frontend/visual/README.md`
- Create: `starter/frontend/.gitignore`

**Interfaces:**
- Produces scripts `figma:export`, `figma:check`, and `test:visual`.
- Read-only export target is exactly Figma file `JPZuFmbhRh9fhkgBLxRymq`.
- Required frame names are `Midnight/Home`, `Midnight/Receipt`, `Midnight/Impact`, `Midnight/Ops`, `Daylight/Home`, `Daylight/Receipt`, `Daylight/Impact`, `Daylight/Ops`.
- Export manifest contains `fileKey`, `fileVersion`, `exportedAt`, discovered node IDs, image SHA-256 values, and semantic token values.
- Evidence older than 24 hours or missing any required frame returns exit code 2 and prints `FIGMA_COMPARISON_UNAVAILABLE`.

- [ ] **Step 1: Write failing evidence-gate tests**

```js
import assert from "node:assert/strict";
import test from "node:test";
import { validateEvidence } from "./check-figma-evidence.mjs";

test("missing evidence cannot become a parity claim", () => {
  const result = validateEvidence(null, new Date("2026-09-01T12:00:00Z"));
  assert.deepEqual(result, { ok: false, code: "FIGMA_COMPARISON_UNAVAILABLE", reasons: ["manifest missing"] });
});

test("stale evidence is rejected", () => {
  const result = validateEvidence({ fileKey: "JPZuFmbhRh9fhkgBLxRymq", exportedAt: "2026-08-30T00:00:00Z", frames: {}, tokens: {} }, new Date("2026-09-01T12:00:00Z"));
  assert.equal(result.ok, false);
  assert.equal(result.code, "FIGMA_COMPARISON_UNAVAILABLE");
});
```

- [ ] **Step 2: Run and verify failure**

Run: `cd starter/frontend && node --test scripts/check-figma-evidence.test.mjs`
Expected: FAIL because the evidence validator does not exist.

- [ ] **Step 3: Implement read-only Figma export**

`export-figma.mjs` requires `FIGMA_TOKEN`, requests `GET https://api.figma.com/v1/files/JPZuFmbhRh9fhkgBLxRymq`, recursively finds the eight exact frame names, requests PNG URLs with `GET /v1/images/JPZuFmbhRh9fhkgBLxRymq?ids={comma-separated-node-ids}&format=png&scale=1`, and requests local variables with `GET /v1/files/JPZuFmbhRh9fhkgBLxRymq/variables/local`. It downloads PNGs, hashes each file with SHA-256, resolves the exact semantic variables `ground`, `ground-deep`, `surface-1`, `surface-2`, `text`, `text-dim`, `border`, `focus`, `shadow`, and `texture-opacity` for the separate Midnight and Daylight collections, and writes the generated manifest. It sends only `X-Figma-Token`; it performs no POST, PUT, PATCH, or DELETE request. A 401, 403, absent variable collection, unresolved alias, or missing mode exits 2 with `FIGMA_COMPARISON_UNAVAILABLE` and the exact reason.

If a frame name is absent, the script exits 2 and prints its exact missing name. It does not create, rename, or modify Figma nodes.

- [ ] **Step 4: Implement token drift and visual tests**

`figma:check` compares exported semantic tokens to computed Midnight and Daylight CSS token maps. It reports each mismatch as `{theme}.{token}: figma={value} react={value}`. Visual Playwright tests take route screenshots at 390×844 for both themes with animations disabled and compare to checked-in Playwright baselines. Figma screenshots are kept as evidence references; they are not silently substituted for app baselines.

```ts
for (const theme of ["midnight", "daylight"] as const) {
  for (const route of ["/", "/receipt/c1", "/impact", "/ops"]) {
    test(`${theme} ${route}`, async ({ page }) => {
      await page.emulateMedia({ reducedMotion: "reduce", colorScheme: theme === "daylight" ? "light" : "dark" });
      await page.goto(`${route}?theme=${theme}`);
      await expect(page).toHaveScreenshot(`${theme}-${route.replaceAll("/", "_") || "home"}.png`, { animations: "disabled", fullPage: true });
    });
  }
}
```

- [ ] **Step 5: Run evidence and visual gates**

Run without export evidence: `cd starter/frontend && npm run figma:check`
Expected: exit 2 with `FIGMA_COMPARISON_UNAVAILABLE`; do not write a parity statement.

Run when a read-only token is available: `cd starter/frontend && npm run figma:export && npm run figma:check`
Expected: eight named frames exported and token comparison passes, or exact drift is reported without mutating Figma.

Run: `cd starter/frontend && npm run test:visual`
Expected: Midnight and Daylight route baselines pass independently.

- [ ] **Step 6: Commit**

```bash
git add starter/frontend/e2e/visual.spec.ts starter/frontend/scripts starter/frontend/package.json starter/frontend/package-lock.json starter/frontend/visual/README.md starter/frontend/.gitignore starter/frontend/e2e/visual.spec.ts-snapshots
git commit -m "UI: gate visual regression on Figma export evidence"
```

---

### Task 13: Verify the visible engagement-to-operations loop

**Files:**
- Create: `starter/backend/tests/test_language_ops_e2e.py`
- Create: `starter/frontend/e2e/governed-loop.spec.ts`
- Create: `starter/frontend/STAGE_7_8_EVIDENCE.md`
- Modify: `05_amazwi/P0.md`
- Modify: `05_amazwi/BUILD_LOG.md`
- Modify: `HANDOVER_SBU.md`

**Interfaces:**
- Verifies peer truth → reward → advisory insight → aggregate coverage → proposal → human authorisation.
- Preserves peer truth and reward when Council is disabled or failed.
- Records what ran, what did not run, Figma export status, and target-device status without deployment claims.

- [ ] **Step 1: Write the failing backend end-to-end test**

```python
def test_peer_truth_to_human_authorised_mission(db_session, seeded_governed_flow, mtn_operator):
    receipt = seeded_governed_flow.resolve_with_two_peers(training_consent=True)
    assert receipt.peer_decision == "CORPUS_ELIGIBLE"
    assert receipt.reward_event_count == 1
    insight = seeded_governed_flow.run_council()
    coverage = build_coverage(db_session, NOW)
    proposal = propose_mission(db_session, insight.job_id, "tn", "NW", "support", "Peer coverage exceeds current signed model evidence.", 20, 250, 5000)
    assert proposal.state.value == "PROPOSED"
    authorised = authorise_mission(db_session, proposal.id, mtn_operator, "ops-e2e-1", NOW)
    assert authorised.state.value == "AUTHORISED"
    assert seeded_governed_flow.reward_event_count() == 1
    assert coverage.nodes
```

- [ ] **Step 2: Write the failing browser loop**

The browser test starts from seeded receipt `/receipt/{id}`, asserts peer truth appears before advisory insight, opens `/impact`, confirms the updated aggregate node and finite ripple, opens `/ops`, reviews persisted terms, confirms as the seeded human operator, and observes `Authorised by`. Repeat with Council disabled and assert receipt and impact remain usable while no model-readiness claim appears.

- [ ] **Step 3: Run integrated verification**

Run: `cd starter/backend && python -m pytest tests/test_language_ops_e2e.py -v`
Run: `cd starter/backend && python -m pytest -q`
Run: `cd starter/frontend && npm test`
Run: `cd starter/frontend && npm run build`
Run: `cd starter/frontend && npm run test:a11y`
Run: `cd starter/frontend && npm run test:e2e`
Run: `cd starter/frontend && npm run test:visual`
Run: `cd starter/frontend && npm run figma:check`
Expected: all code, accessibility, route, and visual tests pass. `figma:check` either passes against fresh complete evidence or exits 2 with `FIGMA_COMPARISON_UNAVAILABLE`; the latter blocks a Figma parity claim but does not convert tested React behavior into a failure.

- [ ] **Step 4: Record exact evidence and unresolved checks**

`STAGE_7_8_EVIDENCE.md` records command, UTC timestamp, exit code, test count, browser version, viewport/theme matrix, Figma file key, Figma file version and export timestamp when available, screenshot paths, and whether real target-device profiling ran. It must state `No Vercel deployment performed.` It must state `Figma parity not claimed` unless the fresh eight-frame export and token gate both passed. It must state `MTN mission authorisation exercised with a seeded operator and no real campaign launched.`

Update truth documents with the same distinctions: implemented, locally verified, export-compared, target-device verified, and not run. Do not collapse these into a single `done` label.

- [ ] **Step 5: Commit without deploying**

```bash
git add starter/backend/tests/test_language_ops_e2e.py starter/frontend/e2e/governed-loop.spec.ts starter/frontend/STAGE_7_8_EVIDENCE.md 05_amazwi/P0.md 05_amazwi/BUILD_LOG.md HANDOVER_SBU.md
git commit -m "Docs: record Signal Flow and Language Ops evidence"
```

Do not run `vercel`, `vercel deploy`, `git push`, a production campaign command, or a Figma mutation command.

---

## Final Acceptance Checklist

- [ ] The frontend source is split into `api`, `app`, `components`, `features`, and `styles` with no root-level feature component left behind.
- [ ] All eight required routes render through one `AppShell`.
- [ ] Midnight Shweshwe and Signal Daylight pass the same unit, route, accessibility, and visual suites.
- [ ] Ndebele is available only during September or `?season=heritage`, is never persisted as the normal default, and appears only as restrained accents.
- [ ] Signal Flow radii, layered surfaces, controlled overlap, grain, glow, typography, waveform identity, and Kuest-inspired progress/status hierarchy are present.
- [ ] CSS/WAAPI motion follows the causal sequence and timing budget; reduced motion removes morph/ripple/celebration movement without blocking actions.
- [ ] Consent, record, verify, result, and receipt preserve existing server-side consent and peer authority.
- [ ] Receipt renders peer truth before reward and advisory AI; Council disabled/pending/failed states do not affect truth or money.
- [ ] No chance wheel, spin action, random payout, random amount, or 3D map exists.
- [ ] Coverage Constellation is a flat SA map with aggregate privacy-thresholded nodes and an equivalent accessible list.
- [ ] Mission proposals remain advisory and can be authorised only by a human `MTN_LANGUAGE_OPS` operator with an idempotent audited transaction.
- [ ] 320, 360, 390, 430, and 480px widths pass; 200% text sizing causes no horizontal page scroll.
- [ ] Keyboard activation, focus visibility/order, live regions, accessible names, and zero serious/critical axe violations pass in both first-class themes.
- [ ] Visual regression passes for Home, Receipt, Impact, and Ops in both first-class themes.
- [ ] Figma token/image comparison uses fresh read-only evidence from `JPZuFmbhRh9fhkgBLxRymq`, or reports `FIGMA_COMPARISON_UNAVAILABLE` and makes no parity claim.
- [ ] No Vercel deployment, Figma mutation, real payment, or real campaign launch occurs.
