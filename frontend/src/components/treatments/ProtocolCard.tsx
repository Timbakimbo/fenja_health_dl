import { format, parseISO } from 'date-fns';
import { de } from 'date-fns/locale';
import Card from '../shared/Card';
import ComplianceBadge from './ComplianceBadge';
import EntryChecklist from './EntryChecklist';
import { useTreatmentCompliance } from '../../hooks/useInsights';
import type { TreatmentProtocolRead, TreatmentEntryRead } from '../../api/types';

interface Props {
  protocol: TreatmentProtocolRead;
  onAdminister: (entry: TreatmentEntryRead) => void;
}

export default function ProtocolCard({ protocol, onAdminister }: Props) {
  const { data: compliance } = useTreatmentCompliance(protocol.id);

  return (
    <Card>
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-semibold text-gray-900">{protocol.name}</h3>
          <p className="text-xs text-gray-500">
            {protocol.category} — seit{' '}
            {format(parseISO(protocol.start_date + 'T00:00:00'), 'dd. MMM yyyy', { locale: de })}
          </p>
        </div>
        {compliance && <ComplianceBadge rate={compliance.compliance_rate} />}
      </div>

      {protocol.entries.length > 0 ? (
        <EntryChecklist
          entries={protocol.entries.slice(0, 7)}
          onAdminister={onAdminister}
        />
      ) : (
        <p className="text-sm text-gray-400">Keine Eintraege</p>
      )}
    </Card>
  );
}
