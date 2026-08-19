import React, { useState } from 'react';
import { SecurityIncident, IncidentStatus, SeverityLevel } from '../../types/index';
import { DataTable, Column } from './DataTable';
import { StatusBadge } from '../common/StatusBadge';
import { SeverityBadge } from '../common/SeverityBadge';
import { formatDateTime, getRiskLevelColor } from '../../utils/formatters';
import { Filter, ExternalLink } from 'lucide-react';

interface IncidentsTableProps {
  incidents: SecurityIncident[];
  onSelectIncident?: (incident: SecurityIncident) => void;
}

export const IncidentsTable: React.FC<IncidentsTableProps> = ({
  incidents,
  onSelectIncident,
}) => {
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [severityFilter, setSeverityFilter] = useState<string>('ALL');

  const filteredIncidents = incidents.filter((inc) => {
    if (statusFilter !== 'ALL' && inc.status !== statusFilter) return false;
    if (severityFilter !== 'ALL' && inc.severity !== severityFilter) return false;
    return true;
  });

  const columns: Column<SecurityIncident>[] = [
    {
      key: 'incidentId',
      header: 'Incident ID',
      sortable: true,
      render: (row) => (
        <span className="font-mono font-bold text-cyan-400 hover:underline">
          {row.id || row.incidentId}
        </span>
      ),
    },
    {
      key: 'severity',
      header: 'Severity',
      sortable: true,
      render: (row) => <SeverityBadge severity={(row.severity || row.risk_level || 'LOW') as SeverityLevel} />,
    },
    {
      key: 'riskLevel',
      header: 'Risk Level',
      sortable: true,
      render: (row) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-semibold border uppercase font-mono ${getRiskLevelColor(
            (row.risk_level || row.riskLevel || row.severity || 'LOW') as any
          )}`}
        >
          {row.risk_level || row.riskLevel || row.severity || 'LOW'}
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      sortable: true,
      render: (row) => <StatusBadge status={(row.status || 'OPEN') as IncidentStatus} />,
    },
    {
      key: 'createdAt',
      header: 'Created At',
      sortable: true,
      render: (row) => (
        <span className="font-mono text-xs text-slate-400">
          {formatDateTime(row.created_at || row.createdAt || '')}
        </span>
      ),
    },
    {
      key: 'predictionScore',
      header: 'Prediction Score',
      sortable: true,
      render: (row) => {
        const scoreVal = row.anomaly_score != null ? row.anomaly_score * 100 : row.predictionScore;
        return (
          <div className="flex items-center gap-2 font-mono">
            {scoreVal != null ? (
              <>
                <div className="w-16 h-1.5 rounded-full bg-slate-800 overflow-hidden">
                  <div
                    className={`h-full ${
                      scoreVal > 90
                        ? 'bg-red-500'
                        : scoreVal > 75
                        ? 'bg-amber-500'
                        : 'bg-cyan-500'
                    }`}
                    style={{ width: `${scoreVal}%` }}
                  ></div>
                </div>
                <span className="text-xs font-bold text-slate-200">
                  {scoreVal.toFixed(1)}%
                </span>
              </>
            ) : (
              <span className="text-xs text-slate-500">N/A</span>
            )}
          </div>
        );
      },
    },
    {
      key: 'recommendedAction',
      header: 'Description / Recommended Action',
      render: (row) => (
        <p className="text-xs text-slate-300 max-w-xs truncate" title={row.description || row.recommendedAction || row.title}>
          {row.description || row.recommendedAction || row.title}
        </p>
      ),
    },
    {
      key: 'supportTicketRef',
      header: 'Support',
      render: (row) => (
        <span className="inline-flex items-center gap-1 font-mono text-[11px] text-purple-400 hover:text-purple-300">
          {row.supportTicketRef || 'JIRA-SEC'}
          <ExternalLink className="w-3 h-3" />
        </span>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex flex-wrap items-center gap-3 p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
        <div className="flex items-center gap-1.5 text-xs text-slate-400 font-mono">
          <Filter className="w-3.5 h-3.5 text-cyan-400" />
          <span>Filters:</span>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-[11px] text-slate-400 uppercase font-mono">Status:</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-md text-xs text-slate-200 px-2.5 py-1 focus:outline-none focus:border-cyan-500 font-mono"
          >
            <option value="ALL">All Statuses</option>
            <option value="OPEN">Open</option>
            <option value="INVESTIGATING">Investigating</option>
            <option value="CONTAINED">Contained</option>
            <option value="RESOLVED">Resolved</option>
            <option value="CLOSED">Closed</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-[11px] text-slate-400 uppercase font-mono">Severity:</label>
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-md text-xs text-slate-200 px-2.5 py-1 focus:outline-none focus:border-cyan-500 font-mono"
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>
        </div>
      </div>

      <DataTable
        columns={columns}
        data={filteredIncidents}
        searchPlaceholder="Filter incidents by title, ID, user, ticket..."
        searchFilterKey={(row) =>
          `${row.incidentId} ${row.title} ${row.affectedUser || ''} ${row.supportTicketRef || ''} ${row.source}`
        }
        onRowClick={onSelectIncident}
        pageSize={10}
      />
    </div>
  );
};
