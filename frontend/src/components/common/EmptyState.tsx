import React from 'react';
import { ShieldCheck } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionText?: string;
  onAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No Telemetry Records Found',
  description = 'There are no active security logs or anomalies matching your current filter criteria.',
  actionText,
  onAction,
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center bg-slate-900/40 border border-slate-800/80 rounded-xl">
      <div className="p-4 rounded-full bg-cyan-950/50 border border-cyan-800/40 text-cyan-400 mb-4 glow-cyan">
        <ShieldCheck className="w-8 h-8" />
      </div>
      <h4 className="text-base font-semibold text-slate-200 mb-1">{title}</h4>
      <p className="text-xs text-slate-400 max-w-md mb-4">{description}</p>
      {actionText && onAction && (
        <button
          onClick={onAction}
          className="px-4 py-2 text-xs font-semibold text-cyan-300 bg-cyan-950/80 border border-cyan-700/60 rounded-lg hover:bg-cyan-900/80 transition-colors"
        >
          {actionText}
        </button>
      )}
    </div>
  );
};
