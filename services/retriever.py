from services.chroma import retrieve


def retrieve_context(claim: str) -> list[dict]:
    """
    Retrieve relevant context for a claim.
    """
    return retrieve(claim)