#!/bin/bash


for file in RDF.CH.x???.dat
do
  awk '{print $2}' $file > "$file".y
done

paste *.y > grid.dat
rm *.y
