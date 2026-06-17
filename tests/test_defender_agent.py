from agents.research_agent import run_research_agent
from agents.defender_agent import run_defender_agent


def test_defender_agent():
    claim = "Coffee causes dehydration"

    evidence = run_research_agent(claim)

    argument = run_defender_agent(
        claim,
        evidence
    )

    assert isinstance(argument, str)
    assert len(argument.strip()) > 0
