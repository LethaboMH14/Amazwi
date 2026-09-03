import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, userMessage } from "../../api/client";
import type { ChangeEvent } from "react";
import type { Card } from "../../api/contracts";
import { clampDuration, probeDurationMs } from "./digest";
import { StatusAnnouncer } from "../../components/SignalPrimitives";
import "../flow.css";

// `zu-001`, deterministically created by `python -m app.seed_demo`.
const DEMO_CARD_ID = "467e6241-cb06-5395-aaa8-d63832bcc538";

const MAX_SECONDS = 30;
const BARS = 13;

export async function digest(blob: Blob) {
  const hash = await crypto.subtle.digest("SHA-256", await blob.arrayBuffer());
  return Array.from(new Uint8Array(hash)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

function supportedMime(type: string) {
  if (type.startsWith("audio/ogg")) return "audio/ogg";
  if (type.startsWith("audio/wav") || type.startsWith("audio/wave")) return "audio/wav";
  return "audio/webm";
}

export function formatElapsed(ms: number): string {
  const total = Math.max(0, Math.floor(ms / 1000));
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, "0")}`;
}

export function RecordingRoute() {
  const navigate = useNavigate();
  const recorder = useRef<MediaRecorder>();
  const chunks = useRef<Blob[]>([]);
  const startedAt = useRef<number>(0);
  const fileInput = useRef<HTMLInputElement>(null);

  // Live level metering. Kept in refs so the animation frame loop does not
  // re-render the component 60 times a second.
  const audioCtx = useRef<AudioContext>();
  const analyser = useRef<AnalyserNode>();
  const rafId = useRef<number>(0);

  const [recording, setRecording] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [levels, setLevels] = useState<number[]>(() => new Array(BARS).fill(0.08));
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);
  const canRecord =
    typeof navigator !== "undefined" && Boolean(navigator.mediaDevices?.getUserMedia);

  // The card IS the game. Load it before recording so the speaker can see the
  // target and the four words they may not say. Failing to load it must not
  // block recording -- the audio is still worth capturing -- so this degrades
  // to the plain prompt rather than throwing.
  const [card, setCard] = useState<Card | null>(null);
  useEffect(() => {
    let cancelled = false;
    api
      .getCard(DEMO_CARD_ID)
      .then((c) => !cancelled && setCard(c))
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, []);

  // Tear the meter down on unmount, or the AudioContext and its rAF loop
  // outlive the screen and keep the microphone indicator lit.
  useEffect(() => () => stopMeter(), []);

  function stopMeter() {
    if (rafId.current) cancelAnimationFrame(rafId.current);
    rafId.current = 0;
    analyser.current = undefined;
    void audioCtx.current?.close().catch(() => undefined);
    audioCtx.current = undefined;
  }

  /** Drive the meter from real microphone data, never a canned loop. */
  function startMeter(stream: MediaStream) {
    try {
      const Ctx =
        window.AudioContext ??
        (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
      if (!Ctx) return;
      const ctx = new Ctx();
      const node = ctx.createAnalyser();
      node.fftSize = 256;
      ctx.createMediaStreamSource(stream).connect(node);
      audioCtx.current = ctx;
      analyser.current = node;

      const bins = new Uint8Array(node.frequencyBinCount);
      const step = Math.floor(bins.length / BARS) || 1;
      const tick = () => {
        if (!analyser.current) return;
        analyser.current.getByteFrequencyData(bins);
        const next: number[] = [];
        for (let i = 0; i < BARS; i += 1) {
          let sum = 0;
          for (let j = 0; j < step; j += 1) sum += bins[i * step + j] ?? 0;
          next.push(Math.max(0.08, sum / step / 255));
        }
        setLevels(next);
        setElapsed(Date.now() - startedAt.current);
        rafId.current = requestAnimationFrame(tick);
      };
      rafId.current = requestAnimationFrame(tick);
    } catch {
      // A missing AudioContext must never stop a recording. The meter is
      // feedback; the audio is the product.
    }
  }

  async function upload(blob: Blob, durationMs: number) {
    setBusy(true);
    setError("");
    setStatus("Uploading securely…");
    try {
      const contribution = await api.createContribution(DEMO_CARD_ID);
      const uploadTarget = await api.beginUpload(contribution.id);
      const hash = await digest(blob);
      await api.uploadAudio(uploadTarget.audio_object_id, blob);
      await api.finaliseAudio(contribution.id, hash, blob, durationMs);
      setStatus("Sent. Two people will listen.");
      navigate(`/result/${contribution.id}`);
    } catch (err) {
      setError(userMessage(err));
      setStatus("");
    } finally {
      setBusy(false);
    }
  }

  async function start() {
    if (!canRecord) {
      fileInput.current?.click();
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      chunks.current = [];
      const activeRecorder = new MediaRecorder(stream);
      recorder.current = activeRecorder;
      startedAt.current = Date.now();
      setElapsed(0);
      activeRecorder.ondataavailable = (event) =>
        event.data.size && chunks.current.push(event.data);
      activeRecorder.onstop = async () => {
        // Must flip back to false here, before anything async, or a second
        // tap calls .stop() on an already-stopped MediaRecorder -- that
        // throws synchronously and uncaught outside this handler, so the
        // button silently does nothing on the next tap ("won't stop
        // recording" was a stuck button state, not a stuck recorder).
        setRecording(false);
        stopMeter();
        stream.getTracks().forEach((track) => track.stop());
        const blob = new Blob(chunks.current, { type: supportedMime(activeRecorder.mimeType) });
        await upload(blob, clampDuration(Date.now() - startedAt.current));
      };
      activeRecorder.start();
      setRecording(true);
      setStatus("Recording. Describe the word without saying it.");
      startMeter(stream);
    } catch (err) {
      setError(userMessage(err));
    }
  }

  function stop() {
    // Guard against a stale/duplicate tap trying to stop a recorder that
    // is not actually in the "recording" state -- MediaRecorder.stop()
    // throws InvalidStateError otherwise.
    if (recorder.current?.state === "recording") {
      recorder.current.stop();
    }
  }

  async function onCapturedFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    const blob = new Blob([await file.arrayBuffer()], { type: supportedMime(file.type) });
    // Measure the real length rather than asserting 1000ms.
    await upload(blob, await probeDurationMs(blob));
    event.target.value = "";
  }

  return (
    <main className="flow" aria-labelledby="record-title">
      <button type="button" className="flow-back" onClick={() => navigate("/dashboard")}>
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M15 5l-7 7 7 7" />
        </svg>
        My desk
      </button>

      <div className="flow-head">
        <p className="eyebrow">isiZulu contribution</p>
        <h1 id="record-title">Say the card aloud</h1>
      </div>

      {card && (
        <section className="flow-card play-card" aria-label="Your card">
          <p className="eyebrow">Your word</p>
          <p className="play-target">{card.target}</p>
          <p className="eyebrow">Don&rsquo;t say</p>
          <ul className="blocked-list">
            {card.blocked_words.map((w) => (
              <li key={w}>{w}</li>
            ))}
          </ul>
        </section>
      )}

      {recording ? (
        <section className="rec-stage" aria-label="Recording in progress">
          <p className="rec-timer">
            <span className="rec-dot" aria-hidden="true" />
            <span className="rec-elapsed">{formatElapsed(elapsed)}</span>
            <span className="rec-limit">/ {formatElapsed(MAX_SECONDS * 1000)}</span>
          </p>
          {/* Real analyser data. A canned animation here would be a lie
              about whether the microphone is actually picking anything up,
              which is the one thing a speaker needs to know. */}
          <div className="meter" aria-hidden="true">
            {levels.map((level, i) => (
              <span key={i} style={{ height: `${Math.round(level * 46)}px` }} />
            ))}
          </div>
          <p className="rec-hint">Your audio stays private until approved peers verify it.</p>
        </section>
      ) : (
        <section className="rec-stage" aria-label="Ready to record">
          <p className="rec-hint">
            Record one clear take. Two people will listen and type what they
            understood &mdash; they never see your card.
          </p>
          {!canRecord && (
            <p className="rec-hint">
              This page needs HTTPS to reach the microphone. Tap record to use
              your phone&rsquo;s own recorder instead; the audio stays private
              either way.
            </p>
          )}
        </section>
      )}

      {error && <p className="flow-error" role="alert">{error}</p>}

      <input
        ref={fileInput}
        type="file"
        accept="audio/*"
        capture="user"
        onChange={onCapturedFile}
        hidden
        aria-label="Record audio with phone"
      />

      <div className="flow-actions">
        <button
          type="button"
          className={`flow-btn ${recording ? "flow-btn-stop" : "flow-btn-go"}`}
          onClick={() => (recording ? stop() : start())}
          disabled={busy}
        >
          {busy ? (
            "Uploading securely…"
          ) : recording ? (
            <>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <rect x="6" y="6" width="12" height="12" rx="2" />
              </svg>
              Stop recording
            </>
          ) : (
            <>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
                <path d="M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3z" />
                <path d="M5 11a7 7 0 0 0 14 0M12 18v3" />
              </svg>
              Start recording
            </>
          )}
        </button>
      </div>

      <StatusAnnouncer message={status} error={error} />
    </main>
  );
}
