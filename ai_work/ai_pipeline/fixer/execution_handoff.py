from typing import Any, Dict


class ExecutionHandoff:
    """
    Creates a controlled execution handoff for Member 1.

    Member 3 does not execute Kubernetes actions.
    It only hands an approved remediation proposal
    to the infrastructure layer.
    """

    def create(self, proposal: Dict[str, Any]) -> Dict[str, Any]:

        if proposal.get("status") != "APPROVED":
            raise ValueError(
                "Only APPROVED proposals can be handed to execution."
            )

        return {
            "incident_id": proposal.get("incident_id", "UNKNOWN"),
            "action": proposal.get("action", "UNKNOWN"),
            "target": proposal.get("target", "UNKNOWN"),
            "risk": proposal.get("risk", "UNKNOWN"),
            "approved_by": proposal.get("approved_by", "UNKNOWN"),
            "status": "READY_FOR_EXECUTION",
        }