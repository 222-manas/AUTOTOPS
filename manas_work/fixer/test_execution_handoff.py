from manas_work.fixer.execution_handoff import ExecutionHandoff


def test_execution_handoff():

    proposal = {
        "incident_id": "INC-TEST-001",
        "action": "restart",
        "target": "demo-api",
        "reason": "Application pod is repeatedly crashing.",
        "evidence_refs": ["logs"],
        "risk": "MEDIUM",
        "approval_required": True,
        "status": "APPROVED",
        "approved_by": "human",
    }

    handoff_manager = ExecutionHandoff()

    handoff = handoff_manager.create(proposal)

    assert handoff["incident_id"] == "INC-TEST-001"
    assert handoff["action"] == "restart"
    assert handoff["target"] == "demo-api"
    assert handoff["risk"] == "MEDIUM"
    assert handoff["approved_by"] == "human"
    assert handoff["status"] == "READY_FOR_EXECUTION"

    print("Execution Handoff test passed!")
    print("Handoff:")
    print(handoff)


if __name__ == "__main__":
    test_execution_handoff()
