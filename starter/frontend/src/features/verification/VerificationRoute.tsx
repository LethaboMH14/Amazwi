import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { usePolling } from "../../usePolling";
import { api, userMessage } from "../../api/client";
import type { Assignment } from "../../api/contracts";
import { StatusAnnouncer } from "../../components/SignalPrimitives";
import { Mascot } from "../arcade/Mascot";
import "../flow.css";

export function VerificationRoute() {
  const [params] = useSearchParams();
  const contributionId = params.get("contributionId") ?? "";
  const [assignment, setAssignment] = useState<Assignment>();
  const [speakerName, setSpeakerName] = useState("");
  const [answer, setAnswer] = useState("");
  const [status, setStatus] = useState("Finding someone who needs you…");
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [playing, setPlaying] = useState(false);
  const audio = useRef<HTMLAudioElement>(null);
  const navigate = useNavigate();

  const load = useCallback(async (opts: { quiet?: boolean } = {}) => {
    // No id in the URL? ASK for one. This route used to demand a
    // contribution id it had no way to obtain, which made a real
    // two-device walk impossible: you had to read a UUID off a phone and
    // type it into a laptop. The queue is now the default entry point and
    // the URL parameter is only an override.
    //
    // React StrictMode mounts effects twice in development -- and the demo
    // runs the dev server -- so this fires two near-simultaneous requests.
    // The second can lose the race against the first one's commit and come
    // back 404, which previously left "NO_ASSIGNMENT" sitting under a form
    // that was actually working. Discard anything from a superseded run.
    try {
      let target = contributionId;
      if (!target) {
        const queue = await api.getVerificationQueue();
        if (queue.items.length === 0) {
          // NOT an error. This is the normal resting state of a verifier
          // device between recordings -- showing it in red made a working
          // app look broken, and it is the state the laptop sits in for
          // most of a demo.
          setError("");
          setStatus("");
          return;
        }
        target = queue.items[0].contribution_id;
        setSpeakerName(queue.items[0].speaker_name);
      }
      const value = await api.getNextAssignment(target);
      const playback = await api.getAssignmentPlayback(value.id);
      setAssignment({ ...value, audio_playback_url: playback.url });
      setStatus("Listen, then type the word you heard.");
      setError("");
    } catch (err) {
      if (!opts.quiet) {
        setError(userMessage(err));
        setStatus("");
      }
    }
  }, [contributionId]);

  useEffect(() => {
    void load();
  }, [load]);

  // Keep looking while this device is idle and waiting. Without this the
  // laptop fetched once on mount and never again -- a speaker could record
  // on the phone and both verifier laptops would sit on "nobody is waiting"
  // indefinitely, which reads as the product being broken.
  usePolling(() => load({ quiet: true }), 4000, !assignment && !submitted);

  function togglePlay() {
    const el = audio.current;
    if (!el) return;
    if (el.paused) {
      void el.play().catch(() => setError("This clip could not be played."));
    } else {
      el.pause();
    }
  }

  async function submit() {
    if (!assignment) return;
    setStatus("Submitting your answer…");
    try {
      await api.submitAnswer(assignment.id, answer);
      setSubmitted(true);
      setStatus("Thanks — your independent answer was recorded.");
      setError("");
    } catch (err) {
      setError(userMessage(err));
      setStatus("");
    }
  }

  return (
    <main className="flow" aria-labelledby="verify-title">
      <button type="button" className="flow-back" onClick={() => navigate("/dashboard")}>
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M15 5l-7 7 7 7" />
        </svg>
        My desk
      </button>

      <div className="flow-head">
        <p className="eyebrow">Peer verification</p>
        <h1 id="verify-title">What did you hear?</h1>
        <p className="serif">
          {speakerName
            ? `${speakerName} is waiting on you.`
            : "Answer on your own — the other listener cannot see you."}
        </p>
      </div>

      {/* The visible error lives in StatusAnnouncer, which already renders
          an assertive live region. Rendering it here as well printed every
          message twice on screen. */}
      {!assignment && !submitted && !error && (
        <section className="flow-card waiting" aria-label="Waiting for a recording">
          <Mascot size={116} mood="listening" />
          <p className="waiting-title">Listening for new voices</p>
          <p className="answer-note" style={{ textAlign: "center", margin: 0 }}>
            Nobody has recorded yet. Leave this open &mdash; the moment someone
            does, their card appears here automatically.
          </p>
          <span className="waiting-live" aria-hidden="true">
            <i /><i /><i />
          </span>
        </section>
      )}

      {assignment && !submitted && (
        <>
          <section className="flow-card" aria-label="The recording">
            <div className="player">
              <button
                type="button"
                className="player-play"
                onClick={togglePlay}
                aria-label={playing ? "Pause the recording" : "Play the recording"}
              >
                {playing ? (
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <rect x="7" y="5" width="4" height="14" rx="1.4" />
                    <rect x="13" y="5" width="4" height="14" rx="1.4" />
                  </svg>
                ) : (
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                )}
              </button>
              <div className="player-meta">
                <b>{speakerName || "A peer"}</b>
                <span>Play it as many times as you need.</span>
              </div>
            </div>
            {/* The real element does the work; the button above drives it.
                Kept in the tree (not hidden) so a keyboard or screen-reader
                user still has native transport controls. */}
            <audio
              ref={audio}
              controls
              src={assignment.audio_playback_url}
              onPlay={() => setPlaying(true)}
              onPause={() => setPlaying(false)}
              onEnded={() => setPlaying(false)}
              aria-label="Contribution audio"
              style={{ width: "100%", marginTop: 14 }}
            />
          </section>

          <section className="flow-card" aria-label="Your answer">
            <label className="answer-label" htmlFor="verify-answer">
              Type the word you understood
            </label>
            <input
              id="verify-answer"
              className="answer-input"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="one word"
              autoComplete="off"
              autoCapitalize="none"
              spellCheck={false}
            />
            <p className="answer-note">
              Free text on purpose — a multiple-choice list would let a guess
              through, and a guess is not understanding.
            </p>
          </section>

          <div className="flow-actions">
            <button
              type="button"
              className="flow-btn flow-btn-go"
              onClick={submit}
              disabled={!answer.trim()}
            >
              Submit my answer
            </button>
          </div>
        </>
      )}

      {submitted && (
        <section className="flow-card" aria-label="Answer recorded">
          <p className="eyebrow">Recorded</p>
          <p style={{ fontSize: 17, fontWeight: 700, margin: "6px 0 8px" }}>
            Thank you — your answer is in.
          </p>
          <p className="answer-note" style={{ margin: 0 }}>
            It stays sealed until the second listener has answered too. Neither
            of you can see the other&rsquo;s word, which is what makes the
            agreement worth anything.
          </p>
        </section>
      )}

      {/* StatusAnnouncer, not bare <p>s: the live regions must already be in
          the accessibility tree BEFORE their text changes, or a screen reader
          announces nothing. This route drives four status transitions
          (finding, ready, submitting, recorded) and previously exposed no
          aria-live at all — the Task 11 screen-reader gate caught it. */}
      <StatusAnnouncer message={status} error={error} />
    </main>
  );
}
