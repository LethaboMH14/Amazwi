import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { HomeRoute } from "./HomeRoute";

describe("HomeRoute API contract", () => {
  afterEach(() => vi.restoreAllMocks());

  it("reads backend health from the /api/health path", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(JSON.stringify({ status: "ok", provider_mode: "demo" }), { status: 200 }));

    render(
      <MemoryRouter>
        <HomeRoute />
      </MemoryRouter>,
    );

    await waitFor(() => expect(screen.getByText("backend: ok (demo)")).toBeInTheDocument());
    expect(fetchMock).toHaveBeenCalledWith("/api/health");
  });

  it("does not present a demo-ledger credit as a MoMo settlement", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ status: "ok", provider_mode: "demo" }), { status: 200 }),
    );

    render(
      <MemoryRouter>
        <HomeRoute />
      </MemoryRouter>,
    );

    expect(await screen.findByText(/This demo credits your AMAZWI ledger/i)).toBeInTheDocument();
    expect(screen.queryByText(/credited through MoMo/i)).not.toBeInTheDocument();
  });
});
