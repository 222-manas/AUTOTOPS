import json
from incident_loader import IncidentLoader


def test_incident_loader():

    test_file = "manas_work/test_incident.json"

    incident = {
        "incident_id": "INC-TEST-002",
        "service": "demo-api",
        "namespace": "default",
        "failure_type": "CrashLoopBackOff",
        "severity": "HIGH",
        "detected_at": "2026-10-08T10:00:00Z",
        "status": "OPEN",
        "evidence": {
            "pod_status": {
                "phase": "CrashLoopBackOff"
            },
            "kubernetes_events": [],
            "metrics": {},
            "logs": []
        }
    }

    with open(test_file, "w", encoding="utf-8") as file:
        json.dump(incident, file, indent=2)

    loader = IncidentLoader()

    loaded_incident = loader.load(test_file)

    assert loaded_incident["incident_id"] == "INC-TEST-002"
    assert loaded_incident["service"] == "demo-api"
    assert loaded_incident["failure_type"] == "CrashLoopBackOff"
    assert loaded_incident["severity"] == "HIGH"

    print("Incident Loader test passed!")
    print("Incident ID:", loaded_incident["incident_id"])
    print("Service:", loaded_incident["service"])
    print("Failure Type:", loaded_incident["failure_type"])


if __name__ == "__main__":
    test_incident_loader()