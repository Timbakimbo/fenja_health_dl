import { Inbox } from 'lucide-react';
import type { ReactNode } from 'react';

interface Props {
  message: string;
  action?: ReactNode;
}

export default function EmptyState({ message, action }: Props) {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <Inbox className="w-10 h-10 text-gray-300 mb-3" />
      <p className="text-gray-500 mb-4">{message}</p>
      {action}
    </div>
  );
}
