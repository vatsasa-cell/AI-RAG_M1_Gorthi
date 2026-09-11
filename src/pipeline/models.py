from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1)


class Answer(BaseModel):
    content: str
    cost_usd: float
    retries: int
    confidence: float
    sources: list[str]
    schema_version: str = "v1"
