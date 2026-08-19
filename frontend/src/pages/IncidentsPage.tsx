import React, { useState } from 'react';
import { useIncidents } from '../hooks/useSocData';
import { IncidentsTable } from '../components/tables/IncidentsTable';
import { DashboardCard } from '../components/cards/DashboardCard';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { Drawer } from '../components/common/Drawer';
import { SecurityIncident } from '../types/index';
import { formatDateTime } from '../utils/formatters';
import { incidentsApi } from '../api/incidents';
import {
  AlertTriangle,
  Plus,
  ShieldCheck,
  ArrowRight,
  MessageSquare,
  Sparkles,
  RefreshCw,
  FileText,
  ShieldAlert,
  Lock,
  ListChecks,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';

export const IncidentsPage: React.FC = () => {
  const { incidents, loading, setIncidents } = useIncidents();
  const [selectedIncident, setSelectedIncident] = useState<SecurityIncident | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [showRawReport, setShowRawReport] = useState(false);
  const [completedActions, setCompletedActions] = useState<Record<string, boolean>>({});

  const activeId = selectedIncident?.id || selectedIncident?.incidentId || '';

  const handleStatusChange = (incidentId: string, newStatus: any) => {
    if (typeof setIncidents === 'function') {
      setIncidents((prev) =>
        prev.map((inc) =>
          (inc.id === incidentId || inc.incidentId === incidentId)
            ? { ...inc, status: newStatus }
            : inc
        )
      );
    }
    if (selectedIncident && (selectedIncident.id === incidentId || selectedIncident.incidentId === incidentId)) {
      setSelectedIncident((prev) => (prev ? { ...prev, status: newStatus } : null));
    }
  };

  const handleGenerateReport = async () => {
    if (!activeId || isAnalyzing) return;

    try {
      setIsAnalyzing(true);
      setAnalysisError(null);

      const updatedIncident = await incidentsApi.analyzeIncident(activeId);

      // Immediately update selected incident so the drawer rerenders with new report
      setSelectedIncident(updatedIncident);

      // Update list in state
      if (typeof setIncidents === 'function') {
        setIncidents((prev) =>
          prev.map((inc) =>
            (inc.id === activeId || inc.incidentId === activeId) ? updatedIncident : inc
          )
        );
      }
    } catch (err: any) {
      console.error('Failed to generate AI report:', err);
      setAnalysisError('Unable to generate AI investigation report. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const toggleActionCompleted = (actionText: string) => {
    setCompletedActions((prev) => ({
      ...prev,
      [actionText]: !prev[actionText],
    }));
  };

  const report = selectedIncident?.report;
  const hasReport = !!(report && (report.raw_markdown || (typeof report === 'string' && report.length > 0)));
  const rawMarkdown = typeof report === 'string' ? report : (report?.raw_markdown || '');
  const mitreTechniques: string[] = report?.mitre_techniques || (selectedIncident?.mitre_technique_id ? [selectedIncident.mitre_technique_id] : []);
  const nistControls: string[] = report?.nist_controls || [];
  const hipaaImpact: string | null = report?.hipaa_impact || selectedIncident?.hipaa_impact || null;
  const recommendedActions: string[] = report?.recommended_actions || [];

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
            onSelectIncident={(inc) => {
              setSelectedIncident(inc);
              setAnalysisError(null);
              setShowRawReport(false);
            }}
          />
        )}
      </DashboardCard>

      {/* Incident Investigation Drawer */}
      {selectedIncident && (
        <Drawer
          isOpen={!!selectedIncident}
          onClose={() => setSelectedIncident(null)}
          title={`Incident Investigation: ${activeId}`}
          subtitle={selectedIncident.title}
        >
          <div className="space-y-6 text-xs font-sans">
            {/* Case Overview Metrics */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 p-4 bg-slate-950 rounded-xl border border-slate-800 font-mono">
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Severity / Risk:</span>
                <p className="text-red-400 font-bold">{selectedIncident.risk_level || selectedIncident.severity || 'LOW'}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">ML Detector:</span>
                <p className="text-slate-200 font-bold">{selectedIncident.detector || 'ML Engine'}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Current Status:</span>
                <p className="text-cyan-400 font-bold">{selectedIncident.status}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Source Log ID:</span>
                <p className="text-slate-300 font-mono text-[11px] truncate">{selectedIncident.log_id || 'N/A'}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Assigned Analyst:</span>
                <p className="text-slate-200">{selectedIncident.assigned_to || 'Unassigned'}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Created At:</span>
                <p className="text-slate-400">{formatDateTime(selectedIncident.created_at || selectedIncident.createdAt || '')}</p>
              </div>
            </div>

            {/* Incident Status Workflow Buttons */}
            <div>
              <h4 className="font-bold text-slate-200 mb-2 uppercase font-mono">Change Case Status</h4>
              <div className="flex flex-wrap gap-2">
                {['OPEN', 'INVESTIGATING', 'CONTAINED', 'RESOLVED', 'CLOSED'].map((st) => (
                  <button
                    key={st}
                    onClick={() => handleStatusChange(activeId, st)}
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

            {/* AI Investigation Section */}
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2 font-mono text-cyan-400 font-bold uppercase text-sm">
                  <Sparkles className="w-5 h-5 text-cyan-400 animate-pulse" />
                  <span>Grounded AI Investigation</span>
                </div>

                <button
                  onClick={handleGenerateReport}
                  disabled={isAnalyzing}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold font-mono transition-all shadow-md ${
                    isAnalyzing
                      ? 'bg-slate-800 text-slate-400 cursor-not-allowed'
                      : hasReport
                      ? 'bg-slate-800 text-cyan-300 hover:bg-slate-700 border border-cyan-600/40'
                      : 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white hover:from-cyan-500 hover:to-blue-500'
                  }`}
                >
                  {isAnalyzing ? (
                    <>
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                      Generating AI investigation...
                    </>
                  ) : hasReport ? (
                    <>
                      <RefreshCw className="w-3.5 h-3.5" />
                      Refresh AI Report
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-3.5 h-3.5" />
                      Generate AI Report
                    </>
                  )}
                </button>
              </div>

              {analysisError && (
                <div className="p-3 bg-red-950/60 border border-red-800/80 rounded-lg text-red-300 font-mono text-xs flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 shrink-0 text-red-400" />
                  <span>{analysisError}</span>
                </div>
              )}

              {!hasReport && !isAnalyzing && (
                <div className="p-6 bg-slate-900/50 border border-dashed border-slate-800 rounded-xl text-center space-y-2">
                  <FileText className="w-8 h-8 text-slate-600 mx-auto" />
                  <p className="text-slate-400 font-mono text-xs">No AI investigation report generated.</p>
                  <p className="text-slate-500 text-[11px]">
                    Click "Generate AI Report" to retrieve grounded MITRE ATT&CK techniques, NIST controls, and HIPAA compliance context.
                  </p>
                </div>
              )}

              {hasReport && (
                <div className="space-y-4">
                  {/* MITRE ATT&CK Badges */}
                  {mitreTechniques.length > 0 && (
                    <div>
                      <h5 className="font-bold text-slate-300 uppercase font-mono text-[11px] mb-1.5 flex items-center gap-1.5">
                        <ShieldAlert className="w-3.5 h-3.5 text-purple-400" />
                        Relevant MITRE ATT&CK Techniques
                      </h5>
                      <div className="flex flex-wrap gap-2">
                        {mitreTechniques.map((tech, idx) => (
                          <span
                            key={idx}
                            className="px-2.5 py-1 bg-purple-950/80 border border-purple-800/80 rounded text-purple-300 font-mono text-[11px] flex items-center gap-1"
                          >
                            <span className="font-bold text-purple-200">[{tech}]</span>
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* NIST Controls Badges */}
                  {nistControls.length > 0 && (
                    <div>
                      <h5 className="font-bold text-slate-300 uppercase font-mono text-[11px] mb-1.5 flex items-center gap-1.5">
                        <Lock className="w-3.5 h-3.5 text-blue-400" />
                        Mapped NIST SP 800-53 Controls
                      </h5>
                      <div className="flex flex-wrap gap-2">
                        {nistControls.map((ctrl, idx) => (
                          <span
                            key={idx}
                            className="px-2.5 py-1 bg-blue-950/80 border border-blue-800/80 rounded text-blue-300 font-mono text-[11px]"
                          >
                            [{ctrl}]
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* HIPAA Implications */}
                  {hipaaImpact && (
                    <div className="p-3 bg-amber-950/30 border border-amber-800/60 rounded-xl space-y-1">
                      <div className="flex items-center gap-1.5 font-mono text-amber-400 font-bold uppercase text-[11px]">
                        <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
                        <span>HIPAA Compliance Assessment</span>
                      </div>
                      <p className="text-slate-200 text-xs leading-relaxed font-mono whitespace-pre-wrap">
                        {hipaaImpact}
                      </p>
                    </div>
                  )}

                  {/* Recommended Containment & Investigation Actions */}
                  {recommendedActions.length > 0 && (
                    <div className="space-y-2">
                      <h5 className="font-bold text-slate-300 uppercase font-mono text-[11px] flex items-center gap-1.5">
                        <ListChecks className="w-3.5 h-3.5 text-cyan-400" />
                        Recommended SOC Actions & Containment Checklist
                      </h5>
                      <div className="space-y-1.5 font-mono text-xs">
                        {recommendedActions.map((action, idx) => {
                          const isDone = !!completedActions[action];
                          return (
                            <div
                              key={idx}
                              onClick={() => toggleActionCompleted(action)}
                              className={`p-2.5 rounded-lg border flex items-start gap-2.5 cursor-pointer transition-colors ${
                                isDone
                                  ? 'bg-emerald-950/30 border-emerald-800/60 text-slate-400 line-through'
                                  : 'bg-slate-900 border-slate-800 text-slate-200 hover:border-slate-700'
                              }`}
                            >
                              <CheckCircle2
                                className={`w-4 h-4 shrink-0 mt-0.5 ${
                                  isDone ? 'text-emerald-400' : 'text-slate-600'
                                }`}
                              />
                              <span className="text-[11px] leading-snug">{action}</span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {/* Full Report Accordion */}
                  <div className="border-t border-slate-800 pt-3">
                    <button
                      onClick={() => setShowRawReport(!showRawReport)}
                      className="w-full flex items-center justify-between text-slate-400 hover:text-cyan-300 font-mono text-xs py-1"
                    >
                      <span className="flex items-center gap-1.5">
                        <FileText className="w-3.5 h-3.5 text-cyan-400" />
                        {showRawReport ? 'Hide Complete 11-Section AI Report' : 'View Complete 11-Section AI Report'}
                      </span>
                      {showRawReport ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>

                    {showRawReport && (
                      <div className="mt-3 p-3.5 bg-slate-900/90 border border-slate-800 rounded-xl text-slate-300 font-mono text-xs leading-relaxed whitespace-pre-wrap max-h-96 overflow-y-auto">
                        {rawMarkdown}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

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
                          (i.id === activeId || i.incidentId === activeId)
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
