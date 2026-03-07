import type { ReactNode } from 'react';

interface Props {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
}

export default function Card({ children, className = '', onClick }: Props) {
  const base = 'bg-sand rounded-2xl shadow-sm shadow-warm-brown/5 p-4';
  const interactive = onClick ? 'cursor-pointer active:bg-sand/80' : '';
  return (
    <div className={`${base} ${interactive} ${className}`} onClick={onClick}>
      {children}
    </div>
  );
}
