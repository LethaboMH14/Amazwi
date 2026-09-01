import { describe, expect, it, vi } from "vitest";
import { animateSignal } from "./signalMotion";

function elementWithAnimateSpy() {
  const element = document.createElement("div");
  const animate = vi.fn().mockReturnValue({ finished: Promise.resolve() });
  // jsdom does not implement the Web Animations API, so this test verifies
  // the *contract* animateSignal has with element.animate (called once, with
  // keyframes + a duration, never called at all when reduced=true) using a
  // spy, rather than depending on jsdom's incomplete WAAPI support.
  (element as unknown as { animate: typeof animate }).animate = animate;
  return { element, animate };
}

describe("animateSignal", () => {
  it("returns null and never calls element.animate when reduced motion is requested", () => {
    const { element, animate } = elementWithAnimateSpy();
    const result = animateSignal(element, "press", true);
    expect(result).toBeNull();
    expect(animate).not.toHaveBeenCalled();
  });

  it("calls element.animate with keyframes and a finite duration when motion is allowed", () => {
    const { element, animate } = elementWithAnimateSpy();
    animateSignal(element, "press", false);
    expect(animate).toHaveBeenCalledTimes(1);
    const [keyframes, options] = animate.mock.calls[0];
    expect(Array.isArray(keyframes)).toBe(true);
    expect((keyframes as unknown[]).length).toBeGreaterThan(0);
    expect(options.duration).toBeGreaterThan(0);
    expect(Number.isFinite(options.duration)).toBe(true);
  });

  it("defaults to reduced=false when the argument is omitted", () => {
    const { element, animate } = elementWithAnimateSpy();
    animateSignal(element, "press");
    expect(animate).toHaveBeenCalledTimes(1);
  });

  it.each([
    "press",
    "enter",
    "waveformFold",
    "peerConnect",
    "receiptRise",
    "mapRipple",
    "celebrate",
  ] as const)("every declared motion kind (%s) has a finite, positive duration", (kind) => {
    const { element, animate } = elementWithAnimateSpy();
    animateSignal(element, kind, false);
    const [, options] = animate.mock.calls[0];
    expect(options.duration).toBeGreaterThan(0);
    expect(Number.isFinite(options.duration)).toBe(true);
  });

  it("uses fill: 'both' so the animation's end state persists rather than snapping back", () => {
    const { element, animate } = elementWithAnimateSpy();
    animateSignal(element, "celebrate", false);
    const [, options] = animate.mock.calls[0];
    expect(options.fill).toBe("both");
  });
});
