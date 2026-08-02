import os


LETTER_DIR = \
    "storage/generated_letters"


def save_letter(

        claim_id,

        content
):

    path = os.path.join(

        LETTER_DIR,

        f"{claim_id}.txt"
    )

    with open(path, "w") as f:

        f.write(content)

    return path