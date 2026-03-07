import { useFormContext } from 'react-hook-form';
import ScalePicker from '../shared/ScalePicker';
import type { DailyLogCreate } from '../../api/types';

const limbs = ['VL', 'VR', 'HL', 'HR'] as const;

export default function PainSection() {
  const { register, watch, setValue } = useFormContext<DailyLogCreate>();
  const painScore = watch('pain_score');
  const lamenessScore = watch('lameness_score');
  const affectedLimb = watch('affected_limb');
  const stiffness = watch('stiffness_after_rest');

  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-medium text-gray-700 mb-1 block">
          Schmerzscore (Glasgow CMPS-SF): {painScore ?? '–'}/24
        </label>
        <input
          type="range"
          min={0}
          max={24}
          {...register('pain_score', { valueAsNumber: true })}
          className="w-full accent-primary"
        />
        <div className="flex justify-between text-xs text-gray-400">
          <span>0</span><span>6</span><span>12</span><span>18</span><span>24</span>
        </div>
      </div>
      <div>
        <label className="text-sm font-medium text-gray-700 mb-2 block">Lahmheit (0-4)</label>
        <ScalePicker
          value={lamenessScore}
          onChange={(v) => setValue('lameness_score', v)}
          min={0}
          max={4}
          size="sm"
        />
      </div>
      {(lamenessScore ?? 0) > 0 && (
        <div>
          <label className="text-sm font-medium text-gray-700 mb-2 block">Betroffene Gliedmasse</label>
          <div className="flex gap-2">
            {limbs.map((l) => (
              <button
                key={l}
                type="button"
                onClick={() => setValue('affected_limb', l)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  affectedLimb === l
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-gray-700 active:bg-gray-200'
                }`}
              >
                {l}
              </button>
            ))}
          </div>
        </div>
      )}
      <label className="flex items-center gap-3 cursor-pointer">
        <div
          role="switch"
          aria-checked={!!stiffness}
          onClick={() => setValue('stiffness_after_rest', !stiffness)}
          className={`w-11 h-6 rounded-full relative transition-colors ${
            stiffness ? 'bg-primary' : 'bg-gray-300'
          }`}
        >
          <div
            className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform ${
              stiffness ? 'translate-x-5.5' : 'translate-x-0.5'
            }`}
          />
        </div>
        <span className="text-sm text-gray-700">Steifheit nach Ruhe</span>
      </label>
    </div>
  );
}
