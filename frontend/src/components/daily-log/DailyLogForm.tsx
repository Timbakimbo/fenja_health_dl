import { useState } from 'react';
import { useForm, FormProvider } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import DailyLogTabs, { type TabKey } from './DailyLogTabs';
import HeuteTab from './HeuteTab';
import WoechentlichTab from './WoechentlichTab';
import BehandlungTab from './BehandlungTab';
import type { DailyLogCreate, DailyLogRead } from '../../api/types';

const schema = z.object({
  date: z.string(),
  stool_consistency: z.number().min(1).max(5).nullable().optional(),
  stool_color: z.string().nullable().optional(),
  flatulence: z.boolean().nullable().optional(),
  food_offered_g: z.number().positive().nullable().optional(),
  food_eaten_g: z.number().min(0).nullable().optional(),
  water_intake: z.string().nullable().optional(),
  vomiting: z.boolean().nullable().optional(),
  vomiting_count: z.number().min(0).nullable().optional(),
  energy_level: z.number().min(1).max(5).nullable().optional(),
  willingness_to_walk: z.number().min(1).max(5).nullable().optional(),
  play_interest: z.number().min(1).max(5).nullable().optional(),
  pain_score: z.number().min(0).max(24).nullable().optional(),
  lameness_score: z.number().min(0).max(4).nullable().optional(),
  affected_limb: z.string().nullable().optional(),
  stiffness_after_rest: z.boolean().nullable().optional(),
  coat_condition: z.number().min(1).max(5).nullable().optional(),
  muscle_wasting: z.number().min(1).max(5).nullable().optional(),
  notes: z.string().nullable().optional(),
});

interface Props {
  date: string;
  existing?: DailyLogRead;
  onSubmit: (data: DailyLogCreate) => void;
  isPending: boolean;
}

export default function DailyLogForm({ date, existing, onSubmit, isPending }: Props) {
  const [activeTab, setActiveTab] = useState<TabKey>('heute');

  const methods = useForm<DailyLogCreate>({
    resolver: zodResolver(schema),
    defaultValues: {
      date,
      stool_consistency: existing?.stool_consistency ?? undefined,
      stool_color: existing?.stool_color ?? undefined,
      flatulence: existing?.flatulence ?? undefined,
      food_offered_g: existing?.food_offered_g ?? undefined,
      food_eaten_g: existing?.food_eaten_g ?? undefined,
      water_intake: existing?.water_intake ?? undefined,
      vomiting: existing?.vomiting ?? undefined,
      vomiting_count: existing?.vomiting_count ?? undefined,
      energy_level: existing?.energy_level ?? undefined,
      willingness_to_walk: existing?.willingness_to_walk ?? undefined,
      play_interest: existing?.play_interest ?? undefined,
      pain_score: existing?.pain_score ?? undefined,
      lameness_score: existing?.lameness_score ?? undefined,
      affected_limb: existing?.affected_limb ?? undefined,
      stiffness_after_rest: existing?.stiffness_after_rest ?? undefined,
      coat_condition: existing?.coat_condition ?? undefined,
      muscle_wasting: existing?.muscle_wasting ?? undefined,
      notes: existing?.notes ?? undefined,
    },
  });

  const showSaveButton = activeTab !== 'behandlung';

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)} className="pb-24">
        <DailyLogTabs active={activeTab} onChange={setActiveTab} />

        {activeTab === 'heute' && <HeuteTab />}
        {activeTab === 'woechentlich' && <WoechentlichTab />}
        {activeTab === 'behandlung' && <BehandlungTab />}

        {showSaveButton && (
          <div className="fixed bottom-16 left-0 right-0 p-4 z-30">
            <div className="max-w-lg mx-auto">
              <button
                type="submit"
                disabled={isPending}
                className="w-full py-3.5 bg-primary text-white rounded-2xl font-semibold text-base shadow-md active:scale-[0.98] disabled:opacity-50 transition-all duration-150"
              >
                {isPending ? 'Speichern...' : existing ? 'Aktualisieren' : 'Speichern'}
              </button>
            </div>
          </div>
        )}
      </form>
    </FormProvider>
  );
}
