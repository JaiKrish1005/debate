from pydantic import BaseModel


class DebateRequest(BaseModel):
    claim: str
