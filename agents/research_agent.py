from schemas.evidence import Evidence, EvidenceSource
from services.wikipedia_service import get_summary


TOPICS = [
    "Coffee",
    "Caffeine",
    "Dehydration",
    "Hydration",
]


def run_research_agent(claim: str) -> Evidence:
    sources = []

    for topic in TOPICS:
        result = get_summary(topic)

        if result:
            sources.append(
                EvidenceSource(
                    title=result["title"],
                    summary=result["summary"]
                )
            )

    return Evidence(sources=sources)