import { get, post, patch, del, buildQuery } from './client';
import type {
  PaginatedResponse,
  TreatmentTemplateCreate, TreatmentTemplateRead,
  TreatmentProtocolCreate, TreatmentProtocolUpdate, TreatmentProtocolRead,
  TreatmentEntryCreate, TreatmentEntryUpdate, TreatmentEntryRead,
} from './types';

// Templates
const TEMPLATES = '/api/treatment-templates';

export function listTemplates(params: { page?: number; page_size?: number; category?: string } = {}) {
  return get<PaginatedResponse<TreatmentTemplateRead>>(TEMPLATES + buildQuery(params));
}

export function createTemplate(data: TreatmentTemplateCreate) {
  return post<TreatmentTemplateRead>(TEMPLATES, data);
}

// Protocols
const PROTOCOLS = '/api/treatment-protocols';

export function listProtocols(params: {
  page?: number; page_size?: number; active?: boolean; category?: string;
} = {}) {
  return get<PaginatedResponse<TreatmentProtocolRead>>(PROTOCOLS + buildQuery(params));
}

export function getProtocol(id: number) {
  return get<TreatmentProtocolRead>(`${PROTOCOLS}/${id}`);
}

export function createProtocol(data: TreatmentProtocolCreate) {
  return post<TreatmentProtocolRead>(PROTOCOLS, data);
}

export function updateProtocol(id: number, data: TreatmentProtocolUpdate) {
  return patch<TreatmentProtocolRead>(`${PROTOCOLS}/${id}`, data);
}

export function deleteProtocol(id: number) {
  return del(`${PROTOCOLS}/${id}`);
}

// Entries
export function listEntries(protocolId: number, params: {
  page?: number; page_size?: number; from_date?: string; to_date?: string; skipped_only?: boolean;
} = {}) {
  return get<PaginatedResponse<TreatmentEntryRead>>(
    `${PROTOCOLS}/${protocolId}/entries` + buildQuery(params),
  );
}

export function createEntry(protocolId: number, data: TreatmentEntryCreate) {
  return post<TreatmentEntryRead>(`${PROTOCOLS}/${protocolId}/entries`, data);
}

export function updateEntry(protocolId: number, entryId: number, data: TreatmentEntryUpdate) {
  return patch<TreatmentEntryRead>(`${PROTOCOLS}/${protocolId}/entries/${entryId}`, data);
}

export function deleteEntry(protocolId: number, entryId: number) {
  return del(`${PROTOCOLS}/${protocolId}/entries/${entryId}`);
}
