import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, userMessage } from "../../api/client";
import type { ChangeEvent } from "react";

// `zu-001`, deterministically created by `python -m app.seed_demo`.
const DEMO_CARD_ID = "467e6241-cb06-5395-aaa8-d63832bcc538";

export async function digest(blob: Blob) {
  const hash = await crypto.subtle.digest("SHA-256", await blob.arrayBuffer());
  return Array.from(new Uint8Array(hash)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

function supportedMime(type: string) {
  if (type.startsWith("audio/ogg")) return "audio/ogg";
  if (type.startsWith("audio/wav") || type.startsWith("audio/wave")) return "audio/wav";
  return "audio/webm";
}

export function RecordingRoute() {
  const navigate = useNavigate();
  const recorder = useRef<MediaRecorder>();
  const chunks = useRef<Blob[]>([]);
  const startedAt = useRef<number>(0);
  const fileInput = useRef<HTMLInputElement>(null);
  const [recording, setRecording] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const canRecord = typeof navigator !== "undefined" && Boolean(navigator.mediaDevices?.getUserMedia);

  async function upload(blob: Blob, durationMs: number) {
    setBusy(true);
    setError("");
    try {
      const contribution = await api.createContribution(DEMO_CARD_ID);
      const uploadTarget = await api.beginUpload(contribution.id);
      const hash = await digest(blob);
      await api.uploadAudio(uploadTarget.audio_object_id, blob);
      await api.finaliseAudio(contribution.id, hash, blob);
      navigate(`/result/${contribution.id}`);
    } catch (err) {
      setError(userMessage(err));
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
      activeRecorder.ondataavailable = (event) => event.data.size && chunks.current.push(event.data);
      activeRecorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        const blob = new Blob(chunks.current, { type: supportedMime(activeRecorder.mimeType) });
        await upload(blob, Math.max(500, Math.min(20_000, Date.now() - startedAt.current)));
      };
      activeRecorder.start();
      setRecording(true);
    } catch (err) {
      setError(userMessage(err));
    }
  }

  async function onCapturedFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    const blob = new Blob([await file.arrayBuffer()], { type: supportedMime(file.type) });
    await upload(blob, 1000);
    event.target.value = "";
  }

  return <main className="route" aria-labelledby="record-title"><p className="eyebrow">isiZulu contribution</p><h1 id="record-title">Say the card aloud</h1><p>Record one clear take. Your audio stays private until approved peers verify it.</p>{!canRecord && <p>Microphone access needs HTTPS. Use your phone&rsquo;s recorder here; the audio remains private.</p>}{error && <p role="alert">{error}</p>}<input ref={fileInput} type="file" accept="audio/*" capture="user" onChange={onCapturedFile} hidden aria-label="Record audio with phone" /><button onClick={() => recording ? recorder.current?.stop() : start()} disabled={busy}>{busy ? "Uploading securely…" : recording ? "Stop recording" : "Start recording"}</button></main>;
}
