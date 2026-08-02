import json
import os

CLAIMS_DIR = "storage/claims"

os.makedirs(
    CLAIMS_DIR,
    exist_ok=True
)


def save_claim(state):

    path = os.path.join(
        CLAIMS_DIR,
        f"{state['claim_id']}.json"
    )

    with open(path, "w") as f:

        json.dump(
            state,
            f,
            indent=2
        )


def get_all_claims():

    claims = []

    if not os.path.exists(
            CLAIMS_DIR
    ):
        return claims

    for file in os.listdir(
            CLAIMS_DIR
    ):

        if not file.endswith(".json"):
            continue

        with open(
            os.path.join(
                CLAIMS_DIR,
                file
            )
        ) as f:

            claims.append(
                json.load(f)
            )

    return claims