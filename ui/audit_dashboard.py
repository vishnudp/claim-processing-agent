import streamlit as st
import os
import json


AUDIT_DIR = "storage/audits"


def render_audit_dashboard():

    st.title("Audit Dashboard")

    if not os.path.exists(AUDIT_DIR):

        st.warning(
            "No audit logs available."
        )

        return

    audit_files = [

        f for f in os.listdir(AUDIT_DIR)

        if f.endswith(".json")
    ]

    if not audit_files:

        st.info(
            "No audit records found."
        )

        return

    selected = st.selectbox(

        "Select Claim Audit",

        audit_files
    )

    audit_path = os.path.join(
        AUDIT_DIR,
        selected
    )

    with open(audit_path) as f:

        logs = json.load(f)

    st.subheader(
        f"Audit Timeline - {selected}"
    )

    st.json(logs)