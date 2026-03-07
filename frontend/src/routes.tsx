import { Suspense, lazy } from 'react';
import { createBrowserRouter } from 'react-router-dom';
import AppShell from './components/layout/AppShell';
import LoadingSpinner from './components/shared/LoadingSpinner';

const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const DailyLogPage = lazy(() => import('./pages/DailyLogPage'));
const DailyLogHistoryPage = lazy(() => import('./pages/DailyLogHistoryPage'));
const TrendsPage = lazy(() => import('./pages/TrendsPage'));
const TreatmentsPage = lazy(() => import('./pages/TreatmentsPage'));
const LabResultsPage = lazy(() => import('./pages/LabResultsPage'));
const VetVisitsPage = lazy(() => import('./pages/VetVisitsPage'));

function withSuspense(element: React.ReactNode) {
  return (
    <Suspense
      fallback={
        <div className="max-w-lg mx-auto px-4 py-8">
          <LoadingSpinner />
        </div>
      }
    >
      {element}
    </Suspense>
  );
}

export const router = createBrowserRouter([
  {
    element: <AppShell />,
    children: [
      { index: true, element: withSuspense(<DashboardPage />) },
      { path: 'log', element: withSuspense(<DailyLogPage />) },
      { path: 'log/:date', element: withSuspense(<DailyLogPage />) },
      { path: 'history', element: withSuspense(<DailyLogHistoryPage />) },
      { path: 'trends', element: withSuspense(<TrendsPage />) },
      { path: 'treatments', element: withSuspense(<TreatmentsPage />) },
      { path: 'labs', element: withSuspense(<LabResultsPage />) },
      { path: 'vet', element: withSuspense(<VetVisitsPage />) },
    ],
  },
]);
