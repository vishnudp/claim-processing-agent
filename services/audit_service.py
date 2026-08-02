import os
import json
from datetime import datetime

AUDIT_FILE = "storage/audit_logs.json"


def save_audit_log(
    message,
    claim_id="",
    policy_number="",
    insured_name="",
    stage="",
    status=""
):

    os.makedirs(
        "storage",
        exist_ok=True
    )

    logs = []

    if os.path.exists(AUDIT_FILE):

        with open(AUDIT_FILE) as f:
            logs = json.load(f)

    logs.append(
        {
            "timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "claim_id":
                claim_id,

            "policy_number":
                policy_number,

            "insured_name":
                insured_name,

            "stage":
                stage,

            "status":
                status,

            "message":
                message
        }
    )

    with open(
        AUDIT_FILE,
        "w"
    ) as f:

        json.dump(
            logs,
            f,
            indent=2
        )


def get_audit_logs():

    if not os.path.exists(
            AUDIT_FILE
    ):
        return []

    with open(AUDIT_FILE) as f:
        return json.load(f)