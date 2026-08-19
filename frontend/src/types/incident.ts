export interface IncidentReport {
  raw_markdown?: string;
  generated_at?: string;
  mitre_techniques?: string[];
  nist_controls?: string[];
  hipaa_impact?: string | null;
  risk_assessment?: string | null;
  recommended_actions?: string[];
  status?: string;
}

export interface Incident {
  id: string;
  title: string;
  description: string;
  log_id?: string;
  detector?: string;
  anomaly_score?: number;
  risk_level: string;
  riskLevel?: string;
  severity?: string;
  status: string;
  hipaa_impact?: string;
  mitre_technique_id?: string;
  report?: IncidentReport | Record<string, any>;
  assigned_to?: string;
  assignedAnalyst?: string;
  created_at: string;
  createdAt?: string;
  updated_at?: string;
  resolved_at?: string;
  incidentId?: string;
  predictionScore?: number;
  recommendedAction?: string;
  supportTicketRef?: string;
  mitreTactics?: string[];
  investigationNotes?: string[];
  source?: string;
}

export type SecurityIncident = Incident;
export type IncidentStatus = "OPEN" | "INVESTIGATING" | "CONTAINED" | "RESOLVED" | "CLOSED" | string;
export type RiskLevel = "CRITICAL" | "HIGH" | "ELEVATED" | "MODERATE" | "LOW" | string;
export type SeverityLevel = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO" | string;