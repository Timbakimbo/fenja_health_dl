import { useFormContext } from 'react-hook-form';
import ScalePicker from '../shared/ScalePicker';
import type { DailyLogCreate } from '../../api/types';

const colors = ['braun', 'gelb', 'grau', 'schwarz'] as const;

export default function StoolSection() {
  const { watch, setValue } = useFormContext<DailyLogCreate>();
  const consistency = watch('stool_consistency');
  const color = watch('stool_color');
  const flatulence = watch('flatulence');

  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-medium text-gray-700 mb-2 block">
          Konsistenz (1=waessrig, 5=fest)
        </label>
        <ScalePicker
          value={consistency}
          onChange={(v) => setValue('stool_consistency', v)}
          min={1}
          max={5}
          labels={['Waessrig', 'Breiig', 'Weich', 'Geformt', 'Fest']}
        />
      </div>
      <div>
        <label className="text-sm font-medium text-gray-700 mb-2 block">Farbe</label>
        <div className="flex gap-2 flex-wrap">
          {colors.map((c) => (
            <button
              key={c}
              type="button"
              onClick={() => setValue('stool_color', c)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                color === c
                  ? 'bg-primary text-white'
                  : 'bg-gray-100 text-gray-700 active:bg-gray-200'
              }`}
            >
              {c.charAt(0).toUpperCase() + c.slice(1)}
            </button>
          ))}
        </div>
      </div>
      <label className="flex items-center gap-3 cursor-pointer">
        <div
          role="switch"
          aria-checked={!!flatulence}
          onClick={() => setValue('flatulence', !flatulence)}
          className={`w-11 h-6 rounded-full relative transition-colors ${
            flatulence ? 'bg-primary' : 'bg-gray-300'
          }`}
        >
          <div
            className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform ${
              flatulence ? 'translate-x-5.5' : 'translate-x-0.5'
            }`}
          />
        </div>
        <span className="text-sm text-gray-700">Blaehungen</span>
      </label>
    </div>
  );
}
