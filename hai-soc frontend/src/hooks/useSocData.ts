import { useState, useEffect, useCallback } from "react";

import { socService } from "../api";

import {
  DashboardOverview,
  RiskDistribution,
  SourceDistribution,
  DepartmentDistribution,
  ModelDistribution,
  DailyTrend,
  Log,
  Incident,
  AnomalyScore,
  SystemHealth,
  RecentLog,
  RecentIncident,
  RecentAnomaly,
} from "../types";

/* =======================================================
   Dashboard
======================================================= */

export function useDashboardData() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [overview, setOverview] =
    useState<DashboardOverview | null>(null);

  const [riskDistribution, setRiskDistribution] =
    useState<RiskDistribution[]>([]);

  const [sources, setSources] =
    useState<SourceDistribution[]>([]);

  const [departments, setDepartments] =
    useState<DepartmentDistribution[]>([]);

  const [models, setModels] =
    useState<ModelDistribution[]>([]);

  const [anomalyTrend, setAnomalyTrend] =
    useState<DailyTrend[]>([]);

  const refetch = useCallback(async () => {
    try {
      setLoading(true);

      const [
        overviewData,
        riskData,
        sourceData,
        departmentData,
        modelData,
        trendData,
      ] = await Promise.all([
        socService.getOverview(),
        socService.getRiskDistribution(),
        socService.getSources(),
        socService.getDepartments(),
        socService.getModels(),
        socService.getTrend(),
      ]);

      setOverview(overviewData);

      setRiskDistribution(riskData);

      setSources(sourceData);

      setDepartments(departmentData);

      setModels(modelData);

      setAnomalyTrend(trendData);

      setError(null);
    } catch (err) {
      console.error(err);

      setError("Unable to fetch dashboard.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return {
    loading,
    error,

    overview,
    riskDistribution,
    sources,
    departments,
    models,
    anomalyTrend,

    refetch,
  };
}

/* =======================================================
   Logs
======================================================= */

export function useLogs() {
  const [logs, setLogs] = useState<Log[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchLogs = useCallback(async () => {
    try {
      const data = await socService.getLogs();
      setLogs(data);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  return {
    logs,
    loading,
    refetch: fetchLogs,
  };
}

/* =======================================================
   Incidents
======================================================= */

export function useIncidents() {
  const [incidents, setIncidents] =
    useState<Incident[]>([]);

  const [loading, setLoading] = useState(true);

  const fetchIncidents = useCallback(async () => {
    try {
      const data = await socService.getIncidents();

      setIncidents(data);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchIncidents();
  }, [fetchIncidents]);

  return {
    incidents,
    loading,
    refetch: fetchIncidents,
  };
}

/* =======================================================
   Anomalies
======================================================= */

export function useAnomalies() {
  const [anomalies, setAnomalies] =
    useState<AnomalyScore[]>([]);

  const [loading, setLoading] = useState(true);

  const fetchAnomalies = useCallback(async () => {
    try {
      const data =
        await socService.getAnomalies();

      setAnomalies(data);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAnomalies();
  }, [fetchAnomalies]);

  return {
    anomalies,
    loading,
    refetch: fetchAnomalies,
  };
}

/* =======================================================
   System Health
======================================================= */

export function useSystemHealth() {
  const [health, setHealth] =
    useState<SystemHealth | null>(null);

  useEffect(() => {
    socService
      .getSystemHealth()
      .then(setHealth);
  }, []);

  return health;
}

/* =======================================================
   Recent Dashboard Widgets
======================================================= */

export function useRecentDashboardData() {
  const [logs, setLogs] =
    useState<RecentLog[]>([]);

  const [incidents, setIncidents] =
    useState<RecentIncident[]>([]);

  const [anomalies, setAnomalies] =
    useState<RecentAnomaly[]>([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    async function load() {
      const [l, i, a] =
        await Promise.all([
          socService.getRecentLogs(),
          socService.getRecentIncidents(),
          socService.getRecentAnomalies(),
        ]);

      setLogs(l);
      setIncidents(i);
      setAnomalies(a);

      setLoading(false);
    }

    load();
  }, []);

  return {
    logs,
    incidents,
    anomalies,
    loading,
  };
}