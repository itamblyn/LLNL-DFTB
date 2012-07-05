#!/usr/bin/env python

import sys, os
import numpy

filedir='/Users/tamblyn2/nasa/mixture09/'
logFile = open(filedir+'/log','w')
############################
#############################
                            ##
num_x_sites = 4             ##
num_y_sites = 2             ##
num_z_sites = 2             ##
                            ##
#############################
############################

site_spacing = 4.3

filler = False

total_sites = num_x_sites*num_y_sites*num_z_sites
print 'There are ', total_sites, ' open molecular sites (' +str(num_x_sites) + '*' + str(num_y_sites) + '*' + str(num_z_sites) + ')'
logFile.write('There are '+ str(total_sites) +' open molecular sites\n')
print 'The spacing between each site is ', site_spacing ,' angstrom'
logFile.write('The spacing between each site is ' +str(site_spacing) +' angstrom\n')

site_list = numpy.arange(total_sites)
#numpy.random.shuffle(site_list)

a1 = numpy.array([1.0,0.0,0.0])
a2 = numpy.array([0.0,1.0,0.0])
a3 = numpy.array([0.0,0.0,1.0])

<<<<<<< HEAD
print 'Lattice constants: '
lx = a1*site_spacing*num_x_sites
print lx
ly = a2*site_spacing*num_y_sites
print ly
lz = a3*site_spacing*num_z_sites
print lz

logFile.write('Lattice constants: \n')
logFile.write(str(a1*site_spacing*num_x_sites) + '\n')
logFile.write(str(a2*site_spacing*num_y_sites) + '\n')
logFile.write(str(a3*site_spacing*num_z_sites) + '\n')

site = []
for ix in range(num_x_sites):
  for iy in range(num_y_sites):
    for iz in range(num_z_sites):
      site_coordinates = ix*a1*site_spacing + iy*a2*site_spacing + iz*a3*site_spacing
      site.append(site_coordinates)

electron_count = {'H':1,'C':4,'O':6,'N':5, 'S':6}
mass_count = {'H':1,'C':12,'O':15.9994,'N':14.0067, 'S':32.065}

#species_list =  [['water', 3], \
#                 ['carbon_monoxide', 3], \
#                 ['carbon_dioxide', 3], \
#                 ['methanol', 3], \
#                 ['formaldehyde', 3], \
#                 ['ammonia', 3], \
#                 ['HCN', 3]]

logFile.write('This is what I read in from species.in: \n')
species_list = []
inputFile = open(filedir+'/species.in', 'r')
for line in inputFile.readlines():
    species_list.append([line.split()[0],int(line.split()[1])])
    logFile.write(str(species_list[-1]) + '\n')
inputFile.close()



molecule_counter = 0

for array_element in species_list:
    molecule_counter += array_element[1]

if (molecule_counter > total_sites):
    print 'Warning, total number of molecules (' + str(molecule_counter) + ') exeeds number of sites (' + str(total_sites) + '). \
Increase the number of sites or decrease the number of molecules.'
    sys.exit()

species = []

for array_element in species_list:

    molecule = []
    inputFile = open(filedir+'/species/'+str(array_element[0])+'.xyz','r')
    inputFile.readline()
    inputFile.readline()

    for line in inputFile.readlines():
        element = line.split()[0]
        x,y,z = float(line.split()[1]),float(line.split()[2]), float(line.split()[3])
        molecule.append([element,[x,y,z]])
    species.append(molecule)
    inputFile.close()

xyzFile = []
i = 0
atom_counter = 0
electron_counter = 0
mass_counter = 0
molecule_counter = 0
for array_element in species_list:
    chemical_name = array_element[0]
    concentration = array_element[1]

    for j in range(concentration):
        molecule = species[i]
        for line in molecule:
            element_name = line[0][0]
            electron_counter += electron_count[element_name]
            mass_counter += mass_count[element_name]
            x = line[1][0] + site[site_list[molecule_counter]][0]
            y = line[1][1] + site[site_list[molecule_counter]][1]
            z = line[1][2] + site[site_list[molecule_counter]][2]
            xyzFile.append([element_name, x, y, z])
            atom_counter +=1
        molecule_counter += 1
    i+=1

print 'I have filled ', molecule_counter, ' molecular sites'
logFile.write('I have filled ' + str(molecule_counter) + ' molecular sites \n')

if (molecule_counter < total_sites and filler == True):
  fill_counter = species_list[0][1]
  print 'Since there were open sites available, I will fill the remaining with ', species_list[0][0]
  logFile.write('Since there were open sites available, I will fill the remaining with ' + str(species_list[0][0]) + '\n')
  while molecule_counter < total_sites:
      molecule = species[0]
      for line in molecule:
          element_name = line[0][0]
          electron_counter += electron_count[element_name]
          x = line[1][0] + site[site_list[molecule_counter]][0]
          y = line[1][1] + site[site_list[molecule_counter]][1]
          z = line[1][2] + site[site_list[molecule_counter]][2]
          xyzFile.append([element_name, x, y, z])
          atom_counter +=1
      molecule_counter += 1
      fill_counter += 1
  print 'There are now ', fill_counter, species_list[0][0], ' molecules'
  logFile.write('There are now ' +str(fill_counter) + ' ' +str(species_list[0][0]) + ' molecules\n')


print 'The total number of atoms is: ', atom_counter
logFile.write('The total number of atoms is: ' +str(atom_counter) +'\n')
print 'The total number of electrons is: ', electron_counter
logFile.write('The total number of electrons is: ' +str(electron_counter) +'\n')

print 'The total mass of the cell is: ', mass_counter, ' amu'
# mass in grams is mass_counter*1.66053886e-24 grams

volume = numpy.abs(numpy.dot(lx,numpy.cross(ly,lz)))
density = (mass_counter*1.66053886e-24)/(volume*1e-24)
print 'This corresponds to a density of: ', density
print 'To get 1g/cc, mult all lattice vectors by: ', density**(1./3.)

filename = filedir+'/mixture.xyz'
=======
sc =      numpy.array([[0.0,0.0,0.0]])

basis_atoms = sc 

bravis_lattice = []

for i in range(num_x_trans):
     for j in range(num_y_trans):
          for k in range(num_z_trans):
               for l in range(len(basis_atoms)):
                    bravis_lattice.append(i*a1 + j*a2 + k*a3 + basis_atoms[l])

filename = 'xred.dat'
>>>>>>> 6338efc2b07ed86620d7cfcebe6ba54ca69a13aa

outputFile = open(filename,'w')
outputFile.write(str(atom_counter)+'\n')
outputFile.write('\n')

for quad in xyzFile:
    outputFile.write(str(quad[0])+' '+str(quad[1]) + '   ' + str(quad[2]) + '   ' + str(quad[3]) + '\n')
             
outputFile.close()
logFile.close()
os.system('open ' + filedir+'/mixture.xyz')


filename = filedir+'/density.xyz'

outputFile = open(filename,'w')
outputFile.write(str(atom_counter)+'\n')
outputFile.write('\n')

for quad in xyzFile:
    outputFile.write(str(quad[0])+' '+str(quad[1]*density**(1./3.)) + '   ' + str(quad[2]*density**(1./3.)) + '   ' + str(quad[3]*density**(1./3.)) + '\n')
             
outputFile.close()
logFile.close()
#os.system('open ' + filedir+'/mixture.xyz')

