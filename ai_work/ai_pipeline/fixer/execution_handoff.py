from typing import Any, Dict


class ExecutionHandoff:
    """Prepare an approved remediation proposal for execution."""

    def create(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        if proposal.get("status") != "APPROVED":
            raise ValueError(
                "Only APPROVED proposals can be handed to execution."
            )

        if proposal.get("approval_required") is not True:
            raise ValueError(
                "A valid approval requirement must be recorded."
            )

        approved_by = proposal.get("approved_by")
        if not isinstance(approved_by, str) or not approved_by.strip():
            raise ValueError(
                "A non-empty approver identity is required."
            )

        required_fields = ("incident_id", "action", "target", "risk")
        for field in required_fields:
            value = proposal.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"Missing or invalid required field: {field}"
                )

        return {
            "incident_id": proposal["incident_id"],
            "action": proposal["action"],
            "target": proposal["target"],
            "risk": proposal["risk"],
            "approved_by": approved_by.strip(),
            "status": "READY_FOR_EXECUTION",
        }
