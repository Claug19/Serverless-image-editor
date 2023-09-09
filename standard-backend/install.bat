python -m venv venv
start "Requirements" cmd /c "echo 'Installing requirements inside application venv' & timeout /t 3 & dir & pip install -r src/requirements.txt & timeout /t 5"
venv/Scripts/activate.bat
