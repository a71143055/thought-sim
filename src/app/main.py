from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from src.app.sim_engine import SimulationEngine
from src.app.api.routes import router as api_router
import os
import uvicorn

app = FastAPI(title="ThoughtSim")

# 정적/템플릿 경로
BASE_DIR = os.path.dirname(__file__)
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.include_router(api_router, prefix="/api")

# 시뮬레이션 엔진 인스턴스 (서버 전역)
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
            result = engine.step(data)
            await ws.send_text(result)
    except WebSocketDisconnect:
        # 연결 종료 시 간단 로깅(확장 가능)
        pass

# PyCharm에서 main.py를 직접 Run 할 수 있도록 엔트리 제공
if __name__ == "__main__":
    # 개발용: uvicorn을 내부에서 실행
    uvicorn.run("src.app.main:app", host="127.0.0.1", port=8000, reload=True)
