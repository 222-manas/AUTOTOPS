import sys
from pathlib import Path

# Add manas_work to Python's import path
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from incident_loader import IncidentLoader
from diagnoser.context import DiagnosticContext
from diagnoser.ollama import OllamaDiagnoser


def test_ollama_diagnoser():

    # Load a real incident produced by Member 2
    incident_file = "examples/incident-CrashLoopBackOff.json"

    loader = IncidentLoader()
    incident = loader.load(incident_file)

    # Build normalized diagnostic context
    context_builder = DiagnosticContext()
    context = context_builder.build(incident)

    # Run the local Ollama diagnoser
    diagnoser = OllamaDiagnoser()

    diagnosis = diagnoser.diagnose(context)

    # Validate the diagnosis structure
    assert diagnosis["incident_id"] == incident["incident_id"]
    assert diagnosis["root_cause"] != ""
    assert isinstance(diagnosis["evidence"], list)
    assert 0 <= diagnosis["confidence"] <= 1
    assert diagnosis["recommended_action"] != ""

    print("\n========================================")
    print("OLLAMA DIAGNOSER TEST PASSED")
    print("========================================")

    print("\nDiagnosis:")
    print(diagnosis)


if __name__ == "__main__":
    test_ollama_diagnoser()