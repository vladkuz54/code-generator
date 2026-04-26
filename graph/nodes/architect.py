from typing import Any, Dict

from chains import architect_chain

from graph.state import GraphState


def architect(state: GraphState) -> Dict[str, Any]:
    print("---ARCHITECT---")
    query = state["query"]

    architect_task = architect_chain.invoke({"query": query})

    return {"architect_task": architect_task}
