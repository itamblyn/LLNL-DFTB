#!/bin/bash

value=`hostname`

if [ "$value" == 'cadmium' ]; then
 for file in ?.?.Hmat
   do
   $HOME/git/LLNL-DFTB/show_matrix.py $file -20 20 &
 done

 for file in ?.?.Smat
   do
   $HOME/git/LLNL-DFTB/show_matrix.py $file -20 20 &
 done


else
 for file in ?.?.Hmat
 do
   arch -i386 /Library/Frameworks/Python.framework/Versions/2.7/bin/python $HOME/git/LLNL-DFTB/show_matrix.py $file -20 20 & 
 done

 for file in ?.?.Smat
 do
   arch -i386 /Library/Frameworks/Python.framework/Versions/2.7/bin/python $HOME/git/LLNL-DFTB/show_matrix.py $file -20 20 &
 done


fi

wait
