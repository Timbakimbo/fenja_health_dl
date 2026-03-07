import { get, buildQuery } from './client';
import type { WeightTrendPoint, B12TrendPoint, StoolTrendPoint, WeeklySummary, MonthlySummary, ComplianceReport } from './types';

const BASE = '/api/insights';

export function getWeightTrend() {
  return get<WeightTrendPoint[]>(`${BASE}/weight-trend`);
}

export function getB12Trend() {
  return get<B12TrendPoint[]>(`${BASE}/b12-trend`);
}

export function getStoolTrend() {
  return get<StoolTrendPoint[]>(`${BASE}/stool-trend`);
}

export function getWeeklySummary(date?: string) {
  return get<WeeklySummary>(`${BASE}/weekly-summary` + buildQuery({ date }));
}

export function getMonthlySummary(year: number, month: number) {
  return get<MonthlySummary>(`${BASE}/monthly-summary` + buildQuery({ year, month }));
}

export function getTreatmentCompliance(protocolId: number) {
  return get<ComplianceReport>(`${BASE}/treatment-compliance` + buildQuery({ protocol_id: protocolId }));
}
