#!/usr/bin/env python

import numpy, sys
import matplotlib, pylab

if len(sys.argv) == 1:
     print 'usage: ' + sys.argv[0] + ' matrix.dat'

inputFilename = sys.argv[1]
inputFile = open (inputFilename,'r')
savefile1 = inputFilename.split('.')[0]+inputFilename.split('.')[1]+inputFilename.split('.')[2]+'.png'

file_linecounter = 0
for line in inputFile.readlines():
  file_linecounter += 1
inputFile.seek(0) # rewind the file

header = inputFile.readline().split()
if (header[0]) == 'Hamiltonian:': # check if this is nir's old format
    dimension = (file_linecounter - 3)/2 # 3 info lines, and both matrix and diagonal are printed
    unit_scale = 1.0
else:
   inputFile.seek(0) # rewind the file
   dimension = file_linecounter
   unit_scale = 27.211383
line_counter = 0

HAMILITONIAN_array = []

for line_counter in range(dimension):

    HAMILITONIAN_array.append([])
    
    line = inputFile.readline()
    row_counter = 0
    for element in line.split():
      if (row_counter > 0) and (row_counter < len(line.split()) - 1): # skips first and last element
        HAMILITONIAN_array[-1].append(float(element))
      row_counter += 1
#    print HAMILITONIAN_array[-1]
#    print line_counter 
inputFile.close()

print numpy.shape(HAMILITONIAN_array)

HAMILITONIAN_array = numpy.reshape(HAMILITONIAN_array,(dimension,dimension))
HAMILITONIAN_array *= unit_scale

# remove diagonal components for plotting purposes

for i in range(numpy.shape(HAMILITONIAN_array)[0]):
    for j in range(numpy.shape(HAMILITONIAN_array)[1]):
        if (i == j): HAMILITONIAN_array[i][j] = 0

if len(sys.argv) == 4:
     vmin_value = float(sys.argv[2])
     vmax_value = float(sys.argv[3])
#     savefile = sys.argv[4]

else:
     vmin_value = HAMILITONIAN_array.min()
     vmax_value = HAMILITONIAN_array.max()
#     savefile = sys.argv[2]


im = pylab.imshow(HAMILITONIAN_array,vmin=vmin_value,vmax=vmax_value)
im.set_interpolation('nearest')
#pylab.xticks([1],' ')
#pylab.yticks([1],' ')
pylab.colorbar(cax=pylab.axes([0.85,0.1,0.05,0.8]))
pylab.savefig(savefile1)
