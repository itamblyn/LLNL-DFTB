#!/usr/bin/env python

import sys
import numpy as np
from scipy import linalg as LA
import matplotlib, pylab

natom = 3
nbasis = 1 + 3 + 5
zatom = 4

absoluteH = False

def main():

  if len(sys.argv) == 1:
       print 'usage: ' + sys.argv[0] + ' matrix.dat'

  inputFilename = sys.argv[1]

  # Hamiltonian  
  inputFilename = inputFilename.split('.')[0]+'.'+inputFilename.split('.')[1]+'.Hmat'
  inputFile = open (inputFilename,'r')

  file_linecounter = 0
  for line in inputFile.readlines():
    file_linecounter += 1
  inputFile.seek(0) # rewind the file

  header = inputFile.readline().split()
  if (header[0]) == 'Hamiltonian:': # check if this is nir's old format
      dimension = (file_linecounter - 3)/2 # 3 info lines, and both matrix and diagonal are printed
  else:
     inputFile.seek(0) # rewind the file
     dimension = file_linecounter
  unit_scale = 27.2116

  HAMILITONIAN_array = []

  for line_counter in range(dimension):

      HAMILITONIAN_array.append([])
      
      line = inputFile.readline()
      row_counter = 0
      for element in line.split():
        if (row_counter > 0) and (row_counter < len(line.split()) - 1): # skips first and last element
            if (absoluteH == True): HAMILITONIAN_array[-1].append(np.abs(float(element)))
            else: HAMILITONIAN_array[-1].append(float(element))
        row_counter += 1
  inputFile.close()

  HAMILITONIAN_array = np.reshape(HAMILITONIAN_array,(dimension,dimension))
  HAMILITONIAN_array *= unit_scale

  print HAMILITONIAN_array[0][0]

  inputFile.close()

#####

  inputFilename = inputFilename.split('.')[0]+'.'+inputFilename.split('.')[1]+'.Smat'

  inputFile = open (inputFilename,'r')

  file_linecounter = 0
  for line in inputFile.readlines():
    file_linecounter += 1
  inputFile.seek(0) # rewind the file

  header = inputFile.readline().split()
  if (header[0]) == 'Overlap:': # check if this is nir's old format
      dimension = (file_linecounter - 3)/2 # 3 info lines, and both matrix and diagonal are printed
  else:
     inputFile.seek(0) # rewind the file
     dimension = file_linecounter

  unit_scale = 1.0

  OVERLAP_array = []

  for line_counter in range(dimension):

      OVERLAP_array.append([])
      
      line = inputFile.readline()
      row_counter = 0
      for element in line.split():
        if (row_counter > 0) and (row_counter < len(line.split()) - 1): # skips first and last element
            OVERLAP_array[-1].append(float(element))
        row_counter += 1
  inputFile.close()

  OVERLAP_array = np.reshape(OVERLAP_array,(dimension,dimension))

  COMPUTED_array = np.zeros((np.shape(HAMILITONIAN_array)[0],np.shape(HAMILITONIAN_array)[1]))

  K = 0.00

  for i in range(np.shape(COMPUTED_array)[0]):
    for j in range(np.shape(COMPUTED_array)[1]):
        if (i == j):
            COMPUTED_array[i][j] =  HAMILITONIAN_array[i][j]
        else:
            COMPUTED_array[i][j] = -K*(1./2.)*(HAMILITONIAN_array[i][i]+HAMILITONIAN_array[j][j])*OVERLAP_array[i][j]

  print COMPUTED_array[0][0]

  if len(sys.argv) == 4:
       vmin_value = float(sys.argv[2])
       vmax_value = float(sys.argv[3])
 
  else:
       vmin_value = COMPUTED_array.min()
       vmax_value = COMPUTED_array.max()

  savefile1 = inputFilename.split('.')[0]+inputFilename.split('.')[1]+inputFilename.split('.')[2]+'.png'

  im = pylab.imshow(COMPUTED_array,vmin=vmin_value,vmax=vmax_value)
  pylab.title('Computed Hamiltonian matrix')
  for i in np.arange(1,natom,1):
      pylab.axvline(x= nbasis*i - .5)
      pylab.axhline(y= nbasis*i - .5)
  im.set_interpolation('nearest')
  pylab.colorbar(cax=pylab.axes([0.85,0.1,0.05,0.8]))
  pylab.savefig('computed.png')

  #####
  print 'The first natom*nvalence states are '
  eigenvalues, eigenvectors = LA.eigh(HAMILITONIAN_array, OVERLAP_array)
  print eigenvalues[0:natom*zatom]

  print 'The first natom*nvalence states are '
  eigenvalues, eigenvectors = LA.eigh(COMPUTED_array)
  print eigenvalues[0:natom*zatom]

if __name__ == '__main__':
    main()
