from typing import Optional
from datetime import date

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class ClaimEntity(BaseModel):

    claim_id: Optional[str] = None

    insurer_name: Optional[str] = None

    insured_name: str = Field(
        ...,
        description="Policy holder name"
    )

    patient_name: str = Field(
        ...,
        description="Patient name"
    )

    policy_number: str = Field(
        ...,
        description="Insurance policy number"
    )

    employee_number: Optional[str] = None

    email: Optional[EmailStr] = None

    claim_type: Optional[str] = None

    hospital_name: Optional[str] = None

    admission_date: Optional[date] = None

    discharge_date: Optional[date] = None

    hospital_bill: float = 0

    pre_hospitalization_bill: float = 0

    post_hospitalization_bill: float = 0

    pharmacy_bill: float = 0

    total_claim_amount: float = 0

    currency: str = "INR"

    invoice_number: Optional[str] = None

class ValidationResult(BaseModel):

    rule_name: str

    status: str

    message: str

    severity: str = "INFO"

class ExceptionSummary(BaseModel):

    claim_id: str

    reason: str

    risk_level: str

    recommendation: str

    summary: str

class HumanReview(BaseModel):

    reviewer_name: str

    decision: str

    comments: Optional[str] = None

    reviewed_at: Optional[str] = None

class FinalDecision(BaseModel):

    claim_id: str

    status: str

    approved_amount: Optional[float] = None

    rejection_reason: Optional[str] = None

    generated_letter_path: Optional[str] = None

class ClaimRecord(BaseModel):

    claim_id: str

    status: str

    entities: ClaimEntity

    validations: list[ValidationResult]

    hitl_required: bool

    exception_summary: Optional[
        ExceptionSummary
    ] = None

    review: Optional[
        HumanReview
    ] = None

    final_decision: Optional[
        FinalDecision
    ] = None