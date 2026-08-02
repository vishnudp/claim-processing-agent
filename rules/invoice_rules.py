def validate_invoice(claim):

    print(
                f"invoice claim: "
                f"{claim}%"
            )

    calculated = (

        claim["total_hospital_bill"]

        # + claim["pre_hospitalization_bill"]

        # + claim["post_hospitalization_bill"]

        # + claim["pharmacy_bill"]
    )

    if calculated != \
            claim["total_hospital_bill"]:

        return {

            "status": "FAIL",

            "message":
                "Invoice mismatch"
        }

    return {

        "status": "PASS"
    }