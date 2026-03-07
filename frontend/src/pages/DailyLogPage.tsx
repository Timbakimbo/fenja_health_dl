import { useParams, useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import PageHeader from '../components/layout/PageHeader';
import DatePickerComp from '../components/shared/DatePicker';
import DailyLogForm from '../components/daily-log/DailyLogForm';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import { useDailyLogsByDate, useCreateDailyLog, useUpdateDailyLog } from '../hooks/useDailyLogs';
import { useState } from 'react';
import type { DailyLogCreate } from '../api/types';

export default function DailyLogPage() {
  const { date: paramDate } = useParams();
  const navigate = useNavigate();
  const [selectedDate, setSelectedDate] = useState(
    paramDate ?? format(new Date(), 'yyyy-MM-dd'),
  );

  const { data, isLoading, error, refetch } = useDailyLogsByDate(selectedDate);
  const existing = data?.items?.[0];

  const createMut = useCreateDailyLog();
  const updateMut = useUpdateDailyLog();

  const [toast, setToast] = useState('');

  function handleSubmit(formData: DailyLogCreate) {
    const cleaned = Object.fromEntries(
      Object.entries({ ...formData, date: selectedDate }).filter(
        ([, v]) => v !== undefined && v !== '' && !Number.isNaN(v),
      ),
    ) as unknown as DailyLogCreate;

    if (existing) {
      updateMut.mutate(
        { id: existing.id, data: cleaned },
        {
          onSuccess: () => {
            setToast('Gespeichert!');
            setTimeout(() => navigate('/'), 1200);
          },
        },
      );
    } else {
      createMut.mutate(cleaned, {
        onSuccess: () => {
          setToast('Gespeichert!');
          setTimeout(() => navigate('/'), 1200);
        },
      });
    }
  }

  return (
    <div>
      <PageHeader title="Tages-Log" />
      <div className="max-w-lg mx-auto px-4 pt-4">
        <div className="flex justify-center mb-4">
          <DatePickerComp value={selectedDate} onChange={setSelectedDate} />
        </div>

        {isLoading && <LoadingSpinner />}
        {error && <ErrorMessage message="Daten konnten nicht geladen werden" onRetry={refetch} />}
        {!isLoading && !error && (
          <DailyLogForm
            key={selectedDate + (existing?.id ?? 'new')}
            date={selectedDate}
            existing={existing}
            onSubmit={handleSubmit}
            isPending={createMut.isPending || updateMut.isPending}
          />
        )}
      </div>

      {toast && (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 bg-success text-white px-6 py-3 rounded-xl shadow-lg z-50 animate-pulse">
          {toast}
        </div>
      )}
    </div>
  );
}
