@echo off
git pull origin master

call %ProgramData%\Anaconda3\Scripts\activate.bat base
conda env update --name nanosquared --file ../conda-environment.yml --prune
conda activate nanosquared
pip install .
echo Press any key to exit . . .
pause>nul