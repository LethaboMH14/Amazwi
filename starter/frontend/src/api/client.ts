import type { ArcadeDashboard, Assignment, Rewards, Card, ConsentScope, ConsentState, Contribution, Impact, MissionProposal, OpsView, Result } from "./contracts";
export class ApiError extends Error { constructor(public readonly status:number, public readonly code:string, message:string){super(message);} }
function headers(): HeadersInit { const env=(import.meta as ImportMeta & {env:Record<string,string|undefined>}).env; const h:Record<string,string>={Accept:"application/json"}; if(env.VITE_USER_ID)h["X-User-ID"]=env.VITE_USER_ID; if(env.VITE_PROVIDER_SUBJECT)h["X-Provider-Subject"]=env.VITE_PROVIDER_SUBJECT; return h; }
// FastAPI wraps every error body as {"detail": ...}, and this backend raises
// HTTPException(detail={"code": "..."}) -- so the code lives at
// `body.detail.code`, NOT `body.code`, and `body.detail` is an OBJECT.
// Reading the top level meant the code was always undefined and the message
// was an object, which React renders as the literal string "[object Object]".
// That was on screen for a real user on the verifier route, not hypothetical.
// Handles all three shapes the API can produce: nested object, plain-string
// detail, and a body with no detail at all.
type ErrorBody = { detail?: string | { code?: string; message?: string } };
function parseError(status: number, body: ErrorBody): ApiError {
  const detail = body?.detail;
  if (detail && typeof detail === "object") {
    return new ApiError(status, detail.code ?? "HTTP_ERROR", detail.message ?? detail.code ?? "Request failed. Please try again.");
  }
  return new ApiError(status, "HTTP_ERROR", typeof detail === "string" && detail ? detail : "Request failed. Please try again.");
}
async function request<T>(path:string, init:RequestInit={}):Promise<T>{ const r=await fetch(`/api${path}`,{...init,headers:{...headers(),...(init.headers??{})}}); if(!r.ok){let d:ErrorBody={};try{d=await r.json();}catch{} throw parseError(r.status,d);} return r.status===204?undefined as T:r.json(); }
/** Codec label derived from the blob's real type, not assumed. */
export function codecFor(mimeType:string):string{if(mimeType.includes("ogg"))return "opus";if(mimeType.includes("wav"))return "pcm";return "webm";}
export const api={
 grantConsent:(scopes:ConsentScope[],version="2026-09-01")=>request<ConsentState[]>("/consents",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({version,scopes})}),
 getCard:(cardId:string)=>request<Card>(`/cards/${cardId}`),
 createContribution:(cardId:string)=>request<Contribution>("/contributions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({card_id:cardId})}),
 beginUpload:(contributionId:string)=>request<{audio_object_id:string}>(`/contributions/${contributionId}/audio/uploads`,{method:"POST"}),
 uploadAudio:async(id:string,blob:Blob)=>{const r=await fetch(`/api/private-audio/uploads/${id}`,{method:"PUT",headers:{...headers(),"Content-Type":blob.type},body:blob});if(!r.ok)throw new ApiError(r.status,"UPLOAD_FAILED","Audio upload failed.");},
 // `durationMs` is REQUIRED and must be real. It used to be hardcoded to
 // 0 here while the recorder computed the true value and threw it away --
 // and the backend rejects anything outside 500..20000ms, so every single
 // finalise failed with AUDIO_DURATION_INVALID and every upload was left
 // stranded as a .pending file that no verifier could ever play.
 finaliseAudio:(id:string,sha256:string,blob:Blob,durationMs:number)=>request(`/contributions/${id}/audio/finalise`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({sha256,mime_type:blob.type||"audio/webm",codec:codecFor(blob.type),duration_ms:Math.round(durationMs),byte_length:blob.size})}),
 getNextAssignment:(id:string,language="zu")=>request<Assignment>(`/assignments/next?contribution_id=${encodeURIComponent(id)}&language=${encodeURIComponent(language)}`),
 getAssignmentPlayback:(id:string)=>request<{url:string}>(`/assignments/${id}/playback`,{method:"POST"}),
 submitAnswer:(id:string,answer:string)=>request(`/assignments/${id}/answer`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({answer_text:answer,violation_vote:false})}),
 getResult:(id:string)=>request<Result>(`/contributions/${id}/result`),
 getImpact:()=>request<Impact>("/impact"),
 getOps:()=>request<OpsView>("/ops"),
 getRewards:()=>request<Rewards>("/rewards"),
 getArcade:(language?:string)=>request<ArcadeDashboard>(`/arcade${language?`?language=${encodeURIComponent(language)}`:""}`),
 // The only body field is the operator's verbatim confirmation echo. No
 // mission terms are sent -- see contracts.ts. `idempotencyKey` is generated
 // per human click so a double-submit cannot authorise twice.
 authoriseMission:(proposalId:string,idempotencyKey:string,confirmation:string)=>request<MissionProposal>(`/ops/missions/${proposalId}/authorise`,{method:"POST",headers:{"Content-Type":"application/json","Idempotency-Key":idempotencyKey},body:JSON.stringify({confirmation})}),
};
export function userMessage(e:unknown){if(e instanceof ApiError&&e.status===401)return "Sign in to MoMo to continue.";if(e instanceof ApiError&&e.status===409)return "This action is not available for the current round.";return e instanceof Error?e.message:"Something went wrong. Please try again.";}
