#!/bin/bash

for i in {1..300};
do
    echo $i
    qsub submit_cell_sort.sh
done