from graph.langgraph_workflow import run_debate_graph


def test_langgraph_workflow():
    result = run_debate_graph("The Earth is round")

    assert "claim" in result
    assert "evidence" in result
    assert "defender_argument" in result
    assert "skeptic_argument" in result
    assert "verdict" in result