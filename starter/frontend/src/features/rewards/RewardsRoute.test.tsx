/**
 * RewardsRoute tests.
 *
 * The load-bearing ones are the honesty tests. A rewards catalogue is
 * the single easiest screen in this product on which to imply a
 * commercial relationship that does not exist, or to make demo credit
 * look spendable.
 */
import { afterEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { RewardsRoute, availabilityLabel } from "./RewardsRoute";
import { ApiError, api } from "../../api/client";
import type { Rewards } from "../../api/contracts";

function dto(overrides: Partial<Rewards> = {}): Rewards {
  return {
    balance_cents: 400,
    provider_mode: "demo",
    provider_connected: false,
    thresholds_are_proposed: true,
    items: [
      {
        key: "airtime",
        title: "Airtime top-up",
        description: "Send airtime to your own registered number.",
        threshold_cents: 500,
        momo_product: "Airtime purchase",
        availability: "PROVIDER_NOT_CONNECTED",
        shortfall_cents: 100,
      },
      {
        key: "data",
        title: "Data bundle",
        description: "Turn what you earned into data for your phone.",
        threshold_cents: 1000,
        momo_product: "Data bundle purchase",
        availability: "PROVIDER_NOT_CONNECTED",
        shortfall_cents: 600,
      },
    ],
    generated_at: "2026-09-02T21:00:00Z",
    ...overrides,
  };
}

function renderRoute() {
  return render(
    <MemoryRouter initialEntries={["/rewards"]}>
      <RewardsRoute />
    </MemoryRouter>,
  );
}

afterEach(() => vi.restoreAllMocks());

describe("availabilityLabel", () => {
  it("never implies a live provider when there is none", () => {
    expect(availabilityLabel("PROVIDER_NOT_CONNECTED", 0)).toBe(
      "Not redeemable in demo mode",
    );
  });

  it("states the exact shortfall rather than a vague nudge", () => {
    expect(availabilityLabel("INSUFFICIENT_CREDIT", 600)).toBe(
      "R6.00 more to unlock",
    );
  });

  it("only says ready when the server says redeemable", () => {
    expect(availabilityLabel("REDEEMABLE", 0)).toBe("Ready to redeem");
  });
});

describe("RewardsRoute", () => {
  it("shows the real ledger figure and refuses the word balance", async () => {
    vi.spyOn(api, "getRewards").mockResolvedValue(dto());
    const { container } = renderRoute();

    expect(await screen.findByText("R4.00")).toBeTruthy();
    const text = container.textContent ?? "";
    expect(text).toMatch(/Credited in the reward ledger/i);
    expect(text).not.toMatch(/\bbalance\b/i);
    expect(text).not.toMatch(/\byour wallet balance\b/i);
  });

  it("renders NO redeem button while the provider is not connected", async () => {
    vi.spyOn(api, "getRewards").mockResolvedValue(dto());
    const { container } = renderRoute();
    await screen.findByText("R4.00");

    // Not a disabled button either -- a disabled control still reads as
    // an offer that exists. There must be none at all.
    expect(container.querySelector(".btn-redeem")).toBeNull();
    expect(screen.queryByRole("button", { name: /redeem/i })).toBeNull();
  });

  it("states the demo-provider truth once, prominently", async () => {
    vi.spyOn(api, "getRewards").mockResolvedValue(dto());
    renderRoute();
    expect(
      await screen.findByText(/no live MoMo provider is connected/i),
    ).toBeTruthy();
  });

  it("renders a redeem button only when the server says redeemable", async () => {
    vi.spyOn(api, "getRewards").mockResolvedValue(
      dto({
        balance_cents: 5000,
        provider_mode: "live",
        provider_connected: true,
        items: [
          {
            key: "airtime",
            title: "Airtime top-up",
            description: "Send airtime to your own registered number.",
            threshold_cents: 500,
            momo_product: "Airtime purchase",
            availability: "REDEEMABLE",
            shortfall_cents: 0,
          },
        ],
      }),
    );
    const { container } = renderRoute();

    expect(await screen.findByRole("button", { name: "Redeem" })).toBeTruthy();
    expect(container.querySelector(".provider-note")).toBeNull();
  });

  it("names no merchant, prize draw or fake scarcity", async () => {
    vi.spyOn(api, "getRewards").mockResolvedValue(dto());
    const { container } = renderRoute();
    await screen.findByText("R4.00");

    const text = (container.textContent ?? "").toLowerCase();
    // The reference design shows a retailer discount and an iPhone
    // giveaway with a countdown. AMAZWI has neither relationship.
    for (const forbidden of [
      "nishat",
      "iphone",
      "lucky draw",
      "slots left",
      "hurry",
      "% off",
      "limited time",
      "expires in",
    ]) {
      expect(text).not.toContain(forbidden);
    }
  });

  it("shows no points currency alongside rand", async () => {
    vi.spyOn(api, "getRewards").mockResolvedValue(dto());
    const { container } = renderRoute();
    await screen.findByText("R4.00");
    const text = (container.textContent ?? "").toLowerCase();
    expect(text).not.toMatch(/\d+\s*points\b/);
    expect(text).not.toContain("coins");
  });

  it("discloses that thresholds are not final", async () => {
    vi.spyOn(api, "getRewards").mockResolvedValue(dto());
    renderRoute();
    expect(
      await screen.findByText(/Redemption amounts are proposed, not final/i),
    ).toBeTruthy();
  });

  it("toggles details with correct aria wiring", async () => {
    vi.spyOn(api, "getRewards").mockResolvedValue(dto());
    renderRoute();
    const buttons = await screen.findAllByRole("button", { name: "view details" });
    const first = buttons[0];

    expect(first.getAttribute("aria-expanded")).toBe("false");
    fireEvent.click(first);

    const expanded = screen.getByRole("button", { name: "hide details" });
    expect(expanded.getAttribute("aria-expanded")).toBe("true");
    expect(screen.getByText("Airtime purchase")).toBeTruthy();
    expect(
      document.getElementById(expanded.getAttribute("aria-controls") ?? ""),
    ).toBeTruthy();
  });

  it("surfaces an API failure instead of spinning forever", async () => {
    vi.spyOn(api, "getRewards").mockRejectedValue(
      new ApiError(401, "AUTHENTICATION_REQUIRED", "nope"),
    );
    renderRoute();

    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toMatch(/Sign in to MoMo to continue\./);
    expect(screen.queryByText(/Loading your rewards/)).toBeNull();
  });

  it("shows an honest zero for a contributor who has earned nothing", async () => {
    vi.spyOn(api, "getRewards").mockResolvedValue(
      dto({ balance_cents: 0, items: [] }),
    );
    renderRoute();
    expect(await screen.findByText("R0.00")).toBeTruthy();
  });
});
