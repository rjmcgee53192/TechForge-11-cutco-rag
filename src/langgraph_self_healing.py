from typing import TypedDict
from langgraph.graph import StateGraph, END
import subprocess
import re


class AgentState(TypedDict):
    script_path: str
    error: str
    retry_count: int
    success: bool


def execute_script(state: AgentState):
    """Executes the target python script and captures errors."""
    try:
        result = subprocess.run(
            ["python", state["script_path"]], capture_output=True, text=True, check=True
        )
        return {"success": True, "error": ""}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr}


def analyze_error_and_patch(state: AgentState):
    """Placeholder for LLM-based error analysis and file patching."""
    # In a real implementation, you'd pass state["error"] and the script content to an LLM
    # Here we simulate the patch generation.
    print(f"Self-healing agent analyzing error: {state['error'][:100]}...")

    # Simulate a patch application
    with open(state["script_path"], "a") as f:
        f.write("\n# Self-healing agent applied a patch.")

    return {"retry_count": state["retry_count"] + 1}


def routing_logic(state: AgentState):
    """Decides if the workflow should end or retry."""
    if state["success"]:
        return "end"
    if state["retry_count"] >= 3:
        return "end"
    return "patch"


# 1. Initialize Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("execute", execute_script)
workflow.add_node("patch", analyze_error_and_patch)

# 3. Set Entry Point
workflow.set_entry_point("execute")

# 4. Add Conditional Edges
workflow.add_conditional_edges("execute", routing_logic, {"end": END, "patch": "patch"})

# 5. Complete cycle
workflow.add_edge("patch", "execute")

# Compile
app = workflow.compile()

if __name__ == "__main__":
    # Example usage: targeting the ingest script
    initial_state = {
        "script_path": "./src/ingest.py",
        "error": "",
        "retry_count": 0,
        "success": False,
    }

    for s in app.stream(initial_state):
        print(s)
