import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { ModeLabel, modeLabelFor } from "./ModeLabel";

describe("modeLabelFor", () => {
  it("labels the community-doc bridge as MoMo host mode, explicitly unverified", () => {
    const { text } = modeLabelFor("community-doc-unverified");
    expect(text).toContain("MoMo");
    expect(text.toLowerCase()).toContain("unverified");
  });

  it("labels the standalone bridge as browser demo mode, never as if it were the real host", () => {
    const { text } = modeLabelFor("standalone");
    expect(text).toContain("Browser demo mode");
  });

  it("never silently claims a live host for an unrecognised mode", () => {
    const { text } = modeLabelFor("something-new");
    expect(text).toContain("Unknown host mode");
    expect(text).not.toContain("MoMo");
  });
});

describe("ModeLabel component", () => {
  it("renders the honest label text visibly, not hidden", () => {
    render(<ModeLabel mode="standalone" />);
    expect(screen.getByRole("status")).toHaveTextContent("Browser demo mode");
  });
});
