import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { format, parseISO } from 'date-fns';
import type { StoolTrendPoint } from '../../api/types';

interface Props {
  data: StoolTrendPoint[];
}

function getColor(consistency: number): string {
  if (consistency <= 2) return '#dc2626'; // rot — zu weich
  if (consistency === 3) return '#16a34a'; // gruen — ideal
  return '#d97706'; // gelb — zu fest
}

export default function StoolChart({ data }: Props) {
  const chartData = data.map((p) => ({
    date: format(parseISO(p.date + 'T00:00:00'), 'dd.MM'),
    consistency: p.stool_consistency,
    color: p.stool_color,
  }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis domain={[0, 5]} ticks={[1, 2, 3, 4, 5]} tick={{ fontSize: 12 }} width={30} />
        <Tooltip
          formatter={(value) => [`${value}/5`, 'Konsistenz']}
        />
        <Bar dataKey="consistency" name="Konsistenz" radius={[4, 4, 0, 0]}>
          {chartData.map((entry, idx) => (
            <Cell key={idx} fill={getColor(entry.consistency)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
