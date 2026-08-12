import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from './components/layout/AppLayout';
import { DashboardPage } from './pages/DashboardPage';
import { LogsPage } from './pages/LogsPage';
import { IncidentsPage } from './pages/IncidentsPage';
import { AnomaliesPage } from './pages/AnomaliesPage';
import { ThreatIntelPage } from './pages/ThreatIntelPage';
import { MitrePage } from './pages/MitrePage';
import { HipaaPage } from './pages/HipaaPage';
import { PlaybooksPage } from './pages/PlaybooksPage';
import { SettingsPage } from './pages/SettingsPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="logs" element={<LogsPage />} />
          <Route path="incidents" element={<IncidentsPage />} />
          <Route path="anomalies" element={<AnomaliesPage />} />
          <Route path="threat-intel" element={<ThreatIntelPage />} />
          <Route path="mitre" element={<MitrePage />} />
          <Route path="hipaa" element={<HipaaPage />} />
          <Route path="playbooks" element={<PlaybooksPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
