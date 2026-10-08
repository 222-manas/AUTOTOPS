# AI Work — Incident Response Pipeline

This component consumes normalized incident JSON from the observability Watcher and runs diagnosis, validation, remediation proposal, approval handoff, recovery-result handling, and reporting.

- `incident_loader.py` — loads and validates the shared incident JSON contract.
- `diagnoser/` — diagnostic context, mock/Ollama diagnosis, and output validation.
- `fixer/` — remediation proposals, approval manager, and execution handoff.
- `recovery/` — recovery-result validation.
- `reporter/` — incident report generation.
- `tests/` — end-to-end, loader, schema, and pipeline tests.

Run from the repository root:

```powershell
python -m pytest .\ai_work\ai_pipeline -v
```

Ollama-backed tests require Ollama at `http://localhost:11434` with `llama3.2:3b`. Sample incidents are in `ai_work/examples/`; schemas are in `ai_work/schemas/`.

**Execution boundary:** the pipeline validates diagnoses and prepares approval-gated remediation handoffs. Tests simulate execution and recovery; they do not prove real Kubernetes resources were changed.
