#!/bin/bash
#
#SBATCH --job-name=procStartParams
#SBATCH --comment="Process Start Params of fitting"
#SBATCH --ntasks=50
#SBATCH --time=24:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=Yudong.Sun@physik.uni-muenchen.de
#SBATCH --chdir=/home/y/Yudong.Sun/attoworld/nanosquared/tests
#SBATCH --output=/home/y/Yudong.Sun/attoworld/slurm/slurm.%j.%N.out
#SBATCH --error=/home/y/Yudong.Sun/attoworld/slurm/slurm.%j.%N.err.out

# source /etc/profile.d/modules.sh
# module load openmpi

mpiexec -n $SLURM_NTASKS python3 processstartparam.py
