from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from src.app.sim_engine import SimulationEngine
from src.app.api.routes import router as api_router
import os

app = FastAPI(title="ThoughtSim")

# 정적 파일 및 템플릿 경로 설정
static_dir = os.path.join(os.path.dirname(__file__), "static")
templates_dir = os.path.join(os.path.dirname(__file__), "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.include_router(api_router, prefix="/api")

engine = SimulationEngine()

@app.get("/", response_class=HTMLResponse)
async def index():
    index_path = os.path.join(templates_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws/sim")
async def websocket_sim(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            # 시뮬레이션 엔진에 입력 전달
            result = engine.step(data)
            await ws.send_text(result)
    except WebSocketDisconnect:
        # 연결 종료 처리
        pass
