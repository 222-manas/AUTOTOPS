# Observability Metrics

The demo app exposes `/metrics`; Prometheus scrapes it using `observability/prometheus/servicemonitor.yaml`.

| Metric | Source | PromQL | Purpose |
|---|---|---|---|
| CPU usage | Prometheus (cAdvisor) | `sum(rate(container_cpu_usage_seconds_total{pod=~"demo-api.*",container="demo-api"}[1m]))` | Resource pressure |
| Memory usage | Prometheus (cAdvisor) | `sum(container_memory_working_set_bytes{pod=~"demo-api.*",container="demo-api"})` | Memory pressure |
| Request rate | App metrics | `sum(rate(http_requests_total[1m]))` | Traffic/workload |
| HTTP error count | App metrics | `sum(increase(http_requests_total{status=~"5.."}[1m]))` | Detect 5xx failures |
| Request latency (p95) | App metrics | `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` | Slow service |
| Pod status | Kubernetes | `kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"}` | Unhealthy pods |
| Restarts | Kubernetes | `kube_pod_container_status_restarts_total{pod=~"demo-api.*"}` | Repeated crashes |
| OOM kills | Kubernetes | `kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}` | Memory kills |

## Logs
Promtail sends container logs to Loki. In Grafana Explore, query `{app="demo-api"}`.

## Watcher rules
| Failure type | Rule |
|---|---|
| CrashLoopBackOff | A container waiting reason is `CrashLoopBackOff` |
| OOMKilled | Last termination reason is `OOMKilled` or exit code 137 |
| HighHTTP5xxRate | More than 5 new HTTP 5xx responses in the last minute |

The threshold is `ERRORS_5XX_THRESHOLD` in `observability/watcher/rules.py`. Duplicate incidents are suppressed during the cooldown (default 300 seconds).
