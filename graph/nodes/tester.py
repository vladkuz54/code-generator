from typing import Any, Dict

from chains import tester_chain

from graph.state import GraphState


def coder(state: GraphState) -> Dict[str, Any]:
    print("---TESTER---")
    query = state["query"]
    coder_output = state["coder_output"]

    tester_output = tester_chain.invoke({"query": query, "coder_output": coder_output})

    return {
        "tester_grade": tester_output.tester_grade,
        "tester_bug_report": tester_output.tester_bug_report,
    }
