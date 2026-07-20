@echo off
setlocal
cd /d "%~dp0"
set "PYTHON_EXE=C:\Users\pc\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
"%PYTHON_EXE%" -m streamlit run app.py --server.port 8501 --server.address 127.0.0.1

