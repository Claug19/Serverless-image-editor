python script_set_configuration.py LOCAL
start script_start_local_apps.bat
cd ../tests/memory_tests
timeout /t 12
pytest . -v --count=50
