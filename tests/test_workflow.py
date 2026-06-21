from graph.workflow import run_debate


def test_workflow():
    result = run_debate(
        "The Earth is round"
    )

    assert "claim" in result
    assert "evidence" in result
    assert "defender_argument" in result
    assert "skeptic_argument" in result
    assert "verdict" in result
