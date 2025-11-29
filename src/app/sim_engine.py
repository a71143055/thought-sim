"""
간단한 시뮬레이션 엔진 구현.
- 입력 텍스트(생각)를 받아 토큰화, 노드 생성, 상태 저장
- 아티팩트(요약, 메타데이터, 간단한 파일 컨텐츠)를 반환
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
        # 매우 단순한 토큰화 (확장 가능)
        return [t for t in text.strip().split() if t]

    def step(self, thought_text: str) -> str:
        """
        한 단계 시뮬레이션을 실행하고, 결과 아티팩트를 JSON 문자열로 반환.
        아티팩트는 dist 디렉터리에 간단한 파일로 저장됨.
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

        # 간단한 아티팩트 파일 생성 (예: 텍스트 파일)
        artifact_filename = f"artifact_{node_id}.json"
        artifact_path = os.path.join(self.storage_dir, artifact_filename)
        with open(artifact_path, "w", encoding="utf-8") as f:
            json.dump(node, f, ensure_ascii=False, indent=2)

        # 반환값은 JSON 문자열 (클라이언트가 파싱)
        return json.dumps({"node_id": node_id, "artifact_file": artifact_filename, "summary": node["summary"]}, ensure_ascii=False)
