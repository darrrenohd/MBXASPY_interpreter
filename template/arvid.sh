#!/bin/bash
#SBATCH --account=nano
#SBATCH --partition=vulcan_c20
#SBATCH -t 24:00:00
#SBATCH -e arvid.err
#SBATCH -o arvid.out
#SBATCH -J Job_Name
#SBATCH -n 60
#SBATCH -N 3

 module load MBXAS &> /dev/null

 export MAIN_ROOT=/global/home/groups-sw/nano/mbxas_2021/MBXAS
 ## Modify the above line appropriately..
 export SHIRLEY_ROOT=$MAIN_ROOT/Shirley
 export MBXASPY_ROOT=$MAIN_ROOT/mbxaspy
 export PSEUDO_DIR=$MAIN_ROOT/XCH_pseudos

 $SHIRLEY_ROOT/../xas_script/setup_arvid.sh
 . $SLURM_SUBMIT_DIR/Input_Block.in
 $SHIRLEY_ROOT/scripts/arvid/XAS_arvid.sh

