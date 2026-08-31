import { useEffect, useState } from "react";
import { createHostBridge, type HostBridge } from "./hostBridge";
import { ModeLabel } from "./ModeLabel";

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
    <main
      style={{
        minHeight: "100vh",
        boxSizing: "border-box",
        padding: "var(--sp-5)",
        display: "flex",
        flexDirection: "column",
        gap: "var(--sp-4)",
      }}
    >
      <ModeLabel mode={mode} />
      <h1 className="display" style={{ fontSize: "var(--fs-h1)" }}>
        AMAZWI
      </h1>
      <p style={{ color: "var(--text-dim)" }}>backend: {backendStatus}</p>
    </main>
  );
}
