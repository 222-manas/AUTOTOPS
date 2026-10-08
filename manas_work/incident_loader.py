import json
from pathlib import Path
from typing import Any, Dict


class IncidentLoader:
    """
    Loads an AutoTops Incident JSON file.

    Member 2 produces the Incident JSON.
    Manas Work consumes it.
    """

    def load(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Incident file not found: {file_path}"
            )

        with path.open("r", encoding="utf-8") as file:
            incident = json.load(file)

        self._validate(incident)

        return incident

    def _validate(self, incident: Dict[str, Any]) -> None:
        required_fields = [
            "incident_id",
            "service",
            "namespace",
            "failure_type",
            "severity",
            "detected_at",
            "status",
            "evidence",
        ]

        for field in required_fields:
            if field not in incident:
                raise ValueError(
                    f"Invalid incident: missing field '{field}'"
                )

        evidence = incident["evidence"]

        required_evidence = [
            "pod_status",
            "kubernetes_events",
            "metrics",
            "logs",
        ]

        for field in required_evidence:
            if field not in evidence:
                raise ValueError(
                    f"Invalid incident evidence: missing field '{field}'"
                )