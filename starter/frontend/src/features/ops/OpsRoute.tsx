/**
 * MTN Language Ops (Plan 03, Task 10).
 *
 * CROSS-LANE, PENDING SBU'S REVIEW -- money/authorisation territory.
 *
 * Nothing on this screen can launch a mission on its own. Authorising takes
 * two separate human actions (Review mission, then Authorise inside a modal
 * dialog), and the request carries no mission terms -- only the operator's
 * verbatim confirmation echo. The backend refuses any principal that is not
 * a persisted human MTN_LANGUAGE_OPS operator, so removing controls here is
 * a courtesy to the operator, never the security boundary.
 *
 * Honesty-in-copy: a readiness row whose backing data does not exist yet
 * says so in words. It never shows a number, and the model row is never
 * described as ready.
 */
import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError, userMessage } from "../../api/client";
import type { MissionProposal, OpsView } from "../../api/contracts";

const OPS_ROLE = "MTN_LANGUAGE_OPS";

export function formatRand(cents: number): string {
  return `R ${(cents / 100).toFixed(2)}`;
}

function newIdempotencyKey(): string {
  const suffix =
    typeof crypto !== "undefined" && "randomUUID" in crypto
      ? crypto.randomUUID()
      : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  return `ops-${suffix}`;
}

export function OpsRoute() {
  const [view, setView] = useState<OpsView>();
  const [reviewing, setReviewing] = useState<MissionProposal>();
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [accessDenied, setAccessDenied] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const dialogRef = useRef<HTMLDivElement>(null);

  const load = useCallback(async () => {
    try {
      setView(await api.getOps());
    } catch (err) {
      setError(userMessage(err));
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    if (reviewing) dialogRef.current?.focus();
  }, [reviewing]);

  const isOperator = !!view && view.roles.includes(OPS_ROLE) && !accessDenied;

  async function authorise(proposal: MissionProposal, confirmation: string) {
    setSubmitting(true);
    setError("");
    try {
      // One key per human click: a double-submit replays instead of
      // authorising twice.
      const updated = await api.authoriseMission(
        proposal.id,
        newIdempotencyKey(),
        confirmation,
      );
      setReviewing(undefined);
      setNotice(
        `Authorised by ${updated.authorised_by ?? view?.display_name ?? "this operator"}`,
      );
      await load();
    } catch (err) {
      setReviewing(undefined);
      if (err instanceof ApiError && err.status === 403) {
        // The server refused the principal. Remove every control rather
        // than leave a button that cannot work.
        setAccessDenied(true);
        setError("You do not have access to MTN Language Ops.");
      } else if (err instanceof ApiError && err.status === 409) {
        setError("This mission has already been decided. Showing its committed state.");
        await load();
      } else {
        setError(userMessage(err));
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="route ops-route" aria-labelledby="ops-title">
      <p className="eyebrow">MTN Language Ops</p>
      <h1 id="ops-title">Language coverage operations</h1>

      <div aria-live="polite" aria-atomic="true">
        {notice}
      </div>
      <div aria-live="assertive" aria-atomic="true">
        {error && <p role="alert">{error}</p>}
      </div>

      {!view && !error && <p>Loading operations data…</p>}

      {view && !isOperator && (
        <p>You do not have access to MTN Language Ops.</p>
      )}

      {view && isOperator && (
        <>
          <section aria-labelledby="ops-readiness-title">
            <h2 id="ops-readiness-title">Readiness</h2>
            <dl className="ops-readiness">
              {view.readiness.map((row) => (
                <div key={row.label} className="ops-readiness-row">
                  <dt>{row.label}</dt>
                  <dd>
                    {/* No backing data source yet -- say so, never show a
                        placeholder number dressed up as a measurement. */}
                    {row.available ? row.value : "Model evidence unavailable"}
                    <small> {row.detail}</small>
                  </dd>
                </div>
              ))}
            </dl>
          </section>

          <section aria-labelledby="ops-gaps-title">
            <h2 id="ops-gaps-title">Aggregate coverage</h2>
            {view.gaps.length === 0 ? (
              <p>No peer-verified contributions recorded yet.</p>
            ) : (
              <ul aria-label="Aggregate coverage by language">
                {view.gaps.map((gap) => (
                  <li key={gap.language}>
                    {gap.language}: {gap.verified_contributions} verified contributions
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section aria-labelledby="ops-missions-title">
            <h2 id="ops-missions-title">Mission proposals</h2>
            {view.proposals.length === 0 && <p>No mission proposals are open.</p>}
            <ul aria-label="Mission proposals">
              {view.proposals.map((proposal) => (
                <li key={proposal.id} className="ops-proposal">
                  <h3>
                    {proposal.language} · {proposal.province_code} · {proposal.domain}
                  </h3>
                  <p>{proposal.rationale}</p>
                  <ul>
                    <li>Target: {proposal.target_verified_clips} verified clips</li>
                    <li>{formatRand(proposal.fixed_reward_cents)} fixed reward</li>
                    <li>Budget: {formatRand(proposal.budget_cents)}</li>
                    <li>Status: {proposal.state}</li>
                  </ul>
                  {proposal.state === "AUTHORISED" ? (
                    <p>Authorised by {proposal.authorised_by ?? "an operator"}</p>
                  ) : (
                    <button
                      type="button"
                      onClick={() => {
                        setNotice("");
                        setError("");
                        setReviewing(proposal);
                      }}
                    >
                      Review mission
                    </button>
                  )}
                </li>
              ))}
            </ul>
          </section>

          {reviewing && (
            <div
              role="dialog"
              aria-modal="true"
              aria-labelledby="ops-dialog-title"
              className="ops-dialog"
              ref={dialogRef}
              tabIndex={-1}
            >
              <h2 id="ops-dialog-title">Authorise mission</h2>
              <p>
                {reviewing.language} · {reviewing.province_code} · {reviewing.domain}
              </p>
              <p>
                {formatRand(reviewing.fixed_reward_cents)} fixed reward ·{" "}
                {reviewing.target_verified_clips} verified clips · budget{" "}
                {formatRand(reviewing.budget_cents)}
              </p>
              <p>{view.confirmation_text}</p>
              <p>
                Authorising records your decision. It does not release funds on
                its own — payment remains a separate, reviewed step.
              </p>
              <button
                type="button"
                disabled={submitting}
                onClick={() => void authorise(reviewing, view.confirmation_text)}
              >
                {submitting ? "Authorising…" : "Authorise"}
              </button>
              <button
                type="button"
                disabled={submitting}
                onClick={() => setReviewing(undefined)}
              >
                Cancel
              </button>
            </div>
          )}
        </>
      )}
    </main>
  );
}
