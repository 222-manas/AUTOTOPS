# Incident Schema (version 1.0)

The AUTOTOPS Watcher writes one JSON file per incident to the configured output directory. The authoritative contract is `ai_work/schemas/incident.json`; incidents are validated against it before being written. The AI pipeline consumes the same contract without needing to know how Prometheus, Loki, or Kubernetes work.

| Field | Type | Description |
|---|---|---|
| `incident_id` | string | Unique identifier, e.g. `INC-001` |
| `service` | string | Affected service |
| `namespace` | string | Kubernetes namespace |
| `failure_type` | enum | `CrashLoopBackOff`, `HighHTTP5xxRate`, or `OOMKilled` |
| `severity` | enum | `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL` |
| `detected_at` | string | UTC ISO 8601 timestamp |
| `status` | enum | `OPEN` or `RESOLVED` |
| `source.watcher` | string | Watcher version |
| `evidence.pod_status` | object | Pod phase and container state |
| `evidence.kubernetes_events` | array | Recent Kubernetes events |
| `evidence.metrics` | object | Triggering metric values |
| `evidence.logs` | array | Recent application log lines |

Samples are in `ai_work/examples/`; the consumer is `ai_work/ai_pipeline/incident_loader.py`. Coordinate contract changes with all consumers and update tests and documentation together.
