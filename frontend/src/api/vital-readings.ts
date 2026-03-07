import { get, post, patch, del, buildQuery } from './client';
import type { PaginatedResponse, VitalReadingCreate, VitalReadingUpdate, VitalReadingRead } from './types';

const BASE = '/api/vital-readings';

export function listVitalReadings(params: {
  page?: number; page_size?: number; marker_type?: string; source?: string;
  from_date?: string; to_date?: string;
} = {}) {
  return get<PaginatedResponse<VitalReadingRead>>(BASE + buildQuery(params));
}

export function getVitalReading(id: number) {
  return get<VitalReadingRead>(`${BASE}/${id}`);
}

export function createVitalReading(data: VitalReadingCreate) {
  return post<VitalReadingRead>(BASE, data);
}

export function updateVitalReading(id: number, data: VitalReadingUpdate) {
  return patch<VitalReadingRead>(`${BASE}/${id}`, data);
}

export function deleteVitalReading(id: number) {
  return del(`${BASE}/${id}`);
}
