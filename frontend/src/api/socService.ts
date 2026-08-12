import { dashboardApi } from "./dashboard";
import { logsApi } from "./logs";
import { incidentsApi } from "./incidents";
import { anomaliesApi } from "./anomalies";

export const socService = {
  ...dashboardApi,
  ...logsApi,
  ...incidentsApi,
  ...anomaliesApi,
};