from typing import TypedDict


class ClaimState(TypedDict):

    claim_id: str

    pdf_path: str

    raw_text: str

    metadata: dict

    entities: dict

    validation_results: dict

    hitl_required: bool

    exception_summary: str

    human_decision: str

    final_letter: str

    progress: int

    status: str