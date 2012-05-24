#!/usr/bin/env python

import numpy, sys, commands
import matplotlib, pylab

def main():

  try:
     # Attempt to retrieve required input from user
     prog = sys.argv[0]
     matrix_row = int(sys.argv[1])
     matrix_column = int(sys.argv[2])
  except IndexError:
     # Tell the user what they need to give
     print '\nusage: '+prog+' a b    (where a & b are numbers)\n'
     # Exit the program cleanly
     sys.exit(0)

  files = commands.getoutput('ls *Hmat ').split()
  HAMILITONIAN_array = []

  for filename in files:

     inputFile = open (filename,'r')

     file_linecounter = 0
     for line in inputFile.readlines():   # count number of lines in matrix file
         file_linecounter += 1            #
     inputFile.seek(0)                    # rewind the file

     dimension = file_linecounter
     unit_scale = 27.211383
     line_counter = 0
     
     HAMILITONIAN_array.append([])

     for line_counter in range(dimension):

       HAMILITONIAN_array[-1].append([])
     
       line = inputFile.readline()
       row_counter = 0
       for element in line.split():
         if (row_counter > 0) and (row_counter < len(line.split()) - 1): # skips first and last element
           HAMILITONIAN_array[-1][-1].append(float(element))
         row_counter += 1
#         print HAMILITONIAN_array[-1][-1]
#         print line_counter 
     inputFile.close()

  HAMILITONIAN_array = numpy.reshape(HAMILITONIAN_array,(len(files),dimension,dimension))
  HAMILITONIAN_array *= unit_scale

  # remove diagonal components for plotting purposes

  y = []
  x = []

  outputFile = open('dist'+str(matrix_row)+str(matrix_column)+'.png','w')

  for imatrix in range(len(files)):
      outputFile.write(str(x)+' '+str(y)+'\n')
      y.append(HAMILITONIAN_array[imatrix][matrix_row][matrix_column])
      x.append((0.9 + imatrix*.1)*.529177)


  outputFile.close()

  pylab.plot(x,y)
  pylab.xlabel('Separation')
  pylab.ylim(-50,50)
  pylab.ylabel('Matrix element [eV]')
  pylab.grid(True)
  pylab.title('Matrix element <'+str(matrix_row)+'|H|'+str(matrix_column)+'> vs distance')  
  hostname = commands.getoutput('hostname').split()
  if hostname[0] == 'cadmium':
      pylab.show()
  else:
      pylab.savefig('dist'+str(matrix_row)+str(matrix_column)+'.png')
#  im.set_interpolation('nearest')
#  pylab.yticks([1],' ')
#  pylab.colorbar(cax=pylab.axes([0.85,0.1,0.05,0.8]))
#  pylab.savefig(savefile1)

if __name__ == '__main__':
    main()
