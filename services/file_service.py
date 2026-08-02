import os


UPLOAD_DIR = "storage/uploads"


def save_file(uploaded_file):

    path = os.path.join(

        UPLOAD_DIR,

        uploaded_file.name
    )

    with open(path, "wb") as f:

        f.write(
            uploaded_file.getbuffer()
        )

    return path