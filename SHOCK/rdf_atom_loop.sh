#!/bin/bash

rm -f x??

# 210 atoms + 2 lines of header

if [ ! -e lmp_traj.xyz ]; then
    echo "There is no xyz file, making it now"
    ~/scripts/lammpstoxyz.OHNC.pl d1.xyz # if there is no .xyz for the traj, make it
    
fi

if [ ! -e unwrapped.xyz ]; then
    echo "There is no unwrapped file, making it now"
    echo "lmp_traj.xyz" > wrap.in
    echo "Unwrapping the file"
    ~/git/MD/bin/unwrap_PBC_cell.x < wrap.in

fi


echo "warning, using wrapped trajectory"
split -a 3 -d -424000 lmp_traj.xyz # break file into chunks of 1000 snapshots, i.e. 1 ps
#split -a 3 -d -212000 unwrapped.xyz # break file into chunks of 1000 snapshots, i.e. 1 ps

lastframe=`ls x??? | tail -1`

echo "the last frame is $lastframe"

rm $lastframe

if [ ! -d plot_dat ]; then
    echo "There is no plot_dat directory"
    echo "Making one now"
    mkdir plot_dat 
fi

for file in x???
do
  echo -n $file" " 
  pwd
  for atomtype1 in C H O N
  do

    for atomtype2 in C H O N
    do

      echo "Timestep " $file ", pair " "$atomtype1" "$atomtype2"

      # input file for RDF

      echo "$file" > rdf.in
      echo -n "RDF." >> rdf.in
      echo -n "$atomtype1" >> rdf.in
      echo -n "$atomtype2" >> rdf.in
      echo -n "." >> rdf.in
      echo -n "$file" >> rdf.in
      echo ".dat" >> rdf.in
      echo "$atomtype1" >> rdf.in
      echo "$atomtype2" >> rdf.in
      echo "5.0" >> rdf.in
      echo "0.025" >> rdf.in
      echo "1" >> rdf.in

      RDF < rdf.in >& /dev/null 

      mv RDF*.dat plot_dat/

    done

    # input file for atom VACF

    echo "$file" > vacf.in
    echo -n "VACF." >> vacf.in
    echo -n "$atomtype1" >> vacf.in
    echo -n "." >> vacf.in
    echo -n "$file" >> vacf.in
    echo ".dat" >> vacf.in
    echo "41.34281461881925" >> vacf.in  # 1 fs in au
    echo "100" >> vacf.in # 100 steps between windows
    echo "1" >> vacf.in  # window length in ps
    echo "$atomtype1" >> vacf.in
    VACF < vacf.in >& /dev/null
    
  done

  # input file for ALL VACF

  echo "$file" > vacf.in
  echo -n "VACF." >> vacf.in
  echo -n "ALL" >> vacf.in
  echo -n "." >> vacf.in
  echo -n "$file" >> vacf.in
  echo ".dat" >> vacf.in
  echo "41.34281461881925" >> vacf.in  # 1 fs in au
  echo "100" >> vacf.in # 100 steps between windows
  echo "1" >> vacf.in  # window length in ps
  echo " " >> vacf.in
  VACF < vacf.in >& /dev/null

  # compute spectra from ALL VACF

  echo -n "VACF.ALL." > vdos.in
  echo -n "$file" >> vdos.in
  echo ".dat" >> vdos.in
  echo "41.34281461881925" >> vdos.in # # 1 fs in au
  ~/git/private/VDOS/vdos.x < vdos.in >& /dev/null
  # convert from THz to cm-1
  running_average.py VDOS.dat 50
  awk '{print $1/1E-12*(8.0655E+03/2.41796E+14),$2*1E-12/(8.0655E+03/2.41796E+14)}' raverage.dat > plot_dat/VDOS."$file".dat
  rm VDOS.dat raverage.dat

  mv VACF*.dat plot_dat/

done

rm x???
