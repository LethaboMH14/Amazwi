import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ImpactRoute } from "./ImpactRoute";

const IMPACT = {
  verified_total: 42,
  languages_active: 2,
  missions_completed: 0,
  geography_available: false,
  suppressed_cell_count: 1,
  generated_at: "2026-09-02T00:00:00Z",
  nodes: [
    {
      id: "tn:NATIONAL:support",
      language: "tn",
      province_code: null,
      campaign: "support",
      verified_count_band: "5-19" as const,
      coverage_percent: 24,
      model_gap_percent: null,
      updated_at: "2026-09-02T00:00:00Z",
    },
    {
      id: "zu:NATIONAL:support",
      language: "zu",
      province_code: null,
      campaign: "support",
      verified_count_band: "20-49" as const,
      coverage_percent: 76,
      model_gap_percent: null,
      updated_at: "2026-09-02T00:00:00Z",
    },
  ],
};

function mockImpact(body: unknown, status = 200) {
  return vi
    .spyOn(globalThis, "fetch")
    .mockResolvedValue(new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } }));
}

function renderRoute() {
  return render(
    <MemoryRouter>
      <ImpactRoute />
    </MemoryRouter>,
  );
}

describe("ImpactRoute", () => {
  afterEach(() => vi.restoreAllMocks());

  it("reads aggregate coverage from the real /api/impact endpoint", async () => {
    const fetchMock = mockImpact(IMPACT);
    renderRoute();
    await screen.findByText("42");
    expect(fetchMock.mock.calls[0][0]).toBe("/api/impact");
  });

  it("shows the three progress metrics before the map", async () => {
    mockImpact(IMPACT);
    renderRoute();
    await screen.findByText("42");
    expect(screen.getByText("Verified contributions")).toBeInTheDocument();
    expect(screen.getByText("Languages active")).toBeInTheDocument();
    expect(screen.getByText("Missions completed")).toBeInTheDocument();
    expect(screen.getByText("42")).toBeInTheDocument();
  });

  it("renders the flat coverage map wired to the API data", async () => {
    mockImpact(IMPACT);
    renderRoute();
    expect(await screen.findByRole("img", { name: /south africa language coverage/i })).toBeVisible();
    expect(screen.getByRole("list", { name: /coverage details/i })).toHaveTextContent(
      "Setswana, National, support, 5-19 verified contributions",
    );
    expect(document.querySelector("canvas")).toBeNull();
  });

  it("says model evidence is unavailable instead of implying readiness", async () => {
    mockImpact(IMPACT);
    renderRoute();
    expect(await screen.findByRole("region", { name: /coverage gaps/i })).toBeVisible();
    expect(screen.getAllByText("Model evidence unavailable").length).toBeGreaterThan(0);
  });

  it("explains suppression rather than showing an empty screen", async () => {
    mockImpact({ ...IMPACT, verified_total: 3, nodes: [], suppressed_cell_count: 1 });
    renderRoute();
    expect(await screen.findByText(/below the five-contribution privacy threshold/i)).toBeInTheDocument();
  });

  it("surfaces a real API failure to the user", async () => {
    mockImpact({ code: "HTTP_ERROR", detail: "Coverage is unavailable right now." }, 500);
    renderRoute();
    expect(await screen.findByRole("alert")).toHaveTextContent("Coverage is unavailable right now.");
  });

  it("never renders an identifier, coordinate or audio field", async () => {
    mockImpact(IMPACT);
    const { container } = renderRoute();
    await screen.findByText("42");
    for (const forbidden of ["latitude", "longitude", "audio", "transcript", "user_id", "contribution_id"]) {
      expect(container.innerHTML).not.toContain(forbidden);
    }
  });
});
