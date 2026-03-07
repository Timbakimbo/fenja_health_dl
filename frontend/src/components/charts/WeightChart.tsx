import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { format, parseISO } from 'date-fns';
import type { WeightTrendPoint } from '../../api/types';

interface Props {
  data: WeightTrendPoint[];
}

export default function WeightChart({ data }: Props) {
  const chartData = data.map((p) => ({
    date: format(parseISO(p.timestamp), 'dd.MM'),
    timestamp: p.timestamp,
    weight_kg: p.weight_kg,
    source: p.source,
  }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis
          domain={['auto', 'auto']}
          tick={{ fontSize: 12 }}
          width={45}
          tickFormatter={(v: number) => `${v} kg`}
        />
        <Tooltip
          formatter={(value) => [`${Number(value).toFixed(1)} kg`, 'Gewicht']}
          labelFormatter={(label) => String(label)}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="weight_kg"
          name="Gewicht"
          stroke="#2563eb"
          strokeWidth={2}
          dot={{ r: 3 }}
          activeDot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
