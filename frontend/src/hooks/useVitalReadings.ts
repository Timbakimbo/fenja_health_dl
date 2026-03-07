import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { listVitalReadings, createVitalReading, updateVitalReading, deleteVitalReading } from '../api/vital-readings';
import type { VitalReadingCreate, VitalReadingUpdate } from '../api/types';

const KEY = 'vital-readings';

export function useVitalReadingList(params: {
  page?: number; page_size?: number; marker_type?: string; source?: string;
  from_date?: string; to_date?: string;
} = {}) {
  return useQuery({
    queryKey: [KEY, params],
    queryFn: () => listVitalReadings(params),
  });
}

export function useCreateVitalReading() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: VitalReadingCreate) => createVitalReading(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}

export function useUpdateVitalReading() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: VitalReadingUpdate }) => updateVitalReading(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}

export function useDeleteVitalReading() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteVitalReading(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}
