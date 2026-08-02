import os
import json
from datetime import datetime

CLAIMS_DIR = "storage/claims"
REVIEWS_DIR = "storage/reviews"


def get_pending_reviews():

    pending = []

    if not os.path.exists(CLAIMS_DIR):
        return pending

    for file in os.listdir(CLAIMS_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(
            CLAIMS_DIR,
            file
        )

        with open(path) as f:
            claim = json.load(f)

        if claim.get("status") == \
                "WAITING_FOR_REVIEW":

            pending.append(claim)

    return pending


def save_review(claim_id, review):

    os.makedirs(
        REVIEWS_DIR,
        exist_ok=True
    )

    review["reviewed_at"] = \
        datetime.now().isoformat()

    #
    # Save review file
    #

    review_path = os.path.join(
        REVIEWS_DIR,
        f"{claim_id}.json"
    )

    with open(review_path, "w") as f:

        json.dump(
            review,
            f,
            indent=2
        )

    #
    # Update claim file
    #

    claim_path = os.path.join(
        CLAIMS_DIR,
        f"{claim_id}.json"
    )

    if not os.path.exists(
            claim_path
    ):
        return

    with open(claim_path) as f:

        claim = json.load(f)

    decision = review.get(
        "decision",
        ""
    ).upper()

    if decision == "APPROVE":

        claim["status"] = \
            "APPROVED"

    elif decision == "REJECT":

        claim["status"] = \
            "REJECTED"

    #
    # Persist review details
    #

    claim["review"] = {

        "decision":
            review.get(
                "decision"
            ),

        "notes":
            review.get(
                "notes"
            ),

        "reviewed_at":
            review.get(
                "reviewed_at"
            )
    }

    with open(claim_path, "w") as f:

        json.dump(
            claim,
            f,
            indent=2
        )


def get_review(claim_id):

    review_path = os.path.join(
        REVIEWS_DIR,
        f"{claim_id}.json"
    )

    if not os.path.exists(
            review_path
    ):
        return None

    with open(review_path) as f:

        return json.load(f)


def get_all_reviews():

    reviews = []

    if not os.path.exists(
            REVIEWS_DIR
    ):
        return reviews

    for file in os.listdir(
            REVIEWS_DIR
    ):

        if not file.endswith(
                ".json"
        ):
            continue

        path = os.path.join(
            REVIEWS_DIR,
            file
        )

        with open(path) as f:

            reviews.append(
                json.load(f)
            )

    return reviews