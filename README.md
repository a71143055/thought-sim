# Thought-Sim (PyCharm 실행용)

## 요구사항
- Python 3.11
- PyCharm (또는 다른 IDE)
- 권장: 가상환경(.venv)

## 설치 및 실행 (PyCharm)
1. 프로젝트 열기
2. Python 인터프리터로 Python 3.11 가상환경 생성/선택
3. 터미널에서: `pip install -r requirements.txt`
4. PyCharm에서 `src/app/main.py`를 Run (Run Configuration: Python script)
   또는 터미널에서:
   `python -m uvicorn src.app.main:app --reload --host 127.0.0.1 --port 8000`
5. 브라우저에서 `http://127.0.0.1:8000/` 접속

## Windows exe 빌드 (예시)
- `python src/cli/build_windows.py` (PyInstaller 필요)
