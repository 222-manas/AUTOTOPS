# Observability — Watcher & Monitoring

This component collects signals from Kubernetes and Prometheus and applies deterministic rules to emit normalized incident JSON for the AI Work pipeline.

## Structure
- `watcher/` — Watcher entry point, rules, incident model, collectors, and unit tests.
- `prometheus/` — ServiceMonitor configuration.
- `tests/` — Watcher unit tests.
- `docs/` — metrics and incident-schema documentation.

## Test from repository root

```powershell
python -m pytest .\observability\watcher\tests -v
```

Unit tests mock external monitoring calls. Running the live Watcher requires a configured Kubernetes context and reachable Prometheus endpoint.
