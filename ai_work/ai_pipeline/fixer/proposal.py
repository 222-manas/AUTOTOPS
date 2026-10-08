from typing import Any, Dict, List


class RemediationProposal:
    """
    Creates a structured remediation proposal.

    This component proposes an action but does not execute it.
    """

    def create(
        self,
        incident: Dict[str, Any],
        diagnosis: Dict[str, Any],
    ) -> Dict[str, Any]:

        failure_type = incident.get("failure_type", "UNKNOWN")
        incident_id = incident.get("incident_id", "UNKNOWN")
        service = incident.get("service", "UNKNOWN")

        evidence_refs: List[str] = []

        if incident.get("evidence", {}).get("logs"):
            evidence_refs.append("logs")

        if incident.get("evidence", {}).get("kubernetes_events"):
            evidence_refs.append("kubernetes_events")

        if incident.get("evidence", {}).get("metrics"):
            evidence_refs.append("metrics")

        if failure_type == "CrashLoopBackOff":
            action = "restart"
            reason = diagnosis.get(
                "root_cause",
                "The application pod is repeatedly crashing."
            )
            risk = "MEDIUM"

        elif failure_type == "OOMKilled":
            action = "scale"
            reason = diagnosis.get(
                "root_cause",
                "The application exceeded its memory limit."
            )
            risk = "HIGH"

        elif failure_type == "HighHTTP5xxRate":
            action = "rollback"
            reason = diagnosis.get(
                "root_cause",
                "The application is experiencing a high HTTP 5xx error rate."
            )
            risk = "HIGH"

        else:
            action = "investigate"
            reason = "Insufficient evidence to safely recommend remediation."
            risk = "HIGH"

        return {
            "incident_id": incident_id,
            "action": action,
            "target": service,
            "reason": reason,
            "evidence_refs": evidence_refs,
            "risk": risk,
            "approval_required": True,
            "status": "PROPOSED",
        }