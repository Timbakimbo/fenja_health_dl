import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { listHealthMarkers, getHealthMarker, createHealthMarker, updateHealthMarker, deleteHealthMarker } from '../api/health-markers';
import type { HealthMarkerCreate, HealthMarkerUpdate } from '../api/types';

const KEY = 'health-markers';

export function useHealthMarkerList(params: {
  page?: number; page_size?: number; from_date?: string; to_date?: string;
} = {}) {
  return useQuery({
    queryKey: [KEY, params],
    queryFn: () => listHealthMarkers(params),
  });
}

export function useHealthMarker(id: number | undefined) {
  return useQuery({
    queryKey: [KEY, id],
    queryFn: () => getHealthMarker(id!),
    enabled: id != null,
  });
}

export function useCreateHealthMarker() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: HealthMarkerCreate) => createHealthMarker(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}

export function useUpdateHealthMarker() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: HealthMarkerUpdate }) => updateHealthMarker(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}

export function useDeleteHealthMarker() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteHealthMarker(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}
