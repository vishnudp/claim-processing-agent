import json
import os

CLAIM_DIR = "storage/claims"


def save_claim(claim_id, data):

    os.makedirs(
        CLAIM_DIR,
        exist_ok=True
    )

    path = f"{CLAIM_DIR}/{claim_id}.json"

    with open(path, "w") as f:

        json.dump(
            data,
            f,
            indent=2
        )


def load_claim(claim_id):

    path = f"{CLAIM_DIR}/{claim_id}.json"

    if not os.path.exists(path):
        return None

    with open(path) as f:
        return json.load(f)