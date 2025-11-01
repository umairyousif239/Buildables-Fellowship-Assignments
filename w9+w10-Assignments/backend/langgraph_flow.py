from langgraph.graph import StateGraph, END
from backend.mcp_github import get_repo_activity
from typing import TypedDict, Optional, Dict, Any
import json

# --- Define the state schema ---
class AgentState(TypedDict, total=False):
    query: str
    repo: Optional[str]
    repo_data: Optional[Dict[str, Any]]
    summary: Optional[str]
    error: Optional[str]


# --- Node Functions ---
def user_input_node(state: AgentState) -> AgentState:
    """Extract repo name from user query"""
    query = state.get("query", "")
    state["repo"] = parse_repo_name(query)
    return state

def parse_repo_name(query: str):
    words = query.split()
    for w in words:
        if "/" in w:
            return w
    return "sample-repo/example-project"

def github_retriever_node(state: AgentState) -> AgentState:
    """Fetch repo activity using MCP GitHub retriever"""
    repo = state.get("repo")
    if not repo:
        state["error"] = "No repository specified."
        return state
    
    try:
        owner, repo_name = repo.split("/")
        data = get_repo_activity(owner, repo_name)
        state["repo_data"] = data
    except Exception as e:
        state["error"] = f"Failed to retrieve repo: {e}"
    return state

def summarize_node(state: AgentState) -> AgentState:
    """Summarize fetched GitHub data"""
    data = state.get("repo_data", {})
    summary = []

    commits = data.get("commits", [])
    if commits:
        summary.append(f"🧾 Recent commits ({len(commits)}):")
        for c in commits:
            summary.append(f"- {c['author']}: {c['message']}")

    issues = data.get("open_issues", [])
    if issues:
        summary.append(f"\n🐛 Open issues ({len(issues)}):")
        for i in issues:
            summary.append(f"- {i['title']} (by {i['user']})")

    prs = data.get("pull_requests", [])
    if prs:
        summary.append(f"\n🔃 Pull requests ({len(prs)}):")
        for p in prs:
            summary.append(f"- {p['title']} [{p['state']}] by {p['user']}")

    state["summary"] = "\n".join(summary) or "No recent activity found."
    return state


# --- Define Reasoning Graph ---
graph = StateGraph(AgentState)

graph.add_node("input", user_input_node)
graph.add_node("retrieve", github_retriever_node)
graph.add_node("summarize", summarize_node)

graph.add_edge("input", "retrieve")
graph.add_edge("retrieve", "summarize")

graph.set_entry_point("input")
graph.set_finish_point("summarize")

app = graph.compile()


def run_github_agent(query: str):
    """Run the LangGraph reasoning flow for a GitHub activity query."""
    initial_state: AgentState = {"query": query}
    result = app.invoke(initial_state)
    return result.get("summary", result.get("error", "Something went wrong."))
