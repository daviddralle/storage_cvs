#!/bin/bash
# Job name:
#SBATCH --job-name=test
#
# Account:
#SBATCH --account=fc_hydrology
#
# Partition:
#SBATCH --partition=savio2
#
# Wall clock limit:
#SBATCH --time=24:00:00
#
## Command(s) to run:
git checkout master
source activate gr3_linux
python hpc_cvs.py
DATE=`date +%Y-%m-%d_%H%M`
# TITLESTR="PLOT_$DATE"
# mail -a ./plots/output.pdf -s 'PLOT' daviddralle@gmail.com < /dev/null
# TITLESTR="DATA_$DATE"
mail -a ./monte_carlo_output/output.p -s 'DATA' daviddralle@gmail.com < /dev/null