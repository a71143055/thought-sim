"""
간단한 PyInstaller 기반 빌드 스크립트.
- 목적: src/app/main.py를 단일 exe로 패키징 (uvicorn 포함)
- 실제 배포용으로는 더 정교한 설정(데몬, 서비스, 리소스 포함 등)이 필요합니다.
"""

import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENTRY = ROOT / "src" / "app" / "main.py"
DIST_DIR = ROOT / "dist" / "windows_build"

def ensure_pyinstaller():
    try:
        import PyInstaller  # type: ignore
    except Exception:
        print("PyInstaller가 설치되어 있지 않습니다. 설치를 시도합니다...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build():
    ensure_pyinstaller()
    if not ENTRY.exists():
        print("엔트리 파일을 찾을 수 없습니다:", ENTRY)
        return
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    # 단일 파일 빌드 (예시). 실제로는 uvicorn을 포함한 실행 스크립트를 별도 작성하는 것이 안전.
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "thoughtsim",
        "--add-data", f"{ROOT / 'src' / 'app' / 'templates'}{os.pathsep}templates",
        "--add-data", f"{ROOT / 'src' / 'app' / 'static'}{os.pathsep}static",
        str(ENTRY)
    ]
    print("빌드 명령:", " ".join(cmd))
    subprocess.check_call(cmd)
    print("빌드 완료. dist 폴더를 확인하세요.")

if __name__ == "__main__":
    build()
