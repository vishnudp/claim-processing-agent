Requirement:

Autonomous Enterprise Workflow Agent
The Scenario: A healthcare or insurance enterprise needs to review complex claim documents (PDFs/text). Each claim requires extracting key entities, running validation checks against business rules, and drafting a formal approval or rejection letter for a human caseworker to sign off on.

Objective: Build an agentic workflow that orchestrates document parsing, multi-step validation logic, and human-in-the-loop sign-off.

Deliverables:

A multi-step agent flow (built via LangChain, LlamaIndex, AutoGen, or custom Python orchestration) that ingests sample unstructured claim text, extracts key entities (Name, Claim Amount, Policy Number), and checks them against a business logic rule set.

A Human-in-the-Loop (HITL) trigger: If the claim exceeds a threshold (e.g., >$10,000) or contains conflicting data, the agent halts and drafts an exception review summary for a caseworker.

A short 3-minute video demo (Loom) presenting the system as if delivering a final solution to a client CTO.

What this tests: Complex agentic orchestration, error handling, state management, enterprise UX awareness, and executive-level client communication.


Solution: 


Create the Environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


# Autonomous Enterprise Claim Processing Agent

## Overview

This solution demonstrates an enterprise-grade autonomous workflow for healthcare and insurance claim processing using Agentic AI.

The system ingests unstructured claim PDFs, extracts entities using a local LLM (Ollama Qwen3), validates claims against business rules, routes high-risk claims for human review, and generates approval or rejection letters.

The solution is designed to showcase:

* Agentic orchestration
* Human-in-the-loop workflows
* Enterprise validation pipelines
* Parallel processing
* State management
* Auditability
* Executive-level reporting
* Caching

---

## Technology Stack

### Frontend

* Streamlit

### Orchestration

* LangGraph


### LLM

* Ollama
* Qwen3:4B

### PDF Processing

* PyMuPDF
* PDFPlumber

### Validation

* Custom Rule Engine

### Storage

* Local JSON Storage

---

### Caching

## Architecture Flow:

┌──────────────────────────────────────────────────────────────────────────┐
│                           Streamlit Enterprise Portal                   │
│                                                                          │
│ Upload Claim │ Reviewer Queue │ Metrics │ Audit Dashboard │ Claim History│
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
                                ▼

┌──────────────────────────────────────────────────────────────────────────┐
│                      LangGraph Workflow Orchestrator                     │
│                                                                          │
│  State Management                                                        │
│  Error Handling                                                          │
│  Progress Tracking                                                       │
│  Retry Logic                                                             │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
            ┌───────────────────┴───────────────────┐
            ▼                                       ▼

 ┌────────────────────┐                 ┌────────────────────┐
 │ OCR Agent          │                 │ Metadata Agent     │
 │                    │                 │                    │
 │ PDFPlumber         │                 │ File Details       │
 │ PyMuPDF            │                 │ Page Count         │
 │ OCR Fallback       │                 │ File Size          │
 └─────────┬──────────┘                 └─────────┬──────────┘
           └────────────────┬────────────────────┘
                            ▼

            ┌────────────────────────────────────┐
            │ Chunking Service                   │
            │                                    │
            │ Large PDF → Chunks                 │
            │ Parallel Processing                │
            └────────────────┬───────────────────┘
                             ▼

            ┌────────────────────────────────────┐
            │ Entity Extraction Agent            │
            │                                    │
            │ Ollama Qwen3                       │
            │ Parallel Chunk Extraction          │
            │ Entity Merge Service               │
            └────────────────┬───────────────────┘
                             ▼

            ┌────────────────────────────────────┐
            │ Validation Coordinator             │
            └────────────────┬───────────────────┘
                             ▼

     ┌────────────┬────────────┬────────────┬────────────┐
     ▼            ▼            ▼            ▼

Policy       Coverage     Invoice      Duplicate
Validator    Validator    Validator    Validator

     └────────────┴────────────┴────────────┘
                             ▼

            ┌────────────────────────────────────┐
            │ Decision Routing Agent             │
            └────────────────┬───────────────────┘
                             │

                High Risk / Exception ?
                             │
               ┌─────────────┴─────────────┐
               ▼                           ▼

      Auto Approval                Human Review Queue

               │                           │

               ▼                           ▼

      Approval Letter          Exception Summary
      Generation Agent         Generation Agent

               │                           │
               └─────────────┬─────────────┘
                             ▼

                 Final Claim Decision Store

                    storage/claims
                    storage/reviews
                    storage/audit_logs

                             ▼

                   Metrics & Audit Layer


                    ┌───────────────┐
                    │ DiskCache     │
                    └───────┬───────┘
                            │
                    Cache Hit?
                            │
                    Yes → Return
                    No  → Ollama


## Workflow

1. Upload Claim PDF
2. OCR Agent extracts document text
3. Metadata Agent extracts document metadata
4. Entity Extraction Agent extracts:

   * Insured Name
   * Patient Name
   * Policy Number
   * Claim Amount
   * Hospital Name
   * Diagnosis
5. Validation Agent executes:

   * Policy Validation
   * Coverage Validation
   * Invoice Validation
   * Duplicate Detection
6. Decision Routing
7. Auto Approval or Human Review
8. Letter Generation
9. Audit Logging

---

## Human-In-The-Loop Trigger

Human review is required when:

* Claim Amount > (as per mention in document for maximum annual claim amount)
* Validation conflicts detected
* Policy mismatch identified
* Duplicate claim suspected

---

### Caching

* Entity Extraction Cache
* Prompt Cache
* OCR Cache

## Features

### Parallel Processing

OCR and Metadata extraction execute concurrently.

### Chunked Entity Extraction

Large documents are split into chunks and processed in parallel.

### Audit Logs

Every workflow event is tracked and stored.

### Reviewer Queue

Caseworkers can review exceptions and approve or reject claims.

### Metrics Dashboard

Displays:

* Claims processed
* Auto-approved claims
* Human-reviewed claims
* Average processing time
* Automation savings

---

## Installation

```bash
pip install -r requirements.txt
```

Start Ollama:

```bash
ollama serve
```

Run model:

```bash
ollama run qwen3:4b
```

---

## Run Application

```bash
streamlit run app.py
```

Custom Port:

```bash
streamlit run app.py --server.port 8505
```

---

## Demo Scenario

### Auto Approval

(Sample Files are stored inside "sample files" folder under code repos)

Sample File : 'HEALTHCARE CLAIM SUBMISSION.pdf'
Matching Claim Amount with Approval Amount

Result:

* Validation Passed
* Auto Approved
* Approval Letter Generated

### Human Review

Sample File : 'HEALTHCARE CLAIM SUBMISSION_HUMAN_LOOP.pdf' 

Human Review Trigger:

1. Claim exceeds annual coverage limit
2. Validation conflict detected
3. Duplicate claim detected
4. Policy mismatch detected
5. Confidence score < 80%

Result:

* HITL Triggered
* Exception Summary Generated
* Reviewer Approval Required

---

## Business Value

* 80–90% reduction in manual effort
* Faster claim processing
* Full auditability
* Consistent rule enforcement
* Enterprise-ready architecture

---

## Future Enhancements

* PostgreSQL persistence
* LangChain
* LlamaIndex
* Vector Search
* RAG-based policy retrieval
* Multi-agent AutoGen architecture
* Email notifications
* SLA monitoring
* Role-based access control

---

## Author

Autonomous Enterprise Workflow Agent using LangGraph + Ollama + Streamlit.


