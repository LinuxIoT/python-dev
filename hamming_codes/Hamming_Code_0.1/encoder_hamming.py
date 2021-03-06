# -*- coding: utf-8 -*-

"""Hamming Codes Implementation: https://programmingpraxis.com/2012/05/22/hamming-codes/
"""

__author__ = "Weqaar Janjua & Ahmer Malik"
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "0.1"


import numpy as np
import math
import print_header


p = print_header._header(__file__,__author__,__copyright__,__version__)
p._print()

data_bits = 2
parity_bits = int(math.sqrt(data_bits))+2

# Hamming Rule:  d + p + 1 ≤ 2^p

H1 = data_bits + parity_bits +1
H2 = 2**parity_bits

while  H1 > H2:
    H1 = data_bits + parity_bits +1
    H2 = 2**parity_bits
    parity_bits +=1

parity_bits -=1
print ("Data Bits = %d"% data_bits)
print ("Parity Bits = %d"% parity_bits)

# Hamming Code is described by (c,d)=(Hamming Word , Data)

c = data_bits + parity_bits

#Now generate the matrices, G Generator Matrix & H Syndrome matrix
#G(I:A) & H(A^T:I)
#Generator Matrix is denoted by [I:A]

I1 = np.eye(data_bits)        # Create a dxd identity matrix
I2 = np.eye(parity_bits)        # Create a pxp identity matrix


Comb =[bin(x)[2:].rjust(parity_bits, '0') for x in range(2**parity_bits)]

A = np.zeros((data_bits,parity_bits))
for i in xrange(0,data_bits):
    for j in xrange(0,parity_bits):
        A[i][j] = Comb[i][j]
        
print A
A_Trans = zip(*A)

# Concatenate both the G(I,A), axis=1 becuase put cols of first matrix then second

G = np.concatenate((I1,A), axis=1)
print "G ="
print G

H = np.concatenate((A_Trans,I2), axis=1)
print "H ="
print H



Data = np.array([1, 0])
print Data
Encode = np.dot(Data,G)
Decode = np.dot(H,Encode) % 2

print "Decode = "  
print Decode
