import type { HostBridge } from "./hostBridge";

/**
 * Gate A deliverable: an honest, always-visible label of which mode the
 * app is actually running in. Never silent about a substitution — matches
 * the failure-move language in 05_amazwi/plan/06_PITCH.md §12
 * ("Mini App host unavailable -> Label browser demo mode and show the
 * host adapter/spec separately").
 */
export function modeLabelFor(mode: HostBridge["mode"]): { text: string; tone: "live" | "demo" } {
  switch (mode) {
    case "community-doc-unverified":
      return { text: "Running inside MoMo — heartbeat protocol unverified by organisers", tone: "demo" };
    case "standalone":
      return { text: "Browser demo mode — no Mini App host detected", tone: "demo" };
    default:
      return { text: `Unknown host mode: ${mode}`, tone: "demo" };
  }
}

export function ModeLabel({ mode }: { mode: HostBridge["mode"] }) {
  const { text } = modeLabelFor(mode);
  return (
    <div
      role="status"
      className="label"
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 8,
        padding: "8px 14px",
        borderRadius: "var(--r-pill)",
        background: "var(--surface)",
        border: "1px solid var(--border)",
      }}
    >
      <span
        aria-hidden="true"
        style={{
          width: 7,
          height: 7,
          borderRadius: "999px",
          background: "var(--voice-1)",
          boxShadow: "0 0 8px 1.5px var(--voice-1)",
        }}
      />
      {text}
    </div>
  );
}
