@echo off
git pull origin master

call %ProgramData%\Anaconda3\Scripts\activate.bat base

set envfile="conda-environment.yml"

for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
if "%version%" == "6.1" set envfile="conda-environment.win7.yml"

conda env create -f %envfile%
conda activate nanosquared
pip install .
echo Press any key to exit . . .
pause>nul