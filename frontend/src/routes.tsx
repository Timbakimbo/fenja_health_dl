import { createBrowserRouter } from 'react-router-dom';
import AppShell from './components/layout/AppShell';
import DashboardPage from './pages/DashboardPage';
import DailyLogPage from './pages/DailyLogPage';
import DailyLogHistoryPage from './pages/DailyLogHistoryPage';
import TrendsPage from './pages/TrendsPage';
import TreatmentsPage from './pages/TreatmentsPage';
import LabResultsPage from './pages/LabResultsPage';
import VetVisitsPage from './pages/VetVisitsPage';

export const router = createBrowserRouter([
  {
    element: <AppShell />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'log', element: <DailyLogPage /> },
      { path: 'log/:date', element: <DailyLogPage /> },
      { path: 'history', element: <DailyLogHistoryPage /> },
      { path: 'trends', element: <TrendsPage /> },
      { path: 'treatments', element: <TreatmentsPage /> },
      { path: 'labs', element: <LabResultsPage /> },
      { path: 'vet', element: <VetVisitsPage /> },
    ],
  },
]);
