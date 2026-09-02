export type ConsentScope = "RECORD_PROCESS_ROUND" | "ASSIGNED_VERIFIER_PLAYBACK" | "RETAIN_MODEL_DEVELOPMENT";
export interface ConsentState { scope: ConsentScope; version: string; granted_at: string; revoked_at: string | null; }
export interface Card { id: string; language: string; target: string; blocked_words: string[]; }
// `card` is returned to the contribution's own SPEAKER only -- they are being
// asked to describe the target, so they must see it and the blocked words.
// Verifier-facing routes deliberately withhold it until an answer is locked.
export interface Contribution { id: string; state: string; reward_rule_id: string; card: Card | null; }
export interface Assignment { id: string; contribution_id: string; language: string; prompt_text: string; audio_playback_url?: string; mode: string; }
export interface Result { contribution_id: string; outcome: string; reward_minor: number; currency: string; }
export type CoverageBand = "5-19" | "20-49" | "50-99" | "100+";
/** Aggregate coverage cell. Deliberately carries no identifier, coordinate, audio key or transcript. */
export interface CoverageNodeDTO { id: string; language: string; province_code: string | null; campaign: string; verified_count_band: CoverageBand; coverage_percent: number; model_gap_percent: number | null; updated_at: string; }
export interface Impact { verified_total: number; languages_active: number; missions_completed: number; geography_available: boolean; suppressed_cell_count: number; generated_at: string; nodes: CoverageNodeDTO[]; }

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
