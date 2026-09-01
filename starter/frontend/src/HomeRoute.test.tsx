import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { HomeRoute } from "./HomeRoute";

describe("HomeRoute API contract", () => {
  afterEach(() => vi.restoreAllMocks());

  it("reads backend health from the /api/health path", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(JSON.stringify({ status: "ok", provider_mode: "demo" }), { status: 200 }));

    render(<HomeRoute />);

    await waitFor(() => expect(screen.getByText("backend: ok (demo)")).toBeInTheDocument());
    expect(fetchMock).toHaveBeenCalledWith("/api/health");
  });
});
