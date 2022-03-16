@echo off
git pull origin master

call %ProgramData%\Anaconda3\Scripts\activate.bat base
conda env create -f conda-environment.yml
conda activate nanosquared
pip install .
echo Press any key to exit . . .
pause>nul