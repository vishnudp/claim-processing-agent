POLICIES = {

    "POL-78945-A": {

        "status": "ACTIVE",

        "coverage_limit": 50000
    }
}


def validate_policy(claim):

    policy = POLICIES.get(
        claim["policy_number"]
    )

    if not policy:

        return {
            "status": "FAIL",
            "message": "Policy not found"
        }

    if policy["status"] != "ACTIVE":

        return {
            "status": "FAIL",
            "message": "Policy inactive"
        }

    return {
        "status": "PASS"
    }