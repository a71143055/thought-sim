from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.sim_engine import SimulationEngine
from typing import Dict
import uuid

router = APIRouter()
_engine = SimulationEngine()

class SimRequest(BaseModel):
    text: str

class ExportRequest(BaseModel):
    node_id: str
    format: str = "windows-exe"  # 확장 가능

@router.post("/simulate")
async def simulate(req: SimRequest) -> Dict:
    """REST 방식 시뮬레이션 호출 (동기적 처리)"""
    try:
        artifact_json = _engine.step(req.text)
        return {"ok": True, "artifact": artifact_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export")
async def export(req: ExportRequest) -> Dict:
    """
    시뮬레이션 결과를 Windows 실행 파일 등으로 내보내는 엔드포인트(간단 시뮬레이션).
    실제 빌드는 CLI 스크립트에서 수행.
    """
    # 여기서는 간단히 존재 확인만 수행
    if req.node_id not in _engine.state:
        raise HTTPException(status_code=404, detail="node not found")
    # 실제 빌드 파이프라인과 연동하려면 작업 큐/파일 시스템 연동 필요
    return {"ok": True, "message": f"Export scheduled for {req.node_id} as {req.format}"}
