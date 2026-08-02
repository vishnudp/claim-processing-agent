import os
import json


def calculate_metrics():

    total = 0
    approved = 0
    hitl = 0
    rejected = 0

    for file in os.listdir(
            "storage/claims"
    ):

        total += 1

        with open(
                f"storage/claims/{file}"
        ) as f:

            claim = json.load(f)

        if claim["status"] == "APPROVED":
            approved += 1

        if claim["hitl_required"]:
            hitl += 1

        if claim["status"] == "REJECTED":
            rejected += 1

    return {

        "total_claims": total,

        "auto_approved": approved,

        "hitl_claims": hitl,

        "rejected": rejected
    }