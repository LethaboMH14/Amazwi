export type ConsentScope = "round_participation" | "peer_playback" | "model_improvement";
export interface ConsentState { version: string; scopes: ConsentScope[]; granted_at: string; }
export interface Contribution { id: string; card_id: string; language: string; status: string; }
export interface Assignment { id: string; contribution_id: string; language: string; prompt_text: string; audio_playback_url?: string; status: string; }
export interface Result { contribution_id: string; outcome: string; reward_minor: number; currency: string; }
export type CoverageBand = "5-19" | "20-49" | "50-99" | "100+";
/** Aggregate coverage cell. Deliberately carries no identifier, coordinate, audio key or transcript. */
export interface CoverageNodeDTO { id: string; language: string; province_code: string | null; campaign: string; verified_count_band: CoverageBand; coverage_percent: number; model_gap_percent: number | null; updated_at: string; }
export interface Impact { verified_total: number; languages_active: number; missions_completed: number; geography_available: boolean; suppressed_cell_count: number; generated_at: string; nodes: CoverageNodeDTO[]; }
