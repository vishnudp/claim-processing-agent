from concurrent.futures import ThreadPoolExecutor

from rules.policy_rules import validate_policy
from rules.coverage_rules import validate_coverage
from rules.invoice_rules import validate_invoice
from rules.duplicate_rules import validate_duplicate


def validation_agent(state):

    entities = state["entities"]

    print(
                f"state: "
                f"{state}"
            )

    with ThreadPoolExecutor(max_workers=4) as executor:

        policy_future = executor.submit(
            validate_policy,
            entities
        )

        coverage_future = executor.submit(
            validate_coverage,
            entities
        )

        invoice_future = executor.submit(
            validate_invoice,
            entities
        )

        duplicate_future = executor.submit(
            validate_duplicate,
            entities
        )

    state["validation_results"] = {

        "policy":
            policy_future.result(),

        "coverage":
            coverage_future.result(),

        "invoice":
            invoice_future.result(),

        "duplicate":
            duplicate_future.result()
    }

    return state