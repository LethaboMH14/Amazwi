import { useEffect, useState } from "react";
import { createHostBridge, type HostBridge } from "./hostBridge";
import { ModeLabel } from "./ModeLabel";
import { Link } from "react-router-dom";
import { ThemeControl } from "./theme";

/**
 * Gate A shell. Exit condition (05_BUILD.md): "the same commit runs on both
 * laptops, deploys, resets and loads on the target phones." This is
 * deliberately not a real screen yet -- card reveal / recording / verifier
 * flow are Gate D/E, once real content, consent and recording exist.
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
      <ModeLabel mode={mode} />
      <ThemeControl />
      <h1 className="display" id="home-title" style={{ fontSize: "var(--fs-h1)" }}>
        AMAZWI
      </h1>
      <p style={{ color: "var(--text-dim)" }}>backend: {backendStatus}</p>
      <Link to="/consent">Contribute an isiZulu voice card</Link>
    </main>
  );
}
