from agents.skeptic_agent import run_skeptic_agent
from schemas.evidence import Evidence, EvidenceSource


def test_skeptic_agent_generates_argument():
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

    result = run_skeptic_agent(
        claim=claim,
        evidence=evidence,
    )

    assert isinstance(result, str)
    assert result.strip() != ""
    assert len(result) > 20
