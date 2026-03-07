import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { format, parseISO } from 'date-fns';
import { de } from 'date-fns/locale';
import { Plus, X, Stethoscope } from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import Card from '../components/shared/Card';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import EmptyState from '../components/shared/EmptyState';
import { useVetVisitList, useCreateVetVisit } from '../hooks/useVetVisits';
import type { VetVisitCreate } from '../api/types';

export default function VetVisitsPage() {
  const [showForm, setShowForm] = useState(false);
  const { data, isLoading, error, refetch } = useVetVisitList({ page_size: 50 });
  const createMut = useCreateVetVisit();
  const { register, handleSubmit, reset } = useForm<VetVisitCreate>();

  function onSubmit(formData: VetVisitCreate) {
    const cleaned = Object.fromEntries(
      Object.entries(formData).filter(([, v]) => v !== '' && v != null),
    ) as VetVisitCreate;

    createMut.mutate(cleaned, {
      onSuccess: () => {
        setShowForm(false);
        reset();
      },
    });
  }

  return (
    <div>
      <PageHeader title="Tierarztbesuche" back />
      <div className="max-w-lg mx-auto px-4 pt-4 space-y-4">
        <button
          onClick={() => setShowForm(!showForm)}
          className="w-full flex items-center justify-center gap-2 py-3 bg-primary text-white rounded-xl font-semibold active:bg-primary-dark transition-colors"
        >
          {showForm ? <X className="w-5 h-5" /> : <Plus className="w-5 h-5" />}
          {showForm ? 'Abbrechen' : 'Neuer Besuch'}
        </button>

        {showForm && (
          <Card>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-700 mb-1 block">Grund *</label>
                <input
                  {...register('reason', { required: true })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-base"
                  placeholder="Kontrolluntersuchung..."
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-sm font-medium text-gray-700 mb-1 block">Tierarzt</label>
                  <input
                    {...register('vet_name')}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-base"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-700 mb-1 block">Klinik</label>
                  <input
                    {...register('clinic')}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-base"
                  />
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700 mb-1 block">Diagnose</label>
                <input
                  {...register('diagnosis')}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-base"
                />
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700 mb-1 block">Befunde</label>
                <textarea
                  {...register('findings')}
                  rows={2}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-base resize-y"
                />
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700 mb-1 block">Notizen</label>
                <textarea
                  {...register('notes')}
                  rows={2}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-base resize-y"
                />
              </div>
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
        {error && <ErrorMessage message="Besuche konnten nicht geladen werden" onRetry={refetch} />}
        {data && data.items.length === 0 && !showForm && (
          <EmptyState message="Noch keine Tierarztbesuche eingetragen" />
        )}
        {data?.items.map((visit) => (
          <Card key={visit.id}>
            <div className="flex items-start gap-3">
              <div className="w-9 h-9 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 mt-0.5">
                <Stethoscope className="w-4 h-4 text-primary" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900">{visit.reason}</p>
                <p className="text-xs text-gray-500 mt-0.5">
                  {format(parseISO(visit.timestamp), 'dd. MMM yyyy', { locale: de })}
                  {visit.vet_name && ` — ${visit.vet_name}`}
                  {visit.clinic && ` (${visit.clinic})`}
                </p>
                {visit.diagnosis && (
                  <p className="text-sm text-gray-700 mt-2">
                    <span className="font-medium">Diagnose:</span> {visit.diagnosis}
                  </p>
                )}
                {visit.findings && (
                  <p className="text-sm text-gray-600 mt-1">{visit.findings}</p>
                )}
                {visit.notes && (
                  <p className="text-sm text-gray-500 mt-1 italic">{visit.notes}</p>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
