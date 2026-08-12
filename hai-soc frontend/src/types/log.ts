export interface Log {
  id: string;

  timestamp: string;

  source: string;

  user: string;

  department: string;

  action: string;

  outcome: string;

  severity: string;

  ip_address: string;

  resource: string;

  details: string;
}