export interface Log {
  id: string;
  timestamp: string;
  source: string;
  destination?: string;
  user_id?: string;
  user?: string;
  role?: string;
  device?: string;
  department?: string;
  action: string;
  severity: string;
  protocol?: string;
  port?: number;
  message: string;
  details?: string;
  outcome: string;
  extra?: Record<string, any>;
}