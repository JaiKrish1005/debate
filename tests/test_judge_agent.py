from agents.judge_agent import run_judge_agent
from schemas.evidence import Evidence, EvidenceSource
from schemas.verdict import Verdict


def test_judge_agent_returns_verdict():
    claim = "The Earth is flat"

    evidence = Evidence(
        sources=[
            EvidenceSource(
                title="Earth",
                summary=(
                    "Earth is an oblate spheroid. Observations from space "
                    "and measurements of Earth's curvature support this."
                ),
            )
        ]
    )

    defender_argument = (
        "Some people argue the Earth appears flat when viewed from the ground."
    )

    skeptic_argument = (
        "The evidence states that Earth is an oblate spheroid and "
        "measurements confirm its curvature."
    )

    result = run_judge_agent(
        claim=claim,
        evidence=evidence,
        defender_argument=defender_argument,
        skeptic_argument=skeptic_argument,
    )

    assert isinstance(result, Verdict)

    assert result.verdict in {
        "SUPPORTED",
        "REFUTED",
        "INCONCLUSIVE",
    }

    assert isinstance(result.confidence, int)

    assert result.reasoning.strip() != ""
