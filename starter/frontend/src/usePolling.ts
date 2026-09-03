import { useEffect, useRef } from "react";

/**
 * Re-run `fn` on an interval, and immediately when the tab regains focus.
 *
 * Built because the verifier laptops fetched the verification queue once
 * on mount and never again: a speaker could record on the phone and the
 * two laptops would sit there showing "nobody is waiting" forever. In a
 * live demo that reads as the product being broken, when in fact the work
 * had arrived and nothing had asked for it.
 *
 * Polling rather than websockets on purpose. The demo runs on a phone
 * hotspot with three devices; a dropped socket needs reconnect logic that
 * would be one more thing to fail on stage, while a missed poll simply
 * retries a few seconds later.
 *
 * Two behaviours that matter on a real device:
 *   - the timer stops while the tab is hidden, so a backgrounded laptop
 *     is not burning battery and request quota
 *   - returning to the tab fires immediately, so picking a laptop back up
 *     shows current state without waiting out the interval
 */
export function usePolling(fn: () => void | Promise<void>, intervalMs: number, enabled = true) {
  const saved = useRef(fn);
  saved.current = fn;

  useEffect(() => {
    if (!enabled) return;
    let timer: ReturnType<typeof setInterval> | undefined;

    const run = () => void saved.current();

    const start = () => {
      stop();
      timer = setInterval(run, intervalMs);
    };
    const stop = () => {
      if (timer) clearInterval(timer);
      timer = undefined;
    };
    const onVisibility = () => {
      if (document.visibilityState === "visible") {
        run();
        start();
      } else {
        stop();
      }
    };

    if (document.visibilityState === "visible") start();
    document.addEventListener("visibilitychange", onVisibility);
    window.addEventListener("focus", run);
    return () => {
      stop();
      document.removeEventListener("visibilitychange", onVisibility);
      window.removeEventListener("focus", run);
    };
  }, [intervalMs, enabled]);
}
