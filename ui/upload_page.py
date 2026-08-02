import streamlit as st
import uuid
import traceback

from services.file_service import save_file

from workflow.graph import preprocessing_agent

from agents.extraction_agent import (
    extraction_agent
)

from agents.validation_agent import (
    validation_agent
)

from agents.exception_agent import (
    exception_agent
)

from agents.letter_agent import (
    letter_agent
)

from services.claim_storage_service import (
    save_claim
)

from services.audit_service import (
    save_audit_log
)

import threading

import time

st.set_page_config(
        page_title="Autonomous Claim Processing Agent",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

workflow_start = time.time()


def render_step_status(
        placeholder,
        steps,
        overall_progress=0,
        elapsed=None
):

    markdown = f"""
## Workflow Progress

### Overall Progress: {overall_progress}%

"""

    for step, data in steps.items():

        markdown += (
            f"**{step}** : "
            f"{data['status']} "
            f"({data['progress']}%)\n\n"
        )

    if elapsed:

        markdown += f"\n⏱ Elapsed Time: {elapsed:.1f}s"

    placeholder.markdown(markdown)

def render_upload():

    st.title(
        "🏥 Autonomous Claim Processing Agent"
    )

    

    uploaded_file = st.file_uploader(
        "Upload Claim PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        if st.button(
            "Process Claim"
        ):

            try:

                progress_bar = st.progress(
                    0
                )

                col1, col2 = st.columns([2, 1])

                with col1:
                    workflow_placeholder = st.empty()

                with col2:
                    st.markdown("### Execution Log")
                    log_placeholder = st.empty()

                execution_logs = []

                

                def add_log(
                        message,
                        state=None,
                        stage="",
                        status=""
                ):

                    log = (
                        f"{time.strftime('%H:%M:%S')} - "
                        f"{message}"
                    )

                    execution_logs.append(log)

                    claim_id = ""
                    policy_number = ""
                    insured_name = ""

                    if state:

                        claim_id = state.get(
                            "claim_id",
                            ""
                        )

                        entities = state.get(
                            "entities",
                            {}
                        )

                        policy_number = entities.get(
                            "policy_number",
                            ""
                        )

                        insured_name = entities.get(
                            "insured_name",
                            ""
                        )

                    save_audit_log(
                        message=message,
                        claim_id=claim_id,
                        policy_number=policy_number,
                        insured_name=insured_name,
                        stage=stage,
                        status=status
                    )

                    log_placeholder.code(
                        "\n".join(
                            execution_logs
                        )
                    )
                
                add_log(
                    "Workflow Started"
                )

                path = save_file(
                    uploaded_file
                )

                state = {

                    "claim_id":
                        str(uuid.uuid4()),

                    "pdf_path":
                        path,

                    "raw_text": "",

                    "metadata": {},

                    "entities": {},

                    "validation_results": {},

                    "hitl_required": False,

                    "exception_summary": "",

                    "human_decision": "",

                    "final_letter": "",

                    "status":
                        "PROCESSING",

                    "progress": 0
                }

                steps = {

                    "Upload": {
                        "status": "✅ Complete",
                        "progress": 100
                    },

                    "OCR": {
                        "status": "⏳ Pending",
                        "progress": 0
                    },

                    "Metadata": {
                        "status": "⏳ Pending",
                        "progress": 0
                    },

                    "Entity Extraction": {
                        "status": "⏳ Pending",
                        "progress": 0
                    },

                    "Validation": {
                        "status": "⏳ Pending",
                        "progress": 0
                    },

                    "Decision Routing": {
                        "status": "⏳ Pending",
                        "progress": 0
                    },

                    "Letter Generation": {
                        "status": "⏳ Pending",
                        "progress": 0
                    }
                }

                render_step_status(
                    workflow_placeholder,
                    steps
                )

                # STEP 1 - OCR + Metadata

                steps["OCR"] = {
                    "status": "🔄 Running",
                    "progress": 50
                }

                steps["Metadata"] = {
                    "status": "🔄 Running",
                    "progress": 50
                }

                render_step_status(
                    workflow_placeholder,
                    steps,
                    overall_progress=15,
                    elapsed=time.time() - workflow_start
                )

                progress_bar.progress(20)

                add_log("OCR Started")
                add_log("Metadata Extraction Started")

                state = preprocessing_agent(state)

                add_log("OCR Completed")
                add_log("Metadata Extraction Completed")

                steps["OCR"] = {
                    "status": "✅ Complete",
                    "progress": 100
                }

                steps["Metadata"] = {
                    "status": "✅ Complete",
                    "progress": 100
                }

                render_step_status(
                    workflow_placeholder,
                    steps,
                    overall_progress=30,
                    elapsed=time.time() - workflow_start
                )
                # STEP 2 - Entity Extraction

                steps["Entity Extraction"] = {
                    "status": "🔄 Chunking + Parallel Extraction",
                    "progress": 50
                }

                render_step_status(
                    workflow_placeholder,
                    steps,
                    overall_progress=40,
                    elapsed=time.time() - workflow_start
                )

                add_log(
                    "Document Chunking Started"
                )

                add_log(
                    "Parallel Extraction Started"
                )

                steps["Entity Extraction"] = {
                    "status": "🔄 Chunking",
                    "progress": 10
                }

                
                for p in range(
                        50,
                        90,
                        2
                ):

                    steps[
                        "Entity Extraction"
                    ] = {

                        "status":
                            "🔄 Parallel Extraction",

                        "progress":
                            p
                    }

                    render_step_status(
                        workflow_placeholder,
                        steps,
                        overall_progress=40
                    )

                    time.sleep(0.1)

                def update_entity_progress(
                            progress,
                            completed,
                            total
                    ):

                    steps["Entity Extraction"] = {
                        "status":
                            f"🔄 Chunk {completed}/{total}",
                        "progress":
                            progress
                    }

                    overall = 40 + int(
                        progress * 0.20
                    )

                    render_step_status(
                        workflow_placeholder,
                        steps,
                        overall_progress=overall,
                        elapsed=time.time() - workflow_start
                    )

                state = extraction_agent(
                    state,
                    progress_callback=
                        update_entity_progress
                )

                steps[
                    "Entity Extraction"
                ] = {

                    "status":
                        "🔄 Merging Results",

                    "progress":
                        95
                }

                render_step_status(
                    workflow_placeholder,
                    steps,
                    overall_progress=55
                )

                time.sleep(1)

                steps["Entity Extraction"] = {
                    "status": "✅ Entity Merge Complete",
                    "progress": 100
                }

                add_log(
                    "Entity Merge Completed"
                )

                render_step_status(
                    workflow_placeholder,
                    steps,
                    overall_progress=60,
                    elapsed=time.time() - workflow_start
                )

                # STEP 3 - Validation

                steps["Validation"] = {
                    "status": "🔄 Running Business Rules",
                    "progress": 50
                }

                render_step_status(
                    workflow_placeholder,
                    steps,
                    overall_progress=65,
                    elapsed=time.time() - workflow_start
                )

                progress_bar.progress(60)

                add_log("Validation Started")

                state = validation_agent(state)

                

                steps["Validation"] = {
                    "status": "✅ Complete",
                    "progress": 100
                }

                add_log("Validation Completed")

                render_step_status(
                    workflow_placeholder,
                    steps,
                    overall_progress=80,
                    elapsed=time.time() - workflow_start
                )

                # STEP 4 - Decision Routing

                steps["Decision Routing"] = {
                    "status": "🔄 Evaluating Claim",
                    "progress": 50
                }

                render_step_status(
                    workflow_placeholder,
                    steps,
                    overall_progress=85,
                    elapsed=time.time() - workflow_start
                )

                progress_bar.progress(80)

                add_log("Decision Routing Started")

                claim_amount = (
                    state["entities"]
                    .get("claim_requested_amount", 0)
                )

                annual_coverage_limit = (
                    state["entities"].get(
                        "annual_coverage_limit",
                        0
                    )
                    or 0
                )

                if claim_amount > annual_coverage_limit:

                    add_log(
                        f"HITL Triggered - Claim Amount: ${claim_amount}"
                    )

                    state["hitl_required"] = True

                    state = exception_agent(state)

                    state = letter_agent(state)

                    add_log(
                            "Exception Summary Generated"
                    )

                    state["status"] = \
                        "WAITING_FOR_REVIEW"

                    steps["Decision Routing"] = {
                        "status": "⚠ HITL Triggered",
                        "progress": 100
                    }

                else:

                    state = letter_agent(state)

                    add_log(
                        f"Auto Approved - Claim Amount: ${claim_amount}"
                    )

                    state["status"] = \
                        "AUTO_APPROVED"

                    add_log(
                        "Approval Letter Generated"
                    )

                    steps["Decision Routing"] = {
                        "status": "✅ Auto Approved",
                        "progress": 100
                    }

                render_step_status(
                    workflow_placeholder,
                    steps,
                    overall_progress=95,
                    elapsed=time.time() - workflow_start
                )

               # STEP 5 - Letter Generation

                steps["Letter Generation"] = {
                    "status": "✅ Complete",
                    "progress": 100
                }

                

                render_step_status(
                    workflow_placeholder,
                    steps,
                    overall_progress=100,
                    elapsed=time.time() - workflow_start
                )

                progress_bar.progress(100)
                #
                # RESULTS
                #
                add_log(
                    "Workflow Completed Successfully"
                )

                save_claim(
                    state
                )


                def render_claim_summary(state):

                    metadata = state.get(
                        "metadata",
                        {}
                    )

                    entities = state.get(
                        "entities",
                        {}
                    )


                    st.header(
                        "🏥 Claim Processing Summary"
                    )


                    # Metadata

                    st.subheader(
                        "📄 Document Information"
                    )

                    st.table(
                        {
                            "Field": [
                                "File Name",
                                "Document Type",
                                "Pages",
                                "File Size",
                                "Uploaded"
                            ],

                            "Value":[

                                metadata.get(
                                    "file_name"
                                ),

                                metadata.get(
                                    "document_type"
                                ),

                                metadata.get(
                                    "page_count"
                                ),

                                f"{metadata.get('file_size_mb')} MB",

                                metadata.get(
                                    "upload_time"
                                )
                            ]
                        }
                    )


                    # Claim details

                    st.subheader(
                        "👤 Claim Information"
                    )

                    st.table(
                        {
                            "Field":[
                                "Insured Name",
                                "Patient Name",
                                "Policy Number",
                                "Hospital",
                                "Diagnosis"
                            ],

                            "Value":[

                                entities.get(
                                    "insured_name"
                                ),

                                entities.get(
                                    "patient_name"
                                ),

                                entities.get(
                                    "policy_number"
                                ),

                                entities.get(
                                    "hospital_name"
                                ),

                                entities.get(
                                    "diagnosis"
                                )
                            ]
                        }
                    )


                    # Financial

                    st.subheader(
                        "💰 Financial Assessment"
                    )


                    col1,col2,col3,col4 = st.columns(4)


                    col1.metric(
                        "Requested",
                        f"₹{entities.get('claim_requested_amount',0):,}"
                    )


                    col2.metric(
                        "Hospital Bill",
                        f"₹{entities.get('total_hospital_bill',0):,}"
                    )


                    col3.metric(
                        "Coverage Limit",
                        f"₹{entities.get('annual_coverage_limit',0):,}"
                    )


                    col4.metric(
                        "Remaining",
                        f"₹{entities.get('remaining_coverage',0):,}"
                    )

                    st.subheader(
                        "📜 Approval Letter Preview"
                    )


                    if state.get("hitl_required"):

                        st.warning(
                            "⚠ Human Review Required - Claim is waiting for reviewer action"
                        )

                    else:

                        st.success(
                            "✅ Claim Automatically Approved"
                        )

                    letter = state.get(
                        "final_letter",
                        ""
                    )

                    st.text_area(
                        "Generated Letter Preview",
                        letter,
                        height=600
                    )
                render_claim_summary(state)

            except Exception as e:

                st.error(
                    f"Workflow Failed: {str(e)}"
                )

                st.code(
                    traceback.format_exc()
                )