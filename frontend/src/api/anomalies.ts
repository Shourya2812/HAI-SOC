import apiClient from "./client";
import { AnomalyScore } from "../types";

export const anomaliesApi = {
  getAnomalies: async (): Promise<AnomalyScore[]> => {
    const { data } = await apiClient.get("/anomalies");
    return data;
  },
};