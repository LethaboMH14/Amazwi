import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import type { InvitationRow } from "../../api/contracts";
import "./livealert.css";

/**
 * "Someone just recorded" — the live cross-device moment.
 *
 * Every device polls the dashboard. This watches the invitation list for
 * an id it has NOT seen before and announces it. Watching ids rather than
 * a count matters: a count can stay the same while the work changes (one
 * answered, one arrived) and a count-based check would miss it silently.
 *
 * The very first poll is treated as a baseline, never as news. Otherwise
 * every laptop shouts about a queue that was already there when it
 * opened, which trains people to ignore the alert.
 *
 * `role="status"` and aria-live are on the container, which is always
 * mounted -- a live region inserted at the same moment as its text is
 * frequently not announced at all.
 */
export function LiveAlert({ invitations }: { invitations: InvitationRow[] }) {
  const seen = useRef<Set<string> | null>(null);
  const [fresh, setFresh] = useState<InvitationRow | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const ids = new Set(invitations.map((i) => i.assignment_id));
    if (seen.current === null) {
      seen.current = ids;   // first poll is the baseline, not news
      return;
    }
    const arrived = invitations.find((i) => !seen.current!.has(i.assignment_id));
    seen.current = ids;
    if (arrived) setFresh(arrived);
  }, [invitations]);

  useEffect(() => {
    if (!fresh) return;
    const t = setTimeout(() => setFresh(null), 12000);
    return () => clearTimeout(t);
  }, [fresh]);

  return (
    <div className="live-alert-region" role="status" aria-live="polite" aria-atomic="true">
      {fresh && (
        <div className="live-alert">
          <span className="live-alert-dot" aria-hidden="true" />
          <div className="live-alert-body">
            <b>{fresh.speaker_name} just recorded</b>
            <span>They need a listener. You have not heard it yet.</span>
          </div>
          <button
            type="button"
            className="live-alert-go"
            onClick={() =>
              navigate(
                `/verify?contributionId=${encodeURIComponent(fresh.contribution_id)}`,
              )
            }
          >
            Listen
          </button>
          <button
            type="button"
            className="live-alert-x"
            onClick={() => setFresh(null)}
            aria-label="Dismiss"
          >
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" aria-hidden="true">
              <path d="M6 6l12 12M18 6L6 18" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
}
