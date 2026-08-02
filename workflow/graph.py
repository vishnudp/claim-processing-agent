from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from models.claim_state import ClaimState

from agents.extraction_agent import extraction_agent
from agents.validation_agent import validation_agent
from agents.exception_agent import exception_agent
from agents.letter_agent import letter_agent

from agents.ocr_agent import ocr_agent
from agents.metadata_agent import metadata_agent

from concurrent.futures import ThreadPoolExecutor

from agents.decision_agent import decision_agent

def preprocessing_agent(state):

    with ThreadPoolExecutor(max_workers=2) as executor:

        ocr_future = executor.submit(
            ocr_agent,
            state.copy()
        )

        metadata_future = executor.submit(
            metadata_agent,
            state.copy()
        )

        ocr_result = ocr_future.result()

        metadata_result = metadata_future.result()

    state["raw_text"] = \
        ocr_result["raw_text"]

    print(
                f"OCR Result: "
                f"{ocr_result}%"
            )

    state["metadata"] = \
        metadata_result["metadata"]

    return state


def route_claim(state):

    amount = state["entities"].get(
        "total_hospital_bill",
        0
    )

    if amount > 10000:
        return "exception"

    return "letter"


builder = StateGraph(ClaimState)

builder.add_node(
    "preprocessing",
    preprocessing_agent
)

builder.add_node(
    "extract",
    extraction_agent
)

builder.add_node(
    "validate",
    validation_agent
)

builder.add_node(
    "exception",
    exception_agent
)

builder.add_node(
    "letter",
    letter_agent
)

builder.add_node(
    "decision",
    decision_agent
)

builder.add_edge(
    START,
    "preprocessing"
)

builder.add_edge(
    "preprocessing",
    "extract"
)

builder.add_edge(
    "extract",
    "validate"
)

builder.add_edge(
    "validate",
    "decision"
)




builder.add_conditional_edges(
    "decision",
    lambda state: state["decision"],
    {
        "exception": "exception",
        "letter": "letter"
    }
)





builder.add_edge(
    "exception",
    END
)

builder.add_edge(
    "letter",
    END
)

graph = builder.compile()