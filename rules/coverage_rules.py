def validate_coverage(claim):

    claim_amount = claim.get(
        "claim_requested_amount",
        0
    )

    remaining_coverage = claim.get(
        "remaining_coverage",
        0
    )

    annual_limit = claim.get(
        "annual_coverage_limit",
        0
    )


    if not claim.get("policy_number"):

        return {
            "status": "FAIL",
            "reason": "Policy number missing"
        }


    if remaining_coverage == 0:

        return {
            "status": "FAIL",
            "reason": "Coverage information missing"
        }


    if claim_amount > remaining_coverage:

        return {
            "status": "FAIL",
            "reason": "Claim exceeds remaining coverage",
            "claim_amount": claim_amount,
            "remaining_coverage": remaining_coverage
        }


    if claim_amount > annual_limit:

        return {
            "status": "FAIL",
            "reason": "Claim exceeds annual coverage limit",
            "claim_amount": claim_amount,
            "annual_limit": annual_limit
        }


    return {
        "status": "PASS",
        "reason": "Coverage available",
        "remaining_coverage": remaining_coverage
    }