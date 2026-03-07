import { format } from 'date-fns';
import Card from '../shared/Card';
import LoadingSpinner from '../shared/LoadingSpinner';
import { useProtocolList, useCreateEntry } from '../../hooks/useTreatments';

export default function BehandlungTab() {
  const { data, isLoading } = useProtocolList({ active: true });
  const createEntry = useCreateEntry();

  const protocols = data?.items ?? [];

  function handleAdminister(protocolId: number) {
    const now = new Date();
    createEntry.mutate({
      protocolId,
      data: {
        scheduled_date: format(now, 'yyyy-MM-dd'),
        administered_at: now.toISOString(),
      },
    });
  }

  if (isLoading) return <LoadingSpinner />;

  if (protocols.length === 0) {
    return (
      <div className="tab-enter text-center py-12">
        <p className="text-clay text-sm">Keine aktiven Behandlungen</p>
      </div>
    );
  }

  return (
    <div className="space-y-4 tab-enter">
      {protocols.map((protocol) => (
        <Card key={protocol.id}>
          <h3 className="font-semibold text-warm-brown">{protocol.name}</h3>
          <p className="text-sm text-clay mt-1">{protocol.category}</p>
          {protocol.current_phase && (
            <p className="text-xs text-clay mt-1">
              Phase: {JSON.stringify(protocol.current_phase)}
            </p>
          )}
          <button
            type="button"
            onClick={() => handleAdminister(protocol.id)}
            disabled={createEntry.isPending}
            className="mt-3 w-full h-12 rounded-xl bg-primary text-white font-semibold text-sm active:scale-[0.98] transition-all duration-150 disabled:opacity-50"
          >
            {createEntry.isPending ? 'Speichern...' : 'Gabe dokumentieren'}
          </button>
        </Card>
      ))}
    </div>
  );
}
