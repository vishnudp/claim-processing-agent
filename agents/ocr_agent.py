import pdfplumber
import hashlib

from services.cache_service import cache


def perform_ocr(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def ocr_agent(state):

    pdf_path = state["pdf_path"]

    with open(pdf_path, "rb") as f:

        pdf_hash = hashlib.md5(
            f.read()
        ).hexdigest()

    cache_key = f"ocr_{pdf_hash}"

    cached = cache.get(cache_key)

    if cached:

        state["raw_text"] = cached

        state["progress"] = 20

        return state

    text = perform_ocr(pdf_path)

    cache.set(
        cache_key,
        text
    )

    state["raw_text"] = text

    state["progress"] = 20

    print(
                f"OCR State: "
                f"{state}%"
            )

    return state