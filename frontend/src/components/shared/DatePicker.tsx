import { format } from 'date-fns';
import { de } from 'date-fns/locale';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface Props {
  value: string; // YYYY-MM-DD
  onChange: (date: string) => void;
}

export default function DatePicker({ value, onChange }: Props) {
  const date = new Date(value + 'T00:00:00');
  const today = format(new Date(), 'yyyy-MM-dd');
  const isToday = value === today;

  function shift(days: number) {
    const d = new Date(date);
    d.setDate(d.getDate() + days);
    onChange(format(d, 'yyyy-MM-dd'));
  }

  return (
    <div className="flex items-center gap-2">
      <button
        type="button"
        onClick={() => shift(-1)}
        className="p-2 rounded-lg active:bg-gray-100"
        aria-label="Vorheriger Tag"
      >
        <ChevronLeft className="w-5 h-5" />
      </button>
      <div className="flex flex-col items-center">
        <input
          type="date"
          value={value}
          max={today}
          onChange={(e) => onChange(e.target.value)}
          className="text-center font-medium bg-transparent border-none text-base"
        />
        <span className="text-xs text-gray-500">
          {isToday ? 'Heute' : format(date, 'EEEE', { locale: de })}
        </span>
      </div>
      <button
        type="button"
        onClick={() => shift(1)}
        disabled={isToday}
        className="p-2 rounded-lg active:bg-gray-100 disabled:opacity-30"
        aria-label="Naechster Tag"
      >
        <ChevronRight className="w-5 h-5" />
      </button>
    </div>
  );
}
