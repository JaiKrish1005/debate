from typing import Literal

from pydantic import BaseModel


class Verdict(BaseModel):
    verdict: Literal[
        "SUPPORTED",
        "REFUTED",
        "INCONCLUSIVE",
    ]
    confidence: int
    reasoning: str
