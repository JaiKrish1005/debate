from agents.skeptic_agent import SkepticAgent
from schemas.evidence import Evidence, EvidenceSource


def test_skeptic_agent_generates_argument():
    agent = SkepticAgent()

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

    result = agent.run(
        claim=claim,
        evidence=evidence,
    )

    assert isinstance(result, str)
    assert result.strip() != ""
    assert len(result) > 20
