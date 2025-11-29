"""
PyInstaller 기반 간단 빌드 스크립트 (예시).
주의: 로컬에 PyInstaller가 설치되어 있어야 하며, 복잡한 리소스 포함은 추가 설정 필요.
"""

import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENTRY = ROOT / "src" / "app" / "main.py"

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
    print("빌드 완료. PyInstaller의 dist/ 디렉터리를 확인하세요.")

if __name__ == "__main__":
    build()
