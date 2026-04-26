from typing import Any, Dict

from chains import architect_chain

from graph.state import GraphState


def architect(state: GraphState) -> Dict[str, Any]:
    print("---ARCHITECT---")
    query = state["query"]
    tester_bug_report = state["tester_bug_report"]

    architect_task = architect_chain.invoke(
        {"query": query, "tester_bug_report": tester_bug_report}
    )

    return {"architect_task": architect_task}
