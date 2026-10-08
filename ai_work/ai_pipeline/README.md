# Manas Work AI Pipeline

Consumes the shared incident JSON produced by `manas_work/watcher/` and generates a validated diagnosis, remediation proposal, approval-gated handoff, recovery result, and report.

- `incident_loader.py` — loads incident JSON and checks required fields.
- `diagnoser/` — context builder, mock/Ollama diagnosers, diagnosis validator.
- `fixer/` — remediation proposals, approval manager, execution handoff.
- `recovery/` — recovery-result receiver.
- `reporter/` — structured and text reports.
- `tests/` — end-to-end, loader, schema, and pipeline tests; component tests stay alongside components.

Run from repository root:
```powershell
python -m pytest manas_work/ai_pipeline -v
```
LLM tests require Ollama at `http://localhost:11434` and `llama3.2:3b`. Inputs are in `manas_work/examples/`; schemas are in `manas_work/schemas/`. Execution/recovery results are simulated, not real Kubernetes actions.
