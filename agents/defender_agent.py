from services.llm import get_llm
from schemas.evidence import Evidence
import time


def run_defender_agent(
    claim: str,
    evidence: Evidence
) -> str:

    llm = get_llm()

    evidence_text = "\n\n".join(
        [
            f"Title: {source.title}\nSummary: {source.summary[:500]}"
            for source in evidence.sources
        ]
    )

    prompt = f"""
Claim: {claim}

Evidence:
{evidence_text}

Using ONLY the evidence above:

- Support the claim.
- Do not invent facts.
- Maximum 120 words.
"""

    start = time.time()

    response = llm.invoke(prompt)

    elapsed = time.time() - start

    print(f"Defender Agent: {elapsed:.2f}s")

    return response.content
