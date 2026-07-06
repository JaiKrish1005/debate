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

Evaluate whether the CLAIM is supported by the evidence.

Verdict meanings:

- SUPPORTED:
  The evidence supports the claim.

- REFUTED:
  The evidence contradicts or disproves the claim.

- INCONCLUSIVE:
  The evidence is insufficient to determine whether the claim is true or false.

Rules:

- Use only the provided evidence.
- Compare the defender and skeptic arguments.
- Focus on whether the evidence supports the claim.
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

    # Remove Markdown code fences if present
    if content.startswith("```"):
        lines = content.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        content = "\n".join(lines)

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Judge Agent returned invalid JSON:\n\n{content}") from e

    # Normalize verdict to handle minor LLM variations
    verdict = str(data.get("verdict", "")).upper().strip()

    if verdict.startswith("SUPPOR"):
        data["verdict"] = "SUPPORTED"
    elif verdict.startswith("REFUT"):
        data["verdict"] = "REFUTED"
    else:
        data["verdict"] = "INCONCLUSIVE"

    return Verdict(**data)
