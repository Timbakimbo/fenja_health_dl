import { useFormContext } from 'react-hook-form';
import ScalePicker from '../shared/ScalePicker';
import type { DailyLogCreate } from '../../api/types';

export default function CoatSection() {
  const { watch, setValue } = useFormContext<DailyLogCreate>();

  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-medium text-gray-700 mb-2 block">Fellzustand</label>
        <ScalePicker
          value={watch('coat_condition')}
          onChange={(v) => setValue('coat_condition', v)}
          size="sm"
        />
      </div>
      <div>
        <label className="text-sm font-medium text-gray-700 mb-2 block">Muskelschwund</label>
        <ScalePicker
          value={watch('muscle_wasting')}
          onChange={(v) => setValue('muscle_wasting', v)}
          size="sm"
        />
      </div>
    </div>
  );
}
