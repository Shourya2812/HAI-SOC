import React from 'react';
import { AnomalyPrediction } from '../../types/index';
import { DataTable, Column } from './DataTable';
import { formatDateTime } from '../../utils/formatters';
import { Cpu, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface AnomaliesTableProps {
  anomalies: AnomalyPrediction[];
  onSelectAnomaly?: (anomaly: AnomalyPrediction) => void;
}

export const AnomaliesTable: React.FC<AnomaliesTableProps> = ({
  anomalies,
  onSelectAnomaly,
}) => {
  const columns: Column<AnomalyPrediction>[] = [
    {
      key: 'timestamp',
      header: 'Timestamp',
      sortable: true,
      render: (row) => (
        <span className="font-mono text-xs text-slate-300">
          {formatDateTime(row.timestamp)}
        </span>
      ),
    },
    {
      key: 'detector',
      header: 'ML Detector Model',
      sortable: true,
      render: (row) => (
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-purple-400" />
          <span className="font-semibold text-slate-200">{row.detector}</span>
        </div>
      ),
    },
    {
      key: 'prediction',
      header: 'Prediction',
      sortable: true,
      render: (row) => (
        <span
          className={`inline-flex items-center px-2.5 py-0.5 rounded text-xs font-bold border font-mono ${
            row.prediction === 'ANOMALOUS'
              ? 'bg-red-950/80 text-red-400 border-red-800/60 glow-red'
              : 'bg-emerald-950/80 text-emerald-400 border-emerald-800/60'
          }`}
        >
          {row.prediction === 'ANOMALOUS' ? (
            <AlertTriangle className="w-3 h-3 mr-1" />
          ) : (
            <CheckCircle2 className="w-3 h-3 mr-1" />
          )}
          {row.prediction}
        </span>
      ),
    },
    {
      key: 'anomalyScore',
      header: 'Anomaly Score',
      sortable: true,
      render: (row) => (
        <div className="flex items-center gap-2 font-mono">
          <div className="w-16 h-1.5 rounded-full bg-slate-800 overflow-hidden">
            <div
              className={`h-full ${
                row.anomalyScore > 0.8
                  ? 'bg-red-500'
                  : row.anomalyScore > 0.5
                  ? 'bg-amber-500'
                  : 'bg-emerald-500'
              }`}
              style={{ width: `${row.anomalyScore * 100}%` }}
            ></div>
          </div>
          <span className="text-xs font-bold text-slate-100">
            {row.anomalyScore.toFixed(2)}
          </span>
        </div>
      ),
    },
    {
      key: 'confidence',
      header: 'Confidence',
      sortable: true,
      render: (row) => (
        <span className="font-mono text-xs text-cyan-400 font-bold">
          {row.confidence.toFixed(1)}%
        </span>
      ),
    },
    {
      key: 'flaggedUser',
      header: 'Flagged Subject',
      render: (row) => (
        <span className="font-mono text-xs text-slate-400">
          {row.flaggedUser || 'System Process'}
        </span>
      ),
    },
  ];

  return (
    <DataTable
      columns={columns}
      data={anomalies}
      searchPlaceholder="Search ML detections by detector, subject, features..."
      searchFilterKey={(row) => `${row.detector} ${row.prediction} ${row.flaggedUser || ''}`}
      onRowClick={onSelectAnomaly}
      pageSize={10}
    />
  );
};
