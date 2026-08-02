import os
import json

CLAIMS_DIR = "storage/claims"


def validate_duplicate(entities):

    policy_number = entities.get(
        "policy_number",
        ""
    )

    if not os.path.exists(CLAIMS_DIR):

        return {
            "status": "PASS",
            "message": "No previous claims found"
        }

    for file in os.listdir(CLAIMS_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(
            CLAIMS_DIR,
            file
        )

        with open(path) as f:

            claim = json.load(f)

        existing_policy = (
            claim.get("entities", {})
            .get("policy_number")
        )

        if existing_policy == policy_number:

            return {
                "status": "FAIL",
                "message": "Duplicate policy detected"
            }

    return {
        "status": "PASS",
        "message": "No duplicate found"
    }