import { Log } from "../../types/log";
import { SecurityLog } from "../../types";

/**
 * Convert backend Log model
 * into frontend SecurityLog model.
 */
export function mapLog(log: Log): SecurityLog {
  return {
    id: log.id,

    timestamp: log.timestamp,

    source: log.source,

    user: log.user_id ?? "Unknown",

    department: log.department ?? "Unknown",

    action: log.action,

    severity: log.severity,

    outcome: log.outcome,

    details: log.message,

    ipAddress: "",

    resource: log.destination ?? "",

    device: log.device ?? "",

    riskScore: 0,

    protocol: log.protocol ?? "",

    port: log.port ?? 0,
  };
}