# AutoTops: Observability, ML and Detection (Member 2)

Prometheus + Grafana + Loki collect metrics, logs and Kubernetes state. A deterministic Python Watcher applies three rules and writes a standard incident JSON that the Diagnoser can consume.

## Architecture

    demo-api (Flask) --> Prometheus --\
                     --> Loki --------+--> Grafana
    Kubernetes API ------------------>/
              |
              v
          Watcher (watcher/main.py) --> incidents/INC-xxx.json --> Diagnoser (Member 3)

## Layout

    app/             demo Flask app (/health, /metrics, /error, /crash, /leak)
    k8s/             Kubernetes deployment and service
    observability/   Prometheus ServiceMonitor
    watcher/         Watcher: main.py, rules.py, incident.py, collectors/
    schemas/         incident.json (version-controlled contract)
    docs/            metrics.md, incident-schema.md
    tests/           pytest tests
    scripts/         tunnels.sh, errors.sh helpers

## Setup (Ubuntu 22.04 VM)

1. Install Docker, kubectl, kind and helm.
2. Create the cluster: `kind create cluster --name autotops`
3. Build and load the app:

       cd app && docker build -t demo-api:v1 . && cd ..
       kind load docker-image demo-api:v1 --name autotops
       kubectl apply -f k8s/deployment.yaml

4. Install the monitoring stack:

       kubectl create namespace monitoring
       helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
       helm repo add grafana https://grafana.github.io/helm-charts
       helm repo update
       helm install kps prometheus-community/kube-prometheus-stack -n monitoring \
         --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
         --set grafana.adminPassword=admin --set alertmanager.enabled=false \
         --set nodeExporter.enabled=false --set prometheus.prometheusSpec.retention=2d
       helm install loki grafana/loki-stack -n monitoring --set grafana.enabled=false \
         --set promtail.enabled=true --set loki.persistence.enabled=false --set loki.image.tag=2.9.3
       kubectl apply -f observability/prometheus/servicemonitor.yaml

5. In Grafana (http://localhost:3000, admin/admin) add a Loki data source with URL `http://loki:3100`.
6. Python environment:

       python3 -m venv ~/autotops-venv && source ~/autotops-venv/bin/activate
       pip install kubernetes requests jsonschema pytest

## Run

    scripts/tunnels.sh                 # port-forwards: app 5000, Prometheus 9090, Grafana 3000, Loki 3100
    cd watcher && python main.py       # start the Watcher (leave running)

Incidents are written to `incidents/`.

## Failure tests (run in a second terminal)

| Test | Command | Expected incident |
|---|---|---|
| HTTP 5xx | `scripts/errors.sh` | `HighHTTP5xxRate` |
| OOMKilled | `for i in 1 2 3 4 5; do curl -s localhost:5000/leak; done` | `OOMKilled` |
| CrashLoopBackOff | `for i in 1 2 3 4 5; do curl -s localhost:5000/crash; sleep 15; done` | `CrashLoopBackOff` |

Each failure should produce exactly one incident (5 minute cooldown).

## Unit tests

    pytest tests/ -v

The tests fake Prometheus and need no cluster.

## Configuration (environment variables)

| Variable | Default | Meaning |
|---|---|---|
| `SERVICE` | `demo-api` | Service (pod label `app=`) to watch |
| `NAMESPACE` | `default` | Namespace |
| `INTERVAL` | `10` | Seconds between checks |
| `COOLDOWN` | `300` | Seconds before the same incident can be filed again |
| `PROM_URL` | `http://localhost:9090` | Prometheus address |
| `INCIDENT_DIR` | `~/autotops/incidents` | Where incident files are written |

## Docs

- docs/observability/metrics.md
- docs/observability/incident-schema.md

## Status

| Item | Status |
|---|---|
| Prometheus, Grafana, Loki running on a local kind cluster | Done |
| Standard metrics documented (`docs/observability/metrics.md`) | Done |
| Logs centralised in Loki, queryable in Grafana | Done |
| Kubernetes state, events and restart info collected | Done |
| Three deterministic detection rules (CrashLoopBackOff, HighHTTP5xxRate, OOMKilled) | Done |
| Watcher implementation | Done |
| Versioned incident schema (`schemas/incident.json`) | Done |
| Unit tests (11 passing) and manual failure tests | Done |
| Integration with the DevOps app and the Diagnoser | In progress |

## Example incidents

Real incidents produced by the Watcher are in `examples/`, one per failure type. They are the input format for the Diagnoser.

## Not built yet (by design)

LLM integration, RAG, automatic remediation, failure prediction and ML models are deferred. The Watcher is deterministic on purpose.
