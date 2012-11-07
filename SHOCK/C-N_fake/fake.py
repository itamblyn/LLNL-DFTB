#!/bin/env python

inputFile = open('d1.xyz','r')
outputFile = open('d1Fake.xyz','w')

nsnapshots = 100001
nskip = 170
natoms = 210

ns = 0

while ns < nsnapshots:
   for i in range(3):
       line = inputFile.readline()
       outputFile.write(line)
   line = inputFile.readline() # natoms
   outputFile.write(str(natoms - nskip) + '\n')

   for i in range(5):
       line = inputFile.readline()
       outputFile.write(line)
   for i in range(nskip):
       line = inputFile.readline()
   for i in range(natoms - nskip):
       line = inputFile.readline()
       if int(line.split()[1]) == 3:
           outputFile.write(str(i+1) + ' ' + str(int(line.split()[1])-2) + ' ' + str(line.split()[2]) + ' ' + str(line.split()[3]) + ' ' + str(line.split()[4]) + ' ' + str(line.split()[5]) + '\n')
       elif int(line.split()[1]) == 4:
           outputFile.write(str(i+1) + ' ' + str(int(line.split()[1])-2) + ' ' + str(line.split()[2]) + ' ' + str(line.split()[3]) + ' ' + str(line.split()[4]) + ' ' + str(line.split()[5]) + '\n')
   ns += 1

print ns
line = inputFile.readline()

print line 
