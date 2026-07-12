from schemas.evidence import Evidence, EvidenceSource
from services.retriever import retrieve_context


def run_research_agent(claim: str) -> Evidence:
    """
    Retrieve relevant evidence for a claim using the
    ChromaDB-backed retriever.
    """
    results = retrieve_context(claim)

    if not results:
        return Evidence(sources=[])

    sources = []

    for result in results:
        metadata = result.get("metadata", {})

        sources.append(
            EvidenceSource(
                title=metadata.get("topic", "Wikipedia"),
                summary=result["document"],
            )
        )

    return Evidence(sources=sources)