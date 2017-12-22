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
TITLESTR="ELDER_$DATE"
TXT='.txt'
SAVETXT=$TITLESTR$TXT
x='Finished'
echo $x > $SAVETXT
sendmail daviddralle@gmail.com << EOF
subject:$TITLESTR
$x
EOF