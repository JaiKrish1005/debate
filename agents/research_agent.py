import re

from schemas.evidence import Evidence, EvidenceSource
from services.wikipedia_service import get_summary


def extract_topics(claim: str) -> list[str]:
    claim = re.sub(r"[^\w\s]", "", claim)

    words = claim.split()

    return [
        word
        for word in words
        if len(word) > 3
    ]


def run_research_agent(claim: str) -> Evidence:
    topics = extract_topics(claim)

    sources = []

    for topic in topics:
        result = get_summary(topic)

        if result:
            sources.append(
                EvidenceSource(
                    title=result["title"],
                    summary=result["summary"]
                )
            )

    return Evidence(sources=sources)
