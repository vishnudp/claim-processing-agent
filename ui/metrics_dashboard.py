import streamlit as st
import os
import json


CLAIMS_DIR = "storage/claims"


def render_metrics():

    st.title(
        "📊 Claims Operations Dashboard"
    )

    st.caption(
        "Real-time overview of healthcare claim processing activity"
    )


    total_claims = 0
    auto_approved = 0
    waiting_review = 0
    approved = 0
    rejected = 0


    if os.path.exists(CLAIMS_DIR):

        for file in os.listdir(CLAIMS_DIR):

            if not file.endswith(".json"):
                continue


            path = os.path.join(
                CLAIMS_DIR,
                file
            )


            try:

                with open(path) as f:

                    claim = json.load(f)


            except Exception:

                continue


            total_claims += 1


            status = claim.get(
                "status",
                ""
            )


            if status == "AUTO_APPROVED":

                auto_approved += 1


            elif status == "WAITING_FOR_REVIEW":

                waiting_review += 1


            elif status == "APPROVED":

                approved += 1


            elif status == "REJECTED":

                rejected += 1



    #
    # KPI CARDS
    #

    st.markdown(
        "## 📌 Claim Summary"
    )


    col1, col2, col3, col4 = st.columns(
        4
    )


    with col1:

        st.metric(
            label="📄 Total Claims",
            value=total_claims
        )


    with col2:

        st.metric(
            label="🤖 Auto Approved",
            value=auto_approved
        )


    with col3:

        st.metric(
            label="👨‍⚕️ Pending Review",
            value=waiting_review
        )


    with col4:

        st.metric(
            label="❌ Rejected",
            value=rejected
        )



    st.divider()



    #
    # PROCESSING PIPELINE
    #

    st.markdown(
        "## 🔄 Claim Processing Pipeline"
    )


    pipeline = {

        "Received":
            total_claims,

        "AI Approved":
            auto_approved,

        "Human Review":
            waiting_review,

        "Final Approved":
            approved,

        "Rejected":
            rejected
    }


    for stage, count in pipeline.items():


        percentage = (

            round(
                (count / total_claims) * 100,
                1
            )

            if total_claims > 0

            else 0
        )


        st.write(
            f"**{stage}**"
        )


        st.progress(
            min(
                percentage / 100,
                1.0
            )
        )


        st.caption(
            f"{count} claims ({percentage}%)"
        )



    st.divider()



    #
    # STATUS DISTRIBUTION
    #

    st.markdown(
        "## 📈 Current Status Distribution"
    )


    chart_data = {

        "Status": [

            "Auto Approved",
            "Waiting Review",
            "Approved",
            "Rejected"
        ],

        "Count": [

            auto_approved,
            waiting_review,
            approved,
            rejected
        ]
    }


    st.bar_chart(
        chart_data,
        x="Status",
        y="Count"
    )