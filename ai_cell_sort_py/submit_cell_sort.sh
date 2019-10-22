#!/bin/bash 
#PBS -k o 
#PBS -l nodes=1:ppn=1,walltime=200:00:00
#PBS -M jferrari@iu.edu
#PBS -m abe
#PBS -N ai_cell_sort 
#PBS -j oe

module swap python python/2.7.3

module load compucell3d/3.7.5


paramScan.sh -i /N/u/jferrari/Karst/ai_cell_sort/ai_cell_sort_karst.cc3d -o /N/u/jferrari/Karst/ai_cell_sort/screenShots/ -f 100
