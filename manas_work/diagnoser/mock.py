from typing import Any, Dict

from .interface import Diagnoser


class MockDiagnoser(Diagnoser):
    """
    Simple deterministic diagnoser used to test the
    Manas Work diagnosis pipeline before adding an LLM.
    """

    def diagnose(self, incident: Dict[str, Any]) -> Dict[str, Any]:

        failure_type = incident.get("failure_type", "UNKNOWN")
        incident_id = incident.get("incident_id", "UNKNOWN")

        if failure_type == "CrashLoopBackOff":
            root_cause = "Application pod is repeatedly crashing."
            recommended_action = (
                "Inspect application logs and recent configuration changes."
            )

        elif failure_type == "OOMKilled":
            root_cause = (
                "Application pod was terminated because it exceeded "
                "its memory limit."
            )
            recommended_action = (
                "Inspect memory usage and review the pod memory configuration."
            )

        elif failure_type == "HighHTTP5xxRate":
            root_cause = (
                "Application is returning an unusually high number "
                "of HTTP 5xx responses."
            )
            recommended_action = (
                "Inspect application logs and recent deployment changes."
            )

        else:
            root_cause = (
                "Unable to determine the root cause from the "
                "supplied diagnostic context."
            )
            recommended_action = "Collect additional diagnostic evidence."

        return {
            "incident_id": incident_id,
            "root_cause": root_cause,
            "evidence": {
                "pod_status": incident.get("pod_status", {}),
                "kubernetes_events": incident.get(
                    "kubernetes_events", []
                ),
                "metrics": incident.get("metrics", {}),
                "logs": incident.get("logs", []),
            },
            "confidence": 0.70,
            "recommended_action": recommended_action,
        }