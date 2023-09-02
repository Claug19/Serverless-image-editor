cd ../../
python script_set_configuration.py LOCAL
start script_start_local_apps.bat
cd tests/time_tests_local
timeout /t 12
pytest -m performance -v --count=50
