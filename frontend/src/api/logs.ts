import apiClient from "./client";
import { Log } from "../types";

export const logsApi = {
  getLogs: async (): Promise<Log[]> => {
    const { data } = await apiClient.get("/logs");
    return data;
  },
};