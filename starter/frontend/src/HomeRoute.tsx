import { useEffect, useState } from "react";
import { createHostBridge, type HostBridge } from "./hostBridge";
import { ModeLabel } from "./ModeLabel";
import { Link } from "react-router-dom";
import { ThemeControl } from "./theme";

/**
 * Home. Built to the v2 visual grammar in 04_assets/mockups_v2/README.md:
 * kicker against display type for scale contrast, Instrument Serif italic
 * as the editorial accent, the overlapping-listeners signature device
 * (two people agreeing IS the mechanic, so the mark is literal), a hairline
 * meta strip rather than a heavy card, and an asymmetric circle+type CTA
 * rather than a full-width slab.
 *
 * The Gate A evidence -- host mode, backend health, theme switch -- is real
 * and stays visible, but it belongs in the footer as diagnostic chrome. It
 * is not the product.
 */
export function HomeRoute() {
  const [backendStatus, setBackendStatus] = useState("checking...");
  const [mode, setMode] = useState<HostBridge["mode"]>("standalone");

  useEffect(() => {
    let cancelled = false;
    fetch("/api/health")
      .then((r) => r.json())
      .then((d) => {
        if (!cancelled) setBackendStatus(`${d.status} (${d.provider_mode})`);
      })
      .catch(() => {
        if (!cancelled) setBackendStatus("backend unreachable");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    const bridge = createHostBridge();
    setMode(bridge.mode);
    bridge.start();
    return () => bridge.stop();
  }, []);

  return (
    // `.route` carries the shared 320–480px / 200%-zoom / 44px-target
    // rules from signal-flow.css. The landmark is labelled by its own
    // <h1>: the Task 11 gate asserts every route's <main> is named, and
    // this one was the single route that failed that check.
    <main className="route" aria-labelledby="home-title">
      <p className="eyebrow">Today&rsquo;s voice mission</p>

      <h1 id="home-title">AMAZWI</h1>

      <p className="serif">speak. be understood. earn.</p>

      {/* One raised object rather than four flat siblings -- see the
          .mission-card comment in signal-flow.css for why. */}
      <section className="mission-card" aria-label="Today's mission">
        {/* Decorative: the two initials carry no information a screen-reader
            user needs, and the sentence below states the same thing in words. */}
        <div className="agreement-lens" aria-hidden="true">
          <span className="listener">N</span>
          <span className="listener">T</span>
        </div>

        <p className="serif" style={{ textAlign: "center" }}>
          two people are waiting to hear you
        </p>

        <div className="mission-terms">
          <span>30 seconds &middot; 2 listeners</span>
          <span>
            <span className="money">R2.00</span> when both understand you
          </span>
        </div>
      </section>

      <Link to="/consent" className="cta">
        <span className="cta-dial" aria-hidden="true">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#14060C" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 15a3.5 3.5 0 0 0 3.5-3.5v-5a3.5 3.5 0 0 0-7 0v5A3.5 3.5 0 0 0 12 15z" />
            <path d="M5.5 11.5a6.5 6.5 0 0 0 13 0" />
            <path d="M12 18.5V22" />
          </svg>
        </span>
        <span className="cta-copy">
          <strong>Start speaking</strong>
          <span className="serif">contribute an isiZulu voice card</span>
        </span>
      </Link>

      <div className="how-it-works">
        <p className="eyebrow">How it works</p>
        <ol>
          <li>
            <span className="step-index" aria-hidden="true">01</span>
            <span>
              <b>You speak.</b> Describe the word without saying it, in 30 seconds.
            </span>
          </li>
          <li>
            <span className="step-index" aria-hidden="true">02</span>
            <span>
              <b>Two people listen.</b> They each type what they understood, independently.
            </span>
          </li>
          <li>
            <span className="step-index" aria-hidden="true">03</span>
            <span>
              <b>Both agree, you earn.</b> Your reward is credited through MoMo.
            </span>
          </li>
        </ol>
      </div>

      <div className="route-footer">
        <ModeLabel mode={mode} />
        <ThemeControl />
        <span>backend: {backendStatus}</span>
      </div>
    </main>
  );
}
