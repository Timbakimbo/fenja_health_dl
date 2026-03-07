import { useQuery } from '@tanstack/react-query';
import { getWeightTrend, getB12Trend, getStoolTrend, getWeeklySummary, getMonthlySummary, getTreatmentCompliance } from '../api/insights';

const KEY = 'insights';

export function useWeightTrend() {
  return useQuery({
    queryKey: [KEY, 'weight-trend'],
    queryFn: getWeightTrend,
  });
}

export function useB12Trend() {
  return useQuery({
    queryKey: [KEY, 'b12-trend'],
    queryFn: getB12Trend,
  });
}

export function useStoolTrend() {
  return useQuery({
    queryKey: [KEY, 'stool-trend'],
    queryFn: getStoolTrend,
  });
}

export function useWeeklySummary(date?: string) {
  return useQuery({
    queryKey: [KEY, 'weekly-summary', date],
    queryFn: () => getWeeklySummary(date),
  });
}

export function useMonthlySummary(year: number, month: number) {
  return useQuery({
    queryKey: [KEY, 'monthly-summary', year, month],
    queryFn: () => getMonthlySummary(year, month),
  });
}

export function useTreatmentCompliance(protocolId: number | undefined) {
  return useQuery({
    queryKey: [KEY, 'compliance', protocolId],
    queryFn: () => getTreatmentCompliance(protocolId!),
    enabled: protocolId != null,
  });
}
