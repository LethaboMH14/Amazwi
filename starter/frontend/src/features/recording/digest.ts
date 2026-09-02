

/** Backend accepts 500..20000ms. Keep the clamp here so both the live
 *  recorder and the phone file-capture path obey the same bound. */
export const MIN_DURATION_MS = 500;
export const MAX_DURATION_MS = 20_000;

export function clampDuration(ms: number): number {
  if (!Number.isFinite(ms) || ms <= 0) return MIN_DURATION_MS;
  return Math.round(Math.min(MAX_DURATION_MS, Math.max(MIN_DURATION_MS, ms)));
}

/** Read a captured file's REAL duration instead of assuming one.
 *
 *  The phone path used to hardcode 1000ms for a recording of unknown
 *  length -- inside the valid range, so it never errored, it just
 *  stored a duration that was not true. Falls back to the clamp when
 *  the browser cannot decode metadata.
 */
export async function probeDurationMs(blob: Blob): Promise<number> {
  if (typeof Audio === "undefined" || typeof URL?.createObjectURL !== "function") {
    return MIN_DURATION_MS;
  }
  const url = URL.createObjectURL(blob);
  try {
    return await new Promise<number>((resolve) => {
      const audio = new Audio();
      const done = (ms: number) => resolve(clampDuration(ms));
      audio.preload = "metadata";
      audio.onloadedmetadata = () => done(audio.duration * 1000);
      audio.onerror = () => done(MIN_DURATION_MS);
      // Some browsers never fire either event for a partial blob.
      setTimeout(() => done(MIN_DURATION_MS), 3000);
      audio.src = url;
    });
  } finally {
    URL.revokeObjectURL(url);
  }
}
