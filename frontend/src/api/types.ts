// Pagination
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

// DailyLog
export interface DailyLogCreate {
  date: string; // YYYY-MM-DD
  food_offered_g?: number | null;
  food_eaten_g?: number | null;
  water_intake?: string | null;
  stool_consistency?: number | null; // 1-5
  stool_color?: string | null;
  flatulence?: boolean | null;
  vomiting?: boolean | null;
  vomiting_count?: number | null;
  energy_level?: number | null; // 1-5
  willingness_to_walk?: number | null; // 1-5
  play_interest?: number | null; // 1-5
  coat_condition?: number | null; // 1-5
  muscle_wasting?: number | null; // 1-5
  lameness_score?: number | null; // 0-4
  affected_limb?: string | null;
  stiffness_after_rest?: boolean | null;
  pain_score?: number | null; // 0-24
  notes?: string | null;
}

export type DailyLogUpdate = Partial<DailyLogCreate>;

export interface DailyLogRead extends DailyLogCreate {
  id: number;
  created_at: string;
  appetite_ratio: number | null;
  observations: SymptomObservationRead[];
}

// SymptomObservation
export interface SymptomObservationCreate {
  symptom_type: string;
  value_numeric?: number | null;
  value_text?: string | null;
  value_bool?: boolean | null;
  notes?: string | null;
}

export interface SymptomObservationRead extends SymptomObservationCreate {
  id: number;
  daily_log_id: number;
  timestamp: string;
}

// HealthMarker
export interface HealthMarkerCreate {
  weight_kg?: number | null;
  ctli?: number | null;
  lipase?: number | null;
  amylase?: number | null;
  cobalamin_b12?: number | null;
  folate?: number | null;
  glucose?: number | null;
  vitamin_e?: number | null;
  vitamin_k?: number | null;
  timestamp?: string | null;
}

export type HealthMarkerUpdate = Partial<HealthMarkerCreate>;

export interface HealthMarkerRead extends HealthMarkerCreate {
  id: number;
  timestamp: string;
}

// TreatmentTemplate
export interface TreatmentTemplateCreate {
  name: string;
  category: string;
  default_schedule: Record<string, unknown>;
  notes?: string | null;
}

export interface TreatmentTemplateRead extends TreatmentTemplateCreate {
  id: number;
  created_at: string;
}

// TreatmentProtocol
export interface TreatmentProtocolCreate {
  template_id?: number | null;
  vet_visit_id?: number | null;
  category: string;
  name: string;
  schedule: Record<string, unknown>;
  start_date: string;
  end_date?: string | null;
  prescribed_by?: string | null;
  active?: boolean;
  notes?: string | null;
}

export type TreatmentProtocolUpdate = Partial<TreatmentProtocolCreate>;

export interface TreatmentProtocolRead extends TreatmentProtocolCreate {
  id: number;
  created_at: string;
  updated_at: string;
  current_phase: Record<string, unknown> | null;
  entries: TreatmentEntryRead[];
}

// TreatmentEntry
export interface TreatmentEntryCreate {
  scheduled_date: string;
  administered_at?: string | null;
  dose?: number | null;
  unit?: string | null;
  administered_by?: string | null;
  notes?: string | null;
}

export type TreatmentEntryUpdate = Partial<TreatmentEntryCreate>;

export interface TreatmentEntryRead extends TreatmentEntryCreate {
  id: number;
  protocol_id: number;
  created_at: string;
  was_skipped: boolean;
}

// VetVisit
export interface VetVisitCreate {
  reason: string;
  vet_name?: string | null;
  clinic?: string | null;
  diagnosis?: string | null;
  findings?: string | null;
  next_appointment?: string | null;
  notes?: string | null;
  timestamp?: string | null;
}

export type VetVisitUpdate = Partial<VetVisitCreate>;

export interface VetVisitRead extends VetVisitCreate {
  id: number;
  timestamp: string;
  protocols: TreatmentProtocolRead[];
}

// VitalReading
export interface VitalReadingCreate {
  marker_type: string;
  value: number;
  unit: string;
  source: string;
  timestamp?: string | null;
  notes?: string | null;
}

export type VitalReadingUpdate = Partial<VitalReadingCreate>;

export interface VitalReadingRead extends VitalReadingCreate {
  id: number;
  timestamp: string;
}

// Insights
export interface WeightTrendPoint {
  timestamp: string;
  weight_kg: number;
  source: string;
}

export interface B12TrendPoint {
  timestamp: string;
  cobalamin_b12: number;
}

export interface StoolTrendPoint {
  date: string;
  stool_consistency: number;
  stool_color: string | null;
}

export interface WeeklySummary {
  week_start: string;
  week_end: string;
  days_logged: number;
  avg_energy_level: number | null;
  avg_stool_consistency: number | null;
  avg_appetite_ratio: number | null;
  total_vomiting_episodes: number;
  avg_pain_score: number | null;
  max_pain_score: number | null;
}

export interface MonthlySummary extends WeeklySummary {
  weight_start_kg: number | null;
  weight_end_kg: number | null;
  weight_change_kg: number | null;
}

export interface ComplianceReport {
  protocol_id: number;
  protocol_name: string;
  total_entries: number;
  administered: number;
  skipped: number;
  pending: number;
  compliance_rate: number;
}
