interface Props {
  rate: number; // 0-1
}

export default function ComplianceBadge({ rate }: Props) {
  const pct = Math.round(rate * 100);
  const color = pct >= 90 ? 'bg-green-100 text-green-800' :
                pct >= 70 ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800';

  return (
    <span className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold ${color}`}>
      {pct}%
    </span>
  );
}
