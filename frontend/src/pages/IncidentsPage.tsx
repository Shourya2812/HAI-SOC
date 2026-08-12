import React, { useState } from 'react';
import { useIncidents } from '../hooks/useSocData';
import { IncidentsTable } from '../components/tables/IncidentsTable';
import { DashboardCard } from '../components/cards/DashboardCard';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { Drawer } from '../components/common/Drawer';
import { SecurityIncident } from '../types/index';
import { formatDateTime } from '../utils/formatters';
import { AlertTriangle, Plus, ShieldCheck, ArrowRight, UserCheck, MessageSquare } from 'lucide-react';

export const IncidentsPage: React.FC = () => {
  const { incidents, loading, setIncidents } = useIncidents();
  const [selectedIncident, setSelectedIncident] = useState<SecurityIncident | null>(null);

  const handleStatusChange = (incidentId: string, newStatus: any) => {
    setIncidents((prev) =>
      prev.map((inc) =>
        inc.incidentId === incidentId ? { ...inc, status: newStatus } : inc
      )
    );
    if (selectedIncident && selectedIncident.incidentId === incidentId) {
      setSelectedIncident((prev) => (prev ? { ...prev, status: newStatus } : null));
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <AlertTriangle className="w-6 h-6 text-amber-400" />
            Security Incident Response Cases
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Automated ML-generated cases mapping potential HIPAA breaches, ransomware attempts, and credential theft.
          </p>
        </div>

        <button
          onClick={() => alert('Manual Incident Creation Dialog Opened')}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-cyan-600 to-blue-600 rounded-lg text-xs font-bold text-white shadow-lg hover:from-cyan-500 hover:to-blue-500 transition-all font-mono"
        >
          <Plus className="w-4 h-4" />
          Create Incident Case
        </button>
      </div>

      {/* Main Table */}
      <DashboardCard
        title="Active Incidents Queue"
        subtitle="Cases prioritized by AI prediction risk score and severity"
      >
        {loading ? (
          <LoadingSkeleton rows={8} />
        ) : (
          <IncidentsTable
            incidents={incidents}
            onSelectIncident={setSelectedIncident}
          />
        )}
      </DashboardCard>

      {/* Incident Investigation Drawer */}
      {selectedIncident && (
        <Drawer
          isOpen={!!selectedIncident}
          onClose={() => setSelectedIncident(null)}
          title={`Incident Investigation: ${selectedIncident.incidentId}`}
          subtitle={selectedIncident.title}
        >
          <div className="space-y-6 text-xs font-sans">
            {/* Case Overview Metrics */}
            <div className="grid grid-cols-2 gap-3 p-4 bg-slate-950 rounded-xl border border-slate-800 font-mono">
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Severity:</span>
                <p className="text-red-400 font-bold">{selectedIncident.severity}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Risk Level:</span>
                <p className="text-amber-400 font-bold">{selectedIncident.riskLevel}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Current Status:</span>
                <p className="text-cyan-400 font-bold">{selectedIncident.status}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Assigned Analyst:</span>
                <p className="text-slate-200">{selectedIncident.assignedAnalyst || 'Unassigned'}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Source System:</span>
                <p className="text-slate-300">{selectedIncident.source}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Created At:</span>
                <p className="text-slate-400">{formatDateTime(selectedIncident.createdAt)}</p>
              </div>
            </div>

            {/* Incident Status Workflow Buttons */}
            <div>
              <h4 className="font-bold text-slate-200 mb-2 uppercase font-mono">Change Case Status</h4>
              <div className="flex flex-wrap gap-2">
                {['OPEN', 'INVESTIGATING', 'CONTAINED', 'RESOLVED', 'CLOSED'].map((st) => (
                  <button
                    key={st}
                    onClick={() => handleStatusChange(selectedIncident.incidentId, st)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold border transition-colors ${
                      selectedIncident.status === st
                        ? 'bg-cyan-950 text-cyan-300 border-cyan-500 glow-cyan'
                        : 'bg-slate-950 text-slate-400 border-slate-800 hover:text-white'
                    }`}
                  >
                    {st}
                  </button>
                ))}
              </div>
            </div>

            {/* AI Recommended Action */}
            <div className="p-4 bg-cyan-950/40 border border-cyan-800/60 rounded-xl space-y-2">
              <div className="flex items-center gap-2 font-mono text-cyan-400 font-bold uppercase">
                <ShieldCheck className="w-4 h-4" />
                <span>AI Recommended Containment Action</span>
              </div>
              <p className="text-slate-200 font-mono text-xs">
                {selectedIncident.recommendedAction}
              </p>
            </div>

            {/* MITRE ATT&CK Tactics */}
            {selectedIncident.mitreTactics && selectedIncident.mitreTactics.length > 0 && (
              <div>
                <h4 className="font-bold text-slate-200 mb-2 uppercase font-mono">Mapped MITRE ATT&CK Tactics</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedIncident.mitreTactics.map((tactic, idx) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 bg-purple-950/80 border border-purple-800/60 rounded text-purple-300 font-mono text-[11px]"
                    >
                      {tactic}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Investigation Timeline Notes */}
            <div>
              <h4 className="font-bold text-slate-200 mb-2 uppercase font-mono flex items-center justify-between">
                <span>SOC Analyst Audit Trail</span>
                <button
                  onClick={() => {
                    const note = prompt('Add investigation note:');
                    if (note) {
                      setIncidents((prev) =>
                        prev.map((i) =>
                          i.incidentId === selectedIncident.incidentId
                            ? {
                                ...i,
                                investigationNotes: [
                                  ...(i.investigationNotes || []),
                                  `${new Date().toISOString().substring(11, 16)} UTC - ${note}`,
                                ],
                              }
                            : i
                        )
                      );
                    }
                  }}
                  className="text-[10px] text-cyan-400 hover:underline flex items-center gap-1"
                >
                  <MessageSquare className="w-3 h-3" />
                  + Add Note
                </button>
              </h4>
              <div className="space-y-2 font-mono text-xs">
                {selectedIncident.investigationNotes?.map((note, i) => (
                  <div key={i} className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-start gap-2">
                    <ArrowRight className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                    <span className="text-slate-300">{note}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Drawer>
      )}
    </div>
  );
};
