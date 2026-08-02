import os
from datetime import datetime

import fitz  # PyMuPDF


def metadata_agent(state):

    pdf_path = state["pdf_path"]

    file_name = os.path.basename(pdf_path)

    file_size_mb = round(
        os.path.getsize(pdf_path) / (1024 * 1024),
        2
    )

    doc = fitz.open(pdf_path)

    page_count = len(doc)

    doc.close()

    metadata = {

        "file_name": file_name,

        "file_size_mb": file_size_mb,

        "page_count": page_count,

        "upload_time": str(
            datetime.now()
        ),

        "document_type":
            "insurance_claim"
    }

    state["metadata"] = metadata

    print(
                f"Metadata State: "
                f"{state}%"
            )

    if page_count > 50:
        raise Exception(
            "Document too large"
        )

    if file_size_mb > 25:
        raise Exception(
            "File exceeds limit"
        )

    return state