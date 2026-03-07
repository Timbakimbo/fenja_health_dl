import { get, post, patch, del, buildQuery } from './client';
import type { PaginatedResponse, DailyLogCreate, DailyLogUpdate, DailyLogRead } from './types';

const BASE = '/api/daily-logs';

export function listDailyLogs(params: {
  page?: number;
  page_size?: number;
  from_date?: string;
  to_date?: string;
} = {}) {
  return get<PaginatedResponse<DailyLogRead>>(BASE + buildQuery(params));
}

export function getDailyLog(id: number) {
  return get<DailyLogRead>(`${BASE}/${id}`);
}

export function createDailyLog(data: DailyLogCreate) {
  return post<DailyLogRead>(BASE, data);
}

export function updateDailyLog(id: number, data: DailyLogUpdate) {
  return patch<DailyLogRead>(`${BASE}/${id}`, data);
}

export function deleteDailyLog(id: number) {
  return del(`${BASE}/${id}`);
}
