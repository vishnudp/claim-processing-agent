from pydantic import BaseModel


class UploadResponse(BaseModel):

    claim_id: str

    status: str


class ReviewRequest(BaseModel):

    claim_id: str

    reviewer_name: str

    decision: str

    comments: str


class ClaimStatusResponse(BaseModel):

    claim_id: str

    status: str

    progress: int