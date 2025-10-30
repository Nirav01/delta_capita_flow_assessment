from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from app.flow_manager import FlowManager

app = FastAPI(title="Flow Manager Service")

class RunFlowRequest(BaseModel):
    flow: Dict[str, Any]
    context: Dict[str, Any] | None = None

@app.post("/run-flow")
def run_flow(body: RunFlowRequest):
    try:
        manager = FlowManager(body.model_dump())
        return manager.run(body.context)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))