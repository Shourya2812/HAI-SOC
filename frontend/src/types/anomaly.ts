export interface AnomalyScore {
  id: string;

  timestamp: string;

  detector: string;

  anomaly_score: number;

  confidence: number;

  prediction: number;

  user: string;

  department: string;

  source: string;

  features: string[];
}