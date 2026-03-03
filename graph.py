from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agents.watcher import watcher_agent
from agents.planner import planner_agent
from agents.coder import coder_agent
from agents.validator import validator_agent
from agents.pr_agent import pr_agent
from config import MAX_RETRIES


# Define the shared state across all agents
class AgentState(TypedDict):
    failure_info: Optional[dict]
    plan_info: Optional[dict]
    coder_info: Optional[dict]
    validation_result: Optional[dict]
    pr_result: Optional[str]
    retries: int


# --- Node functions ---

def run_watcher(state: AgentState) -> AgentState:
    result = watcher_agent()
    return {**state, "failure_info": result}


def run_planner(state: AgentState) -> AgentState:
    result = planner_agent(state["failure_info"])
    return {**state, "plan_info": result}


def run_coder(state: AgentState) -> AgentState:
    result = coder_agent(state["plan_info"])
    return {**state, "coder_info": result, "retries": state["retries"] + 1}


def run_validator(state: AgentState) -> AgentState:
    result = validator_agent(state["coder_info"])
    return {**state, "validation_result": result}


def run_pr_agent(state: AgentState) -> AgentState:
    result = pr_agent(
        failure_info=state["failure_info"],
        coder_info=state["coder_info"],
        plan_info=state["plan_info"]
    )
    return {**state, "pr_result": result}


# --- Conditional edge functions ---

def should_proceed_after_watcher(state: AgentState) -> str:
    """Only continue if a failure was found."""
    if state["failure_info"] is None:
        print("✅ No failures found. Exiting.")
        return "end"
    return "planner"


def should_proceed_after_validator(state: AgentState) -> str:
    """Retry coder if tests failed, open PR if they passed."""
    if state["validation_result"]["passed"]:
        return "pr_agent"
    if state["retries"] >= MAX_RETRIES:
        print(f"❌ Max retries ({MAX_RETRIES}) reached. Giving up.")
        return "end"
    print(f"🔁 Retrying coder (attempt {state['retries'] + 1}/{MAX_RETRIES})...")
    return "coder"


# --- Build the graph ---

def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("watcher", run_watcher)
    graph.add_node("planner", run_planner)
    graph.add_node("coder", run_coder)
    graph.add_node("validator", run_validator)
    graph.add_node("pr_agent", run_pr_agent)

    # Set entry point
    graph.set_entry_point("watcher")

    # Add edges
    graph.add_conditional_edges("watcher", should_proceed_after_watcher, {
        "planner": "planner",
        "end": END
    })
    graph.add_edge("planner", "coder")
    graph.add_edge("coder", "validator")
    graph.add_conditional_edges("validator", should_proceed_after_validator, {
        "pr_agent": "pr_agent",
        "coder": "coder",
        "end": END
    })
    graph.add_edge("pr_agent", END)

    return graph.compile()
