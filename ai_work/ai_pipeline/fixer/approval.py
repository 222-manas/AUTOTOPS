from typing import Any, Dict


class ApprovalManager:
    """
    Handles human approval or rejection of a remediation proposal.

    This component does not execute the remediation action.
    """

    def approve(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        approved_proposal = proposal.copy()

        approved_proposal["status"] = "APPROVED"
        approved_proposal["approved_by"] = "human"
        approved_proposal["approval_required"] = True

        return approved_proposal

    def reject(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        rejected_proposal = proposal.copy()

        rejected_proposal["status"] = "REJECTED"
        rejected_proposal["approved_by"] = "human"
        rejected_proposal["approval_required"] = True

        return rejected_proposal