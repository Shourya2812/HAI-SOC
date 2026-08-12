import React, { useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import {
  FileText,
  BrainCircuit,
  AlertTriangle,
  Flame,
  ArrowUpRight,
  Sparkles,
} from 'lucide-react';
import { useDashboardData, useSecurityLogs, useIncidents } from '../hooks/useSocData';
import { MetricCard } from '../components/cards/MetricCard';
import { DashboardCard } from '../components/cards/DashboardCard';
import { ChartCard } from '../components/cards/ChartCard';
import { AnomalyTrendChart } from '../components/charts/AnomalyTrendChart';
import { TopSourcesChart } from '../components/charts/TopSourcesChart';
import { RiskDistributionChart } from '../components/charts/RiskDistributionChart';
import { ModelUsageChart } from '../components/charts/ModelUsageChart';
import { SecurityLogsTable } from '../components/tables/SecurityLogsTable';
import { IncidentsTable } from '../components/tables/IncidentsTable';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { Drawer } from '../components/common/Drawer';
import { SecurityLog, SecurityIncident } from '../types/index';
import { formatDateTime } from '../utils/formatters';

export const DashboardPage: React.FC = () => {
  const { selectedHospital } = useOutletContext<{ selectedHospital: string }>();
  const {
    loading,
    overview,
    riskDistribution,
    sources,
    models,
    anomalyTrend,
  } = useDashboardData(selectedHospital);

  const { logs } = useSecurityLogs();
  const { incidents } = useIncidents();

  const [selectedLog, setSelectedLog] = useState<SecurityLog | null>(null);
  const [selectedIncident, setSelectedIncident] = useState<SecurityIncident | null>(null);

  if (loading || !overview) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <LoadingSkeleton rows={2} />
          <LoadingSkeleton rows={2} />
          <LoadingSkeleton rows={2} />
          <LoadingSkeleton rows={2} />
        </div>
        <LoadingSkeleton rows={6} />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Banner / Hero Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-cyan-950/40 border border-slate-800 relative overflow-hidden">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-950 text-cyan-400 border border-cyan-800/60 uppercase font-mono">
              Live SOC Monitoring
            </span>
            <span className="text-xs text-slate-400 font-mono">
              Facility: <strong className="text-slate-200">{selectedHospital}</strong>
            </span>
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
            Healthcare Security Operations Center
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl">
            Real-time machine learning anomaly engine monitoring EHR transactions, IoMT medical telemetry, and hospital IT infrastructure.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-right font-mono">
            <div className="text-[10px] uppercase text-slate-500">AI Threat Confidence</div>
            <div className="text-lg font-bold text-cyan-400 flex items-center justify-end gap-1">
              <Sparkles className="w-4 h-4 text-purple-400" />
              99.2%
            </div>
          </div>
        </div>
      </div>

      {/* Top KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Ingested Logs"
          value={overview.totalLogs}
          trendPct={overview.logsTrendPct}
          icon={FileText}
          subtitle="All EHR & IoMT events"
          glowColor="cyan"
        />
        <MetricCard
          title="Today's ML Anomalies"
          value={overview.todaysAnomalies}
          trendPct={overview.anomaliesTrendPct}
          icon={BrainCircuit}
          subtitle="Isolation Forest & Autoencoder"
          glowColor="purple"
        />
        <MetricCard
          title="Open Security Incidents"
          value={overview.openIncidents}
          trendPct={overview.incidentsTrendPct}
          icon={AlertTriangle}
          subtitle="Active SOC investigation"
          glowColor="amber"
        />
        <MetricCard
          title="Critical Incidents"
          value={overview.criticalIncidents}
          trendPct={overview.criticalTrendPct}
          icon={Flame}
          subtitle="Immediate containment required"
          glowColor="red"
          isCritical={overview.criticalIncidents > 0}
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Line Chart: Daily Anomaly Trend */}
        <ChartCard
          title="Daily Anomaly Trend"
          subtitle="24-Hour ML anomaly detections vs baseline telemetry"
          height="h-72"
        >
          <AnomalyTrendChart data={anomalyTrend} />
        </ChartCard>

        {/* Bar Chart: Top Log Sources */}
        <ChartCard
          title="Top Log Sources"
          subtitle="Inbound security log volume by clinical subsystem"
          height="h-72"
        >
          <TopSourcesChart data={sources} />
        </ChartCard>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Pie Chart: Risk Distribution */}
        <ChartCard
          title="Anomaly Risk Distribution"
          subtitle="Classification breakdown of active healthcare threats"
          height="h-64"
        >
          <RiskDistributionChart data={riskDistribution} />
        </ChartCard>

        {/* Donut Chart: Model Usage */}
        <ChartCard
          title="ML Model Inference Usage"
          subtitle="Active neural networks and isolation forest engines"
          height="h-64"
        >
          <ModelUsageChart data={models} />
        </ChartCard>
      </div>

      {/* Tables Section */}
      <div className="space-y-6">
        {/* Recent Incidents Table */}
        <DashboardCard
          title="Active Security Incidents"
          subtitle="Automated incident response cases requiring analyst attention"
        >
          <IncidentsTable
            incidents={incidents.slice(0, 5)}
            onSelectIncident={setSelectedIncident}
          />
        </DashboardCard>

        {/* Recent Security Logs Table */}
        <DashboardCard
          title="Recent Security Logs"
          subtitle="Live telemetry feed across EHR, PACS, Pyxis, and IoMT devices"
        >
          <SecurityLogsTable
            logs={logs.slice(0, 5)}
            onSelectLog={setSelectedLog}
          />
        </DashboardCard>
      </div>

      {/* Log Detail Drawer */}
      {selectedLog && (
        <Drawer
          isOpen={!!selectedLog}
          onClose={() => setSelectedLog(null)}
          title={`Log Details: ${selectedLog.id}`}
          subtitle={`Source: ${selectedLog.source}`}
        >
          <div className="space-y-4 text-xs">
            <div className="grid grid-cols-2 gap-3 p-3 bg-slate-950 rounded-xl border border-slate-800 font-mono">
              <div>
                <span className="text-slate-500 uppercase">Timestamp:</span>
                <p className="text-slate-200 font-bold">{formatDateTime(selectedLog.timestamp)}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">User:</span>
                <p className="text-cyan-400 font-bold">{selectedLog.user}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">Action:</span>
                <p className="text-slate-200">{selectedLog.action}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">Department:</span>
                <p className="text-slate-200">{selectedLog.department}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">IP Address:</span>
                <p className="text-purple-400">{selectedLog.ipAddress || '10.240.12.88'}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">Resource ID:</span>
                <p className="text-slate-300">{selectedLog.resourceId || 'N/A'}</p>
              </div>
            </div>

            <div>
              <h4 className="font-bold text-slate-200 mb-1 uppercase font-mono">Raw Payload Details</h4>
              <pre className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-emerald-400 font-mono text-[11px] overflow-x-auto whitespace-pre-wrap">
                {JSON.stringify(selectedLog, null, 2)}
              </pre>
            </div>
          </div>
        </Drawer>
      )}

      {/* Incident Detail Drawer */}
      {selectedIncident && (
        <Drawer
          isOpen={!!selectedIncident}
          onClose={() => setSelectedIncident(null)}
          title={`Incident Investigation: ${selectedIncident.incidentId}`}
          subtitle={selectedIncident.title}
        >
          <div className="space-y-5 text-xs">
            <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-slate-400 font-mono">AI Prediction Score</span>
                <span className="font-mono font-bold text-red-400">{selectedIncident.predictionScore}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                <div
                  className="h-full bg-red-500"
                  style={{ width: `${selectedIncident.predictionScore}%` }}
                ></div>
              </div>
            </div>

            <div>
              <h4 className="font-bold text-slate-200 mb-1 uppercase font-mono">Recommended Action</h4>
              <p className="p-3 bg-cyan-950/40 border border-cyan-800/60 rounded-xl text-cyan-200 font-mono">
                {selectedIncident.recommendedAction}
              </p>
            </div>

            <div>
              <h4 className="font-bold text-slate-200 mb-2 uppercase font-mono">SOC Analyst Investigation Notes</h4>
              <ul className="space-y-2 font-mono text-[11px] text-slate-300">
                {selectedIncident.investigationNotes?.map((note, i) => (
                  <li key={i} className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 flex items-start gap-2">
                    <ArrowUpRight className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                    <span>{note}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </Drawer>
      )}
    </div>
  );
};
