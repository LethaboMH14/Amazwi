import { describe, expect, it, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { api } from "../../api/client";
import { ResultRoute } from "./ResultRoute";

function renderResult() {
  return render(
    <MemoryRouter initialEntries={["/result/demo-contribution"]}>
      <Routes>
        <Route path="/result/:contributionId" element={<ResultRoute />} />
      </Routes>
    </MemoryRouter>,
  );
}

describe("ResultRoute", () => {
  it("renders an accepted contribution in rand minor units and explains why", async () => {
    const getResult = vi.spyOn(api, "getResult").mockResolvedValue({
      contribution_id: "demo-contribution",
      outcome: "CORPUS_ELIGIBLE",
      reward_minor: 200,
      currency: "ZAR",
      provider_mode: "DEMO_PROVIDER",
      ledger_state: "CREDITED",
      settlement_state: "NOT_SUBMITTED",
      currency_disclosure_text: "Demo provider — not a real MoMo transfer or cash-out.",
      reason: "understood by both verifiers, audio quality passed, consent active",
    });

    renderResult();

    expect(await screen.findByText("CORPUS_ELIGIBLE")).toBeInTheDocument();
    expect(screen.getByText(/2[.,]00/)).toBeInTheDocument();
    expect(screen.getByText(/understood by both verifiers/i)).toBeInTheDocument();
    expect(screen.getByText(/Credited to your AMAZWI ledger/i)).toBeInTheDocument();
    expect(screen.getByText("DEMO_PROVIDER")).toBeInTheDocument();
    expect(screen.getByText(/not a real MoMo transfer or cash-out/i)).toBeInTheDocument();
    expect(screen.queryByText(/No reward was released/i)).not.toBeInTheDocument();
    await waitFor(() => expect(getResult).toHaveBeenCalledWith("demo-contribution"));
    getResult.mockRestore();
  });

  it("renders the refusal outcome, zero reward and explanation when verifiers disagree", async () => {
    const getResult = vi.spyOn(api, "getResult").mockResolvedValue({
      contribution_id: "demo-contribution",
      outcome: "UNVALIDATED",
      reward_minor: 0,
      currency: "ZAR",
      provider_mode: "DEMO_PROVIDER",
      ledger_state: "NOT_CREDITED",
      settlement_state: "NOT_SUBMITTED",
      currency_disclosure_text: "Demo provider — not a real MoMo transfer or cash-out.",
      reason: "not both verifier answers matched accepted_answers",
    });

    renderResult();

    expect(await screen.findByText("UNVALIDATED")).toBeInTheDocument();
    expect(screen.getByText(/0[.,]00/)).toBeInTheDocument();
    expect(screen.getByText(/not both verifier answers matched accepted_answers/i)).toBeInTheDocument();
    expect(screen.getByText(/No reward was released for this contribution/i)).toBeInTheDocument();
    expect(screen.getByText("DEMO_PROVIDER")).toBeInTheDocument();
    expect(screen.getByText(/not a real MoMo transfer or cash-out/i)).toBeInTheDocument();
    expect(screen.queryByText(/Credited to your AMAZWI ledger/i)).not.toBeInTheDocument();
    await waitFor(() => expect(getResult).toHaveBeenCalledWith("demo-contribution"));
    getResult.mockRestore();
  });
});
