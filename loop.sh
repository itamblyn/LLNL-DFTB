#!/bin/bash

for file in ?.?.Hmat
do
arch -i386 /Library/Frameworks/Python.framework/Versions/2.7/bin/python ../../show_matrix.py $file -20 20
done
