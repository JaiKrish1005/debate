import json

from agents.base_agent import format_evidence
from schemas.evidence import Evidence
from schemas.verdict import Verdict
from services.llm import get_llm


def run_judge_agent(
    claim: str,
    evidence: Evidence,
    defender_argument: str,
    skeptic_argument: str,
) -> Verdict:
    llm = get_llm()

    evidence_text = format_evidence(evidence)

    prompt = f"""
You are an impartial fact-checking judge.

Claim:
{claim}

Evidence:
{evidence_text}

Defender Argument:
{defender_argument}

Skeptic Argument:
{skeptic_argument}

Instructions:
- Use only the provided evidence.
- Compare the defender and skeptic arguments.
- Decide whether the claim is:
  - SUPPORTED
  - REFUTED
  - INCONCLUSIVE
- Assign a confidence score from 0 to 100.
- Provide concise reasoning.

Return ONLY valid JSON in this exact format:

{{
  "verdict": "SUPPORTED",
  "confidence": 85,
  "reasoning": "Brief explanation."
}}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    if content.startswith("```"):
        lines = content.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        content = "\n".join(lines)

    data = json.loads(content)

    return Verdict(**data)
