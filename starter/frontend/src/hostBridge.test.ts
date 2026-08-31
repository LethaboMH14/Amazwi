import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { CommunityDocBridge, StandaloneBridge, createHostBridge } from "./hostBridge";

describe("createHostBridge", () => {
  afterEach(() => {
    // @ts-expect-error test cleanup of a global we may have added
    delete window.ReactNativeWebView;
  });

  it("selects StandaloneBridge when no host WebView is present", () => {
    const bridge = createHostBridge();
    expect(bridge).toBeInstanceOf(StandaloneBridge);
    expect(bridge.mode).toBe("standalone");
  });

  it("selects CommunityDocBridge when a host WebView is present", () => {
    (window as unknown as { ReactNativeWebView: unknown }).ReactNativeWebView = {
      postMessage: vi.fn(),
    };
    const bridge = createHostBridge();
    expect(bridge).toBeInstanceOf(CommunityDocBridge);
  });
});

describe("CommunityDocBridge", () => {
  let postMessage: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    vi.useFakeTimers();
    postMessage = vi.fn();
    (window as unknown as { ReactNativeWebView: unknown }).ReactNativeWebView = { postMessage };
    (window as unknown as { micrositeToken?: string }).micrositeToken = "test-token";
  });

  afterEach(() => {
    vi.useRealTimers();
    // @ts-expect-error test cleanup
    delete window.ReactNativeWebView;
    // @ts-expect-error test cleanup
    delete window.micrositeToken;
  });

  it("calls onStartJourney with msisdn and token when START_JOURNEY fires", () => {
    const bridge = new CommunityDocBridge();
    const onStartJourney = vi.fn();
    bridge.start({ onStartJourney });

    window.dispatchEvent(
      new CustomEvent("MoMoWebViewEvent", { detail: { event: "START_JOURNEY", msisdn: "27821234567" } })
    );

    expect(onStartJourney).toHaveBeenCalledWith({ msisdn: "27821234567", token: "test-token" });
    bridge.stop();
  });

  it("sends IS_STILL_ACTIVE every 45s after the journey starts — the whole point of this file", () => {
    const bridge = new CommunityDocBridge();
    bridge.start();
    window.dispatchEvent(new CustomEvent("MoMoWebViewEvent", { detail: { event: "START_JOURNEY", msisdn: "x" } }));

    expect(postMessage).not.toHaveBeenCalled();
    vi.advanceTimersByTime(45_000);
    expect(postMessage).toHaveBeenCalledTimes(1);
    expect(JSON.parse(postMessage.mock.calls[0][0])).toMatchObject({ event: "IS_STILL_ACTIVE" });

    vi.advanceTimersByTime(45_000);
    expect(postMessage).toHaveBeenCalledTimes(2);
    bridge.stop();
  });

  it("stops the heartbeat on notify('DONE') so it doesn't fire after the round ends", () => {
    const bridge = new CommunityDocBridge();
    bridge.start();
    window.dispatchEvent(new CustomEvent("MoMoWebViewEvent", { detail: { event: "START_JOURNEY", msisdn: "x" } }));

    bridge.notify("DONE");
    postMessage.mockClear();
    vi.advanceTimersByTime(200_000);
    expect(postMessage).not.toHaveBeenCalled();
  });

  it("stop() removes the listener so a later START_JOURNEY does nothing", () => {
    const bridge = new CommunityDocBridge();
    const onStartJourney = vi.fn();
    bridge.start({ onStartJourney });
    bridge.stop();

    window.dispatchEvent(new CustomEvent("MoMoWebViewEvent", { detail: { event: "START_JOURNEY", msisdn: "x" } }));
    expect(onStartJourney).not.toHaveBeenCalled();
  });
});

describe("StandaloneBridge", () => {
  it("never throws when used exactly like the real bridge", () => {
    const bridge = new StandaloneBridge();
    expect(() => {
      bridge.start({ onStartJourney: vi.fn() });
      bridge.notify("IS_STILL_ACTIVE");
      bridge.stop();
    }).not.toThrow();
  });
});
