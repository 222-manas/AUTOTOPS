# Incident Schema (version 1.0)

The Watcher produces one JSON file per incident in `incidents/`. The schema is version-controlled in `schemas/incident.json` and every incident is validated against it before it is written.

Consumers (the Diagnoser) only need this file. They do not need to know how Prometheus, Loki or the Kubernetes API work.

## Fields

| Field | Type | Description |
|---|---|---|
| `incident_id` | string | Unique id, for example `INC-001` |
| `service` | string | Affected service, for example `demo-api` |
| `namespace` | string | Kubernetes namespace |
| `failure_type` | enum | `CrashLoopBackOff`, `HighHTTP5xxRate` or `OOMKilled` |
| `severity` | enum | `LOW`, `MEDIUM`, `HIGH` or `CRITICAL` |
| `detected_at` | string | UTC timestamp, ISO 8601 |
| `status` | enum | `OPEN` or `RESOLVED` |
| `source.watcher` | string | Watcher version, for example `watcher-v0` |
| `evidence.pod_status` | object | Pod phase and per-container state (restart count, waiting reason, last termination reason and exit code) |
| `evidence.kubernetes_events` | array | Recent Kubernetes events for the pod |
| `evidence.metrics` | object | Metric values that triggered the rule |
| `evidence.logs` | array | Recent application log lines (health and metrics probe lines removed) |

## Example

    {
      "incident_id": "INC-002",
      "service": "demo-api",
      "namespace": "default",
      "failure_type": "OOMKilled",
      "severity": "HIGH",
      "detected_at": "2026-10-04T07:10:00Z",
      "status": "OPEN",
      "source": { "watcher": "watcher-v0" },
      "evidence": {
        "pod_status": {
          "name": "demo-api-5b85dd7778-7vt5d",
          "phase": "Running",
          "containers": [
            {
              "name": "demo-api",
              "ready": true,
              "restart_count": 7,
              "waiting_reason": null,
              "last_terminated_reason": "OOMKilled",
              "last_exit_code": 137
            }
          ]
        },
        "kubernetes_events": [
          { "type": "Normal", "reason": "Started", "message": "Started container demo-api", "count": 4 }
        ],
        "metrics": { "restart_count": 7 },
        "logs": [ "... WARNING leaked 30MB, total = 90 MB" ]
      }
    }

## Changing the schema

Any change to `schemas/incident.json` must be agreed with the Diagnoser owner and the version in this file updated.
