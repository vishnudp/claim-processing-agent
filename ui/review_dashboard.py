import streamlit as st

from services.review_service import (
    get_pending_reviews,
    save_review
)


def status_badge(status):

    if status == "PASS":
        return "🟢 PASS"

    return "🔴 FAIL"



def render_review_dashboard():

    st.title(
        "👨‍⚕️ Human Review Queue"
    )

    claims = get_pending_reviews()


    if not claims:

        st.success(
            "✅ No pending reviews"
        )

        return


    st.info(
        f"Pending Claims Awaiting Review: {len(claims)}"
    )


    for index, claim in enumerate(claims):

        claim_id = claim.get(
            "claim_id",
            "UNKNOWN"
        )


        entities = claim.get(
            "entities",
            {}
        )


        validation = claim.get(
            "validation_results",
            {}
        )


        status = claim.get(
            "status",
            "WAITING_FOR_REVIEW"
        )


        policy_number = entities.get(
            "policy_number",
            "N/A"
        )

        patient_name = entities.get(
            "patient_name",
            "Unknown"
        )

        claim_amount = entities.get(
            "claim_requested_amount",
            0
        )


        with st.expander(
            f"📄 {patient_name} | Policy: {policy_number} | ₹{claim_amount:,} | ⚠ {status}",
            expanded=False
        ):


            #
            # TOP SUMMARY
            #

            st.markdown(
                "### Claim Overview"
            )


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "Requested Amount",
                    f"₹{entities.get('claim_requested_amount',0):,}"
                )


            with col2:

                st.metric(
                    "Hospital Bill",
                    f"₹{entities.get('total_hospital_bill',0):,}"
                )


            with col3:

                st.metric(
                    "Policy Number",
                    entities.get(
                        "policy_number",
                        "-"
                    )
                )


            with col4:

                st.metric(
                    "Current Status",
                    status
                )


            st.divider()



            #
            # CUSTOMER DETAILS
            #

            st.markdown(
                "### 👤 Patient Information"
            )


            patient_table = {

                "Field":[
                    "Insured Name",
                    "Patient Name",
                    "Hospital",
                    "Diagnosis",
                    "Invoice Number"
                ],

                "Value":[
                    entities.get(
                        "insured_name",
                        "-"
                    ),

                    entities.get(
                        "patient_name",
                        "-"
                    ),

                    entities.get(
                        "hospital_name",
                        "-"
                    ),

                    entities.get(
                        "diagnosis",
                        "-"
                    ),

                    entities.get(
                        "invoice_number",
                        "-"
                    )
                ]
            }


            st.table(
                patient_table
            )



            #
            # COVERAGE
            #

            st.markdown(
                "### 💰 Coverage Assessment"
            )


            c1,c2,c3 = st.columns(3)


            c1.metric(
                "Annual Limit",
                f"₹{entities.get('annual_coverage_limit',0):,}"
            )


            c2.metric(
                "Used Coverage",
                f"₹{entities.get('annual_coverage_limit',0) - entities.get('remaining_coverage',0):,}"
            )


            c3.metric(
                "Remaining",
                f"₹{entities.get('remaining_coverage',0):,}"
            )



            st.divider()



            #
            # VALIDATION
            #

            st.markdown(
                "### ✅ Automated Validation"
            )


            validation_cols = st.columns(
                len(validation)
            )


            for idx,(rule,result) in enumerate(
                validation.items()
            ):

                with validation_cols[idx]:

                    st.metric(
                        rule.upper(),
                        status_badge(
                            result.get(
                                "status"
                            )
                        )
                    )


                    if result.get(
                        "message"
                    ):

                        st.caption(
                            result["message"]
                        )

                    if result.get(
                        "reason"
                    ):

                        st.caption(
                            result["reason"]
                        )



            st.divider()



            #
            # EXCEPTION
            #

            st.markdown(
                "### ⚠ Review Reason"
            )

            exception_summary = claim.get(
                "exception_summary",
                {}
            )


            review_reasons = []


            # Handle dictionary exception payload
            if isinstance(exception_summary, dict):

                validation_results = exception_summary.get(
                    "validation_results",
                    {}
                )

                for rule, result in validation_results.items():

                    if result.get("status") == "FAIL":

                        reason = (
                            result.get("reason")
                            or
                            result.get("message")
                            or
                            f"{rule} validation failed"
                        )

                        review_reasons.append(
                            f"• {rule.title()}: {reason}"
                        )


            # Handle string fallback
            elif isinstance(exception_summary, str):

                review_reasons.append(
                    exception_summary
                )


            if review_reasons:

                st.error(
                    "\n\n".join(review_reasons)
                )

            else:

                st.info(
                    "Manual verification required"
                )

            st.divider()



            #
            # REVIEW ACTION
            #

            st.markdown(
                "### 👨‍⚕️ Reviewer Decision"
            )


            decision = st.radio(

                "Decision",

                [
                    "Approve",
                    "Reject"
                ],

                horizontal=True,

                key=f"decision_{claim_id}"
            )



            notes = st.text_area(

                "Reviewer Comments",

                placeholder=
                "Add approval justification or rejection reason",

                key=f"notes_{claim_id}"
            )



            if st.button(

                "✅ Submit Review",

                key=f"submit_{claim_id}"

            ):


                save_review(

                    claim_id,

                    {

                        "decision":
                            decision,

                        "notes":
                            notes
                    }

                )


                st.success(
                    "Review decision submitted"
                )


                st.rerun()