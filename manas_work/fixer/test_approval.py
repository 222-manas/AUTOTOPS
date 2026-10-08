from manas_work.fixer.approval import ApprovalManager


def test_approval():
    proposal = {
        "incident_id": "INC-TEST-001",
        "action": "restart",
        "target": "demo-api",
        "reason": "Application pod is repeatedly crashing.",
        "evidence_refs": ["logs"],
        "risk": "MEDIUM",
        "approval_required": True,
        "status": "PROPOSED",
    }

    manager = ApprovalManager()

    approved = manager.approve(proposal)

    assert approved["incident_id"] == "INC-TEST-001"
    assert approved["status"] == "APPROVED"
    assert approved["approved_by"] == "human"
    assert approved["action"] == "restart"

    rejected = manager.reject(proposal)

    assert rejected["status"] == "REJECTED"
    assert rejected["approved_by"] == "human"

    print("Approval test passed!")
    print("Approved:", approved)
    print("Rejected:", rejected)


if __name__ == "__main__":
    test_approval()
