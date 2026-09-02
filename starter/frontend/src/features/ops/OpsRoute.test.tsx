/**
 * OpsRoute tests (Plan 03, Task 10).
 *
 * The plan's snippet used `createAppRouter` and `userEvent`; neither exists
 * in this project, so these tests follow the established convention in
 * `ConsentRoute.test.tsx` -- MemoryRouter wrapping, `fireEvent`, and
 * `vi.spyOn(api, ...)` -- rather than adding a dependency for one file.
 */
import { afterEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { OpsRoute } from "./OpsRoute";
import { ApiError, api } from "../../api/client";
import type { MissionProposal, OpsView } from "../../api/contracts";

const CONFIRMATION =
  "You are authorising the persisted mission terms. " +
  "AMAZWI will not change the fixed reward or budget from this screen.";

const proposal: MissionProposal = {
  id: "proposal-1",
  language: "tn",
  province_code: "NW",
  domain: "support",
  rationale: "Setswana support coverage is the largest verified gap.",
  target_verified_clips: 100,
  fixed_reward_cents: 250,
  budget_cents: 25000,
  state: "PROPOSED",
  authorised_by: null,
};

function opsDto(overrides: Partial<OpsView> = {}): OpsView {
  return {
    principal_kind: "HUMAN",
    roles: ["MTN_LANGUAGE_OPS"],
    display_name: "Thandi Nkosi",
    confirmation_text: CONFIRMATION,
    readiness: [
      { label: "Peer coverage", value: "42", detail: "42 peer-verified contributions", available: true },
      { label: "Model evidence", value: null, detail: "No evaluation run is recorded.", available: false },
      { label: "Evidence label", value: "Peer truth is authoritative", detail: "Advisory AI never overrides a peer decision.", available: true },
    ],
    gaps: [{ language: "tn", verified_contributions: 42 }],
    proposals: [proposal],
    ...overrides,
  };
}

function renderOps() {
  return render(
    <MemoryRouter initialEntries={["/ops"]}>
      <OpsRoute />
    </MemoryRouter>,
  );
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("OpsRoute", () => {
  it("does not render controls without the MTN Language Ops role", async () => {
    vi.spyOn(api, "getOps").mockResolvedValue(
      opsDto({ roles: [], readiness: [], gaps: [], proposals: [] }),
    );
    renderOps();
    expect(
      await screen.findByText("You do not have access to MTN Language Ops."),
    ).toBeVisible();
    expect(screen.queryByRole("button", { name: /authorise/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /review mission/i })).not.toBeInTheDocument();
  });

  it("requires a second human confirmation and sends no mutable mission terms", async () => {
    vi.spyOn(api, "getOps").mockResolvedValue(opsDto());
    const authorise = vi
      .spyOn(api, "authoriseMission")
      .mockResolvedValue({ ...proposal, state: "AUTHORISED", authorised_by: "Thandi Nkosi" });

    renderOps();

    // The list button reviews. It must not authorise on its own.
    fireEvent.click(await screen.findByRole("button", { name: /review mission/i }));
    expect(authorise).not.toHaveBeenCalled();

    const dialog = screen.getByRole("dialog", { name: /authorise mission/i });
    expect(dialog).toHaveTextContent("R 2.50 fixed reward");
    expect(dialog).toHaveTextContent(CONFIRMATION);

    fireEvent.click(screen.getByRole("button", { name: /^authorise$/i }));
    await waitFor(() =>
      expect(authorise).toHaveBeenCalledWith(
        "proposal-1",
        expect.stringMatching(/^ops-/),
        CONFIRMATION,
      ),
    );
    // Exactly three arguments: id, idempotency key, confirmation echo. No
    // reward, budget or target is sent from this screen.
    expect(authorise.mock.calls[0]).toHaveLength(3);
  });

  it("announces the authorising operator on success", async () => {
    vi.spyOn(api, "getOps").mockResolvedValue(opsDto());
    vi.spyOn(api, "authoriseMission").mockResolvedValue({
      ...proposal,
      state: "AUTHORISED",
      authorised_by: "Thandi Nkosi",
    });
    renderOps();
    fireEvent.click(await screen.findByRole("button", { name: /review mission/i }));
    fireEvent.click(screen.getByRole("button", { name: /^authorise$/i }));
    expect(await screen.findByText("Authorised by Thandi Nkosi")).toBeVisible();
  });

  it("never labels a mission launched before AUTHORISED comes back", async () => {
    vi.spyOn(api, "getOps").mockResolvedValue(opsDto());
    vi.spyOn(api, "authoriseMission").mockReturnValue(new Promise(() => {}));
    renderOps();
    fireEvent.click(await screen.findByRole("button", { name: /review mission/i }));
    fireEvent.click(screen.getByRole("button", { name: /^authorise$/i }));
    await screen.findByRole("button", { name: /authorising/i });
    expect(screen.queryByText(/launched/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/authorised by/i)).not.toBeInTheDocument();
  });

  it("removes controls and announces assertively on a 403", async () => {
    vi.spyOn(api, "getOps").mockResolvedValue(opsDto());
    vi.spyOn(api, "authoriseMission").mockRejectedValue(
      new ApiError(403, "OPERATOR_ROLE_REQUIRED", "nope"),
    );
    renderOps();
    fireEvent.click(await screen.findByRole("button", { name: /review mission/i }));
    fireEvent.click(screen.getByRole("button", { name: /^authorise$/i }));

    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent("You do not have access to MTN Language Ops.");
    expect(alert.closest("[aria-live='assertive']")).not.toBeNull();
    expect(screen.queryByRole("button", { name: /review mission/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^authorise$/i })).not.toBeInTheDocument();
  });

  it("refreshes and shows the committed state on a 409", async () => {
    const getOps = vi
      .spyOn(api, "getOps")
      .mockResolvedValueOnce(opsDto())
      .mockResolvedValue(
        opsDto({
          proposals: [{ ...proposal, state: "AUTHORISED", authorised_by: "Someone Else" }],
        }),
      );
    vi.spyOn(api, "authoriseMission").mockRejectedValue(
      new ApiError(409, "MISSION_ALREADY_DECIDED", "already decided"),
    );
    renderOps();
    fireEvent.click(await screen.findByRole("button", { name: /review mission/i }));
    fireEvent.click(screen.getByRole("button", { name: /^authorise$/i }));

    expect(await screen.findByText(/already been decided/i)).toBeVisible();
    expect(await screen.findByText("Authorised by Someone Else")).toBeVisible();
    expect(getOps).toHaveBeenCalledTimes(2);
  });

  it("labels missing model evidence as unavailable instead of showing a number", async () => {
    vi.spyOn(api, "getOps").mockResolvedValue(opsDto());
    renderOps();
    expect(await screen.findByText("Model evidence")).toBeVisible();
    expect(screen.getByText(/Model evidence unavailable/)).toBeVisible();
    expect(screen.queryByText(/model.*ready/i)).not.toBeInTheDocument();
  });

  it("shows an already-authorised proposal without an authorise control", async () => {
    vi.spyOn(api, "getOps").mockResolvedValue(
      opsDto({ proposals: [{ ...proposal, state: "AUTHORISED", authorised_by: "Thandi Nkosi" }] }),
    );
    renderOps();
    expect(await screen.findByText("Authorised by Thandi Nkosi")).toBeVisible();
    expect(screen.queryByRole("button", { name: /review mission/i })).not.toBeInTheDocument();
  });
});
