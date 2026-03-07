interface Props {
  value: number | null | undefined;
  onChange: (val: number) => void;
  min?: number;
  max?: number;
  labels?: string[];
  size?: 'sm' | 'md' | 'lg';
  colorMap?: Record<number, string>;
}

export default function ScalePicker({ value, onChange, min = 1, max = 5, labels, size = 'md', colorMap }: Props) {
  const count = max - min + 1;
  const items = Array.from({ length: count }, (_, i) => min + i);
  const dim =
    size === 'sm' ? 'w-9 h-9 text-sm' :
    size === 'lg' ? 'w-14 h-14 text-lg' :
    'w-11 h-11 text-base';

  return (
    <div className="flex gap-2 flex-wrap">
      {items.map((n) => {
        const isSelected = value === n;
        const mappedColor = colorMap?.[n];
        let colorClasses: string;

        if (isSelected && mappedColor) {
          colorClasses = `text-white shadow-md scale-105`;
        } else if (isSelected) {
          colorClasses = 'bg-primary text-white shadow-md scale-105';
        } else {
          colorClasses = 'bg-warm-brown/5 text-warm-brown active:bg-warm-brown/10';
        }

        return (
          <button
            key={n}
            type="button"
            onClick={() => onChange(n)}
            className={`${dim} rounded-full font-medium flex items-center justify-center transition-all duration-150 active:scale-95 ${colorClasses}`}
            style={isSelected && mappedColor ? { backgroundColor: mappedColor } : undefined}
            title={labels?.[n - min]}
          >
            {n}
          </button>
        );
      })}
    </div>
  );
}
