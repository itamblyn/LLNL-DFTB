#! /usr/bin/env python

import sys, os
import numpy


#lx = 0.2665010134E+02
#ly = lx/2.
#lz = lx/2.

lx = 19.3018520868
ly = 20.0590730967
lz = 18.9118754813

mass_counter = 360
print 'The total mass of the cell is: ', mass_counter, ' amu'

volume = lx*ly*lz
density = (mass_counter*1.66053886e-24)/(volume*1e-24)
print 'This corresponds to a density of: ', density
print 'To get 1g/cc, mult all lattice vectors by: ', density**(1./3.)

print 'That means '
print 'lx = ', lx*density**(1./3.)
print 'ly = ', ly*density**(1./3.)
print 'lz = ', lz*density**(1./3.)