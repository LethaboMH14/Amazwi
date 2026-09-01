import { Blob as NodeBlob } from "node:buffer";
import { createHash } from "node:crypto";
import { describe, expect, it } from "vitest";
import { digest } from "./RecordingRoute";

// jsdom's polyfilled global Blob does not implement .arrayBuffer() (a real
// browser's does), so these tests construct Node's own spec-complete Blob
// instead of the ambient jsdom one -- a test-environment workaround, not a
// product change; RecordingRoute.tsx itself is untouched. Node's Blob type
// isn't structurally identical to the DOM Blob type digest() expects (their
// .bytes() return types differ), so the cast below is scoped to one helper
// rather than sprinkled through every test.
function testBlob(parts: Uint8Array[], options?: { type?: string }): Blob {
  return new NodeBlob(parts, options) as unknown as Blob;
}

describe("digest", () => {
  it("matches an independently-computed SHA-256 hex digest of the same bytes", async () => {
    const bytes = new TextEncoder().encode("amazwi audio upload integrity check");
    const blob = testBlob([bytes], { type: "audio/webm" });

    const expected = createHash("sha256").update(bytes).digest("hex");
    const actual = await digest(blob);

    expect(actual).toBe(expected);
  });

  it("produces a 64-character lowercase hex string", async () => {
    const blob = testBlob([new Uint8Array([1, 2, 3])], { type: "audio/webm" });
    const hash = await digest(blob);
    expect(hash).toMatch(/^[0-9a-f]{64}$/);
  });

  it("is deterministic for the same content", async () => {
    const bytes = new Uint8Array([9, 8, 7, 6, 5]);
    const hash1 = await digest(testBlob([bytes]));
    const hash2 = await digest(testBlob([bytes]));
    expect(hash1).toBe(hash2);
  });

  it("produces different hashes for different content", async () => {
    const hashA = await digest(testBlob([new Uint8Array([1])]));
    const hashB = await digest(testBlob([new Uint8Array([2])]));
    expect(hashA).not.toBe(hashB);
  });

  it("matches the well-known SHA-256 digest of an empty blob", async () => {
    const hash = await digest(testBlob([]));
    // SHA-256("") -- a standard published test vector, not derived from the implementation
    expect(hash).toBe("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
  });
});
