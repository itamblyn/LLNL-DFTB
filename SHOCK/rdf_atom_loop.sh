#!/bin/bash

rm -f x??

# 210 atoms + 2 headers

split -a 3 -d -212000 lmp_traj.xyz # break file into chunks of 1000 snapshots, i.e. 1 ps

lastframe=`ls x??? | tail -1`

echo "the last frame is $lastframe"

rm $lastframe

for file in x???
do
  echo $file

  for atomtype1 in C H O N
  do

    for atomtype2 in C H O N
    do

      echo "Timestep " $file ", pair " "$atomtype1" "$atomtype2"

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

      if [ ! -d plot_dat ]; then
        echo "There is no plot_dat directory"
        echo "Making one now"
        mkdir plot_dat 
      fi

      mv RDF*.dat plot_dat/

    done

  done

done

#rm x???
