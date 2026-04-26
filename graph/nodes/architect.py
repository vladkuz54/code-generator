from typing import Any, Dict

from graph.chains.architect_chain import architect_chain
from graph.state import GraphState


def architect(state: GraphState) -> Dict[str, Any]:
    print("---ARCHITECT---")
    query = state["query"]
    tester_bug_report = state.get("tester_bug_report", None)

    architect_task = architect_chain.invoke(
        {"query": query, "tester_bug_report": tester_bug_report}
    )

    return {"architect_task": architect_task}
