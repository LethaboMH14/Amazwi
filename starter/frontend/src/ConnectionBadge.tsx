import { useEffect, useState } from "react";
import "./connection.css";

/**
 * Says out loud whether this device can still reach the backend.
 *
 * Built after a demo session where three laptops showed "nothing" while
 * the API, the proxy and the database were all correct. The pages were
 * simply stale -- tabs left open across a dev-server restart, holding a
 * dead HMR socket and old code, with no way to tell from looking.
 *
 * A screen that is silently disconnected is indistinguishable from a
 * screen with no work to do, and during a demo those two states get
 * confused at exactly the wrong moment. This makes the difference
 * visible: green means the device polled the backend successfully within
 * the last few seconds, amber means it is trying, red means it cannot
 * reach the backend and the page should be reloaded.
 *
 * It polls /api/health, which is dual-registered on the backend and
 * needs no identity headers, so a red badge means the network path is
 * broken rather than that this device's credentials are wrong.
 */
type State = "connecting" | "live" | "offline";

export function ConnectionBadge({ intervalMs = 10000 }: { intervalMs?: number }) {
  const [state, setState] = useState<State>("connecting");
  const [checkedAt, setCheckedAt] = useState<Date | null>(null);

  useEffect(() => {
    let cancelled = false;
    let timer: ReturnType<typeof setInterval> | undefined;

    const ping = async () => {
      try {
        const res = await fetch("/api/health", { cache: "no-store" });
        if (cancelled) return;
        setState(res.ok ? "live" : "offline");
        setCheckedAt(new Date());
      } catch {
        if (!cancelled) {
          setState("offline");
          setCheckedAt(new Date());
        }
      }
    };

    void ping();
    timer = setInterval(ping, intervalMs);
    window.addEventListener("focus", ping);
    return () => {
      cancelled = true;
      if (timer) clearInterval(timer);
      window.removeEventListener("focus", ping);
    };
  }, [intervalMs]);

  const label =
    state === "live"
      ? `Connected${checkedAt ? ` · checked ${checkedAt.toLocaleTimeString()}` : ""}`
      : state === "connecting"
        ? "Connecting…"
        : "Cannot reach the backend — reload this page";

  return (
    <p className={`conn conn-${state}`} role="status" aria-live="polite">
      <span className="conn-dot" aria-hidden="true" />
      {state === "offline" ? (
        <>
          <b>Disconnected.</b> Reload this page.
        </>
      ) : (
        <span className="visually-hidden">{label}</span>
      )}
      {state !== "offline" && <span className="conn-text">{state === "live" ? "Live" : "Connecting…"}</span>}
    </p>
  );
}
