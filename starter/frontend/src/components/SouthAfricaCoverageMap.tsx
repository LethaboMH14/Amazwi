/**
 * Flat, honest South Africa Coverage Constellation.
 *
 * Two constraints are non-negotiable here and are enforced by tests:
 *  1. FLAT. One 2D SVG outline. No canvas, no WebGL, no 3D/fantasy
 *     render, no pseudo-terrain. Pins are sized by count band only.
 *  2. AGGREGATE-ONLY. Nothing rendered is ever a person or a place a
 *     person was. Province centroids are coarse visual layout for cells
 *     the backend has already published; they are not user locations.
 *
 * The backend cannot yet produce province-level cells (no geographic
 * column exists -- see starter/backend/app/impact.py). Nodes therefore
 * arrive with `provinceCode === null`, and this component renders the
 * outline with an explicit national-totals state instead of scattering
 * invented pins. The province pin path is real and tested so that it
 * works unchanged the day consented province data exists.
 */
import { useEffect, useRef } from "react";
import { animateSignal } from "../signalMotion";

export type CountBand = "5-19" | "20-49" | "50-99" | "100+";

export interface CoverageNode {
  id: string;
  language: string;
  provinceCode: string | null;
  campaign: string;
  verifiedCountBand: CountBand;
  coveragePercent: number;
  modelGapPercent: number | null;
}

/** Coarse visual layout only -- never a user location. */
export const PROVINCE_CENTROIDS: Record<string, { x: number; y: number; name: string }> = {
  EC: { x: 232, y: 226, name: "Eastern Cape" },
  FS: { x: 178, y: 174, name: "Free State" },
  GP: { x: 202, y: 115, name: "Gauteng" },
  KZN: { x: 246, y: 174, name: "KwaZulu-Natal" },
  LP: { x: 205, y: 62, name: "Limpopo" },
  MP: { x: 248, y: 111, name: "Mpumalanga" },
  NC: { x: 102, y: 154, name: "Northern Cape" },
  NW: { x: 159, y: 111, name: "North West" },
  WC: { x: 80, y: 235, name: "Western Cape" },
};

const BAND_RADIUS: Record<CountBand, number> = {
  "5-19": 6,
  "20-49": 8,
  "50-99": 10,
  "100+": 12,
};

const LANGUAGE_NAMES: Record<string, string> = { zu: "isiZulu", tn: "Setswana" };

export function languageName(code: string): string {
  return LANGUAGE_NAMES[code] ?? code;
}

/** Simplified flat South Africa outline, viewBox 0 0 320 300. */
const SA_OUTLINE =
  "M60 168 L74 132 L96 104 L124 86 L150 74 L172 56 L190 40 L214 36 L238 48 L262 62 " +
  "L276 84 L282 112 L272 138 L262 160 L268 186 L258 212 L236 240 L206 258 L172 264 " +
  "L138 258 L108 244 L84 222 L66 196 Z";

/** Lesotho, drawn as a hole so the outline is honest rather than tidy. */
const LESOTHO = "M222 178 L238 172 L246 184 L238 196 L224 194 Z";

export function pinRadius(band: CountBand): number {
  return BAND_RADIUS[band];
}

export function nodeLabel(node: CoverageNode): string {
  const place = node.provinceCode ? PROVINCE_CENTROIDS[node.provinceCode]?.name ?? node.provinceCode : "National";
  return `${languageName(node.language)}, ${place}, ${node.campaign}, ${node.verifiedCountBand} verified contributions`;
}

export function SouthAfricaCoverageMap({
  nodes,
  reducedMotion,
}: {
  nodes: CoverageNode[];
  reducedMotion: boolean;
}) {
  const rippleRef = useRef<SVGGElement | null>(null);
  const signature = nodes.map((node) => `${node.id}:${node.verifiedCountBand}`).join("|");

  useEffect(() => {
    if (reducedMotion || !rippleRef.current || nodes.length === 0) return;
    // Not every environment implements the Web Animations API (jsdom
    // does not, and neither do some older mobile browsers). The map is
    // fully usable without the ripple, so skip rather than throw.
    if (typeof (rippleRef.current as unknown as { animate?: unknown }).animate !== "function") return;
    // animateSignal is typed for HTMLElement; SVGGElement carries the
    // same .animate() contract, so this cast is a type bridge only.
    animateSignal(rippleRef.current as unknown as HTMLElement, "mapRipple", reducedMotion);
  }, [signature, reducedMotion, nodes.length]);

  const placed = nodes.filter((node) => node.provinceCode && PROVINCE_CENTROIDS[node.provinceCode]);
  const unplaced = nodes.length - placed.length;

  return (
    <div className="coverage-constellation">
      <svg
        viewBox="0 0 320 300"
        role="img"
        aria-label="South Africa language coverage, flat aggregate map"
        className="coverage-map-svg"
        data-render-style="flat"
      >
        <path d={SA_OUTLINE} className="coverage-map-outline" />
        <path d={LESOTHO} className="coverage-map-hole" />
        <g ref={rippleRef}>
          {placed.map((node) => {
            const centroid = PROVINCE_CENTROIDS[node.provinceCode as string];
            return (
              <circle
                key={node.id}
                cx={centroid.x}
                cy={centroid.y}
                r={pinRadius(node.verifiedCountBand)}
                className={`coverage-pin coverage-pin-${node.verifiedCountBand.replace("+", "plus")}`}
                data-testid={`pin-${node.id}`}
              >
                <title>{nodeLabel(node)}</title>
              </circle>
            );
          })}
        </g>
        {Object.entries(PROVINCE_CENTROIDS).map(([code, centroid]) => (
          <text key={code} x={centroid.x} y={centroid.y - 14} className="coverage-province-label">
            {code}
          </text>
        ))}
      </svg>

      {unplaced > 0 && (
        <p className="coverage-note" role="note">
          Province-level coverage is not collected yet. Showing national totals by language and campaign — no
          contributor location is stored or shown.
        </p>
      )}

      <ul aria-label="Coverage details" className="coverage-list">
        {nodes.length === 0 ? (
          <li>No coverage published yet. Cells with fewer than five verified contributions are never shown.</li>
        ) : (
          nodes.map((node) => (
            <li key={node.id}>
              {nodeLabel(node)}
              {node.modelGapPercent === null ? " · Model evidence unavailable" : ` · ${node.modelGapPercent}% model gap`}
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
