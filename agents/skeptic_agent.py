from agents.base_agent import format_evidence
from services.llm import get_llm
from schemas.evidence import Evidence


def run_skeptic_agent(
    claim: str,
    evidence: Evidence,
) -> str:
    llm = get_llm()

    evidence_text = format_evidence(evidence)

    prompt = f"""
You are a skeptical fact-checking agent.

Claim:
{claim}

Evidence:
{evidence_text}

Task:
- Argue against the claim.
- Use only the provided evidence.
- Do not invent facts.
- If the evidence is insufficient to refute the claim, explain the limitations of the evidence.
- Maximum 120 words.
"""

    response = llm.invoke(prompt)

    return response.content.strip()
