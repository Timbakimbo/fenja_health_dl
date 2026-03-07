import { LineChart, Line, ResponsiveContainer } from 'recharts';

interface Props {
  data: { value: number }[];
  color?: string;
  height?: number;
}

export default function MiniSparkline({ data, color = '#2563eb', height = 40 }: Props) {
  if (data.length < 2) return null;

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data}>
        <Line
          type="monotone"
          dataKey="value"
          stroke={color}
          strokeWidth={2}
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
