import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError, api, codecFor, userMessage } from "./client";

function mockFetchOnce(response: { ok: boolean; status: number; json?: () => Promise<unknown>; jsonRejects?: boolean }) {
  const jsonImpl = response.jsonRejects
    ? vi.fn().mockRejectedValue(new Error("not json"))
    : vi.fn().mockResolvedValue((response.json ?? (() => Promise.resolve({})))());
  const fetchMock = vi.fn().mockResolvedValue({
    ok: response.ok,
    status: response.status,
    json: jsonImpl,
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

describe("api client request()", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("returns the parsed JSON body on a 200 response", async () => {
    mockFetchOnce({ ok: true, status: 200, json: () => Promise.resolve({ id: "c1" }) });
    const result = await api.getResult("c1");
    expect(result).toEqual({ id: "c1" });
  });

  it("returns undefined on a 204 response without attempting to parse a body", async () => {
    mockFetchOnce({ ok: true, status: 204 });
    const result = await api.submitAnswer("assignment-1", "sefofane");
    expect(result).toBeUndefined();
  });

  it("does not call response.json() at all for a 204 response", async () => {
    const jsonSpy = vi.fn();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, status: 204, json: jsonSpy }),
    );
    await api.submitAnswer("assignment-1", "sefofane");
    // 204 must short-circuit before parsing an empty body -- calling .json()
    // on a real 204 response throws, so this guards against a real bug, not
    // just a style preference.
    expect(jsonSpy).not.toHaveBeenCalled();
  });

  // This is the REAL shape the backend produces -- verified against the live
  // API: `{"detail":{"code":"CARD_NOT_FOUND"}}`. An earlier version of this
  // test asserted a flat {code, detail} body that the backend never emits,
  // so it passed while the client mis-parsed every real error and rendered
  // "[object Object]" to the user on the verifier screen.
  it("raises ApiError from FastAPI's nested {detail:{code}} error body", async () => {
    mockFetchOnce({
      ok: false,
      status: 409,
      json: () => Promise.resolve({ detail: { code: "ALREADY_RESOLVED", message: "This round is already closed." } }),
    });
    await expect(api.getResult("c1")).rejects.toMatchObject({
      status: 409,
      code: "ALREADY_RESOLVED",
      message: "This round is already closed.",
    });
  });

  it("uses the code as the message when the nested detail carries no message", async () => {
    mockFetchOnce({ ok: false, status: 404, json: () => Promise.resolve({ detail: { code: "CARD_NOT_FOUND" } }) });
    await expect(api.getResult("c1")).rejects.toMatchObject({ status: 404, code: "CARD_NOT_FOUND", message: "CARD_NOT_FOUND" });
  });

  it("never surfaces a raw object as the message", async () => {
    mockFetchOnce({ ok: false, status: 403, json: () => Promise.resolve({ detail: { code: "AUDIO_NOT_AUTHORISED" } }) });
    expect.assertions(1);
    try {
      await api.getResult("c1");
    } catch (e) {
      expect(String((e as Error).message)).not.toContain("[object Object]");
    }
  });

  it("still handles a plain-string detail body", async () => {
    mockFetchOnce({ ok: false, status: 400, json: () => Promise.resolve({ detail: "Bad request." }) });
    await expect(api.getResult("c1")).rejects.toMatchObject({ status: 400, code: "HTTP_ERROR", message: "Bad request." });
  });

  it("falls back to HTTP_ERROR and a generic message when the error body is not JSON", async () => {
    mockFetchOnce({ ok: false, status: 500, jsonRejects: true });
    await expect(api.getResult("c1")).rejects.toMatchObject({
      status: 500,
      code: "HTTP_ERROR",
      message: "Request failed. Please try again.",
    });
  });

  it("sends the request path prefixed with /api", async () => {
    const fetchMock = mockFetchOnce({ ok: true, status: 200, json: () => Promise.resolve({}) });
    await api.getResult("c1");
    expect(fetchMock).toHaveBeenCalledWith("/api/contributions/c1/result", expect.anything());
  });
});

describe("userMessage", () => {
  it("maps a 401 ApiError to a sign-in prompt", () => {
    expect(userMessage(new ApiError(401, "UNAUTHORIZED", "nope"))).toBe("Sign in to MoMo to continue.");
  });

  it("maps a 409 ApiError to a round-unavailable message, regardless of server detail text", () => {
    expect(userMessage(new ApiError(409, "CONFLICT", "some raw server detail"))).toBe(
      "This action is not available for the current round.",
    );
  });

  it("uses the ApiError's own message for other statuses", () => {
    expect(userMessage(new ApiError(500, "HTTP_ERROR", "server exploded"))).toBe("server exploded");
  });

  it("uses a generic Error's message when it is not an ApiError", () => {
    expect(userMessage(new Error("network down"))).toBe("network down");
  });

  it("falls back to a generic message for a non-Error thrown value", () => {
    expect(userMessage("some string")).toBe("Something went wrong. Please try again.");
  });
});

describe("finaliseAudio duration — regression for the stranded-upload bug", () => {
  // This is the test that was missing. duration_ms was hardcoded to 0
  // in the request body while the recorder computed the real value and
  // discarded it. The backend rejects anything outside 500..20000ms, so
  // EVERY finalise failed with AUDIO_DURATION_INVALID and every upload
  // was left as an orphaned .pending file no verifier could ever play.
  it("sends the real recorded duration, never a hardcoded zero", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ audio_object_id: "a1", state: "AVAILABLE" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const blob = new Blob([new Uint8Array(64)], { type: "audio/webm" });
    await api.finaliseAudio("c1", "a".repeat(64), blob, 8123);

    const body = JSON.parse(fetchMock.mock.calls[0][1].body as string);
    expect(body.duration_ms).toBe(8123);
    expect(body.duration_ms).not.toBe(0);
    // The backend's accepted window. A value outside it strands the upload.
    expect(body.duration_ms).toBeGreaterThanOrEqual(500);
    expect(body.duration_ms).toBeLessThanOrEqual(20_000);
    vi.unstubAllGlobals();
  });

  it("derives the codec from the blob type instead of assuming webm", () => {
    expect(codecFor("audio/ogg;codecs=opus")).toBe("opus");
    expect(codecFor("audio/wav")).toBe("pcm");
    expect(codecFor("audio/webm")).toBe("webm");
  });
});
