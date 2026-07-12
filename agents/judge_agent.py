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

SUPPORTED
The evidence clearly confirms the claim.

REFUTED
The evidence clearly contradicts the claim.

INCONCLUSIVE
Use ONLY if the evidence genuinely does not allow a conclusion.
Do NOT use INCONCLUSIVE merely because the wording differs.
If the evidence logically contradicts the claim, return REFUTED.
If the evidence logically confirms the claim, return SUPPORTED.

Rules:

- Use only the provided evidence.
- Compare the defender and skeptic arguments.
- Judge the exact wording of the claim.
- Do not infer support from related facts.
- A claim is NOT SUPPORTED simply because a related statement is true.
- If the evidence says something different from the claim, return REFUTED if it contradicts the claim; otherwise return INCONCLUSIVE.
- Assign a confidence score from 0 to 100.
- Provide concise reasoning.


Example:

Claim:
"Vitamin C prevents colds."

Evidence:
"Vitamin C may reduce the duration of colds but does not prevent them."

Correct Verdict:
REFUTED

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
