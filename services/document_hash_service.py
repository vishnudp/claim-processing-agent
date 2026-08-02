import hashlib


def calculate_hash(path):

    with open(path, "rb") as f:

        return hashlib.md5(
            f.read()
        ).hexdigest()