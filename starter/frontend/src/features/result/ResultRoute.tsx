import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api, userMessage } from "../../api/client";
import { formatMinor } from "../../money";
import type { Result } from "../../api/contracts";

export function ResultRoute() {
  const { contributionId = "" } = useParams();
  const [result, setResult] = useState<Result>();
  const [error, setError] = useState("");
  useEffect(() => {
    if (!contributionId) return;
    let cancelled = false;
    api.getResult(contributionId)
      .then((r) => { if (!cancelled) { setResult(r); setError(""); } })
      .catch((e) => { if (!cancelled) setError(userMessage(e)); });
    return () => { cancelled = true; };
  }, [contributionId]);

  const paid = result ? result.reward_minor > 0 : false;

  return (
    <main className="route" aria-labelledby="result-title">
      <p className="eyebrow">Voice Value Receipt</p>
      <h1 id="result-title">Your contribution is in the ledger</h1>
      {result ? (
        <>
          <p className="receipt-outcome">{result.outcome}</p>
          {/* Minor units -> real money. This read "200 ZAR" for an R2.00
              reward until 2 Sep 2026 -- 100x the published rate, on the
              screen the whole pitch leans on to be financially honest. */}
          <p className="receipt-amount">{formatMinor(result.reward_minor, result.currency)}</p>
          {/* The receipt's actual job is explaining WHY, not just how much.
              The API has always returned this reason; the screen dropped it. */}
          {result.reason && <p className="receipt-reason">{result.reason}</p>}
          {!paid && (
            <p className="receipt-refusal">
              No reward was released for this contribution.
            </p>
          )}
        </>
      ) : (
        !error && <p>Loading your peer decision…</p>
      )}
      {error && <p role="alert">{error}</p>}
      <Link to="/">Back to AMAZWI</Link>
    </main>
  );
}
