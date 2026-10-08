from incident_loader import IncidentLoader
from diagnoser.context import DiagnosticContext
from diagnoser.mock import MockDiagnoser
from fixer.proposal import RemediationProposal
from fixer.approval import ApprovalManager
from fixer.execution_handoff import ExecutionHandoff
from recovery.verifier_result import RecoveryResult
from reporter.reporter import IncidentReporter


def test_real_pipeline():

    # 1. Load the real incident produced by Member 2
    incident_file = "examples/incident-CrashLoopBackOff.json"

    loader = IncidentLoader()
    incident = loader.load(incident_file)

    print("\nIncident loaded:")
    print(incident)

    # 2. Build normalized diagnostic context
    context_builder = DiagnosticContext()
    diagnostic_context = context_builder.build(incident)

    print("\nDiagnostic context created:")
    print(diagnostic_context)

    # 3. Diagnose using the diagnostic context
    diagnoser = MockDiagnoser()
    diagnosis = diagnoser.diagnose(diagnostic_context)

    print("\nDiagnosis:")
    print(diagnosis)

    # 4. Create remediation proposal
    fixer = RemediationProposal()
    proposal = fixer.create(incident, diagnosis)

    # 5. Human approval
    approval_manager = ApprovalManager()
    approval = approval_manager.approve(proposal)

    # 6. Create execution handoff for Member 1
    handoff_manager = ExecutionHandoff()
    handoff = handoff_manager.create(approval)

    # Member 1 execution is simulated here.
    execution = {
        "status": "SUCCESS",
        "action": handoff["action"],
        "target": handoff["target"]
    }

    # 7. Receive recovery verification from Member 2
    recovery_receiver = RecoveryResult()

    recovery = recovery_receiver.receive({
        "incident_id": incident["incident_id"],
        "status": "RECOVERED",
        "details": {
            "pod_ready": True,
            "error_rate_normal": True,
            "restart_count_stable": True
        }
    })

    # 8. Generate final report
    reporter = IncidentReporter()

    report = reporter.generate(
        incident,
        diagnosis,
        proposal,
        approval,
        execution,
        recovery
    )

    # Assertions
    assert report["incident_id"] == incident["incident_id"]
    assert report["service"] == incident["service"]
    assert report["failure_type"] == "CrashLoopBackOff"
    assert report["approval_status"] == "APPROVED"
    assert report["execution_status"] == "SUCCESS"
    assert report["recovery_status"] == "RECOVERED"

    print("\n========================================")
    print("REAL AUTOTOPS PIPELINE TEST PASSED")
    print("========================================")

    print("\nFinal Report:")
    print(reporter.to_text(report))


if __name__ == "__main__":
    test_real_pipeline()