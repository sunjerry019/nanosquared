@echo off
call %ProgramData%\Anaconda3\Scripts\activate.bat nanosquared
python ./src/cli-app/m2-app.py
echo Press any key to exit . . .
pause>nul