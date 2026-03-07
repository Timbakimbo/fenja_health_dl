import { useState } from 'react';
import { useForm, FormProvider } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ChevronDown } from 'lucide-react';
import StoolSection from './StoolSection';
import AppetiteSection from './AppetiteSection';
import EnergySection from './EnergySection';
import PainSection from './PainSection';
import CoatSection from './CoatSection';
import QuickNotes from './QuickNotes';
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

const sections = [
  { key: 'stool', title: 'Stuhlgang', component: StoolSection, defaultOpen: true },
  { key: 'appetite', title: 'Appetit', component: AppetiteSection, defaultOpen: true },
  { key: 'energy', title: 'Energie & Verhalten', component: EnergySection, defaultOpen: true },
  { key: 'pain', title: 'Schmerz & Mobilitaet', component: PainSection, defaultOpen: false },
  { key: 'coat', title: 'Fell & Muskulatur', component: CoatSection, defaultOpen: false },
  { key: 'notes', title: 'Notizen', component: QuickNotes, defaultOpen: false },
] as const;

export default function DailyLogForm({ date, existing, onSubmit, isPending }: Props) {
  const [openSections, setOpenSections] = useState<Set<string>>(
    new Set(sections.filter((s) => s.defaultOpen).map((s) => s.key)),
  );

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

  function toggle(key: string) {
    setOpenSections((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });
  }

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)} className="space-y-3 pb-20">
        {sections.map(({ key, title, component: Component }) => (
          <div key={key} className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <button
              type="button"
              onClick={() => toggle(key)}
              className="w-full flex items-center justify-between px-4 py-3 text-left"
            >
              <span className="font-medium text-gray-900">{title}</span>
              <ChevronDown
                className={`w-5 h-5 text-gray-400 transition-transform ${
                  openSections.has(key) ? 'rotate-180' : ''
                }`}
              />
            </button>
            {openSections.has(key) && (
              <div className="px-4 pb-4">
                <Component />
              </div>
            )}
          </div>
        ))}

        <div className="fixed bottom-16 left-0 right-0 p-4 bg-white border-t border-gray-200 z-30">
          <div className="max-w-lg mx-auto">
            <button
              type="submit"
              disabled={isPending}
              className="w-full py-3 bg-primary text-white rounded-xl font-semibold text-base active:bg-primary-dark disabled:opacity-50 transition-colors"
            >
              {isPending ? 'Speichern...' : existing ? 'Aktualisieren' : 'Speichern'}
            </button>
          </div>
        </div>
      </form>
    </FormProvider>
  );
}
