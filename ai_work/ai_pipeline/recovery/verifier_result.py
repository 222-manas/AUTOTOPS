from typing import Any, Dict


class RecoveryResult:
    """
    Receives the recovery verification result from Member 2.

    Member 2 performs the actual observability checks.
    Manas Work only consumes and validates the result.
    """

    def receive(self, result: Dict[str, Any]) -> Dict[str, Any]:

        required_fields = [
            "incident_id",
            "status",
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(
                    f"Invalid recovery result: missing field '{field}'"
                )

        allowed_statuses = [
            "RECOVERED",
            "NOT_RECOVERED",
            "ESCALATED",
        ]

        if result["status"] not in allowed_statuses:
            raise ValueError(
                f"Invalid recovery status: {result['status']}"
            )

        return result