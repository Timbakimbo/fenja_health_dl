import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { listVetVisits, getVetVisit, createVetVisit, updateVetVisit, deleteVetVisit } from '../api/vet-visits';
import type { VetVisitCreate, VetVisitUpdate } from '../api/types';

const KEY = 'vet-visits';

export function useVetVisitList(params: {
  page?: number; page_size?: number; from_date?: string; to_date?: string;
} = {}) {
  return useQuery({
    queryKey: [KEY, params],
    queryFn: () => listVetVisits(params),
  });
}

export function useVetVisit(id: number | undefined) {
  return useQuery({
    queryKey: [KEY, id],
    queryFn: () => getVetVisit(id!),
    enabled: id != null,
  });
}

export function useCreateVetVisit() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: VetVisitCreate) => createVetVisit(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}

export function useUpdateVetVisit() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: VetVisitUpdate }) => updateVetVisit(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}

export function useDeleteVetVisit() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteVetVisit(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: [KEY] }),
  });
}
