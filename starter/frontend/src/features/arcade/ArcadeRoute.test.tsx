/**
 * ArcadeRoute tests.
 *
 * Follows the established convention in `OpsRoute.test.tsx` --
 * MemoryRouter wrapping, `fireEvent`, `vi.spyOn(api, ...)`.
 *
 * The tests that matter here are the honesty ones. A gamified dashboard
 * is the easiest place in this product to show a number nobody measured,
 * so there are explicit assertions that the screen renders no skill
 * radar, no presence count, and never calls ledger credit a balance.
 */
import { afterEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ArcadeRoute, formatRand, initials, languageName } from "./ArcadeRoute";
import { ApiError, api } from "../../api/client";
import type { ArcadeDashboard } from "../../api/contracts";

function dto(overrides: Partial<ArcadeDashboard> = {}): ArcadeDashboard {
  return {
    display_name: "Demo Speaker (zu)",
    earned_cents: 400,
    progression: {
      xp: 200,
      level: 1,
      tier: "Amateur",
      xp_into_level: 200,
      xp_for_next_level: 300,
      percent_into_level: 67,
      verified_contributions: 2,
      completed_verifications: 0,
    },
    outcomes: {
      understood: 2,
      not_understood: 1,
      awaiting_peers: 0,
      closed: 0,
      total: 3,
    },
    decks: [
      { language: "zu", card_count: 8, contributors: 5, verified_contributions: 13 },
      { language: "tn", card_count: 8, contributors: 4, verified_contributions: 9 },
    ],
    quests: [
      {
        key: "speak_today",
        label: "Record 2 voice cards",
        detail: "Describe the word without saying it.",
        progress: 0,
        target: 2,
        reward_xp: 140,
        complete: false,
      },
    ],
    invitations: [],
    peers: [
      {
        user_id: "peer-1",
        display_name: "Demo Verifier 1 (zu)",
        language: "zu",
        tier: "Beginner",
        verified_contributions: 0,
      },
    ],
    leaderboard: [
      {
        rank: 1,
        user_id: "u1",
        display_name: "Nomsa K.",
        verified_contributions: 5,
        xp: 500,
        tier: "Veteran",
        is_current_user: false,
      },
      {
        rank: 2,
        user_id: "u2",
        display_name: "Sipho M.",
        verified_contributions: 3,
        xp: 300,
        tier: "Amateur",
        is_current_user: false,
      },
      {
        rank: 3,
        user_id: "u3",
        display_name: "Ayanda D.",
        verified_contributions: 2,
        xp: 200,
        tier: "Amateur",
        is_current_user: false,
      },
      {
        rank: 4,
        user_id: "u4",
        display_name: "Demo Speaker (zu)",
        verified_contributions: 2,
        xp: 200,
        tier: "Amateur",
        is_current_user: true,
      },
    ],
    leaderboard_language: "zu",
    generated_at: "2026-09-02T20:00:00Z",
    ...overrides,
  };
}

function renderRoute() {
  return render(
    <MemoryRouter initialEntries={["/dashboard"]}>
      <ArcadeRoute />
    </MemoryRouter>,
  );
}

afterEach(() => vi.restoreAllMocks());

describe("pure helpers", () => {
  it("strips non-letters from initials", () => {
    // The seeded names carry a language suffix; taking the last word's
    // first character blindly rendered "D(" on the real dashboard.
    expect(initials("Demo Speaker (zu)")).toBe("DZ");
    expect(initials("Nomsa K.")).toBe("NK");
    expect(initials("Sipho")).toBe("SI");
    expect(initials("   ")).toBe("?");
    expect(initials("(((")).toBe("?");
  });

  it("formats rand from cents", () => {
    expect(formatRand(0)).toBe("R0.00");
    expect(formatRand(400)).toBe("R4.00");
    expect(formatRand(12345)).toBe("R123.45");
  });

  it("names known languages and passes unknown codes through", () => {
    expect(languageName("zu")).toBe("isiZulu");
    expect(languageName("tn")).toBe("Setswana");
    expect(languageName("xh")).toBe("xh");
  });
});

describe("ArcadeRoute", () => {
  it("renders real progression, decks and leaderboard from the API", async () => {
    vi.spyOn(api, "getArcade").mockResolvedValue(dto());
    renderRoute();

    // The name appears twice by design -- profile panel and the
    // leaderboard row for the current user -- so assert on both.
    expect((await screen.findAllByText("Demo Speaker (zu)")).length).toBe(2);
    expect(screen.getByText("R4.00")).toBeTruthy();
    expect(screen.getByText(/Level 1 · Amateur/)).toBeTruthy();
    expect(screen.getByText("Nomsa K.")).toBeTruthy();
    // Scoped by role: "isiZulu" is also the leaderboard's language tag,
    // so a bare text query is ambiguous by design here.
    expect(screen.getByRole("heading", { name: "isiZulu", level: 3 })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Setswana", level: 3 })).toBeTruthy();
  });

  it("describes money as credited, never as a balance or as paid", async () => {
    vi.spyOn(api, "getArcade").mockResolvedValue(dto());
    const { container } = renderRoute();
    await screen.findByText("R4.00");

    const text = container.textContent ?? "";
    expect(text).toMatch(/Credited in the reward ledger/i);
    expect(text).not.toMatch(/\bbalance\b/i);
    expect(text).not.toMatch(/\bwithdraw\b/i);
    expect(text).not.toMatch(/\bpaid out\b/i);
  });

  it("renders no fabricated engagement metric", async () => {
    vi.spyOn(api, "getArcade").mockResolvedValue(dto());
    const { container } = renderRoute();
    await screen.findByText("R4.00");

    const text = (container.textContent ?? "").toLowerCase();
    // The reference dashboard shows a five-axis skill radar and a live
    // "N playing" figure. AMAZWI measures neither.
    for (const forbidden of [
      "teamwork",
      "creativity",
      "curiosity",
      "discipline",
      "playing",
      "online now",
      "streak",
    ]) {
      expect(text).not.toContain(forbidden);
    }
  });

  it("shows the real outcome split instead of a skill chart", async () => {
    vi.spyOn(api, "getArcade").mockResolvedValue(dto());
    renderRoute();
    await screen.findByText("R4.00");

    expect(screen.getByText("Understood")).toBeTruthy();
    expect(screen.getByText("Not understood")).toBeTruthy();
    // Zero-valued buckets are omitted rather than drawn as empty axes.
    expect(screen.queryByText("Waiting on peers")).toBeNull();
  });

  it("keeps leaderboard DOM order as rank order despite the visual podium", async () => {
    vi.spyOn(api, "getArcade").mockResolvedValue(dto());
    const { container } = renderRoute();
    await screen.findByText("Nomsa K.");

    // Visual order is 2nd-1st-3rd via CSS `order`; assistive tech and
    // Tab must still meet first place first.
    const names = [...container.querySelectorAll(".podium-name")].map(
      (n) => n.textContent,
    );
    expect(names).toEqual(["Nomsa K.", "Sipho M.", "Ayanda D."]);
  });

  it("marks the current user in the leaderboard", async () => {
    vi.spyOn(api, "getArcade").mockResolvedValue(dto());
    const { container } = renderRoute();
    await screen.findByText("Nomsa K.");
    expect(container.querySelector(".lb-list li.is-you")).toBeTruthy();
  });

  it("shows an honest empty state rather than placeholder numbers", async () => {
    vi.spyOn(api, "getArcade").mockResolvedValue(
      dto({
        earned_cents: 0,
        outcomes: {
          understood: 0,
          not_understood: 0,
          awaiting_peers: 0,
          closed: 0,
          total: 0,
        },
        leaderboard: [],
        peers: [],
      }),
    );
    renderRoute();

    expect(await screen.findByText("R0.00")).toBeTruthy();
    expect(
      screen.getByText(/No clips yet\. Your first recording appears here\./),
    ).toBeTruthy();
    expect(
      screen.getByText(/No verified contributions in this language yet\./),
    ).toBeTruthy();
  });

  it("badges pending peer requests and renders each invitation", async () => {
    vi.spyOn(api, "getArcade").mockResolvedValue(
      dto({
        invitations: [
          {
            assignment_id: "a1",
            contribution_id: "c1",
            language: "zu",
            speaker_name: "Thandeka N.",
            created_at: "2026-09-02T19:00:00Z",
          },
        ],
      }),
    );
    const { container } = renderRoute();

    expect(await screen.findByText("Thandeka N.")).toBeTruthy();
    expect(container.querySelector(".desk-badge")?.textContent).toContain("1");
    expect(screen.getByText(/wants you to listen/)).toBeTruthy();
  });

  it("filters the peer list without hiding that a filter is active", async () => {
    vi.spyOn(api, "getArcade").mockResolvedValue(dto());
    renderRoute();
    await screen.findByText("Demo Verifier 1 (zu)");

    fireEvent.change(screen.getByLabelText(/Filter peers by name/i), {
      target: { value: "zzzz" },
    });
    // A no-match must say so, and must not read as "you have no peers".
    expect(screen.getByText(/No peer matches that name\./)).toBeTruthy();
  });

  it("surfaces an API failure instead of spinning forever", async () => {
    vi.spyOn(api, "getArcade").mockRejectedValue(
      new ApiError(401, "AUTHENTICATION_REQUIRED", "nope"),
    );
    renderRoute();

    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toMatch(/Sign in to MoMo to continue\./);
    expect(screen.queryByText(/Loading your desk/)).toBeNull();
  });

  it("exposes progress bars with real accessible values", async () => {
    vi.spyOn(api, "getArcade").mockResolvedValue(dto());
    renderRoute();
    await screen.findByText("R4.00");

    const bars = screen.getAllByRole("progressbar");
    const xp = bars.find(
      (b) => b.getAttribute("aria-label") === "Experience toward level 2",
    );
    expect(xp?.getAttribute("aria-valuenow")).toBe("200");
    expect(xp?.getAttribute("aria-valuemax")).toBe("300");
  });
});
