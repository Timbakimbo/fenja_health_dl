import { format, parseISO } from 'date-fns';
import { de } from 'date-fns/locale';
import { Check, X, Clock } from 'lucide-react';
import type { TreatmentEntryRead } from '../../api/types';

interface Props {
  entries: TreatmentEntryRead[];
  onAdminister: (entry: TreatmentEntryRead) => void;
}

export default function EntryChecklist({ entries, onAdminister }: Props) {
  const sorted = [...entries].sort(
    (a, b) => b.scheduled_date.localeCompare(a.scheduled_date),
  );

  return (
    <div className="space-y-2">
      {sorted.map((entry) => {
        const administered = !!entry.administered_at;
        const skipped = entry.was_skipped;

        return (
          <div
            key={entry.id}
            className="flex items-center gap-3 py-2 border-b border-gray-100 last:border-0"
          >
            {administered ? (
              <div className="w-7 h-7 rounded-full bg-green-100 flex items-center justify-center">
                <Check className="w-4 h-4 text-green-600" />
              </div>
            ) : skipped ? (
              <div className="w-7 h-7 rounded-full bg-red-100 flex items-center justify-center">
                <X className="w-4 h-4 text-red-600" />
              </div>
            ) : (
              <button
                onClick={() => onAdminister(entry)}
                className="w-7 h-7 rounded-full bg-gray-100 flex items-center justify-center active:bg-primary active:text-white transition-colors"
              >
                <Clock className="w-4 h-4 text-gray-400" />
              </button>
            )}
            <div className="flex-1 min-w-0">
              <p className="text-sm text-gray-900">
                {format(parseISO(entry.scheduled_date + 'T00:00:00'), 'dd. MMM', { locale: de })}
              </p>
              {entry.dose && (
                <p className="text-xs text-gray-500">
                  {entry.dose} {entry.unit}
                </p>
              )}
            </div>
            {administered && entry.administered_at && (
              <span className="text-xs text-gray-400">
                {format(parseISO(entry.administered_at), 'HH:mm')}
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
}
