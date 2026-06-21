from agents.research_agent import (
    extract_topics,
    run_research_agent,
)


def test_extract_topics():
    topics = extract_topics(
        "The Earth is round"
    )

    assert "Earth" in topics


def test_research_agent_returns_evidence():
    evidence = run_research_agent(
        "The Earth is round"
    )

    assert len(evidence.sources) > 0
