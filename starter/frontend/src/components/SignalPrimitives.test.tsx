import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { PeerTruthStatus, StatusAnnouncer } from "./SignalPrimitives";

describe("StatusAnnouncer", () => {
  it("puts the status message in a polite live region", () => {
    render(<StatusAnnouncer message="Listen once, then choose." />);
    const region = screen.getByText("Listen once, then choose.");
    expect(region.getAttribute("aria-live")).toBe("polite");
    expect(region.getAttribute("aria-atomic")).toBe("true");
  });

  it("puts the error in an assertive live region with role=alert", () => {
    render(<StatusAnnouncer error="Something went wrong." />);
    const region = screen.getByText("Something went wrong.");
    expect(region.getAttribute("aria-live")).toBe("assertive");
    expect(region.getAttribute("role")).toBe("alert");
  });

  it("does not set role=alert on the error region when there is no error", () => {
    const { container } = render(<StatusAnnouncer message="ok" />);
    const assertiveRegion = container.querySelector('[aria-live="assertive"]');
    expect(assertiveRegion).not.toBeNull();
    expect(assertiveRegion?.getAttribute("role")).toBeNull();
  });

  it("renders both regions even when only one prop is supplied", () => {
    const { container } = render(<StatusAnnouncer message="ok" />);
    expect(container.querySelector('[aria-live="polite"]')).not.toBeNull();
    expect(container.querySelector('[aria-live="assertive"]')).not.toBeNull();
  });
});

describe("PeerTruthStatus", () => {
  it("announces the decision and verifier count in a status region", () => {
    render(<PeerTruthStatus decision="UNDERSTOOD" verifierCount={2} />);
    const region = screen.getByRole("status", { name: "Peer verification" });
    expect(region.textContent).toContain("UNDERSTOOD");
    expect(region.textContent).toContain("Confirmed by 2 proficient peers");
  });
});
