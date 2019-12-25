#!/bin/bash

for filename in eebo_zipped/*.zip; do
  sbatch -p RM-shared -N 1 --ntasks-per-node 1 --mail-type ALL -t 05:00:00 uz.sh $filename
done
