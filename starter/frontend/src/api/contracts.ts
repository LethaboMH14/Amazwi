export type ConsentScope = "round_participation" | "peer_playback" | "model_improvement";
export interface ConsentState { version: string; scopes: ConsentScope[]; granted_at: string; }
export interface Contribution { id: string; card_id: string; language: string; status: string; }
export interface Assignment { id: string; contribution_id: string; language: string; prompt_text: string; audio_playback_url?: string; status: string; }
export interface Result { contribution_id: string; outcome: string; reward_minor: number; currency: string; }
