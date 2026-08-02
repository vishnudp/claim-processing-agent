import streamlit as st

from services.claim_storage_service import (
    get_all_claims
)


def status_badge(status):

    mapping = {

        "AUTO_APPROVED":
            "🟢 AUTO APPROVED",

        "WAITING_FOR_REVIEW":
            "🟡 HUMAN REVIEW REQUIRED",

        "REJECTED":
            "🔴 REJECTED"
    }

    return mapping.get(
        status,
        status
    )



def render_claims_dashboard():

    st.title(
        "📋 Processed Claims Dashboard"
    )


    claims = get_all_claims()


    if not claims:

        st.info(
            "No claims processed yet"
        )

        return



    # -------------------------
    # Dashboard Metrics
    # -------------------------

    total_claims = len(claims)

    approved_claims = [
        c for c in claims
        if c.get("status") == "AUTO_APPROVED"
    ]

    review_claims = [
        c for c in claims
        if c.get("status") == "WAITING_FOR_REVIEW"
    ]

    rejected_claims = [
        c for c in claims
        if c.get("status") == "REJECTED"
    ]



    if "claim_filter" not in st.session_state:

        st.session_state.claim_filter = "ALL"



    col1, col2, col3, col4 = st.columns(4)


    with col1:

        if st.button(
            f"📄 Total\n{total_claims}",
            use_container_width=True
        ):

            st.session_state.claim_filter = "ALL"



    with col2:

        if st.button(
            f"🟢 Approved\n{len(approved_claims)}",
            use_container_width=True
        ):

            st.session_state.claim_filter = "AUTO_APPROVED"



    with col3:

        if st.button(
            f"🟡 Review\n{len(review_claims)}",
            use_container_width=True
        ):

            st.session_state.claim_filter = "WAITING_FOR_REVIEW"



    with col4:

        if st.button(
            f"🔴 Rejected\n{len(rejected_claims)}",
            use_container_width=True
        ):

            st.session_state.claim_filter = "REJECTED"



    st.divider()



    # -------------------------
    # Apply Filter
    # -------------------------

    selected = st.session_state.claim_filter


    if selected != "ALL":

        claims = [
            c for c in claims
            if c.get("status") == selected
        ]



    st.subheader(
        f"Claims : {len(claims)}"
    )



    # -------------------------
    # Accordion Claims List
    # -------------------------

    for claim in claims:


        entities = claim.get(
            "entities",
            {}
        )


        status = claim.get(
            "status",
            ""
        )


        accordion_title = (

            f"{status_badge(status)}  | "

            f"{entities.get('policy_number','')} | "

            f"₹{entities.get('claim_requested_amount',0):,}"

        )


        with st.expander(
            accordion_title,
            expanded=False
        ):


            st.markdown(
                f"""
**Claim ID**

`{claim.get("claim_id")}`


**Status**

{status_badge(status)}

"""
            )


            # Financial cards

            a,b,c,d = st.columns(4)


            a.metric(
                "Requested",
                f"₹{entities.get('claim_requested_amount',0):,}"
            )


            b.metric(
                "Hospital Bill",
                f"₹{entities.get('total_hospital_bill',0):,}"
            )


            c.metric(
                "Coverage",
                f"₹{entities.get('annual_coverage_limit',0):,}"
            )


            d.metric(
                "Remaining",
                f"₹{entities.get('remaining_coverage',0):,}"
            )



            tab1, tab2, tab3 = st.tabs(
                [
                    "👤 Claim Details",
                    "🔍 Validation",
                    "📜 Letter"
                ]
            )



            with tab1:

                st.table(
                    {

                    "Field":[

                        "Insured Name",
                        "Patient",
                        "Policy Number",
                        "Hospital",
                        "Diagnosis",
                        "Invoice"

                    ],

                    "Value":[

                        entities.get("insured_name"),
                        entities.get("patient_name"),
                        entities.get("policy_number"),
                        entities.get("hospital_name"),
                        entities.get("diagnosis"),
                        entities.get("invoice_number")

                    ]

                    }
                )



            with tab2:

                validations = claim.get(
                    "validation_results",
                    {}
                )


                for name,result in validations.items():

                    if result.get("status") == "PASS":

                        st.success(
                            f"✅ {name.upper()} PASS"
                        )

                    else:

                        st.error(
                            f"❌ {name.upper()} FAIL"
                        )



            with tab3:

                letter = claim.get(
                    "final_letter",
                    ""
                )


                if letter:

                    st.text_area(
                        "Letter Preview",
                        letter,
                        height=450,
                        key=f"letter_{claim['claim_id']}"
                    )

                else:

                    st.info(
                        "No letter available"
                    )