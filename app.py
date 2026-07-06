from fastapi import FastAPI

from graph.langgraph_workflow import run_debate_graph
from schemas.request import DebateRequest

app = FastAPI(
    title="debAIte API",
    version="0.1.0",
)


@app.post("/debate")
def debate(request: DebateRequest):
    return run_debate_graph(request.claim)
