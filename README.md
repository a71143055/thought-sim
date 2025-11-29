# Thought-Sim

웹 기반으로 **생각의 흐름을 시뮬레이션**하고, 시뮬레이션 결과물을 Windows 실행 파일로 내보내는 프로젝트입니다.

## 요구사항
- Python 3.11
- PyCharm 권장

## 실행 (개발)
1. 가상환경 생성 및 활성화
2. `pip install -r requirements.txt`
3. 프로젝트 루트에서:
   `uvicorn src.app.main:app --reload --host 127.0.0.1 --port 8000`

## 빌드 (Windows exe)
- `python src/cli/build_windows.py` 를 사용해 PyInstaller 기반으로 exe 생성

