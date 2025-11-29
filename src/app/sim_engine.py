"""
간단한 시뮬레이션 엔진.
- 입력 텍스트를 받아 토큰화, 노드 생성, 상태 저장
- 아티팩트를 dist 디렉터리에 JSON으로 저장
"""

from typing import Dict, Any
import uuid
import json
import datetime
import os

class SimulationEngine:
    def __init__(self, storage_dir: str | None = None):
        self.state: Dict[str, Dict[str, Any]] = {}
        self.storage_dir = storage_dir or os.path.join(os.getcwd(), "dist")
        os.makedirs(self.storage_dir, exist_ok=True)

    def _tokenize(self, text: str) -> list[str]:
        # 간단 토큰화: 공백 기준, 불필요 공백 제거
        return [t for t in text.strip().split() if t]

    def step(self, thought_text: str) -> str:
        """
        한 단계 시뮬레이션 실행:
        - 노드 생성
        - 상태 저장
        - 아티팩트 파일 생성 (artifact_<id>.json)
        - 클라이언트에 보낼 JSON 문자열 반환
        """
        node_id = str(uuid.uuid4())
        tokens = self._tokenize(thought_text)
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        node = {
            "id": node_id,
            "input": thought_text,
            "tokens": tokens,
            "summary": " ".join(tokens[:16]),
            "created_at": timestamp,
        }
        self.state[node_id] = node

        artifact_filename = f"artifact_{node_id}.json"
        artifact_path = os.path.join(self.storage_dir, artifact_filename)
        with open(artifact_path, "w", encoding="utf-8") as f:
            json.dump(node, f, ensure_ascii=False, indent=2)

        return json.dumps({
            "node_id": node_id,
            "artifact_file": artifact_filename,
            "summary": node["summary"]
        }, ensure_ascii=False)
