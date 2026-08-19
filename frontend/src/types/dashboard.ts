export interface DashboardOverview {
  total_logs: number;
  todays_anomalies: number;
  open_incidents: number;
  critical_incidents: number;

  logs_trend_pct: number;
  anomalies_trend_pct: number;
  incidents_trend_pct: number;
  critical_trend_pct: number;

  active_hospital: string;
  system_health: string;
}

export interface RiskDistribution {
  category: string;
  count: number;
  percentage: number;
  color: string;
}

export interface SourceDistribution {
  source: string;
  count: number;
  color: string;
}

export interface DepartmentDistribution {
  department: string;
  count: number;
  color: string;
}

export interface ModelDistribution {
  model: string;
  count: number;
  accuracy: number;
}

export interface DailyTrend {
  hour: string;
  anomalies: number;
  baseline: number;
}

export interface SystemHealth {
  mongodb: string;
  backend: string;
  ml_model: string;
  api: string;
  uptime: string;
}

export interface RecentLog {
  id: string;
  timestamp: string;
  severity: string;
  source: string;
  message: string;
}

export interface RecentIncident {
  id: string;
  title: string;
  severity: string;
  status: string;
}

export interface RecentAnomaly {
  id: string;
  detector: string;
  score: number;
  prediction: number;
}