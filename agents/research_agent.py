from schemas.evidence import Evidence, EvidenceSource
from services.wikipedia_service import search_claim


def run_research_agent(claim: str) -> Evidence:
    results = search_claim(claim)

    sources = [
        EvidenceSource(
            title=item["title"],
            summary=item["summary"]
        )
        for item in results
    ]

    return Evidence(sources=sources)