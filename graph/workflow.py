from agents.research_agent import run_research_agent
from agents.defender_agent import run_defender_agent
from agents.skeptic_agent import run_skeptic_agent
from agents.judge_agent import run_judge_agent


def run_debate(claim: str):
    evidence = run_research_agent(claim)

    defender_argument = run_defender_agent(
        claim=claim,
        evidence=evidence,
    )

    skeptic_argument = run_skeptic_agent(
        claim=claim,
        evidence=evidence,
    )

    verdict = run_judge_agent(
        claim=claim,
        evidence=evidence,
        defender_argument=defender_argument,
        skeptic_argument=skeptic_argument,
    )

    return {
        "claim": claim,
        "evidence": evidence,
        "defender_argument": defender_argument,
        "skeptic_argument": skeptic_argument,
        "verdict": verdict,
    }
