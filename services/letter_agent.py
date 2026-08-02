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

        decision_text = "PENDING HUMAN REVIEW"

    else:

        decision_text = "APPROVED"


    letter = f"""
====================================================

              HEALTHCARE CLAIM APPROVAL

====================================================


Date:
{datetime.now().strftime("%d-%b-%Y")}


To,

{entities.get("insured_name","")}


Subject: Claim Approval Notification
Policy Number: {entities.get("policy_number","")}


Dear {entities.get("insured_name","")},


We are pleased to inform you that your healthcare
claim has been successfully processed.


Claim Details
----------------------------------------------------

Hospital:
{entities.get("hospital_name","")}


Diagnosis:
{entities.get("diagnosis","")}


Claim Requested Amount:
₹{entities.get("claim_requested_amount",0):,}


Approved Amount:
₹{entities.get("total_hospital_bill",0):,}


Invoice Number:
{entities.get("invoice_number","")}



Policy Information
----------------------------------------------------

Annual Coverage Limit:
₹{entities.get("annual_coverage_limit",0):,}


Available Coverage:
₹{entities.get("remaining_coverage",0):,}



Decision:
{decision_text}



Thank you for choosing our healthcare insurance
services.


Regards,

Claims Processing Department

====================================================
"""


    state["final_letter"] = letter

    return state