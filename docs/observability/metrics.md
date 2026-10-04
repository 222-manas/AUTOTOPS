# Observability Metrics

All metrics are collected by Prometheus. The demo app exposes `/metrics` and is scraped every 10s via a ServiceMonitor (`observability/prometheus/servicemonitor.yaml`).

| Metric | Source | PromQL | Purpose |
|---|---|---|---|
| CPU usage | Prometheus (cAdvisor) | `sum(rate(container_cpu_usage_seconds_total{pod=~"demo-api.*",container="demo-api"}[1m]))` | Resource pressure |
| Memory usage | Prometheus (cAdvisor) | `sum(container_memory_working_set_bytes{pod=~"demo-api.*",container="demo-api"})` | Memory pressure |
| Request rate | App `/metrics` | `sum(rate(http_requests_total[1m]))` | Traffic / workload |
| HTTP error rate | App `/metrics` | `sum(increase(http_requests_total{status=~"5.."}[1m]))` | Detect 5xx failures |
| Request latency (p95) | App `/metrics` | `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` | Detect slow service |
| Pod status | kube-state-metrics | `kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"}` | Detect unhealthy pods |
| Pod restart count | kube-state-metrics | `kube_pod_container_status_restarts_total{pod=~"demo-api.*"}` | Detect repeated crashes |
| OOM kills | kube-state-metrics | `kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}` | Detect memory kills |
| Application health | App `/health` | `up{job="demo-api"}` | Service health |

## Logs

Container logs are collected by Promtail and stored in Loki. Query in Grafana Explore with:

    {app="demo-api"}

## Detection rules used by the Watcher

| Failure type | Signal | Rule |
|---|---|---|
| CrashLoopBackOff | Kubernetes pod state | A container's waiting reason is `CrashLoopBackOff` |
| OOMKilled | Kubernetes pod state | Last termination reason is `OOMKilled` or exit code is 137 |
| HighHTTP5xxRate | Prometheus | More than 5 new HTTP 5xx responses in the last minute |

The 5xx threshold is `ERRORS_5XX_THRESHOLD` in `watcher/rules.py`.

## Notes

- The Watcher reports the same failure at most once per 5 minutes (`COOLDOWN`, default 300s) to avoid duplicate incidents while a pod flaps between states.
- Kubernetes only remembers the last termination reason of a container, so an OOMKilled reason can be replaced by a later crash.
