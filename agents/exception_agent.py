from services.ollama_client import generate


def exception_agent(state):

    entities = state.get(
        "entities",
        {}
    )

    validations = state.get(
        "validation_results",
        {}
    )

    prompt = f"""
    Create an exception review summary
    for a human claims reviewer.

    Claim Data:
    {entities}

    Validation Results:
    {validations}

    Explain:
    - Why review is required
    - Key risks
    - Recommendation
    """

    response = generate(prompt)

    state["exception_summary"] = response

    state["status"] = "WAITING_FOR_REVIEW"

    return state