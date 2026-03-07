import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { format, parseISO } from 'date-fns';
import { de } from 'date-fns/locale';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import Card from '../components/shared/Card';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import EmptyState from '../components/shared/EmptyState';
import { useDailyLogList } from '../hooks/useDailyLogs';

export default function DailyLogHistoryPage() {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const { data, isLoading, error, refetch } = useDailyLogList({ page, page_size: 20 });

  return (
    <div>
      <PageHeader title="Verlauf" back />
      <div className="max-w-lg mx-auto px-4 pt-4 space-y-3">
        {isLoading && <LoadingSpinner />}
        {error && <ErrorMessage message="Verlauf konnte nicht geladen werden" onRetry={refetch} />}
        {data && data.items.length === 0 && (
          <EmptyState message="Noch keine Eintraege vorhanden" />
        )}
        {data?.items.map((log) => (
          <Card
            key={log.id}
            onClick={() => navigate(`/log/${log.date}`)}
            className="cursor-pointer"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900">
                  {format(parseISO(log.date + 'T00:00:00'), 'EEEE, dd. MMM yyyy', { locale: de })}
                </p>
                <div className="flex gap-3 mt-1 text-xs text-gray-500">
                  {log.stool_consistency != null && <span>Stuhl: {log.stool_consistency}/5</span>}
                  {log.energy_level != null && <span>Energie: {log.energy_level}/5</span>}
                  {log.appetite_ratio != null && (
                    <span>Appetit: {Math.round(log.appetite_ratio * 100)}%</span>
                  )}
                </div>
              </div>
              <ChevronRight className="w-5 h-5 text-gray-300" />
            </div>
          </Card>
        ))}

        {data && data.pages > 1 && (
          <div className="flex items-center justify-center gap-4 py-4">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-2 rounded-lg active:bg-gray-100 disabled:opacity-30"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <span className="text-sm text-gray-600">
              {page} / {data.pages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(data.pages, p + 1))}
              disabled={page >= data.pages}
              className="p-2 rounded-lg active:bg-gray-100 disabled:opacity-30"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
