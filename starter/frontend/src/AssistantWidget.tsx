import { FormEvent, useState } from "react";
import { Link } from "react-router-dom";
import { api, userMessage } from "./api/client";
import type { AssistantResponse } from "./api/contracts";
import "./assistant-widget.css";

export function AssistantWidget() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState<AssistantResponse | null>(null);
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!message.trim() || sending) return;
    setSending(true);
    setError("");
    try {
      setResponse(await api.assistant(message.trim()));
      setMessage("");
    } catch (cause) {
      setError(userMessage(cause));
    } finally {
      setSending(false);
    }
  }

  return (
    <aside className="assistant-widget" aria-label="Voice Compass assistant">
      {open && (
        <section className="assistant-panel" aria-labelledby="assistant-title">
          <div className="assistant-heading">
            <div>
              <p className="eyebrow">AMAZWI guide</p>
              <h2 id="assistant-title">Voice Compass</h2>
            </div>
            <button className="assistant-close" type="button" onClick={() => setOpen(false)} aria-label="Close Voice Compass">×</button>
          </div>
          <p className="assistant-intro">Ask me to open a page or explain a credited reward. I never move money from chat.</p>
          <form onSubmit={submit}>
            <label htmlFor="assistant-message">Ask AMAZWI</label>
            <div className="assistant-input-row">
              <input id="assistant-message" value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Take me to rewards" maxLength={2000} />
              <button type="submit" aria-label="Send message" disabled={sending}>{sending ? "…" : "Send"}</button>
            </div>
          </form>
          {error && <p className="assistant-error" role="alert">{error}</p>}
          {response && (
            <div className="assistant-response" aria-live="polite">
              <p>{response.reply}</p>
              {response.route && <Link to={response.route} className="assistant-route">Open {response.route.replace("/", "") || "home"}</Link>}
              <small>{response.provider} · advisory only</small>
            </div>
          )}
        </section>
      )}
      {!open && <button className="assistant-launch" type="button" onClick={() => setOpen(true)} aria-label="Ask Voice Compass">✦ <span>Ask Voice Compass</span></button>}
    </aside>
  );
}
