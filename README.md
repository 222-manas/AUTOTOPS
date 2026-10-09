# AutoTops — AI Incident Response & Kubernetes Observability

AutoTops combines Kubernetes observability, deterministic incident detection, and an AI-assisted incident-response pipeline.

## End-to-end workflow

```text
Demo API -> Prometheus / Kubernetes API -> Observability Watcher
         -> normalized incident JSON -> AI Work pipeline
         -> diagnosis -> validation -> remediation proposal
         -> approval-gated handoff -> recovery verification -> report
```

## Repository layout

- `app/` — Flask demo API.
- `k8s/` — Kubernetes manifests.
- `observability/watcher/` — incident rules, collectors, Watcher, and tests.
- `observability/prometheus/` — Prometheus ServiceMonitor.
- `observability/docs/` — metrics and incident contract documentation.
- `ai_work/ai_pipeline/` — incident loader, diagnosis, validation, remediation proposals, approval handoff, recovery results, and reporting.
- `ai_work/examples/` and `ai_work/schemas/` — sample incidents and JSON contracts.
- `scripts/` — local demo helpers.

## Run tests (PowerShell, repository root)

```powershell
python -m pytest .\observability\watcher\tests -v
python -m pytest .\ai_work\ai_pipeline -v
```

Ollama-backed tests require Ollama at `http://localhost:11434` with `llama3.2:3b`. Watcher unit tests mock monitoring calls and do not require a live Kubernetes cluster.

## Run the Watcher

Configure Kubernetes credentials and ensure Prometheus is reachable first.

```powershell
$env:INCIDENT_DIR = "$HOME\autotops\incidents"
python .\observability\watcher\main.py
```

## Demo deployment

Review failure-simulation endpoints first; they intentionally disrupt the demo application.

```bash
kind create cluster --name autotops
cd app && docker build -t demo-api:v1 . && cd ..
kind load docker-image demo-api:v1 --name autotops
kubectl apply -f k8s/deployment.yaml
kubectl apply -f observability/prometheus/servicemonitor.yaml
```

Install and configure Prometheus, Grafana, and Loki before starting the Watcher. Helper scripts are in `scripts/`.

## Execution boundary

The AI pipeline validates diagnoses and prepares remediation proposals with an approval handoff. Automated tests simulate execution and recovery; they do **not** demonstrate that real Kubernetes resources were remediated. A production executor must enforce authorization and approval before cluster-changing actions.
