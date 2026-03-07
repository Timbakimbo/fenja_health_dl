import { useFormContext } from 'react-hook-form';
import type { DailyLogCreate } from '../../api/types';

export default function QuickNotes() {
  const { register } = useFormContext<DailyLogCreate>();

  return (
    <div>
      <label className="text-sm font-medium text-gray-700 mb-1 block">Notizen</label>
      <textarea
        {...register('notes')}
        rows={3}
        className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-base resize-y"
        placeholder="Beobachtungen, Besonderheiten..."
      />
    </div>
  );
}
