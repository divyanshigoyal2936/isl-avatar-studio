export interface LanguageInfo {
  code: string;
  name: string;
  native_name: string;
  stt_status: string;
  translation_status: string;
}

export interface RetrievedExemplar {
  id: string;
  dataset: string;
  source_text: string;
  normalized_english: string;
  gloss_sequence: string[];
  similarity_score: number;
  grammar_annotations?: Record<string, any>;
}

export interface GlossTokenDetail {
  token: string;
  syntax_role: string;
  is_verified: boolean;
  description?: string;
  fallback_fingerspelling: boolean;
}

export interface ScheduledClip {
  clip_id: string;
  gloss_token: string;
  start_time_ms: number;
  duration_ms: number;
  end_time_ms: number;
  transition_in_ms: number;
  transition_out_ms: number;
  hand_dominance: string;
  hand_shape: string;
  palm_orientation: string;
  signing_space: string;
  movement_type: string;
  non_manual_markers: Record<string, string>;
  is_verified: boolean;
  joint_targets?: Record<string, any>;
  description?: string;
}

export interface SignGenerateResponse {
  request_id: string;
  original_input: string;
  detected_language: string;
  transcript: string;
  normalized_sentence: string;
  rag_enabled: bool;
  retrieved_exemplars: RetrievedExemplar[];
  generated_gloss: string[];
  gloss_details: GlossTokenDetail[];
  supported_gloss_tokens: string[];
  unsupported_gloss_tokens: string[];
  animation_coverage_pct: number;
  scheduled_clips: ScheduledClip[];
  total_animation_duration_ms: number;
  explanation: string;
  grammar_notes: string[];
  warnings: string[];
  timings: Array<{ stage: string; duration_ms: number }>;
}
