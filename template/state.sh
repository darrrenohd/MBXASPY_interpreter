#!/bin/bash
#SBATCH --account=nano
#SBATCH --partition=vulcan
#SBATCH -t 01:00:00
#SBATCH -e state.err
#SBATCH -o state.out
#SBATCH -J Job_Name
#SBATCH -n 32
#SBATCH -N 4

 module load MBXAS/1.0 &> /dev/null

 export MBXAS=/global/home/groups-sw/nano/mbxas_2021/MBXAS
 ## Modify the above line appropriately..
 export SHIRLEY_ROOT=$MBXAS/Shirley
 export MBXASPY_ROOT=$MBXAS/mbxaspy
 export PSEUDO_DIR=$MBXAS/XCH_pseudos

 $SHIRLEY_ROOT/../xas_script/setup_arvid.sh
 . $SLURM_SUBMIT_DIR/Input_Block.in
  $SHIRLEY_ROOT/scripts/arvid/XAS_state.sh
  #$SHIRLEY_ROOT/scripts/arvid/xas_gs_state.sh
