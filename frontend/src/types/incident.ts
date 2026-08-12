export interface Incident {
  id: string;

  title: string;

  severity: string;

  status: string;

  assigned_to: string;

  created_at: string;

  updated_at: string;

  mitre_tactic: string;

  mitre_technique: string;

  description: string;

  affected_asset: string;
}