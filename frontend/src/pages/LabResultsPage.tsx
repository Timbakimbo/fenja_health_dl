import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { format, parseISO } from 'date-fns';
import { de } from 'date-fns/locale';
import { Plus, X } from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import Card from '../components/shared/Card';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import EmptyState from '../components/shared/EmptyState';
import { useHealthMarkerList, useCreateHealthMarker } from '../hooks/useHealthMarkers';
import type { HealthMarkerCreate } from '../api/types';

const fields: { name: keyof HealthMarkerCreate; label: string; unit: string }[] = [
  { name: 'weight_kg', label: 'Gewicht', unit: 'kg' },
  { name: 'ctli', label: 'cTLI', unit: 'ug/L' },
  { name: 'cobalamin_b12', label: 'Cobalamin B12', unit: 'pg/mL' },
  { name: 'folate', label: 'Folsaeure', unit: 'ng/mL' },
  { name: 'lipase', label: 'Lipase', unit: 'U/L' },
  { name: 'amylase', label: 'Amylase', unit: 'U/L' },
  { name: 'glucose', label: 'Glukose', unit: 'mg/dL' },
  { name: 'vitamin_e', label: 'Vitamin E', unit: 'mg/L' },
  { name: 'vitamin_k', label: 'Vitamin K', unit: 'ng/mL' },
];

export default function LabResultsPage() {
  const [showForm, setShowForm] = useState(false);
  const { data, isLoading, error, refetch } = useHealthMarkerList({ page_size: 50 });
  const createMut = useCreateHealthMarker();
  const { register, handleSubmit, reset } = useForm<HealthMarkerCreate>();

  function onSubmit(formData: HealthMarkerCreate) {
    const cleaned = Object.fromEntries(
      Object.entries(formData).filter(([, v]) => v !== '' && v != null && !Number.isNaN(v)),
    ) as HealthMarkerCreate;

    createMut.mutate(cleaned, {
      onSuccess: () => {
        setShowForm(false);
        reset();
      },
    });
  }

  return (
    <div>
      <PageHeader title="Laborwerte" back />
      <div className="max-w-lg mx-auto px-4 pt-4 space-y-4">
        <button
          onClick={() => setShowForm(!showForm)}
          className="w-full flex items-center justify-center gap-2 py-3 bg-primary text-white rounded-xl font-semibold active:bg-primary-dark transition-colors"
        >
          {showForm ? <X className="w-5 h-5" /> : <Plus className="w-5 h-5" />}
          {showForm ? 'Abbrechen' : 'Neue Laborwerte'}
        </button>

        {showForm && (
          <Card>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
              {fields.map(({ name, label, unit }) => (
                <div key={name} className="flex items-center gap-3">
                  <label className="text-sm text-gray-700 w-28 flex-shrink-0">{label}</label>
                  <input
                    type="number"
                    step="any"
                    inputMode="decimal"
                    {...register(name as keyof HealthMarkerCreate, { valueAsNumber: true })}
                    className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-base"
                    placeholder="–"
                  />
                  <span className="text-xs text-gray-400 w-14">{unit}</span>
                </div>
              ))}
              <button
                type="submit"
                disabled={createMut.isPending}
                className="w-full py-2.5 bg-primary text-white rounded-xl font-semibold active:bg-primary-dark disabled:opacity-50"
              >
                {createMut.isPending ? 'Speichern...' : 'Speichern'}
              </button>
            </form>
          </Card>
        )}

        {isLoading && <LoadingSpinner />}
        {error && <ErrorMessage message="Laborwerte konnten nicht geladen werden" onRetry={refetch} />}
        {data && data.items.length === 0 && !showForm && (
          <EmptyState message="Noch keine Laborwerte vorhanden" />
        )}
        {data?.items.map((marker) => (
          <Card key={marker.id}>
            <p className="text-sm font-medium text-gray-900 mb-2">
              {format(parseISO(marker.timestamp), 'dd. MMM yyyy, HH:mm', { locale: de })}
            </p>
            <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-sm">
              {fields.map(({ name, label, unit }) => {
                const val = marker[name as keyof typeof marker];
                if (val == null) return null;
                return (
                  <div key={name} className="flex justify-between">
                    <span className="text-gray-500">{label}</span>
                    <span className="font-medium">
                      {typeof val === 'number' ? val.toFixed(1) : val} {unit}
                    </span>
                  </div>
                );
              })}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
