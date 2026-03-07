import type { ReactNode } from 'react';

interface Props {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
}

export default function Card({ children, className = '', onClick }: Props) {
  const base = 'bg-white rounded-xl border border-gray-200 p-4';
  const interactive = onClick ? 'cursor-pointer active:bg-gray-50' : '';
  return (
    <div className={`${base} ${interactive} ${className}`} onClick={onClick}>
      {children}
    </div>
  );
}
