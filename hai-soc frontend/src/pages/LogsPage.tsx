import React, { useState } from 'react';
import { useSecurityLogs } from '../hooks/useSocData';
import { SecurityLogsTable } from '../components/tables/SecurityLogsTable';
import { DashboardCard } from '../components/cards/DashboardCard';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { Drawer } from '../components/common/Drawer';
import { SecurityLog } from '../types/index';
import { formatDateTime } from '../utils/formatters';
import { Download, RefreshCw, FileText } from 'lucide-react';

export const LogsPage: React.FC = () => {
  const { logs, loading, refetch } = useSecurityLogs();
  const [selectedLog, setSelectedLog] = useState<SecurityLog | null>(null);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <FileText className="w-6 h-6 text-cyan-400" />
            Healthcare Security Logs
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time audit trails from Epic Hyperspace, PACS Radiology, Pyxis Dispensing, and IoMT telemetry.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => refetch()}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-300 hover:text-white hover:border-slate-700 transition-colors font-mono"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Refresh Stream
          </button>
          <button
            onClick={() => alert('Exporting log stream in CEF / Syslog format...')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-cyan-950 border border-cyan-800 rounded-lg text-xs text-cyan-300 hover:bg-cyan-900 transition-colors font-mono"
          >
            <Download className="w-3.5 h-3.5" />
            Export CEF
          </button>
        </div>
      </div>

      {/* Main Table */}
      <DashboardCard
        title="Ingested Audit Logs"
        subtitle="Searchable security events across clinical systems"
      >
        {loading ? (
          <LoadingSkeleton rows={10} />
        ) : (
          <SecurityLogsTable logs={logs} onSelectLog={setSelectedLog} />
        )}
      </DashboardCard>

      {/* Log Payload Drawer */}
      {selectedLog && (
        <Drawer
          isOpen={!!selectedLog}
          onClose={() => setSelectedLog(null)}
          title={`Log Payload Inspection: ${selectedLog.id}`}
          subtitle={`Ingested via ${selectedLog.source}`}
        >
          <div className="space-y-4 text-xs font-mono">
            <div className="grid grid-cols-2 gap-3 p-4 bg-slate-950 rounded-xl border border-slate-800">
              <div>
                <span className="text-slate-500 uppercase">Timestamp:</span>
                <p className="text-slate-200 font-bold">{formatDateTime(selectedLog.timestamp)}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">User / Principal:</span>
                <p className="text-cyan-400 font-bold">{selectedLog.user}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">Department:</span>
                <p className="text-slate-300">{selectedLog.department}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">Action Trigger:</span>
                <p className="text-slate-200">{selectedLog.action}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">Outcome Status:</span>
                <p className="text-emerald-400 font-bold">{selectedLog.outcome}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">Severity:</span>
                <p className="text-red-400 font-bold">{selectedLog.severity}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">Origin IP:</span>
                <p className="text-purple-400">{selectedLog.ipAddress || '10.240.12.88'}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase">Resource GUID:</span>
                <p className="text-slate-400">{selectedLog.resourceId || 'PHI-REF-01'}</p>
              </div>
            </div>

            <div>
              <h4 className="font-bold text-slate-200 mb-2 uppercase">Diagnostic Summary</h4>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-slate-300">
                {selectedLog.details || 'Standard transactional audit log entry.'}
              </div>
            </div>

            <div>
              <h4 className="font-bold text-slate-200 mb-2 uppercase">Full Structured Event (JSON)</h4>
              <pre className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-cyan-300 font-mono text-[11px] overflow-x-auto">
                {JSON.stringify(selectedLog, null, 2)}
              </pre>
            </div>
          </div>
        </Drawer>
      )}
    </div>
  );
};
