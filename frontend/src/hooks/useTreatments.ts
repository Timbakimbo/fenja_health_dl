import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  listProtocols, getProtocol, createProtocol, updateProtocol, deleteProtocol,
  listEntries, createEntry, updateEntry, deleteEntry,
} from '../api/treatments';
import type {
  TreatmentProtocolCreate, TreatmentProtocolUpdate,
  TreatmentEntryCreate, TreatmentEntryUpdate,
} from '../api/types';

const PKEY = 'treatment-protocols';
const EKEY = 'treatment-entries';

export function useProtocolList(params: {
  page?: number; page_size?: number; active?: boolean; category?: string;
} = {}) {
  return useQuery({
    queryKey: [PKEY, params],
    queryFn: () => listProtocols(params),
  });
}

export function useProtocol(id: number | undefined) {
  return useQuery({
    queryKey: [PKEY, id],
    queryFn: () => getProtocol(id!),
    enabled: id != null,
  });
}

export function useCreateProtocol() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: TreatmentProtocolCreate) => createProtocol(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: [PKEY] }),
  });
}

export function useUpdateProtocol() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: TreatmentProtocolUpdate }) => updateProtocol(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: [PKEY] }),
  });
}

export function useDeleteProtocol() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteProtocol(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: [PKEY] }),
  });
}

export function useEntryList(protocolId: number, params: {
  page?: number; page_size?: number; from_date?: string; to_date?: string; skipped_only?: boolean;
} = {}) {
  return useQuery({
    queryKey: [EKEY, protocolId, params],
    queryFn: () => listEntries(protocolId, params),
  });
}

export function useCreateEntry() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ protocolId, data }: { protocolId: number; data: TreatmentEntryCreate }) =>
      createEntry(protocolId, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: [EKEY] });
      qc.invalidateQueries({ queryKey: [PKEY] });
    },
  });
}

export function useUpdateEntry() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ protocolId, entryId, data }: { protocolId: number; entryId: number; data: TreatmentEntryUpdate }) =>
      updateEntry(protocolId, entryId, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: [EKEY] });
      qc.invalidateQueries({ queryKey: [PKEY] });
    },
  });
}

export function useDeleteEntry() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ protocolId, entryId }: { protocolId: number; entryId: number }) =>
      deleteEntry(protocolId, entryId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: [EKEY] });
      qc.invalidateQueries({ queryKey: [PKEY] });
    },
  });
}
