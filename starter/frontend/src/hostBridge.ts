/**
 * Host bridge adapter — generic mini-app-shell integration.
 *
 * ⚠️ The wire protocol below (`MoMoWebViewEvent`, `START_JOURNEY`,
 * `IS_STILL_ACTIVE` every 45-50s) is transcribed from a COMMUNITY-AUTHORED
 * integration article, not a confirmed current organiser specification.
 * See ../../05_amazwi/research/B_MOMO_API.md and 05_amazwi/plan/02_TECH.md
 * ("Do not hard-code an unverified public-doc assumption as platform truth").
 *
 * This is why it's an adapter, not a hard dependency: `CommunityDocBridge`
 * is a labelled best-guess, swappable for whatever the mentors confirm on
 * day one without touching anything that calls `HostBridge`.
 */

export interface HostBridgeEvents {
  onStartJourney?: (info: { msisdn: string; token: string }) => void;
  onError?: (message: string) => void;
}

export interface HostBridge {
  readonly mode: string;
  start(events?: HostBridgeEvents): void;
  stop(): void;
  notify(event: string, payload?: Record<string, unknown>): void;
}

/**
 * Best-guess implementation of the community-documented protocol.
 * Sends a keep-alive every 45s (inside the reported 50s-recommended /
 * 60s-timeout window) so a long user interaction (reading a card,
 * recording) doesn't silently expire the host session.
 */
export class CommunityDocBridge implements HostBridge {
  readonly mode = "community-doc-unverified";
  private intervalId: ReturnType<typeof setInterval> | null = null;
  private listener: ((e: Event) => void) | null = null;
  private token: string | null = null;

  private post(message: Record<string, unknown>): void {
    const bridge = (window as unknown as { ReactNativeWebView?: { postMessage: (s: string) => void } })
      .ReactNativeWebView;
    if (bridge) {
      bridge.postMessage(JSON.stringify(message));
    } else {
      // eslint-disable-next-line no-console
      console.log("[hostBridge:community-doc] would send:", message);
    }
  }

  start(events: HostBridgeEvents = {}): void {
    this.listener = (e: Event) => {
      const detail = (e as CustomEvent<{ event: string; msisdn?: string }>).detail;
      if (!detail) return;
      if (detail.event === "START_JOURNEY") {
        this.token = (window as unknown as { micrositeToken?: string }).micrositeToken ?? null;
        if (detail.msisdn && this.token) {
          events.onStartJourney?.({ msisdn: detail.msisdn, token: this.token });
        }
        this.beginHeartbeat();
      }
    };
    window.addEventListener("MoMoWebViewEvent", this.listener);
  }

  private beginHeartbeat(): void {
    this.stopHeartbeat();
    this.intervalId = setInterval(() => {
      this.post({ event: "IS_STILL_ACTIVE", micrositeToken: this.token });
    }, 45_000);
  }

  private stopHeartbeat(): void {
    if (this.intervalId !== null) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  notify(event: string, payload: Record<string, unknown> = {}): void {
    this.post({ event, micrositeToken: this.token, ...payload });
    if (event === "DONE") this.stopHeartbeat();
  }

  stop(): void {
    this.stopHeartbeat();
    if (this.listener) {
      window.removeEventListener("MoMoWebViewEvent", this.listener);
      this.listener = null;
    }
  }
}

/** No-op bridge for local dev and any context with no host WebView. */
export class StandaloneBridge implements HostBridge {
  readonly mode = "standalone";
  start(_events?: HostBridgeEvents): void {
    // eslint-disable-next-line no-console
    console.log("[hostBridge:standalone] no host WebView detected — running unbridged");
  }
  stop(): void {}
  notify(_event: string, _payload?: Record<string, unknown>): void {}
}

/** Selects a bridge without the caller needing to know which one. */
export function createHostBridge(): HostBridge {
  const hasHost = typeof window !== "undefined" && "ReactNativeWebView" in window;
  return hasHost ? new CommunityDocBridge() : new StandaloneBridge();
}
