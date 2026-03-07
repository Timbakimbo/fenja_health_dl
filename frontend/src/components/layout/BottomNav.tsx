import { NavLink } from 'react-router-dom';
import { Home, PlusCircle, TrendingUp, Pill } from 'lucide-react';

const tabs = [
  { to: '/', icon: Home, label: 'Dashboard' },
  { to: '/log', icon: PlusCircle, label: 'Logbuch' },
  { to: '/trends', icon: TrendingUp, label: 'Trends' },
  { to: '/treatments', icon: Pill, label: 'Behandlung' },
] as const;

export default function BottomNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-cream shadow-[0_-2px_12px_rgba(61,43,31,0.08)] z-50">
      <div className="max-w-lg mx-auto flex">
        {tabs.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex-1 flex flex-col items-center py-2 text-xs transition-colors min-h-[56px] justify-center ${
                isActive ? 'text-primary font-semibold' : 'text-clay'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <Icon className="w-6 h-6 mb-0.5" />
                {label}
                {isActive && (
                  <span className="w-1 h-1 rounded-full bg-primary mt-0.5" />
                )}
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}
