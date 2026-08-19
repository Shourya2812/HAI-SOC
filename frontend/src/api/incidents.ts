import apiClient from "./client";
import { Incident } from "../types";

export const incidentsApi = {
  getIncidents: async (): Promise<Incident[]> => {
    const { data } = await apiClient.get("/incidents");
    return data;
  },

  getIncident: async (incidentId: string): Promise<Incident> => {
    const { data } = await apiClient.get(`/incidents/${incidentId}`);
    return data;
  },

  analyzeIncident: async (incidentId: string): Promise<Incident> => {
    const { data } = await apiClient.post(
      `/incidents/${incidentId}/analyze`,
      {},
      { timeout: 300000 } // 5 minutes dedicated timeout for Ollama local LLM generation
    );
    return data;
  },
};