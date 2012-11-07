#!/bin/bash


for file in RDF.CN.x???.dat
do
  awk '{print $2}' $file > "$file".y
done

paste *.y > grid.CN.dat
rm *.y

for file in RDF.CC.x???.dat
do
  awk '{print $2}' $file > "$file".y
done

paste *.y > grid.CC.dat
rm *.y

