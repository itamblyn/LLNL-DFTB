#!/bin/bash

export OMP_NUM_THREADS=4

if [ ! -d molanal.CN ]; then
  echo "There is no molanal directory"
  echo "Making one now"
  mkdir molanal.CN
fi

if [ ! -e lmp_traj.CN.gen ]; then
    echo "There is no gen file, making it now"
    ~/scripts/lammpstogen.NC.pl d1.xyz # if there is no .gen for the traj, make it
fi

cd molanal

rm -f x???

# 210 atoms + 6 headers
split -a 3 -d -216000 ../lmp_traj.gen # break file into chunks of 1000 snapshots, i.e. 1 ps
                                      # although the MD timestep is 0.2 fs, because I only output
                                      # once every 5 steps, the effective xyz timestep is 1 fs
for file in x???
do
  echo -n $file" "
  pwd
  if [ -d molecules ]; then
    rm -f molecules/* # if there is a molecules directory from previous run, clear it out
  fi

  cp $HOME/bin/molanalysis/input_nasa/bond*.dat . # bring molanal input files to current directory

  ~/bin/molanalysis/molanal.new $file > molanal."$file"
  ~/bin/molanalysis/findmolecules.pl molanal."$file" > findmolecules."$file"

done

rm x???

rm -f molecules/*

~/bin/molanalysis/molanal.new ../lmp_traj.gen > molanal.full
~/bin/molanalysis/findmolecules.pl molanal.full > findmolecules.full
