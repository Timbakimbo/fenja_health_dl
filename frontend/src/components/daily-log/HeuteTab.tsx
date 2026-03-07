import { useFormContext, Controller } from 'react-hook-form';
import ScalePicker from '../shared/ScalePicker';
import type { DailyLogCreate } from '../../api/types';

const STOOL_COLOR_MAP: Record<number, string> = {
  1: '#C53030',
  2: '#C53030',
  3: '#2F855A',
  4: '#D69E2E',
  5: '#D69E2E',
};

export default function HeuteTab() {
  const { control, watch, setValue } = useFormContext<DailyLogCreate>();
  const vomiting = watch('vomiting');

  return (
    <div className="space-y-8 tab-enter">
      {/* Energie */}
      <div>
        <label className="block text-base font-semibold text-warm-brown mb-3">
          Energie
        </label>
        <Controller
          name="energy_level"
          control={control}
          render={({ field }) => (
            <ScalePicker
              value={field.value}
              onChange={field.onChange}
              min={1}
              max={5}
              size="lg"
              labels={['Sehr schlecht', 'Schlecht', 'Mittel', 'Gut', 'Sehr gut']}
            />
          )}
        />
      </div>

      {/* Erbrechen */}
      <div>
        <label className="block text-base font-semibold text-warm-brown mb-3">
          Erbrechen
        </label>
        <button
          type="button"
          onClick={() => setValue('vomiting', !vomiting, { shouldDirty: true })}
          className={`w-full h-14 rounded-2xl font-semibold text-base transition-all duration-150 active:scale-[0.98] ${
            vomiting
              ? 'bg-danger text-white shadow-md'
              : 'bg-warm-brown/5 text-warm-brown'
          }`}
        >
          {vomiting ? 'Ja — Erbrechen' : 'Nein'}
        </button>
      </div>

      {/* Stuhlkonsistenz */}
      <div>
        <label className="block text-base font-semibold text-warm-brown mb-3">
          Stuhlkonsistenz
        </label>
        <Controller
          name="stool_consistency"
          control={control}
          render={({ field }) => (
            <ScalePicker
              value={field.value}
              onChange={field.onChange}
              min={1}
              max={5}
              size="lg"
              colorMap={STOOL_COLOR_MAP}
              labels={['Waessrig', 'Weich', 'Normal', 'Fest', 'Hart']}
            />
          )}
        />
      </div>
    </div>
  );
}
