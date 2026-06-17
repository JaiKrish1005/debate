import wikipedia


def search_claim(claim: str, limit: int = 3):
    """
    Search Wikipedia for topics related to a claim.
    """

    results = wikipedia.search(claim)

    pages = []

    for title in results[:limit]:
        try:
            summary = wikipedia.summary(title, sentences=4)

            pages.append(
                {
                    "title": title,
                    "summary": summary,
                }
            )

        except Exception:
            continue

    return pages