from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.langgraph_flow import run_github_agent

app = FastAPI(
    title = " MCP GitHub Agent API",
    description = "A FastAPI backend that powers the MCP-Based Github reasoning agent.",
    version = "1.0.0")

# Allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Streamlit or Next.js frontend will call from browser
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "MCP GitHub Agent API is running!"}

@app.get("/analyze_repo")
def analyze_repo(query: str = Query(..., description="GitHub repository query, e.g. 'analyze facebook/react'")):
    """Example: /analyze_repo?query=analyze openai/gpt-4"""
    try:
        summary = run_github_agent(query)
        return {"query": query, "summary": summary}
    except Exception as e:
        return {"error": str(e)}