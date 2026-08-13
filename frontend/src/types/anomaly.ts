export interface AnomalyScore {
  id: string;
  detector: string;
  score?: number;
  anomalyScore?: number;
  anomaly_score?: number;
  prediction: number | string;
  confidence?: number;
  timestamp?: string;
  user?: string;
  flaggedUser?: string;
  department?: string;
  source?: string;
  features?: string[];
  featuresAnalyzed?: string[];
}

export type AnomalyPrediction = AnomalyScore;