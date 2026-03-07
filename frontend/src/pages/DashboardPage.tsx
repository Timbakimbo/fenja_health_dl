import { useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import { PlusCircle, History, FlaskConical, Stethoscope } from 'lucide-react';
import Card from '../components/shared/Card';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import MiniSparkline from '../components/charts/MiniSparkline';
import { useWeeklySummary, useWeightTrend, useStoolTrend } from '../hooks/useInsights';

export default function DashboardPage() {
  const navigate = useNavigate();
  const todayApi = format(new Date(), 'yyyy-MM-dd');
  const { data: weekly, isLoading } = useWeeklySummary(todayApi);
  const { data: weightData } = useWeightTrend();
  const { data: stoolData } = useStoolTrend();

  const weightSparkline = (weightData ?? []).slice(-14).map((p) => ({ value: p.weight_kg }));
  const stoolSparkline = (stoolData ?? []).slice(-14).map((p) => ({ value: p.stool_consistency }));

  return (
    <div>
      <div className="max-w-lg mx-auto px-4 pt-6 space-y-5">
        {/* Fenja Header */}
        <div className="flex items-center gap-4">
          <img
            src="/icons/fenja-avatar.png"
            alt="Fenja"
            className="w-16 h-16 rounded-full shadow-md object-cover"
          />
          <div>
            <h1 className="text-2xl">Fenja</h1>
            <p className="text-sm text-clay">Altdeutsche Schäferhündin (bestest girl)</p>
          </div>
        </div>

        {/* Quick Action */}
        <button
          onClick={() => navigate('/log')}
          className="w-full flex items-center justify-center gap-2 py-3.5 bg-primary text-white rounded-2xl font-semibold text-base shadow-md active:scale-[0.98] transition-all duration-150"
        >
          <PlusCircle className="w-5 h-5" />
          Heute loggen
        </button>

        {/* Weekly Summary */}
        {isLoading && <LoadingSpinner />}
        {weekly && (
          <Card>
            <h2 className="text-lg mb-3">Woche {weekly.week_start} — {weekly.week_end}</h2>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <SummaryItem label="Tage geloggt" value={`${weekly.days_logged}/7`} />
              <SummaryItem
                label="Energie"
                value={weekly.avg_energy_level?.toFixed(1) ?? '–'}
                suffix="/5"
              />
              <SummaryItem
                label="Stuhl"
                value={weekly.avg_stool_consistency?.toFixed(1) ?? '–'}
                suffix="/5"
              />
              <SummaryItem
                label="Appetit"
                value={weekly.avg_appetite_ratio != null ? `${Math.round(weekly.avg_appetite_ratio * 100)}%` : '–'}
              />
              <SummaryItem
                label="Erbrechen"
                value={String(weekly.total_vomiting_episodes)}
                warn={weekly.total_vomiting_episodes > 0}
              />
              <SummaryItem
                label="Schmerz"
                value={weekly.avg_pain_score?.toFixed(1) ?? '–'}
                suffix="/24"
                warn={(weekly.avg_pain_score ?? 0) > 6}
              />
            </div>
          </Card>
        )}

        {/* Mini Charts */}
        <div className="grid grid-cols-2 gap-3">
          <Card>
            <p className="text-xs font-medium text-clay mb-1">Gewicht</p>
            <MiniSparkline data={weightSparkline} />
            {weightData?.length ? (
              <p className="text-sm font-semibold mt-1">
                {weightData[weightData.length - 1].weight_kg.toFixed(1)} kg
              </p>
            ) : (
              <p className="text-xs text-clay mt-1">Keine Daten</p>
            )}
          </Card>
          <Card>
            <p className="text-xs font-medium text-clay mb-1">Stuhl</p>
            <MiniSparkline data={stoolSparkline} color="#2F855A" />
            {stoolData?.length ? (
              <p className="text-sm font-semibold mt-1">
                {stoolData[stoolData.length - 1].stool_consistency}/5
              </p>
            ) : (
              <p className="text-xs text-clay mt-1">Keine Daten</p>
            )}
          </Card>
        </div>

        {/* Quick Links */}
        <div className="grid grid-cols-3 gap-3">
          <QuickLink icon={History} label="Verlauf" onClick={() => navigate('/history')} />
          <QuickLink icon={FlaskConical} label="Labor" onClick={() => navigate('/labs')} />
          <QuickLink icon={Stethoscope} label="Tierarzt" onClick={() => navigate('/vet')} />
        </div>
      </div>
    </div>
  );
}

function SummaryItem({ label, value, suffix, warn }: {
  label: string; value: string; suffix?: string; warn?: boolean;
}) {
  return (
    <div>
      <p className="text-clay text-xs">{label}</p>
      <p className={`font-semibold ${warn ? 'text-danger' : 'text-warm-brown'}`}>
        {value}{suffix && <span className="text-clay font-normal">{suffix}</span>}
      </p>
    </div>
  );
}

function QuickLink({ icon: Icon, label, onClick }: {
  icon: typeof History; label: string; onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="flex flex-col items-center gap-1 py-3 bg-sand shadow-sm shadow-warm-brown/5 rounded-2xl active:scale-[0.98] transition-all duration-150"
    >
      <Icon className="w-5 h-5 text-clay" />
      <span className="text-xs text-clay">{label}</span>
    </button>
  );
}
