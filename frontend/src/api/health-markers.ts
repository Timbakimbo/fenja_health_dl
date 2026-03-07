import { get, post, patch, del, buildQuery } from './client';
import type { PaginatedResponse, HealthMarkerCreate, HealthMarkerUpdate, HealthMarkerRead } from './types';

const BASE = '/api/health-markers';

export function listHealthMarkers(params: {
  page?: number;
  page_size?: number;
  from_date?: string;
  to_date?: string;
} = {}) {
  return get<PaginatedResponse<HealthMarkerRead>>(BASE + buildQuery(params));
}

export function getHealthMarker(id: number) {
  return get<HealthMarkerRead>(`${BASE}/${id}`);
}

export function createHealthMarker(data: HealthMarkerCreate) {
  return post<HealthMarkerRead>(BASE, data);
}

export function updateHealthMarker(id: number, data: HealthMarkerUpdate) {
  return patch<HealthMarkerRead>(`${BASE}/${id}`, data);
}

export function deleteHealthMarker(id: number) {
  return del(`${BASE}/${id}`);
}
