from datetime import datetime


def reviewer_agent(state):

    """
    Human approval/rejection step.

    This agent is executed after
    exception_agent generates the review summary.

    Human decision comes from UI.
    """

    decision = state.get("human_decision")

    if not decision:

        state["status"] = "WAITING_FOR_REVIEW"

        return state

    state["reviewed_at"] = str(datetime.now())

    state["reviewed_by"] = state.get(
        "reviewed_by",
        "caseworker"
    )

    state["status"] = decision.upper()

    return state