import { useFormContext } from 'react-hook-form';
import type { DailyLogCreate } from '../../api/types';

const waterLevels = ['wenig', 'normal', 'viel'] as const;

export default function AppetiteSection() {
  const { register, watch, setValue } = useFormContext<DailyLogCreate>();
  const offered = watch('food_offered_g');
  const eaten = watch('food_eaten_g');
  const water = watch('water_intake');
  const vomiting = watch('vomiting');

  const ratio = offered && eaten ? Math.round((eaten / offered) * 100) : null;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-sm font-medium text-gray-700 mb-1 block">Angeboten (g)</label>
          <input
            type="number"
            inputMode="numeric"
            {...register('food_offered_g', { valueAsNumber: true })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-base"
            placeholder="400"
          />
        </div>
        <div>
          <label className="text-sm font-medium text-gray-700 mb-1 block">Gefressen (g)</label>
          <input
            type="number"
            inputMode="numeric"
            {...register('food_eaten_g', { valueAsNumber: true })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-base"
            placeholder="300"
          />
        </div>
      </div>
      {ratio !== null && (
        <p className="text-sm text-gray-600">
          <span className={`font-semibold ${ratio >= 80 ? 'text-success' : ratio >= 50 ? 'text-warning' : 'text-danger'}`}>
            {ratio}% gefressen
          </span>
        </p>
      )}
      <div>
        <label className="text-sm font-medium text-gray-700 mb-2 block">Wasseraufnahme</label>
        <div className="flex gap-2">
          {waterLevels.map((w) => (
            <button
              key={w}
              type="button"
              onClick={() => setValue('water_intake', w)}
              className={`flex-1 py-2 rounded-full text-sm font-medium transition-colors ${
                water === w
                  ? 'bg-primary text-white'
                  : 'bg-gray-100 text-gray-700 active:bg-gray-200'
              }`}
            >
              {w.charAt(0).toUpperCase() + w.slice(1)}
            </button>
          ))}
        </div>
      </div>
      <div className="space-y-2">
        <label className="flex items-center gap-3 cursor-pointer">
          <div
            role="switch"
            aria-checked={!!vomiting}
            onClick={() => setValue('vomiting', !vomiting)}
            className={`w-11 h-6 rounded-full relative transition-colors ${
              vomiting ? 'bg-danger' : 'bg-gray-300'
            }`}
          >
            <div
              className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform ${
                vomiting ? 'translate-x-5.5' : 'translate-x-0.5'
              }`}
            />
          </div>
          <span className="text-sm text-gray-700">Erbrechen</span>
        </label>
        {vomiting && (
          <div>
            <label className="text-sm text-gray-600 mb-1 block">Wie oft?</label>
            <input
              type="number"
              inputMode="numeric"
              {...register('vomiting_count', { valueAsNumber: true })}
              className="w-20 border border-gray-300 rounded-lg px-3 py-2 text-base"
              min={1}
              placeholder="1"
            />
          </div>
        )}
      </div>
    </div>
  );
}
