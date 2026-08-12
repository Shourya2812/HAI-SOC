import React, { useState } from 'react';
import { SecurityLog, SeverityLevel } from '../../types/index';
import { DataTable, Column } from './DataTable';
import { SeverityBadge } from '../common/SeverityBadge';
import { formatDateTime, getOutcomeBadgeColor } from '../../utils/formatters';
import { Filter } from 'lucide-react';

interface SecurityLogsTableProps {
  logs: SecurityLog[];
  onSelectLog?: (log: SecurityLog) => void;
}

export const SecurityLogsTable: React.FC<SecurityLogsTableProps> = ({ logs, onSelectLog }) => {
  const [severityFilter, setSeverityFilter] = useState<string>('ALL');
  const [sourceFilter, setSourceFilter] = useState<string>('ALL');

  // Filter logic
  const filteredLogs = logs.filter((log) => {
    if (severityFilter !== 'ALL' && log.severity !== severityFilter) return false;
    if (sourceFilter !== 'ALL' && log.source !== sourceFilter) return false;
    return true;
  });

  const columns: Column<SecurityLog>[] = [
    {
      key: 'timestamp',
      header: 'Timestamp',
      sortable: true,
      render: (row) => (
        <span className="font-mono text-xs text-slate-300 whitespace-nowrap">
          {formatDateTime(row.timestamp)}
        </span>
      ),
    },
    {
      key: 'source',
      header: 'Source',
      sortable: true,
      render: (row) => (
        <span className="font-semibold text-cyan-400">{row.source}</span>
      ),
    },
    {
      key: 'user_id',
      header: 'User',
      sortable: true,
      render: (row) => (
        <span className="font-mono text-slate-300">{row.user_id || row.user || 'N/A'}</span>
      ),
    },
    {
      key: 'department',
      header: 'Department',
      sortable: true,
      render: (row) => (
        <span className="text-slate-400">{row.department || 'N/A'}</span>
      ),
    },
    {
      key: 'action',
      header: 'Action',
      sortable: true,
      render: (row) => (
        <span className="font-mono text-xs px-2 py-0.5 rounded bg-slate-950 border border-slate-800 text-slate-200">
          {row.action || row.message || 'EVENT'}
        </span>
      ),
    },
    {
      key: 'outcome',
      header: 'Outcome',
      sortable: true,
      render: (row) => (
        <span
          className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold border font-mono ${getOutcomeBadgeColor(
            row.outcome || 'SUCCESS'
          )}`}
        >
          {row.outcome || 'SUCCESS'}
        </span>
      ),
    },
    {
      key: 'severity',
      header: 'Severity',
      sortable: true,
      render: (row) => <SeverityBadge severity={row.severity as SeverityLevel} />,
    },
  ];

  return (
    <div className="space-y-4">
      {/* Table Level Filters */}
      <div className="flex flex-wrap items-center gap-3 p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
        <div className="flex items-center gap-1.5 text-xs text-slate-400 font-mono">
          <Filter className="w-3.5 h-3.5 text-cyan-400" />
          <span>Filters:</span>
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
            <option value="INFO">Info</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-[11px] text-slate-400 uppercase font-mono">Source:</label>
          <select
            value={sourceFilter}
            onChange={(e) => setSourceFilter(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-md text-xs text-slate-200 px-2.5 py-1 focus:outline-none focus:border-cyan-500 font-mono"
          >
            <option value="ALL">All Log Sources</option>
            <option value="Epic Hyperspace EHR">Epic Hyperspace EHR</option>
            <option value="IoMT Patient Monitors">IoMT Patient Monitors</option>
            <option value="PACS Medical Imaging">PACS Medical Imaging</option>
            <option value="Active Directory / Okta">Active Directory / Okta</option>
            <option value="Pyxis Pharmacy Dispenser">Pyxis Pharmacy Dispenser</option>
          </select>
        </div>
      </div>

      <DataTable
        columns={columns}
        data={filteredLogs}
        searchPlaceholder="Filter logs by user, action, IP, resource..."
        searchFilterKey={(row) => `${row.user_id || row.user || ''} ${row.source} ${row.action} ${row.message || row.details || ''} ${row.department || ''}`}
        onRowClick={onSelectLog}
        pageSize={10}
      />
    </div>
  );
};
