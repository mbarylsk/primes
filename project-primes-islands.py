#
# Copyright (c) 2022-2024, Marcin Barylski
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
# OF SUCH DAMAGE.
#

import os
import sys
import primes
import calculations
import graphs
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csc_matrix

#############################################################
# Settings - configuration
#############################################################

# Minimal and maximum number - range of iterations
min_num = 0
max_num = 100000
min_neighbours = 3

# Checkpoint value when partial results are drawn/displayed
# should be greater than zero
checkpoint_value = 10000

# Caching previous primality results
#   o True  - auxilary sets of primes and composite numbers will grow
#             it will speed up further primality tests but more RAM will
#             be occupied
#   o False - do not cache new primality test results
caching_primality_results = False

# Helper files
#   o file_input_primes - contains prime numbers
#   o file_input_nonprimes - contains composite numbers
file_input_primes = 't_prime_numbers.txt'
file_input_nonprimes = 't_nonprime_numbers.txt'

# Graphs
#   o True - writes the graphs (visual form) to the file, separate switch to show on screen
#   o False - be quiet
show_graphs = True
show_graphs_screen = False

#############################################################
# Settings - output directory and files
#############################################################

directory = "results/" + str(max_num)
if not os.path.exists(directory):
    os.makedirs(directory)
file_output_extension = ".png"

#############################################################
# Results of calculations
#############################################################

k = 0
cols = 10000
rows = int(cols/2)
arr = np.zeros((rows, cols))

#############################################################
# Business logic
#############################################################


def calculate_base (prime):
    # examination of islands for pxq+1
    return prime+1

#############################################################
# Presentation
#############################################################

    
#############################################################
# Main
#############################################################

print ("Initialize objects...")
p = primes.Primes(caching_primality_results)
c = calculations.Calculations()
g = graphs.Graphs()
print ("DONE")
print ("Loading helper sets...")
p.init_set(file_input_primes, True)
p.init_set(file_input_nonprimes, False)
print ("DONE")
print ("Sorting primes...")
p.sort_primes_set()
print ("DONE")

# new calculations
prime = p.get_ith_prime (0)
for k in range (min_num, max_num):


    prime = p.get_ith_prime (k)
    
    candidate = calculate_base (prime)
    pairs = []
    pairs = p.factorize_to_pairs (candidate)
    #print("All possible pairs : " + str(prime), str(candidate), str(pairs))
    
    for pair in pairs:
        (x, y) = pair
        if y < cols and x < rows:
            arr[x][y]=1

# final results

arr2 = c.get_neighbours (arr)

plt.matshow(arr2, origin='lower')
plt.show()

for i in range (0, rows):
    for j in range (0, cols):

        if arr2[i][j] >= min_neighbours:
            print (i, j)
            title = "Dimensions:" + str(i) + ",", str(j)
            delta = 5
            subarr2 = c.get_submatrix (arr2, i-delta, i+delta, j-delta, j+delta)
            
            plt.matshow(subarr2, origin='lower')
            plt.title (title)
            plt.show()
            
