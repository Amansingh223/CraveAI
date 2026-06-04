@echo off
echo Starting CraveAI Backend (FastAPI) and Frontend (Streamlit)

REM Start FastAPI in the background
start /B cmd /c "uvicorn src.api.main:app --reload --port 8000"

REM Wait 2 seconds for API to boot
timeout /t 2 /nobreak > NUL

REM Start Streamlit
streamlit run app/main.py --server.port 8501

echo Application exited.
