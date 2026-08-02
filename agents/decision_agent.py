def decision_agent(state):

    print("=" * 80)
    print("DECISION AGENT STARTED")
    print("=" * 80)

    print("Entities received:")
    print(state.get("entities"))

    amount = (
        state["entities"].get(
            "claim_requested_amount",
            0
        )
        or 0
    )

    annual_coverage_limit = (
        state["entities"].get(
            "annual_coverage_limit",
            0
        )
        or 0
    )
    print(
        f"Decision claim requested amount: {amount}"
    )

    if amount > annual_coverage_limit:

        state["hitl_required"] = True

        state["status"] = "WAITING_FOR_REVIEW"

    else:

        state["hitl_required"] = False

        state["status"] = "AUTO_APPROVED"

    return state