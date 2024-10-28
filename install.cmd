set "currentDirectory=%cd%
pyinstaller --distpath %currentDirectory% -i favicon.ico --onefile --noconsole Katamino.py
pause
