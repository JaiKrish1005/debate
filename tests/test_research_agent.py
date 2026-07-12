from unittest.mock import patch

from agents.research_agent import run_research_agent


@patch("agents.research_agent.retrieve_context")
def test_run_research_agent(mock_retrieve):
    mock_retrieve.return_value = [
        {
            "document": "Vitamin C may slightly reduce the duration of the common cold.",
            "metadata": {
                "topic": "Vitamin C",
                "chunk": 0,
                "source": "Wikipedia",
            },
        },
        {
            "document": "Evidence does not support vitamin C preventing the common cold.",
            "metadata": {
                "topic": "Common cold",
                "chunk": 1,
                "source": "Wikipedia",
            },
        },
    ]

    evidence = run_research_agent("Vitamin C prevents colds")

    assert len(evidence.sources) == 2

    assert evidence.sources[0].title == "Vitamin C"
    assert (
        evidence.sources[0].summary
        == "Vitamin C may slightly reduce the duration of the common cold."
    )

    assert evidence.sources[1].title == "Common cold"
    assert (
        evidence.sources[1].summary
        == "Evidence does not support vitamin C preventing the common cold."
    )


@patch("agents.research_agent.retrieve_context")
def test_run_research_agent_no_results(mock_retrieve):
    mock_retrieve.return_value = []

    evidence = run_research_agent("Unknown claim")

    assert evidence.sources == []