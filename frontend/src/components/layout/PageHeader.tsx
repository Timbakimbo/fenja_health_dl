import { useNavigate } from 'react-router-dom';
import { ChevronLeft } from 'lucide-react';

interface Props {
  title: string;
  back?: boolean;
}

export default function PageHeader({ title, back }: Props) {
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 bg-white border-b border-gray-200 z-40">
      <div className="max-w-lg mx-auto flex items-center h-12 px-4">
        {back && (
          <button
            onClick={() => navigate(-1)}
            className="mr-2 -ml-2 p-2 rounded-lg active:bg-gray-100"
            aria-label="Zurueck"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
        )}
        <h1 className="text-lg font-semibold truncate">{title}</h1>
      </div>
    </header>
  );
}
