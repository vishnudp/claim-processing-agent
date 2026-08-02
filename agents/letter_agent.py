from datetime import datetime


def letter_agent(state):

    entities = state.get(
        "entities",
        {}
    )

    status = state.get(
        "status",
        "PROCESSING"
    )


    if status == "WAITING_FOR_REVIEW":

        title = "HEALTHCARE CLAIM REVIEW REQUIRED"

        decision_text = "PENDING HUMAN REVIEW"

        message = """
We have received and processed your healthcare claim.
The claim requires additional review by our claims
specialist before final approval.
"""

    else:

        title = "HEALTHCARE CLAIM APPROVAL"

        decision_text = "APPROVED"

        message = """
We are pleased to inform you that your healthcare
claim has been successfully processed and approved.
"""


    letter = f"""
====================================================

          {title}

====================================================


Date:
{datetime.now().strftime("%d-%b-%Y")}


To,

{entities.get("insured_name","")}


Subject: Claim Processing Notification
Policy Number: {entities.get("policy_number","")}


Dear {entities.get("insured_name","")},


{message}


Claim Details
----------------------------------------------------

Hospital:
{entities.get("hospital_name","")}


Diagnosis:
{entities.get("diagnosis","")}


Claim Requested Amount:
₹{entities.get("claim_requested_amount",0):,}


Hospital Bill Amount:
₹{entities.get("total_hospital_bill",0):,}


Invoice Number:
{entities.get("invoice_number","")}



Policy Information
----------------------------------------------------

Annual Coverage Limit:
₹{entities.get("annual_coverage_limit",0):,}


Available Coverage:
₹{entities.get("remaining_coverage",0):,}



Decision
----------------------------------------------------

{decision_text}



"""

    if status == "WAITING_FOR_REVIEW":

        letter += """
Reviewer Action Required:

This claim has exceeded the automatic processing
threshold and requires manual verification.

Please review:

✓ Claim amount
✓ Supporting documents
✓ Policy eligibility
✓ Coverage availability


Current Status:
WAITING FOR HUMAN REVIEW


"""

    letter += """
Thank you for choosing our healthcare insurance
services.


Regards,

Claims Processing Department

====================================================
"""


    state["final_letter"] = letter

    return state