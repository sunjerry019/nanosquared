@echo off
git pull origin master

call %ProgramData%\Anaconda3\Scripts\activate.bat nanosquared
pip install .

echo Press any key to exit . . .
pause>nul
