import React, { useState } from 'react';
import { useAnomalies } from '../hooks/useSocData';
import { AnomaliesTable } from '../components/tables/AnomaliesTable';
import { DashboardCard } from '../components/cards/DashboardCard';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { Drawer } from '../components/common/Drawer';
import { AnomalyPrediction } from '../types/index';
import { formatDateTime } from '../utils/formatters';
import { BrainCircuit, Cpu, Sparkles, SlidersHorizontal } from 'lucide-react';

export const AnomaliesPage: React.FC = () => {
  const { anomalies, loading } = useAnomalies();
  const [selectedAnomaly, setSelectedAnomaly] = useState<AnomalyPrediction | null>(null);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <BrainCircuit className="w-6 h-6 text-purple-400" />
            Machine Learning Anomaly Detections
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time inference predictions from Isolation Forest, Autoencoder, and Transformer neural networks.
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          <div className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>Isolation Forest v4.2</span>
          </div>
        </div>
      </div>

      {/* Model Performance Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-1">
          <span className="text-[10px] uppercase font-mono text-slate-500">Detector Accuracy</span>
          <div className="text-2xl font-bold text-cyan-400 font-mono">98.6%</div>
          <p className="text-[11px] text-slate-400">Validated against 1.2M clinical transactions</p>
        </div>

        <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-1">
          <span className="text-[10px] uppercase font-mono text-slate-500">Avg Inference Latency</span>
          <div className="text-2xl font-bold text-purple-400 font-mono">4.2 ms</div>
          <p className="text-[11px] text-slate-400">Sub-millisecond streaming pipeline</p>
        </div>

        <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-1">
          <span className="text-[10px] uppercase font-mono text-slate-500">Anomalies Detected Today</span>
          <div className="text-2xl font-bold text-amber-400 font-mono">{anomalies.length}</div>
          <p className="text-[11px] text-slate-400">Flagged for automated SOC triage</p>
        </div>
      </div>

      {/* Table */}
      <DashboardCard
        title="ML Anomaly Prediction Stream"
        subtitle="Unsupervised outlier detections across clinical network traffic"
      >
        {loading ? (
          <LoadingSkeleton rows={8} />
        ) : (
          <AnomaliesTable
            anomalies={anomalies}
            onSelectAnomaly={setSelectedAnomaly}
          />
        )}
      </DashboardCard>

      {/* Detail Drawer */}
      {selectedAnomaly && (
        <Drawer
          isOpen={!!selectedAnomaly}
          onClose={() => setSelectedAnomaly(null)}
          title={`Anomaly Prediction: ${selectedAnomaly.id}`}
          subtitle={`Detector Model: ${selectedAnomaly.detector}`}
        >
          <div className="space-y-5 text-xs font-sans">
            <div className="grid grid-cols-2 gap-3 p-4 bg-slate-950 rounded-xl border border-slate-800 font-mono">
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Timestamp:</span>
                <p className="text-slate-200 font-bold">{formatDateTime(selectedAnomaly.timestamp)}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Prediction Outcome:</span>
                <p className="text-red-400 font-bold">{selectedAnomaly.prediction}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Anomaly Score:</span>
                <p className="text-amber-400 font-bold">{selectedAnomaly.anomalyScore.toFixed(2)}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Model Confidence:</span>
                <p className="text-cyan-400 font-bold">{selectedAnomaly.confidence.toFixed(1)}%</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Flagged Subject:</span>
                <p className="text-slate-200">{selectedAnomaly.flaggedUser || 'System Process'}</p>
              </div>
              <div>
                <span className="text-slate-500 uppercase text-[10px]">Department:</span>
                <p className="text-slate-300">{selectedAnomaly.department || 'Clinical Systems'}</p>
              </div>
            </div>

            <div>
              <h4 className="font-bold text-slate-200 mb-2 uppercase font-mono flex items-center gap-1.5">
                <SlidersHorizontal className="w-4 h-4 text-cyan-400" />
                <span>Features Analyzed by Neural Net</span>
              </h4>
              <div className="space-y-2">
                {selectedAnomaly.featuresAnalyzed.map((feat, i) => (
                  <div key={i} className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-between font-mono">
                    <span className="text-slate-300">{feat}</span>
                    <span className="text-xs text-purple-400 font-bold">Deviation &gt; 3.5 σ</span>
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
