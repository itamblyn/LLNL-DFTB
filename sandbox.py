#!/usr/bin/python

import sys

diagonal_n = 3 

import numpy as np
import scipy
import scipy.linalg
import random
from scipy import linalg as LA


e_mol = 0. 
em1 = 3.
em2 = 100.
V = float(sys.argv[1])
sigma_mol = 3.
sigma_metal1 = 0.
sigma_metal2 = 0.


H0 =   np.array([[ e_mol, V,   V],
                 [   V,  em1,  0.],
                 [   V,  0., em2]])


eigenvalues, eigenvectors = LA.eig(H0)


diagonalized_DFT = np.diag(eigenvalues)

v1, v2, v3 = eigenvectors[0], eigenvectors[1], eigenvectors[2]

molecular_contrib = sigma_mol*np.array([[ v1[0]*v1[0], v1[0]*v2[0], v1[0]*v3[0] ],
                                        [ v2[0]*v1[0], v2[0]*v2[0], v2[0]*v3[0] ],
                                        [ v3[0]*v1[0], v3[0]*v2[0], v3[0]*v3[0] ] ])

metal1_contrib = sigma_metal1*np.array([[ v1[1]*v1[1], v1[1]*v2[1], v1[1]*v3[1] ],
                                        [ v2[1]*v1[1], v2[1]*v2[1], v2[1]*v3[1] ],
                                        [ v3[1]*v1[1], v3[1]*v2[1], v3[1]*v3[1] ] ])

metal2_contrib = sigma_metal2*np.array([[ v1[2]*v1[2], v1[2]*v2[2], v1[2]*v3[2] ],
                                        [ v2[2]*v1[2], v2[2]*v2[2], v2[2]*v3[2] ],
                                        [ v3[2]*v1[2], v3[2]*v2[2], v3[2]*v3[2] ] ])


sigma_matrix_with_offdiagonals = molecular_contrib + metal1_contrib + metal2_contrib 

H_GW_full = diagonalized_DFT + sigma_matrix_with_offdiagonals

H_GW_nfull = diagonalized_DFT + np.diag([sigma_matrix_with_offdiagonals[0][0], sigma_matrix_with_offdiagonals[1][1],sigma_matrix_with_offdiagonals[2][2]])

diagonalized_GW_full = np.diag(LA.eigvals(H_GW_full))
diagonalized_GW_nfull = np.diag(LA.eigvals(H_GW_nfull))

print 'original matrix: '
print H0
print
print 'diagonalized DFT matrix'
print diagonalized_DFT 
print
print 'self energies (molecule, metal1, metal2)'
print sigma_mol, sigma_metal1, sigma_metal2
print
print 'diagonalized matrix, with corrections just added along the diagonal'
diagonalized_DFT_direct = np.zeros((3,3),dtype=float)
diagonalized_DFT_direct[0][0] = diagonalized_DFT[0][0] + sigma_mol
diagonalized_DFT_direct[1][1] = diagonalized_DFT[1][1] + sigma_metal1
diagonalized_DFT_direct[2][2] = diagonalized_DFT[2][2] + sigma_metal2
print diagonalized_DFT_direct
print
print 'What happens if I simply add the corrections to the DFT Hamiltonian, prior to diagonalization, THEN diagonalize???'
H0[0][0] += sigma_mol
H0[1][1] += sigma_metal1
H0[2][2] += sigma_metal2
dft_plus_sigma = np.diag(LA.eigvals(H0))
print dft_plus_sigma
print
#print np.sort([dft_plus_sigma[0][0], dft_plus_sigma[1][1],dft_plus_sigma[2][2]])

print 'Note that it matters whether your add the correction before or after diagonalization.\n'
print 'The second approach is correct.\n'
print 'So this raises the question, How can I predict what the result of a \"DFT+U then diagonalize\" calculation will be,'
print 'will be without doing that process?'
print
print 'The answer is I take the value of the correction in the gas phase,'
print 'and multiply by the projection of the mixed state onto the gas phase one.\n'

print 'The projection onto the gas phase is ' + str(round(v1[0]*v1[0], 3))
print '*** debug ' + str(round(v1[0]*v1[0], 3)) + ' ' + str(round(v2[0]*v2[0], 3)) + ' ' +  str(round(v3[0]*v3[0], 3)) + ' <- 0th of v1, v2, v3'
print '*** debug ' + str(round(v1[1]*v1[1], 3)) + ' ' + str(round(v2[1]*v2[1], 3)) + ' ' +  str(round(v3[1]*v3[1], 3)) + ' <- 1st of v1, v2, v3'
print '*** debug ' + str(round(v1[2]*v1[2], 3)) + ' ' + str(round(v2[2]*v2[2], 3)) + ' ' +  str(round(v3[2]*v3[2], 3)) + ' <- 2st of v1, v2, v3'
print '*** ' + str(round(eigenvalues[0], 3)) + ' ' + str(round(eigenvalues[1], 3)) + ' ' + str(round(eigenvalues[2], 3)) 
print 'Numerically, this works out to a shift of ' + str(round(v1[0]*v1[0]*sigma_mol,2))
print
print 'If I straight up add this to my original DFT eigenvalue, I get\n'
print str(round(diagonalized_DFT[0][0] + v1[0]*v1[0]*sigma_mol,2)) + ' ' + 'compared to ' + str(round(dft_plus_sigma[0][0],3)) 
print

if True:
    print 'If I want to get an even better result, I can construct a full matrix, based on projections,'
    print 'which can be directly added to the premixed case'

    print sigma_matrix_with_offdiagonals
    print
    print 'diagonalized_DFT + projection_matrix'
    print H_GW_full
    print
    print 'Eigenvalues of this matrix'
#print diagonalized_GW_full
    print np.sort([diagonalized_GW_full[0][0], diagonalized_GW_full[1][1],diagonalized_GW_full[2][2]     ])


#    print 'What about if I didn\'t include offdiagonal elements in my expression for sigma?'

#print diagonalized_GW_nfull
#    print np.sort([diagonalized_GW_nfull[0][0], diagonalized_GW_nfull[1][1],diagonalized_GW_nfull[2][2]])
