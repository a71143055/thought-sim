from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.app.sim_engine import SimulationEngine
from typing import Dict

router = APIRouter()
_engine = SimulationEngine()

class SimRequest(BaseModel):
    text: str

class ExportRequest(BaseModel):
    node_id: str
    format: str = "windows-exe"

@router.post("/simulate")
async def simulate(req: SimRequest) -> Dict:
    try:
        artifact_json = _engine.step(req.text)
        return {"ok": True, "artifact": artifact_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export")
async def export(req: ExportRequest) -> Dict:
    if req.node_id not in _engine.state:
        raise HTTPException(status_code=404, detail="node not found")
    # 실제 빌드는 CLI 스크립트에서 수행되므로 여기서는 스케줄링 메시지 반환
    return {"ok": True, "message": f"Export scheduled for {req.node_id} as {req.format}"}
