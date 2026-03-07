export type TabKey = 'heute' | 'woechentlich' | 'behandlung';

interface Props {
  active: TabKey;
  onChange: (tab: TabKey) => void;
}

const tabs: { key: TabKey; label: string }[] = [
  { key: 'heute', label: 'Heute' },
  { key: 'woechentlich', label: 'Woechentlich' },
  { key: 'behandlung', label: 'Behandlung' },
];

export default function DailyLogTabs({ active, onChange }: Props) {
  return (
    <div className="flex border-b border-warm-brown/10 mb-6">
      {tabs.map(({ key, label }) => (
        <button
          key={key}
          type="button"
          onClick={() => onChange(key)}
          className={`flex-1 pb-3 text-sm font-medium transition-colors ${
            active === key
              ? 'border-b-2 border-primary text-warm-brown font-semibold'
              : 'text-clay'
          }`}
        >
          {label}
        </button>
      ))}
    </div>
  );
}
