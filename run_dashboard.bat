@echo off
start "CogniServer" python -m uvicorn cogniserver.main:app --reload --port 8000
timeout /t 3
start dashboard\index.html
echo Dashboard launched!
