export type ConsentScope = "RECORD_PROCESS_ROUND" | "ASSIGNED_VERIFIER_PLAYBACK" | "RETAIN_MODEL_DEVELOPMENT";
export interface ConsentState { scope: ConsentScope; version: string; granted_at: string; revoked_at: string | null; }
export interface Card { id: string; language: string; target: string; blocked_words: string[]; }
// `card` is returned to the contribution's own SPEAKER only -- they are being
// asked to describe the target, so they must see it and the blocked words.
// Verifier-facing routes deliberately withhold it until an answer is locked.
export interface Contribution { id: string; state: string; reward_rule_id: string; card: Card | null; }
export interface Assignment { id: string; contribution_id: string; language: string; prompt_text: string; audio_playback_url?: string; mode: string; }
// `reward_minor` is MINOR units (cents), not rand -- 200 means R2.00. It was
// rendered raw as "200 ZAR" on the receipt, i.e. 100x the real published rate,
// on the one screen whose entire job is being financially truthful.
export interface Result { contribution_id: string; status?: string; outcome: string; reward_minor: number; currency: string; provider_mode?: string | null; ledger_state?: string | null; settlement_state?: string | null; currency_disclosure_text?: string | null; understood?: boolean; corpus_eligible?: boolean; reason?: string; }
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

// --- Engagement layer (arcade) -------------------------------------------
// Mirrors app/api_types.py's ArcadeDashboardResponse. Note what is NOT here:
// no skill/personality scores and no "players online" count. AMAZWI measures
// neither, so the backend publishes neither, and the UI has nothing to render
// them from even by accident.
export interface Progression {
  xp: number; level: number; tier: string;
  xp_into_level: number; xp_for_next_level: number; percent_into_level: number;
  verified_contributions: number; completed_verifications: number;
}
/** The real replacement for a fabricated skill radar. */
export interface SpeakerOutcomes {
  understood: number; not_understood: number; awaiting_peers: number;
  closed: number; total: number;
}
export interface LeaderboardRow {
  rank: number; user_id: string; display_name: string;
  verified_contributions: number; xp: number; tier: string; is_current_user: boolean;
}
export interface PeerRow {
  user_id: string; display_name: string; language: string;
  tier: string; verified_contributions: number;
}
/** A pending peer-verification request -- a real assignment, not a synthetic invite. */
export interface InvitationRow {
  assignment_id: string; contribution_id: string;
  language: string; speaker_name: string; created_at: string;
}
export interface DeckSummary {
  language: string; card_count: number;
  contributors: number; verified_contributions: number;
}
export interface QuestRow {
  key: string; label: string; detail: string;
  progress: number; target: number; reward_xp: number; complete: boolean;
}
export interface ArcadeDashboard {
  display_name: string;
  earned_cents: number;
  progression: Progression;
  outcomes: SpeakerOutcomes;
  decks: DeckSummary[];
  quests: QuestRow[];
  invitations: InvitationRow[];
  peers: PeerRow[];
  leaderboard: LeaderboardRow[];
  leaderboard_language: string | null;
  generated_at: string;
}

// --- Reward catalogue -----------------------------------------------------
// Mirrors app/api_types.py's RewardsResponse. `availability` is computed
// server-side from the live provider mode, so the client cannot render a
// redeem button the backend would refuse. Note the absence of a points
// balance: the ledger is rand cents, and a parallel currency would be a
// second source of truth for money.
export type RewardAvailability =
  | "REDEEMABLE"
  | "INSUFFICIENT_CREDIT"
  | "PROVIDER_NOT_CONNECTED";
export interface CatalogueRow {
  key: string;
  title: string;
  description: string;
  threshold_cents: number;
  /** The real MTN MoMo product this maps to -- never a partner brand. */
  momo_product: string;
  availability: RewardAvailability;
  shortfall_cents: number;
}
export interface Rewards {
  balance_cents: number;
  provider_mode: string;
  provider_connected: boolean;
  /** Thresholds are placeholders pending Sbu's money review. */
  thresholds_are_proposed: boolean;
  items: CatalogueRow[];
  generated_at: string;
}

export interface AssistantResponse {
  reply: string;
  intent: string;
  route: string | null;
  provider: string;
  advisory: boolean;
}
