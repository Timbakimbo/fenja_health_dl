import { useFormContext } from 'react-hook-form';
import ScalePicker from '../shared/ScalePicker';
import type { DailyLogCreate } from '../../api/types';

const fields = [
  { name: 'energy_level' as const, label: 'Energie' },
  { name: 'willingness_to_walk' as const, label: 'Lauffreude' },
  { name: 'play_interest' as const, label: 'Spielinteresse' },
];

export default function EnergySection() {
  const { watch, setValue } = useFormContext<DailyLogCreate>();

  return (
    <div className="space-y-4">
      {fields.map(({ name, label }) => (
        <div key={name}>
          <label className="text-sm font-medium text-gray-700 mb-2 block">{label}</label>
          <ScalePicker
            value={watch(name)}
            onChange={(v) => setValue(name, v)}
            size="sm"
          />
        </div>
      ))}
    </div>
  );
}
