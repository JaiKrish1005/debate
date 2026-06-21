from schemas.evidence import Evidence


def format_evidence(
    evidence: Evidence,
    max_chars: int = 500
) -> str:

    return "\n\n".join(
        [
            f"Title: {source.title}\nSummary: {source.summary[:max_chars]}"
            for source in evidence.sources
        ]
    )
