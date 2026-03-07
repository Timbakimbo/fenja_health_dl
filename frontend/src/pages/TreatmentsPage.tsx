import PageHeader from '../components/layout/PageHeader';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import EmptyState from '../components/shared/EmptyState';
import ProtocolCard from '../components/treatments/ProtocolCard';
import { useProtocolList, useUpdateEntry } from '../hooks/useTreatments';
import type { TreatmentEntryRead } from '../api/types';

export default function TreatmentsPage() {
  const { data, isLoading, error, refetch } = useProtocolList({ active: true });
  const updateEntry = useUpdateEntry();

  function handleAdminister(entry: TreatmentEntryRead) {
    updateEntry.mutate({
      protocolId: entry.protocol_id,
      entryId: entry.id,
      data: { administered_at: new Date().toISOString() },
    });
  }

  return (
    <div>
      <PageHeader title="Behandlungen" />
      <div className="max-w-lg mx-auto px-4 pt-4 space-y-4">
        {isLoading && <LoadingSpinner />}
        {error && <ErrorMessage message="Behandlungen konnten nicht geladen werden" onRetry={refetch} />}
        {data && data.items.length === 0 && (
          <EmptyState message="Keine aktiven Behandlungen" />
        )}
        {data?.items.map((protocol) => (
          <ProtocolCard
            key={protocol.id}
            protocol={protocol}
            onAdminister={handleAdminister}
          />
        ))}
      </div>
    </div>
  );
}
