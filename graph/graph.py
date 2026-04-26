from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from graph.chains.code_grader_chain import code_grader_chain
from graph.consts import ARCHITECT, CODER, TESTER
from graph.nodes import architect, coder, tester
from graph.state import GraphState

load_dotenv()


def decide_to_transform(state: GraphState) -> str:
    print("---TESTING---")
    query = state["query"]
    coder_output = state["coder_output"]

    grader_output = code_grader_chain.invoke(
        {"query": query, "coder_output": coder_output}
    )

    if not grader_output.tester_grade:
        return TESTER
    else:
        return END


workflow = StateGraph(GraphState)

workflow.add_node(ARCHITECT, architect)
workflow.add_node(CODER, coder)
workflow.add_node(TESTER, tester)

workflow.set_entry_point(ARCHITECT)
workflow.add_edge(ARCHITECT, CODER)
# workflow.add_edge(CODER, TESTER)

workflow.add_conditional_edges(
    CODER, decide_to_transform, path_map={TESTER: TESTER, END: END}
)

workflow.add_edge(TESTER, ARCHITECT)


app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
