from agents.research_agent import run_research_agent


def test_research_agent_returns_evidence():
    evidence = run_research_agent(
        "Coffee causes dehydration"
    )

    assert evidence is not None
    assert len(evidence.sources) > 0