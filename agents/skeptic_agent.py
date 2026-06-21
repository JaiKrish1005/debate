from agents.base_agent import format_evidence
from services.llm import get_llm
from schemas.evidence import Evidence


class SkepticAgent:
    def __init__(self):
        self.llm = get_llm()

    def run(
        self,
        claim: str,
        evidence: Evidence,
    ) -> str:
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

        response = self.llm.invoke(prompt)

        return response.content.strip()
