import streamlit as st

from ui.upload_page import (
    render_upload
)

from ui.review_dashboard import (
    render_review_dashboard
)

from ui.metrics_dashboard import (
    render_metrics
)

from ui.audit_dashboard import (
    render_audit_dashboard
)

from ui.claims_dashboard import (
    render_claims_dashboard
)


st.set_page_config(
    page_title="Autonomous Claim Processing Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

page = st.sidebar.selectbox(

    "Navigation",

    [
        "Upload Claim",
        "Processed Claims",
        "Reviewer Queue",
        "Metrics",
        "Audit Logs"
    ]
)

if page == "Processed Claims":

    render_claims_dashboard()

if page == "Upload Claim":

    render_upload()

elif page == "Reviewer Queue":

    render_review_dashboard()

elif page == "Metrics":

    render_metrics()

elif page == "Audit Logs":

    render_audit_dashboard()