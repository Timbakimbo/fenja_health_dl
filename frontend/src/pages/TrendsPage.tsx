import { useState } from 'react';
import PageHeader from '../components/layout/PageHeader';
import Card from '../components/shared/Card';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import EmptyState from '../components/shared/EmptyState';
import WeightChart from '../components/charts/WeightChart';
import B12Chart from '../components/charts/B12Chart';
import StoolChart from '../components/charts/StoolChart';
import { useWeightTrend, useB12Trend, useStoolTrend } from '../hooks/useInsights';
import { subDays } from 'date-fns';

type Range = '30d' | '90d' | 'all';

function filterByRange<T extends { timestamp?: string; date?: string }>(
  data: T[],
  range: Range,
): T[] {
  if (range === 'all') return data;
  const days = range === '30d' ? 30 : 90;
  const cutoff = subDays(new Date(), days).getTime();
  return data.filter((p) => {
    const raw = p.timestamp ?? (p.date ? `${p.date}T00:00:00` : null);
    if (!raw) return false;
    const parsed = new Date(raw).getTime();
    return Number.isFinite(parsed) && parsed >= cutoff;
  });
}

export default function TrendsPage() {
  const [range, setRange] = useState<Range>('30d');
  const weight = useWeightTrend();
  const b12 = useB12Trend();
  const stool = useStoolTrend();

  const isLoading = weight.isLoading || b12.isLoading || stool.isLoading;
  const error = weight.error || b12.error || stool.error;

  return (
    <div>
      <PageHeader title="Trends" />
      <div className="max-w-lg mx-auto px-4 pt-4 space-y-4">
        {/* Range Selector */}
        <div className="flex gap-2 justify-center">
          {(['30d', '90d', 'all'] as Range[]).map((r) => (
            <button
              key={r}
              onClick={() => setRange(r)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                range === r
                  ? 'bg-primary text-white'
                  : 'bg-gray-100 text-gray-600 active:bg-gray-200'
              }`}
            >
              {r === 'all' ? 'Alle' : r}
            </button>
          ))}
        </div>

        {isLoading && <LoadingSpinner />}
        {error && <ErrorMessage message="Trend-Daten konnten nicht geladen werden" />}

        {!isLoading && !error && (
          <>
            <Card>
              <h2 className="font-semibold text-gray-900 mb-3">Gewicht</h2>
              {weight.data?.length ? (
                <WeightChart data={filterByRange(weight.data, range)} />
              ) : (
                <EmptyState message="Keine Gewichtsdaten vorhanden" />
              )}
            </Card>

            <Card>
              <h2 className="font-semibold text-gray-900 mb-3">Cobalamin B12</h2>
              {b12.data?.length ? (
                <B12Chart data={filterByRange(b12.data, range)} />
              ) : (
                <EmptyState message="Keine B12-Daten vorhanden" />
              )}
            </Card>

            <Card>
              <h2 className="font-semibold text-gray-900 mb-3">Stuhlkonsistenz</h2>
              {stool.data?.length ? (
                <StoolChart data={filterByRange(stool.data, range)} />
              ) : (
                <EmptyState message="Keine Stuhldaten vorhanden" />
              )}
            </Card>
          </>
        )}
      </div>
    </div>
  );
}
