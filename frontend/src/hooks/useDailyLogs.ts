import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { listDailyLogs, getDailyLog, createDailyLog, updateDailyLog, deleteDailyLog } from '../api/daily-logs';
import type { DailyLogCreate, DailyLogUpdate } from '../api/types';

const KEY = 'daily-logs';

export function useDailyLogList(params: {
  page?: number; page_size?: number; from_date?: string; to_date?: string;
} = {}) {
  return useQuery({
    queryKey: [KEY, params],
    queryFn: () => listDailyLogs(params),
  });
}

export function useDailyLog(id: number | undefined) {
  return useQuery({
    queryKey: [KEY, id],
    queryFn: () => getDailyLog(id!),
    enabled: id != null,
  });
}

export function useDailyLogsByDate(date: string) {
  return useQuery({
    queryKey: [KEY, 'by-date', date],
    queryFn: () => listDailyLogs({ from_date: date, to_date: date, page_size: 1 }),
  });
}

export function useCreateDailyLog() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: DailyLogCreate) => createDailyLog(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}

export function useUpdateDailyLog() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: DailyLogUpdate }) => updateDailyLog(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}

export function useDeleteDailyLog() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteDailyLog(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}
