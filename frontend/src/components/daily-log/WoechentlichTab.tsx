import { useFormContext, Controller } from 'react-hook-form';
import ScalePicker from '../shared/ScalePicker';
import type { DailyLogCreate } from '../../api/types';

export default function WoechentlichTab() {
  const { register, control } = useFormContext<DailyLogCreate>();

  return (
    <div className="space-y-6 tab-enter">
      {/* Gewicht */}
      <div>
        <label className="block text-sm font-semibold text-warm-brown mb-2">
          Gewicht (kg)
        </label>
        <input
          type="number"
          step="0.1"
          {...register('food_offered_g', { valueAsNumber: true })}
          placeholder="z.B. 42.5"
          className="w-full h-12 px-4 rounded-xl bg-warm-brown/5 text-warm-brown placeholder:text-clay/50 focus:outline-none focus:ring-2 focus:ring-primary/30"
        />
      </div>

      {/* Fell */}
      <div>
        <label className="block text-sm font-semibold text-warm-brown mb-2">
          Fell
        </label>
        <Controller
          name="coat_condition"
          control={control}
          render={({ field }) => (
            <ScalePicker
              value={field.value}
              onChange={field.onChange}
              min={1}
              max={5}
              size="md"
              labels={['Sehr schlecht', 'Schlecht', 'Mittel', 'Gut', 'Sehr gut']}
            />
          )}
        />
      </div>

      {/* Muskulatur */}
      <div>
        <label className="block text-sm font-semibold text-warm-brown mb-2">
          Muskulatur
        </label>
        <Controller
          name="muscle_wasting"
          control={control}
          render={({ field }) => (
            <ScalePicker
              value={field.value}
              onChange={field.onChange}
              min={1}
              max={5}
              size="md"
              labels={['Stark abgebaut', 'Abgebaut', 'Normal', 'Gut', 'Sehr gut']}
            />
          )}
        />
      </div>

      {/* Schmerz (Glasgow CMPS-SF) */}
      <div>
        <label className="block text-sm font-semibold text-warm-brown mb-2">
          Schmerz (Glasgow 0–24)
        </label>
        <Controller
          name="pain_score"
          control={control}
          render={({ field }) => (
            <div>
              <input
                type="range"
                min={0}
                max={24}
                value={field.value ?? 0}
                onChange={(e) => field.onChange(Number(e.target.value))}
                className="w-full accent-primary"
              />
              <div className="flex justify-between text-xs text-clay mt-1">
                <span>0</span>
                <span className="font-semibold text-warm-brown">
                  {field.value ?? 0}
                </span>
                <span>24</span>
              </div>
            </div>
          )}
        />
      </div>
    </div>
  );
}
