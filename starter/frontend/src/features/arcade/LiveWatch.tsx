import { useCallback, useState } from "react";
import { useLocation } from "react-router-dom";
import { usePolling } from "../../usePolling";
import { api } from "../../api/client";
import type { InvitationRow } from "../../api/contracts";
import { LiveAlert } from "./LiveAlert";

/**
 * App-wide "someone just recorded" watch.
 *
 * LiveAlert used to be mounted only inside the dashboard, which made the
 * notification useless exactly when it mattered: a verifier waiting on
 * the /verify screen -- the single most likely place for them to be
 * sitting during a demo -- was never told that a recording had arrived.
 * They had to navigate back to the desk, or reload, to find out.
 *
 * Mounting it in the app shell means every screen gets the alert without
 * a reload, on whichever device the person happens to be holding.
 *
 * Two screens are deliberately excluded:
 *   /record  -- interrupting someone mid-recording with a toast is worse
 *               than telling them a few seconds later
 *   /verify  -- that screen already loads the clip itself, so an alert
 *               would announce work the person is already looking at
 */
export function LiveWatch() {
  const [invitations, setInvitations] = useState<InvitationRow[]>([]);
  const { pathname } = useLocation();
  const muted = pathname.startsWith("/record") || pathname.startsWith("/verify");

  const poll = useCallback(async () => {
    try {
      const data = await api.getArcade();
      setInvitations(data.invitations ?? []);
    } catch {
      /* offline or mid-restart -- ConnectionBadge reports it; retry next tick */
    }
  }, []);

  // 4s: fast enough that "record on the phone, watch the laptop" feels
  // immediate to a room, slow enough that three devices on a hotspot are
  // not hammering the backend.
  usePolling(poll, 4000, !muted);

  if (muted) return null;
  return <LiveAlert invitations={invitations} />;
}
