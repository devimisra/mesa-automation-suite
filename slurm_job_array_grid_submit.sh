#!/bin/bash
#SBATCH --account= # ADD
#SBATCH --partition=norma2
#SBATCH -N 1
#SBATCH --cpus-per-task=4
#SBATCH --ntasks-per-node=1
#SBATCH --time=2-00:00:00
#SBATCH --job-name="mesa_grid"
#SBATCH --output=slurm-%A_%a.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user= # ADD
#SBATCH --mem-per-cpu=4G
#SBATCH --array= # ADD

# Add MESASDK path
# Add MESA path 

# get the run directory for this job index
RUN_DIR=$(awk -v id=$SLURM_ARRAY_TASK_ID '$1==id {print $2}' joblist.txt)
cd PATH/$RUN_DIR || exit 1

./clean
./mk
./rn |tee log.txt
