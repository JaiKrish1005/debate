from pydantic import BaseModel
from typing import List


class EvidenceSource(BaseModel):
    title: str
    summary: str


class Evidence(BaseModel):
    sources: List[EvidenceSource]