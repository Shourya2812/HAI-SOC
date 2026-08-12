import { SeverityLevel, IncidentStatus, RiskLevel } from '../types/index';

export function formatNumber(num: number): string {
  if (num >= 1_000_000) {
    return (num / 1_000_000).toFixed(1) + 'M';
  }
  if (num >= 1_000) {
    return (num / 1_000).toFixed(1) + 'K';
  }
  return num.toLocaleString();
}

export function formatDateTime(isoString: string): string {
  if (!isoString) return 'N/A';
  try {
    const d = new Date(isoString);
    return d.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    });
  } catch {
    return isoString;
  }
}

export function getSeverityBgColor(severity: SeverityLevel): string {
  switch (severity) {
    case 'CRITICAL':
      return 'bg-red-950/80 text-red-400 border-red-800/60 glow-red';
    case 'HIGH':
      return 'bg-orange-950/80 text-orange-400 border-orange-800/60';
    case 'MEDIUM':
      return 'bg-amber-950/80 text-amber-400 border-amber-800/60';
    case 'LOW':
      return 'bg-blue-950/80 text-blue-400 border-blue-800/60';
    case 'INFO':
    default:
      return 'bg-slate-900 text-slate-400 border-slate-700/60';
  }
}

export function getStatusBgColor(status: IncidentStatus): string {
  switch (status) {
    case 'OPEN':
      return 'bg-red-950/80 text-red-400 border-red-800/60';
    case 'INVESTIGATING':
      return 'bg-cyan-950/80 text-cyan-400 border-cyan-800/60 glow-cyan';
    case 'CONTAINED':
      return 'bg-amber-950/80 text-amber-400 border-amber-800/60';
    case 'RESOLVED':
      return 'bg-emerald-950/80 text-emerald-400 border-emerald-800/60';
    case 'CLOSED':
      return 'bg-slate-900 text-slate-400 border-slate-700/60';
    default:
      return 'bg-slate-900 text-slate-300 border-slate-700/60';
  }
}

export function getRiskLevelColor(risk: RiskLevel): string {
  switch (risk) {
    case 'CRITICAL':
      return 'text-red-400 bg-red-950/60 border-red-800/50';
    case 'HIGH':
      return 'text-orange-400 bg-orange-950/60 border-orange-800/50';
    case 'ELEVATED':
      return 'text-amber-400 bg-amber-950/60 border-amber-800/50';
    case 'MODERATE':
      return 'text-yellow-400 bg-yellow-950/60 border-yellow-800/50';
    case 'LOW':
    default:
      return 'text-emerald-400 bg-emerald-950/60 border-emerald-800/50';
  }
}

export function getOutcomeBadgeColor(outcome: string): string {
  switch (outcome) {
    case 'SUCCESS':
      return 'bg-emerald-950/50 text-emerald-400 border-emerald-800/40';
    case 'FAILURE':
      return 'bg-red-950/50 text-red-400 border-red-800/40';
    case 'BLOCKED':
      return 'bg-purple-950/50 text-purple-400 border-purple-800/40';
    case 'FLAGGED':
      return 'bg-amber-950/50 text-amber-400 border-amber-800/40';
    default:
      return 'bg-slate-900 text-slate-400 border-slate-700/40';
  }
}
