import type { Assignment, ConsentScope, ConsentState, Contribution, Impact, MissionProposal, OpsView, Result } from "./contracts";
export class ApiError extends Error { constructor(public readonly status:number, public readonly code:string, message:string){super(message);} }
function headers(): HeadersInit { const env=(import.meta as ImportMeta & {env:Record<string,string|undefined>}).env; const h:Record<string,string>={Accept:"application/json"}; if(env.VITE_USER_ID)h["X-User-ID"]=env.VITE_USER_ID; if(env.VITE_PROVIDER_SUBJECT)h["X-Provider-Subject"]=env.VITE_PROVIDER_SUBJECT; return h; }
async function request<T>(path:string, init:RequestInit={}):Promise<T>{ const r=await fetch(`/api${path}`,{...init,headers:{...headers(),...(init.headers??{})}}); if(!r.ok){let d:{code?:string;detail?:string}={};try{d=await r.json();}catch{} throw new ApiError(r.status,d.code??"HTTP_ERROR",d.detail??"Request failed. Please try again.");} return r.status===204?undefined as T:r.json(); }
export const api={
 grantConsent:(scopes:ConsentScope[],version="2026-09-01")=>request<ConsentState[]>("/consents",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({version,scopes})}),
 createContribution:(cardId:string)=>request<Contribution>("/contributions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({card_id:cardId})}),
 beginUpload:(contributionId:string)=>request<{audio_object_id:string}>(`/contributions/${contributionId}/audio/uploads`,{method:"POST"}),
 uploadAudio:async(id:string,blob:Blob)=>{const r=await fetch(`/api/private-audio/uploads/${id}`,{method:"PUT",headers:{...headers(),"Content-Type":blob.type},body:blob});if(!r.ok)throw new ApiError(r.status,"UPLOAD_FAILED","Audio upload failed.");},
 finaliseAudio:(id:string,sha256:string,blob:Blob)=>request(`/contributions/${id}/audio/finalise`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({sha256,mime_type:blob.type||"audio/webm",codec:"webm",duration_ms:0,byte_length:blob.size})}),
 getNextAssignment:(id:string,language="zu")=>request<Assignment>(`/assignments/next?contribution_id=${encodeURIComponent(id)}&language=${encodeURIComponent(language)}`),
 getAssignmentPlayback:(id:string)=>request<{url:string}>(`/assignments/${id}/playback`,{method:"POST"}),
 submitAnswer:(id:string,answer:string)=>request(`/assignments/${id}/answer`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({answer_text:answer,violation_vote:false})}),
 getResult:(id:string)=>request<Result>(`/contributions/${id}/result`),
 getImpact:()=>request<Impact>("/impact"),
 getOps:()=>request<OpsView>("/ops"),
 // The only body field is the operator's verbatim confirmation echo. No
 // mission terms are sent -- see contracts.ts. `idempotencyKey` is generated
 // per human click so a double-submit cannot authorise twice.
 authoriseMission:(proposalId:string,idempotencyKey:string,confirmation:string)=>request<MissionProposal>(`/ops/missions/${proposalId}/authorise`,{method:"POST",headers:{"Content-Type":"application/json","Idempotency-Key":idempotencyKey},body:JSON.stringify({confirmation})}),
};
export function userMessage(e:unknown){if(e instanceof ApiError&&e.status===401)return "Sign in to MoMo to continue.";if(e instanceof ApiError&&e.status===409)return "This action is not available for the current round.";return e instanceof Error?e.message:"Something went wrong. Please try again.";}
