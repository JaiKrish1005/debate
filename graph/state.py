from typing import TypedDict

from schemas.evidence import Evidence
from schemas.verdict import Verdict


class DebateState(TypedDict):
    claim: str

    evidence: Evidence | None

    defender_argument: str

    skeptic_argument: str

    verdict: Verdict | None