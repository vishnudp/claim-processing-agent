import json
import re
import traceback

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from services.ollama_client import generate
from services.chunking_service import chunk_text
from services.entity_merge_service import merge_entities




def clean_json_response(text):

    if not text:
        raise ValueError(
            "Empty LLM response"
        )

    text = text.strip()

    # remove markdown
    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    # find JSON
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        return text[start:end+1]

    raise ValueError(
        f"No JSON found:\n{text}"
    )


def extract_chunk(chunk):

    prompt = f"""
Return ONLY JSON.

Do not explain.
Do not reason.
Do not add markdown.

Extract these fields:

{{
"insured_name": null,
"patient_name": null,
"policy_number": null,
"hospital_name": null,
"diagnosis": null,
"claim_requested_amount": 0,
"total_hospital_bill": 0,
"annual_coverage_limit": 0,
"remaining_coverage": 0,
"invoice_number": null
}}

Document:

{chunk}
"""

    try:

        print("=" * 80)
        print("Sending prompt to Ollama...")
        print("=" * 80)

        response = generate(prompt)

        print("RAW RESPONSE:")
        print(response)
        print("=" * 80)

        cleaned = clean_json_response(response)

        print("CLEANED JSON:")
        print(cleaned)

        data = json.loads(cleaned)

        print("PARSED JSON:")
        print(data)

        return data

    except Exception as e:

        print("\nEXTRACTION ERROR")
        print(type(e).__name__, e)
        traceback.print_exc()

        if "response" in locals():
            print("\nMODEL RESPONSE:")
            print(response)

        return {}


def extraction_agent(state, progress_callback=None):

    print("\nStarting entity extraction...\n")

    state["entity_stage"] = "chunking"

    # Don't chunk small documents.
    # if len(state["raw_text"]) < 8000:
    #     chunks = [state["raw_text"]]
    # else:
    chunks = chunk_text(state["raw_text"])

    print(f"Chunks: {len(chunks)}")

    state["entity_stage"] = "parallel_extraction"

    results = []

    total_chunks = len(chunks)
    completed = 0

    with ThreadPoolExecutor(max_workers=4) as executor:

        futures = [
            executor.submit(
                extract_chunk,
                chunk
            )
            for chunk in chunks
        ]

        for future in as_completed(futures):

            result = future.result()

            print("\nChunk Result:")
            print(result)

            results.append(result)

            completed += 1

            progress = int(
                completed * 100 / total_chunks
            )

            print(
                f"Entity Extraction Progress: {progress}%"
            )

            state["entity_progress"] = progress

            if progress_callback:

                progress_callback(
                    progress,
                    completed,
                    total_chunks
                )

    print("\nResults Before Merge:")
    print(json.dumps(results, indent=4))

    state["entity_stage"] = "merge"

    merged = merge_entities(results)

    print("\nMerged Entities:")
    print(json.dumps(merged, indent=4))

    state["entity_stage"] = "completed"

    state["entities"] = merged

    return state