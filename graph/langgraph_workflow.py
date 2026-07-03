from langgraph.graph import START, END, StateGraph

from agents.research_agent import run_research_agent
from agents.defender_agent import run_defender_agent
from agents.skeptic_agent import run_skeptic_agent
from agents.judge_agent import run_judge_agent

from graph.state import DebateState


def research_node(state: DebateState) -> DebateState:
    """Run the Research Agent and update the state with retrieved evidence."""

    evidence = run_research_agent(state["claim"])

    return {
        **state,
        "evidence": evidence,
    }


def defender_node(state: DebateState) -> DebateState:
    """Run the Defender Agent and update the state with its argument."""

    defender_argument = run_defender_agent(
        claim=state["claim"],
        evidence=state["evidence"],
    )

    return {
        **state,
        "defender_argument": defender_argument,
    }


def skeptic_node(state: DebateState) -> DebateState:
    """Run the Skeptic Agent and update the state with its argument."""

    skeptic_argument = run_skeptic_agent(
        claim=state["claim"],
        evidence=state["evidence"],
    )

    return {
        **state,
        "skeptic_argument": skeptic_argument,
    }


def judge_node(state: DebateState) -> DebateState:
    """Run the Judge Agent and update the state with the final verdict."""

    verdict = run_judge_agent(
        claim=state["claim"],
        evidence=state["evidence"],
        defender_argument=state["defender_argument"],
        skeptic_argument=state["skeptic_argument"],
    )

    return {
        **state,
        "verdict": verdict,
    }


# ---------------------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------------------

builder = StateGraph(DebateState)

builder.add_node("research", research_node)
builder.add_node("defender", defender_node)
builder.add_node("skeptic", skeptic_node)
builder.add_node("judge", judge_node)

builder.add_edge(START, "research")
builder.add_edge("research", "defender")
builder.add_edge("defender", "skeptic")
builder.add_edge("skeptic", "judge")
builder.add_edge("judge", END)

debate_graph = builder.compile()


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def run_debate_graph(claim: str) -> DebateState:
    """
    Execute the complete debate workflow using LangGraph.

    Args:
        claim: User claim to verify.

    Returns:
        DebateState containing evidence, arguments, and verdict.
    """

    initial_state: DebateState = {
        "claim": claim,
        "evidence": None,
        "defender_argument": "",
        "skeptic_argument": "",
        "verdict": None,
    }

    return debate_graph.invoke(initial_state)