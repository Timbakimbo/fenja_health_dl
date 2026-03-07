interface Props {
  value: number | null | undefined;
  onChange: (val: number) => void;
  min?: number;
  max?: number;
  labels?: string[];
  size?: 'sm' | 'md';
}

export default function ScalePicker({ value, onChange, min = 1, max = 5, labels, size = 'md' }: Props) {
  const count = max - min + 1;
  const items = Array.from({ length: count }, (_, i) => min + i);
  const dim = size === 'sm' ? 'w-9 h-9 text-sm' : 'w-11 h-11 text-base';

  return (
    <div className="flex gap-2 flex-wrap">
      {items.map((n) => (
        <button
          key={n}
          type="button"
          onClick={() => onChange(n)}
          className={`${dim} rounded-full font-medium transition-colors flex items-center justify-center ${
            value === n
              ? 'bg-primary text-white'
              : 'bg-gray-100 text-gray-700 active:bg-gray-200'
          }`}
          title={labels?.[n - min]}
        >
          {n}
        </button>
      ))}
    </div>
  );
}
