# api.py
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
from backend.langgraph_flow import run_flow

app = FastAPI()

class MCPRequest(BaseModel):
    mcp_version: str
    user_id: str | None = None
    context: dict
    query: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/mcp")
async def mcp_endpoint(req: MCPRequest):
    try:
        # run_flow should return something like: {"answer": "...", "trace": [...], "actions": [...]}
        result = await run_flow(req.dict())
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
