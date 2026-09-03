import { afterEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AssistantWidget } from "./AssistantWidget";

describe("AssistantWidget", () => {
  afterEach(() => vi.restoreAllMocks());

  it("sends a message and renders the guarded navigation result", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(
        JSON.stringify({
          reply: "I can take you to /rewards.",
          intent: "NAVIGATE",
          route: "/rewards",
          provider: "deterministic",
          advisory: true,
        }),
        { status: 200 },
      ),
    );

    render(
      <MemoryRouter>
        <AssistantWidget />
      </MemoryRouter>,
    );

    await screen.getByRole("button", { name: /ask voice compass/i }).click();
    fireEvent.change(screen.getByRole("textbox", { name: /ask amazwi/i }), { target: { value: "take me to rewards" } });
    await screen.getByRole("button", { name: /send message/i }).click();

    await waitFor(() => expect(screen.getByText("I can take you to /rewards.")).toBeInTheDocument());
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/assistant",
      expect.objectContaining({ method: "POST" }),
    );
    expect(screen.getByRole("link", { name: /open rewards/i })).toHaveAttribute("href", "/rewards");
  });

  it("shows the safety boundary for payment requests", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(
        JSON.stringify({
          reply: "I cannot move money from chat.",
          intent: "PAYMENT_CONFIRMATION_REQUIRED",
          route: null,
          provider: "deterministic",
          advisory: true,
        }),
        { status: 200 },
      ),
    );

    render(
      <MemoryRouter>
        <AssistantWidget />
      </MemoryRouter>,
    );

    await screen.getByRole("button", { name: /ask voice compass/i }).click();
    fireEvent.change(screen.getByRole("textbox", { name: /ask amazwi/i }), { target: { value: "cash me out" } });
    await screen.getByRole("button", { name: /send message/i }).click();

    expect(await screen.findByText("I cannot move money from chat.")).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: /open/i })).not.toBeInTheDocument();
  });
});
