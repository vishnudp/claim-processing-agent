def merge_entities(results):

    final = {
        "insured_name": None,
        "patient_name": None,
        "policy_number": None,
        "hospital_name": None,
        "diagnosis": None,
        "claim_requested_amount": 0,
        "total_hospital_bill": 0,
        "annual_coverage_limit": 0,
        "remaining_coverage": 0,
        "invoice_number": None
    }

    for item in results:

        if not final["insured_name"]:
            final["insured_name"] = item.get(
                "insured_name"
            )

        if not final["patient_name"]:
            final["patient_name"] = item.get(
                "patient_name"
            )

        if not final["policy_number"]:
            final["policy_number"] = item.get(
                "policy_number"
            )

        if not final["hospital_name"]:
            final["hospital_name"] = item.get(
                "hospital_name"
            )

        if not final["diagnosis"]:
            final["diagnosis"] = item.get(
                "diagnosis"
            )

        if not final["invoice_number"]:
            final["invoice_number"] = item.get(
                "invoice_number"
            )


        # Numeric fields - keep highest value
        claim_amount = item.get(
            "claim_requested_amount",
            0
        ) or 0

        if claim_amount > final[
            "claim_requested_amount"
        ]:
            final[
                "claim_requested_amount"
            ] = claim_amount


        hospital_bill = item.get(
            "total_hospital_bill",
            0
        ) or 0

        if hospital_bill > final[
            "total_hospital_bill"
        ]:
            final[
                "total_hospital_bill"
            ] = hospital_bill


        coverage = item.get(
            "annual_coverage_limit",
            0
        ) or 0

        if coverage > final[
            "annual_coverage_limit"
        ]:
            final[
                "annual_coverage_limit"
            ] = coverage


        remaining = item.get(
            "remaining_coverage",
            0
        ) or 0

        if remaining > final[
            "remaining_coverage"
        ]:
            final[
                "remaining_coverage"
            ] = remaining


    return final