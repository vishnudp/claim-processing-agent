def validate_duplicate(claim):

    claim_id = claim["claim_id"]

    path = "storage/claims"

    for file in os.listdir(path):

        existing = load_claim(file)

        if existing["claim_id"] == claim_id:

            return {
                "status":"FAIL"
            }

    return {
        "status":"PASS"
    }