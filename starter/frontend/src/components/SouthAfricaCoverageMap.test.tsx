import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import {
  PROVINCE_CENTROIDS,
  SouthAfricaCoverageMap,
  nodeLabel,
  pinRadius,
} from "./SouthAfricaCoverageMap";
import type { CoverageNode } from "./SouthAfricaCoverageMap";

function node(overrides: Partial<CoverageNode> = {}): CoverageNode {
  return {
    id: "tn:NW:support",
    language: "tn",
    provinceCode: "NW",
    campaign: "support",
    verifiedCountBand: "5-19",
    coveragePercent: 40,
    modelGapPercent: null,
    ...overrides,
  };
}

describe("SouthAfricaCoverageMap", () => {
  afterEach(() => vi.restoreAllMocks());

  it("renders a flat aggregate map with an equivalent accessible list", () => {
    render(<SouthAfricaCoverageMap nodes={[node()]} reducedMotion={false} />);
    expect(screen.getByRole("img", { name: /south africa language coverage/i })).toBeVisible();
    expect(screen.getByRole("list", { name: /coverage details/i })).toHaveTextContent(
      "Setswana, North West, support, 5-19 verified contributions",
    );
  });

  it("is flat, not a 3D or canvas render", () => {
    const { container } = render(<SouthAfricaCoverageMap nodes={[node()]} reducedMotion={false} />);
    expect(container.querySelector("canvas")).toBeNull();
    expect(container.querySelector("[data-render-style='3d']")).toBeNull();
    expect(container.querySelector("svg")?.getAttribute("data-render-style")).toBe("flat");
  });

  it("sizes pins by count band only", () => {
    expect(pinRadius("5-19")).toBe(6);
    expect(pinRadius("20-49")).toBe(8);
    expect(pinRadius("50-99")).toBe(10);
    expect(pinRadius("100+")).toBe(12);
  });

  it("places each pin at the fixed coarse province centroid", () => {
    const { container } = render(
      <SouthAfricaCoverageMap nodes={[node({ verifiedCountBand: "100+" })]} reducedMotion={false} />,
    );
    const pin = container.querySelector("[data-testid='pin-tn:NW:support']");
    expect(pin?.getAttribute("cx")).toBe(String(PROVINCE_CENTROIDS.NW.x));
    expect(pin?.getAttribute("cy")).toBe(String(PROVINCE_CENTROIDS.NW.y));
    expect(pin?.getAttribute("r")).toBe("12");
  });

  it("never renders an exact count, identifier, coordinate or audio field", () => {
    const { container } = render(
      <SouthAfricaCoverageMap nodes={[node({ coveragePercent: 40 })]} reducedMotion={false} />,
    );
    const markup = container.innerHTML;
    for (const forbidden of ["latitude", "longitude", "audio", "transcript", "user_id", "contribution_id"]) {
      expect(markup).not.toContain(forbidden);
    }
  });

  it("shows national totals honestly when no province data exists", () => {
    render(<SouthAfricaCoverageMap nodes={[node({ provinceCode: null, id: "tn:NATIONAL:support" })]} reducedMotion={false} />);
    expect(screen.getByRole("note")).toHaveTextContent(/province-level coverage is not collected yet/i);
    expect(screen.getByRole("list", { name: /coverage details/i })).toHaveTextContent(
      "Setswana, National, support, 5-19 verified contributions",
    );
    expect(document.querySelector("[data-testid^='pin-']")).toBeNull();
  });

  it("says model evidence is unavailable rather than inferring readiness", () => {
    render(<SouthAfricaCoverageMap nodes={[node()]} reducedMotion={false} />);
    expect(screen.getByRole("list", { name: /coverage details/i })).toHaveTextContent(
      "Model evidence unavailable",
    );
  });

  it("runs one ripple on update, and none under reduced motion", () => {
    const animate = vi.fn().mockReturnValue({});
    // jsdom has no Web Animations API; spy on the contract instead.
    Object.defineProperty(SVGElement.prototype, "animate", { value: animate, configurable: true, writable: true });

    const { unmount } = render(<SouthAfricaCoverageMap nodes={[node()]} reducedMotion={false} />);
    expect(animate).toHaveBeenCalledTimes(1);
    expect(animate.mock.calls[0][1]).toMatchObject({ duration: 500 });
    unmount();

    animate.mockClear();
    render(<SouthAfricaCoverageMap nodes={[node()]} reducedMotion={true} />);
    expect(animate).not.toHaveBeenCalled();
  });

  it("renders an explicit empty state that explains suppression", () => {
    render(<SouthAfricaCoverageMap nodes={[]} reducedMotion={true} />);
    expect(screen.getByRole("list", { name: /coverage details/i })).toHaveTextContent(
      /fewer than five verified contributions are never shown/i,
    );
  });

  it("labels a node with aggregate facts only", () => {
    expect(nodeLabel(node({ language: "zu", provinceCode: "KZN", campaign: "code switch", verifiedCountBand: "20-49" }))).toBe(
      "isiZulu, KwaZulu-Natal, code switch, 20-49 verified contributions",
    );
  });
});
