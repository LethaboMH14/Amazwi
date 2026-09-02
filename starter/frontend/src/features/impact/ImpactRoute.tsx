/**
 * Impact Map route -- the aggregate Coverage Constellation.
 *
 * Order matters and is asserted by tests: the three real progress
 * metrics first (verified contributions, languages active, missions
 * completed), then the flat map, then the campaign gap cards. Nothing
 * here infers model readiness: when `model_gap_percent` is null the UI
 * says "Model evidence unavailable" rather than filling the gap.
 */
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, userMessage } from "../../api/client";
import type { Impact } from "../../api/contracts";
import { SouthAfricaCoverageMap, languageName } from "../../components/SouthAfricaCoverageMap";
import type { CoverageNode } from "../../components/SouthAfricaCoverageMap";

function prefersReducedMotion(): boolean {
  return typeof window !== "undefined" && typeof window.matchMedia === "function"
    ? window.matchMedia("(prefers-reduced-motion: reduce)").matches
    : false;
}

export function toCoverageNodes(impact: Impact): CoverageNode[] {
  return impact.nodes.map((node) => ({
    id: node.id,
    language: node.language,
    provinceCode: node.province_code,
    campaign: node.campaign,
    verifiedCountBand: node.verified_count_band,
    coveragePercent: node.coverage_percent,
    modelGapPercent: node.model_gap_percent,
  }));
}

export function ImpactRoute() {
  const [impact, setImpact] = useState<Impact>();
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .getImpact()
      .then(setImpact)
      .catch((err) => setError(userMessage(err)));
  }, []);

  return (
    <main className="route" aria-labelledby="impact-title">
      <p className="eyebrow">Coverage Constellation</p>
      <h1 id="impact-title">Where the language is coming from</h1>
      <p>
        Aggregate totals only. No contributor, clip or location is ever shown, and a cell appears only once at
        least five peer-verified contributions sit behind it.
      </p>

      {error && <p role="alert">{error}</p>}
      {!impact && !error && <p>Loading aggregate coverage…</p>}

      {impact && (
        <>
          <dl aria-label="Progress metrics" className="impact-metrics">
            <div>
              <dt>Verified contributions</dt>
              <dd>{impact.verified_total}</dd>
            </div>
            <div>
              <dt>Languages active</dt>
              <dd>{impact.languages_active}</dd>
            </div>
            <div>
              <dt>Missions completed</dt>
              <dd>{impact.missions_completed}</dd>
            </div>
          </dl>

          <SouthAfricaCoverageMap nodes={toCoverageNodes(impact)} reducedMotion={prefersReducedMotion()} />

          <section aria-label="Coverage gaps">
            <h2>Where the gaps are</h2>
            {impact.nodes.length === 0 ? (
              <p>
                Nothing to show yet
                {impact.suppressed_cell_count > 0
                  ? ` — ${impact.suppressed_cell_count} cell(s) are below the five-contribution privacy threshold.`
                  : "."}
              </p>
            ) : (
              <ul className="impact-gap-cards">
                {impact.nodes.map((node) => (
                  <li key={node.id} className="impact-gap-card">
                    <strong>
                      {languageName(node.language)} · {node.campaign}
                    </strong>
                    <span>{node.verified_count_band} verified contributions</span>
                    <span>{node.coverage_percent}% of all verified volume</span>
                    <span>
                      {node.model_gap_percent === null
                        ? "Model evidence unavailable"
                        : `${node.model_gap_percent}% model gap`}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </>
      )}

      <Link to="/">Back to AMAZWI</Link>
    </main>
  );
}
