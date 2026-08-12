import apiClient from "./client";
import { Incident } from "../types";

export const incidentsApi = {
  getIncidents: async (): Promise<Incident[]> => {
    const { data } = await apiClient.get("/incidents");
    return data;
  },
};