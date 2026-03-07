import { get, post, patch, del, buildQuery } from './client';
import type { PaginatedResponse, VetVisitCreate, VetVisitUpdate, VetVisitRead } from './types';

const BASE = '/api/vet-visits';

export function listVetVisits(params: {
  page?: number; page_size?: number; from_date?: string; to_date?: string;
} = {}) {
  return get<PaginatedResponse<VetVisitRead>>(BASE + buildQuery(params));
}

export function getVetVisit(id: number) {
  return get<VetVisitRead>(`${BASE}/${id}`);
}

export function createVetVisit(data: VetVisitCreate) {
  return post<VetVisitRead>(BASE, data);
}

export function updateVetVisit(id: number, data: VetVisitUpdate) {
  return patch<VetVisitRead>(`${BASE}/${id}`, data);
}

export function deleteVetVisit(id: number) {
  return del(`${BASE}/${id}`);
}
