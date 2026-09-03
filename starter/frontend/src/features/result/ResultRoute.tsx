import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api, userMessage } from "../../api/client";
import { formatMinor } from "../../money";
import type { Result } from "../../api/contracts";
import { StatusAnnouncer } from "../../components/SignalPrimitives";
import { Mascot } from "../arcade/Mascot";
import "../flow.css";

export function ResultRoute() {
  const { contributionId = "" } = useParams();
  const navigate = useNavigate();
  const [result, setResult] = useState<Result>();
  const [error, setError] = useState("");
  const [status, setStatus] = useState("Waiting on your two listeners…");

  useEffect(() => {
    if (!contributionId) return;
    let cancelled = false;
    api
      .getResult(contributionId)
      .then((r) => {
        if (cancelled) return;
        setResult(r);
        setError("");
        setStatus("");
      })
      .catch((e) => {
        if (cancelled) return;
        setError(userMessage(e));
        setStatus("");
      });
    return () => {
      cancelled = true;
    };
  }, [contributionId]);

  const understood = result?.understood === true;
  const resolved = result?.status === "RESOLVED";
  const hasReward = result ? result.reward_minor > 0 : false;

  return (
    <main className="flow" aria-labelledby="result-title">
      <button type="button" className="flow-back" onClick={() => navigate("/dashboard")}>
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M15 5l-7 7 7 7" />
        </svg>
        My desk
      </button>

      <div className="flow-head">
        <p className="eyebrow">Voice value receipt</p>
        <h1 id="result-title">
          {!resolved
            ? "Sent — two people are listening"
            : understood
              ? "Both listeners understood you"
              : "They heard it differently"}
        </h1>
      </div>

      {result && (
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Mascot
            size={128}
            mood={!resolved ? "listening" : understood ? "understood" : "missed"}
          />
        </div>
      )}

      {error && <p className="flow-error" role="alert">{error}</p>}
      {!result && !error && <p className="rec-hint">{status}</p>}

      {result && (
        <>
          {/* Peer truth is the product, so the outcome is stated as the
              two people's decision -- not as a score the system awarded. */}
          <section className="flow-card" aria-label="The decision">
            <p className="eyebrow">Outcome</p>
            <p style={{ fontSize: 19, fontWeight: 800, margin: "6px 0 0" }}>
              {resolved
                ? understood
                  ? "Understood by both"
                  : "Not both listeners agreed"
                : "Awaiting two answers"}
            </p>
            {result.reason && (
              <p className="reason-note" style={{ marginTop: 12 }}>
                <b>Why:</b> {result.reason}
              </p>
            )}
          </section>

          <section className="receipt-money" aria-label="Reward">
            <p className="eyebrow">{hasReward ? "Credited to you" : "Nothing was released"}</p>
            {/* Minor units -> real money. This read "200 ZAR" for an R2.00
                reward until 2 Sep 2026 -- 100x the published rate, on the
                screen the whole pitch leans on to be financially honest. */}
            <p className="receipt-amount money">
              {formatMinor(result.reward_minor, result.currency)}
            </p>
            {/* The exact wording here is load-bearing and is asserted by
                tests. "Credited to your AMAZWI ledger" names WHERE the money
                is -- vaguer copy would let a reader assume a MoMo wallet --
                and the refusal states plainly that nothing was released
                rather than leaving a zero to be interpreted. */}
            <p className="receipt-disclosure">
              {hasReward ? (
                <>Credited to your AMAZWI ledger.</>
              ) : (
                <>
                  No reward was released for this contribution. When two
                  people do not agree, nobody is paid &mdash; that refusal is
                  what protects the corpus and the campaign budget.
                </>
              )}
            </p>
            {/* Provider mode is disclosed on EVERY receipt, paid or refused.
                A reader must never have to infer which provider settled (or
                did not settle) a contribution from whether money moved. */}
            <p className="receipt-disclosure">
              <strong>{result.provider_mode ?? "UNVERIFIED_PROVIDER"}</strong>
              {result.currency_disclosure_text
                ? ` · ${result.currency_disclosure_text}`
                : " · Provider settlement is unverified."}
            </p>
          </section>

          <section className="flow-card" aria-label="Receipt detail">
            <dl className="detail-rows">
              {/* The raw resolver outcome, kept verbatim. The headline above
                  says it in plain words, but the exact enum stays on the
                  receipt so the screen is auditable against the database
                  row -- a receipt a judge cannot check is just a slide. */}
              <div className="detail-row">
                <dt>Resolver outcome</dt>
                <dd>{result.outcome}</dd>
              </div>
              <div className="detail-row">
                <dt>Ledger</dt>
                <dd>{result.ledger_state ?? "—"}</dd>
              </div>
              <div className="detail-row">
                <dt>Settlement</dt>
                <dd>{result.settlement_state ?? "NOT_SUBMITTED"}</dd>
              </div>
              <div className="detail-row">
                <dt>Corpus</dt>
                <dd>{result.corpus_eligible ? "Eligible" : "Not eligible"}</dd>
              </div>
            </dl>
          </section>
        </>
      )}

      <div className="flow-actions">
        <button
          type="button"
          className="flow-btn flow-btn-go"
          onClick={() => navigate("/consent")}
        >
          Record another card
        </button>
        <button
          type="button"
          className="flow-btn flow-btn-quiet"
          onClick={() => navigate("/dashboard")}
        >
          Back to my desk
        </button>
      </div>

      <StatusAnnouncer message={status} error={error} />
    </main>
  );
}
