import React from 'react';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';
import { formatNumber } from '../../utils/formatters';

interface MetricCardProps {
  title: string;
  value: number | string;
  trendPct?: number;
  icon: LucideIcon;
  subtitle?: string;
  glowColor?: 'cyan' | 'purple' | 'red' | 'amber' | 'emerald';
  isCritical?: boolean;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  trendPct,
  icon: Icon,
  subtitle,
  glowColor = 'cyan',
  isCritical = false,
}) => {
  const isPositiveTrend = trendPct !== undefined && trendPct > 0;
  // For security metrics: higher anomalies/incidents is usually worse (unless trendPct is negative)
  const isNegativeGood = title.toLowerCase().includes('anomaly') || title.toLowerCase().includes('incident');

  const glowClass = {
    cyan: 'hover:border-cyan-500/50 hover:shadow-[0_0_20px_-3px_rgba(6,182,212,0.2)]',
    purple: 'hover:border-purple-500/50 hover:shadow-[0_0_20px_-3px_rgba(139,92,246,0.2)]',
    red: 'border-red-900/60 shadow-[0_0_20px_-3px_rgba(239,68,68,0.25)] hover:border-red-500/60',
    amber: 'hover:border-amber-500/50 hover:shadow-[0_0_20px_-3px_rgba(245,158,11,0.2)]',
    emerald: 'hover:border-emerald-500/50 hover:shadow-[0_0_20px_-3px_rgba(16,185,129,0.2)]',
  }[glowColor];

  const iconBg = {
    cyan: 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/40',
    purple: 'bg-purple-950/60 text-purple-400 border border-purple-800/40',
    red: 'bg-red-950/70 text-red-400 border border-red-800/60',
    amber: 'bg-amber-950/60 text-amber-400 border border-amber-800/40',
    emerald: 'bg-emerald-950/60 text-emerald-400 border border-emerald-800/40',
  }[glowColor];

  return (
    <div
      className={`bg-slate-900/90 border border-slate-800 rounded-xl p-5 transition-all duration-300 relative overflow-hidden backdrop-blur-md ${glowClass} ${
        isCritical ? 'bg-gradient-to-br from-slate-900 via-slate-900 to-red-950/40 border-red-900/80' : ''
      }`}
    >
      <div className="flex items-start justify-between mb-3">
        <span className="text-xs font-semibold tracking-wider text-slate-400 uppercase">
          {title}
        </span>
        <div className={`p-2.5 rounded-lg ${iconBg}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>

      <div className="flex items-baseline justify-between mt-1">
        <div className="text-3xl font-bold tracking-tight text-white font-mono">
          {typeof value === 'number' ? formatNumber(value) : value}
        </div>

        {trendPct !== undefined && (
          <div
            className={`flex items-center text-xs font-medium px-2 py-0.5 rounded-full border ${
              isPositiveTrend
                ? isNegativeGood
                  ? 'bg-red-950/60 text-red-400 border-red-800/40'
                  : 'bg-emerald-950/60 text-emerald-400 border-emerald-800/40'
                : isNegativeGood
                ? 'bg-emerald-950/60 text-emerald-400 border-emerald-800/40'
                : 'bg-red-950/60 text-red-400 border-red-800/40'
            }`}
          >
            {isPositiveTrend ? (
              <TrendingUp className="w-3 h-3 mr-1" />
            ) : (
              <TrendingDown className="w-3 h-3 mr-1" />
            )}
            {Math.abs(trendPct)}%
          </div>
        )}
      </div>

      {subtitle && (
        <p className="mt-2 text-xs text-slate-500 flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-cyan-500/80"></span>
          {subtitle}
        </p>
      )}
    </div>
  );
};
