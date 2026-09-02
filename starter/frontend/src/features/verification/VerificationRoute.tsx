import { useEffect, useState } from "react"; import { useSearchParams } from "react-router-dom"; import { api, userMessage } from "../../api/client"; import type { Assignment } from "../../api/contracts";
import { StatusAnnouncer } from "../../components/SignalPrimitives";
export function VerificationRoute() { const [params] = useSearchParams(); const contributionId = params.get("contributionId") ?? ""; const [assignment, setAssignment] = useState<Assignment>(); const [answer, setAnswer] = useState(""); const [status, setStatus] = useState("Loading the next peer card…"); const [error, setError] = useState(""); useEffect(() => {
   if (!contributionId) { setError("A contribution is required."); return; }
   // React StrictMode mounts effects twice in development -- and the demo runs
   // the dev server -- so this fires two near-simultaneous requests. The second
   // can lose the race against the first one's commit and come back 404, which
   // previously left "NO_ASSIGNMENT" sitting under a form that was actually
   // working. Discard anything from a superseded run rather than letting a
   // stale loser overwrite good state. Found by walking the route in a browser.
   let cancelled = false;
   api.getNextAssignment(contributionId).then(async (value) => {
     const playback = await api.getAssignmentPlayback(value.id);
     if (cancelled) return;
     setAssignment({ ...value, audio_playback_url: playback.url });
     setStatus("Listen once, then choose the matching card.");
     setError("");
   }).catch((err) => {
     if (cancelled) return;
     setError(userMessage(err));
     setStatus("");
   });
   return () => { cancelled = true; };
 }, [contributionId]); async function submit() { if (!assignment) return; setStatus("Submitting verification…"); try { await api.submitAnswer(assignment.id, answer); setStatus("Thanks — your independent answer was recorded."); } catch (err) { setError(userMessage(err)); setStatus(""); } } return <main className="route" aria-labelledby="verify-title"><p className="eyebrow">Peer verification</p><h1 id="verify-title">Does the audio match?</h1>{assignment?.audio_playback_url && <audio controls src={assignment.audio_playback_url} aria-label="Contribution audio" />}{assignment && <><p>{assignment.prompt_text}</p><input aria-label="Your answer" value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Type what you heard" /><button onClick={submit} disabled={!answer.trim()}>Submit answer</button></>}{/* StatusAnnouncer, not bare <p>s: the live regions must already be in
    the accessibility tree BEFORE their text changes, or a screen reader
    announces nothing. This route drives four status transitions (loading,
    ready, submitting, recorded) and previously exposed no aria-live at
    all — the Task 11 screen-reader gate caught it. */}
<StatusAnnouncer message={status} error={error} /></main>; }
