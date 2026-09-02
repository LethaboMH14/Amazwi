export type ConsentScope = "round_participation" | "peer_playback" | "model_improvement";
export interface ConsentState { version: string; scopes: ConsentScope[]; granted_at: string; }
export interface Contribution { id: string; card_id: string; language: string; status: string; }
export interface Assignment { id: string; contribution_id: string; language: string; prompt_text: string; audio_playback_url?: string; status: string; }
export interface Result { contribution_id: string; outcome: string; reward_minor: number; currency: string; }

// --- MTN Language Ops (Plan 03, Tasks 9-10) ------------------------------
// Mission terms are read-only on the client. `authoriseMission` deliberately
// sends no terms at all: the backend copies language, domain, target, fixed
// reward and budget from the persisted proposal, so nothing on this screen
// can change what is being authorised.
export interface MissionProposal {
  id: string;
  language: string;
  province_code: string;
  domain: string;
  rationale: string;
  target_verified_clips: number;
  fixed_reward_cents: number;
  budget_cents: number;
  state: "PROPOSED" | "AUTHORISED" | "REJECTED";
  authorised_by: string | null;
}
export interface OpsReadinessRow { label: string; value: string | null; detail: string; available: boolean; }
export interface OpsGap { language: string; verified_contributions: number; }
export interface OpsView {
  principal_kind: string;
  roles: string[];
  display_name: string;
  confirmation_text: string;
  readiness: OpsReadinessRow[];
  gaps: OpsGap[];
  proposals: MissionProposal[];
}
