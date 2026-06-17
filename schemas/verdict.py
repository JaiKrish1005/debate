from pydantic import BaseModel


class Verdict(BaseModel):
    verdict: str
    confidence: int
    reasoning: str