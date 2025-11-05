from typing import Optional, List
from pydantic import BaseModel, Field


class StandardResponse(BaseModel):
    model_name: str
    model_id: str
    client: str
    response: str
    success: bool
    pixel: List[str]
    confirmation_response: Optional[str] = None


class StandardConfirmation(BaseModel):
    confirmation_response: str = Field(
        ..., description="Explanation of the confirmation"
    )
    confirmed: bool
