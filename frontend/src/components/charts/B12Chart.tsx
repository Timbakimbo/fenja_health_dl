import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer } from 'recharts';
import { format, parseISO } from 'date-fns';
import type { B12TrendPoint } from '../../api/types';

interface Props {
  data: B12TrendPoint[];
}

const DEFICIENCY_THRESHOLD = 250;

export default function B12Chart({ data }: Props) {
  const chartData = data.map((p) => ({
    date: format(parseISO(p.timestamp), 'dd.MM'),
    b12: p.cobalamin_b12,
  }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} width={55} tickFormatter={(v: number) => `${v}`} />
        <Tooltip
          formatter={(value) => [`${Number(value).toFixed(0)} pg/mL`, 'B12']}
        />
        <ReferenceLine
          y={DEFICIENCY_THRESHOLD}
          stroke="#dc2626"
          strokeDasharray="4 4"
          label={{ value: 'Mangel', position: 'right', fill: '#dc2626', fontSize: 12 }}
        />
        <Line
          type="monotone"
          dataKey="b12"
          name="Cobalamin B12"
          stroke="#16a34a"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
