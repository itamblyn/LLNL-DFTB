#!/usr/bin/env python

import sys, commands
import numpy as np
from scipy import linalg as LA
import matplotlib, pylab

natom = 3
nbasis = 1 + 3 + 5
zatom = 4

absoluteH = False

MullikenApproximation = False

def diagonal_screening(matrix_element):

   screened_value = 2.*matrix_element
   return screened_value

def offdiagonal_screening(matrix_element):

   screened_value = 1.matrix_element
   return screened_value


def main():

  try:
  # Attempt to retrieve required input from user
    prog = sys.argv[0]
    inputFilename = sys.argv[1]
    
  except IndexError:
  # Tell the user what they need to give
    print '\nusage: '+prog+' filename    (X.Hmat)\n'
    # Exit the program cleanly
    sys.exit(0)


  # Hamiltonian  
  inputFilename = inputFilename.split('.')[0]+'.'+inputFilename.split('.')[1]+'.Hmat' # cleaning
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

  HAMILTONIAN_array = []

  for line_counter in range(dimension):

      HAMILTONIAN_array.append([])
      
      line = inputFile.readline()
      row_counter = 0
      for element in line.split():
        if (row_counter > 0) and (row_counter < len(line.split()) - 1): # skips first and last element
            if (absoluteH == True): HAMILTONIAN_array[-1].append(np.abs(float(element)))
            else: HAMILTONIAN_array[-1].append(float(element))
        row_counter += 1
  inputFile.close()

  HAMILTONIAN_array = np.reshape(HAMILTONIAN_array,(dimension,dimension))
  unit_scale = 27.2116
  HAMILTONIAN_array *= unit_scale

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
  
#  print HAMILTONIAN_array
#  print OVERLAP_array

  COMPUTED_array = np.zeros((np.shape(HAMILTONIAN_array)[0],np.shape(HAMILTONIAN_array)[1]))


  if (MullikenApproximation == True):

    K = 1.00

    for i in range(np.shape(COMPUTED_array)[0]):
      for j in range(np.shape(COMPUTED_array)[1]):
          if (i == j):
              COMPUTED_array[i][j] =  HAMILTONIAN_array[i][j]
          else:
              COMPUTED_array[i][j] = -K*(1./2.)*(HAMILTONIAN_array[i][i]+HAMILTONIAN_array[j][j])*OVERLAP_array[i][j]

  else:

    for i in range(np.shape(COMPUTED_array)[0]):
      for j in range(np.shape(COMPUTED_array)[1]):
          if (i == j):
              COMPUTED_array[i][j] = diagonal_screening(HAMILTONIAN_array[i][j])
          else:
              COMPUTED_array[i][j] = offdiagonal_screening(HAMILTONIAN_array[i][j])


  if len(sys.argv) == 4:
       vmin_value = float(sys.argv[2])
       vmax_value = float(sys.argv[3])
 
  else:
       vmin_value = COMPUTED_array.min()
       vmax_value = COMPUTED_array.max()

  savefile1 = inputFilename.split('.')[0]+inputFilename.split('.')[1]+inputFilename.split('.')[2]+'.png'

  im = pylab.imshow(HAMILTONIAN_array,vmin=vmin_value,vmax=vmax_value)
  pylab.title('Hamiltonian matrix')
  for i in np.arange(1,natom,1):
      pylab.axvline(x= nbasis*i - .5)
      pylab.axhline(y= nbasis*i - .5)
  im.set_interpolation('nearest')
  pylab.colorbar(cax=pylab.axes([0.85,0.1,0.05,0.8]))

  # cadmium has a working version of pylab, other machines sadly do not..
  hostname = commands.getoutput('hostname').split()
#  if hostname[0] == 'cadmium':
#      pylab.show()
#  else:
  pylab.savefig('computed.png')

  #####
  print 'The first natom*nvalence eigenavlues from H are '
  eigenvalues, eigenvectors = LA.eigh(HAMILTONIAN_array, OVERLAP_array)
  print eigenvalues[0:natom*zatom]

  print 'The first natom*nvalence eigenvalues from COMPUTED array are '
  eigenvalues, eigenvectors = LA.eigh(COMPUTED_array, OVERLAP_array)
  print eigenvalues[0:natom*zatom]



if __name__ == '__main__':
    main()

