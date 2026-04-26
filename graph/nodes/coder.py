from typing import Any, Dict

from graph.chains.coder_chain import coder_chain
from graph.state import GraphState


def coder(state: GraphState) -> Dict[str, Any]:
    print("---CODER---")
    architect_task = state["architect_task"]

    coder_output = coder_chain.invoke({"architect_task": architect_task})

    return {"coder_output": coder_output}
