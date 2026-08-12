import apiClient from "./client";
import {
  DashboardOverview,
  RiskDistribution,
  SourceDistribution,
  DepartmentDistribution,
  ModelDistribution,
  DailyTrend,
  SystemHealth,
  RecentLog,
  RecentIncident,
  RecentAnomaly,
} from "../types";

export const dashboardApi = {
  getOverview: async (): Promise<DashboardOverview> => {
    const { data } = await apiClient.get("/dashboard/overview");
    return data;
  },

  getRiskDistribution: async (): Promise<RiskDistribution[]> => {
    const { data } = await apiClient.get("/dashboard/risk-distribution");
    return data;
  },

  getSources: async (): Promise<SourceDistribution[]> => {
    const { data } = await apiClient.get("/dashboard/sources");
    return data;
  },

  getDepartments: async (): Promise<DepartmentDistribution[]> => {
    const { data } = await apiClient.get("/dashboard/departments");
    return data;
  },

  getModels: async (): Promise<ModelDistribution[]> => {
    const { data } = await apiClient.get("/dashboard/models");
    return data;
  },

  getTrend: async (): Promise<DailyTrend[]> => {
    const { data } = await apiClient.get("/dashboard/anomaly-trend");
    return data;
  },

  getSystemHealth: async (): Promise<SystemHealth> => {
    const { data } = await apiClient.get("/dashboard/system-health");
    return data;
  },

  getRecentLogs: async (): Promise<RecentLog[]> => {
    const { data } = await apiClient.get("/dashboard/recent-logs");
    return data;
  },

  getRecentIncidents: async (): Promise<RecentIncident[]> => {
    const { data } = await apiClient.get("/dashboard/recent-incidents");
    return data;
  },

  getRecentAnomalies: async (): Promise<RecentAnomaly[]> => {
    const { data } = await apiClient.get("/dashboard/recent-anomalies");
    return data;
  },
};