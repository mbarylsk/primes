#
# Copyright (c) 2024, Marcin Barylski
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

import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
sys.path.insert(0, '..\\primes\\')
import primes
sys.path.insert(0, '..\\goldbach-partition\\')
import dataprocessing
import calculations
import numpy as np

#############################################################
# Syntax
#############################################################

#   TBD

#############################################################
# Settings - configuration
#############################################################

# Caching previous primality results
#   o True  - auxilary sets of primes and composite numbers will grow
#             it will speed up further primality tests but more RAM will
#             be occupied
#   o False - do not cache new primality test results
caching_primality_results = False
min_num = 1
if len(sys.argv) > 1:
    min_num = int(sys.argv[1])
max_num = 1000
if len(sys.argv) > 2:
    max_num = int(sys.argv[2])

# Checkpoint value when partial results are drawn/displayed
# should be greater than zero
checkpoint_value =  int(max_num/1000)

search_sequence_lenght = 7
search_sequence_gap = 1

verbose = False
verbose_figures = True

file_input_primes = '..\\primes\\t_prime_numbers.txt'
file_input_nonprimes = '..\\primes\\t_nonprime_numbers.txt'

#############################################################
# Settings - output directory and files
#############################################################

directory = "results/" + str(max_num)
if not os.path.exists(directory):
    os.makedirs(directory)
file_output_extension = ".png"
file_output_fig1 = directory + "/f_mnplus1_1" + file_output_extension
file_output_fig2 = directory + "/f_mnplus1_1" + file_output_extension

#############################################################
# Business logic
#############################################################

matrix_of_results = np.zeros ((max_num, max_num))
result_prime_nmpl1 = 1
result_prime_nmmi1 = -1
result_prime_nmplmi1 = 2

def detect_lines (length, gap):

    # mn+1 of given length
    for n in range (min_num, max_num, gap):
        for m in range (min_num, max_num, gap):
            multmnpl1 = 1
            for d in range (0, length, 1):
                if m+d < max_num and n+d < max_num:
                    #print ("Mult:", n+d, m+d, matrix_of_results [n+d][m+d])
                    if matrix_of_results [n+d][m+d] < 0:
                        multmnpl1 = 0
                    multmnpl1 *=  matrix_of_results [n+d][m+d]

            #print ("Results:", n, m, mult)
            if multmnpl1 > 0:
                print ("Found mn+1", " of lenght ", length, " and gap", gap, ": n=", n, "m=", m)
                n1 = n
                m1 = m
                for i in range (0, length, 1):
                    print (n1*m1+1)
                    n1 += gap
                    m1 += gap


#############################################################
# Presentation
#############################################################


#############################################################
# Main - Phase 1
# Preload files & restore previous calculations
#############################################################

print ("---------------------------------------------------")
print ("Initialize objects...")
p = primes.Primes(caching_primality_results)
dp = dataprocessing.DataProcessing()
c = calculations.Calculations()
print ("DONE")
print ("Loading helper sets...")
p.init_set(file_input_primes, True)
p.init_set(file_input_nonprimes, False)
print ("DONE")
print ("Sorting primes...")
p.sort_primes_set()
print ("DONE")
print ("---------------------------------------------------")

#############################################################
# Main - Phase 2
# New calculations
#############################################################


fig, ax = plt.subplots()
for m in range (min_num, max_num, 1):

    for n in range (min_num, m, 1):
        l1 = m*n + 1
        l2 = m*n - 1
        if p.is_prime (l1) and p.is_prime (l2):
            ax.scatter(m, n, c='green')
            matrix_of_results [n][m] = result_prime_nmplmi1
        elif p.is_prime (l1) and not p.is_prime (l2):
            ax.scatter(m, n, c='blue')
            matrix_of_results [n][m] = result_prime_nmpl1
        elif not p.is_prime (l1) and p.is_prime (l2):
            ax.scatter(m, n, c='yellow')
            matrix_of_results [n][m] = result_prime_nmmi1
        else:
            ax.scatter(m, n, c='red')

    plt.savefig(file_output_fig1)
    #print (matrix_of_results)

    detect_lines (search_sequence_lenght, search_sequence_gap)


plt.show()
plt.savefig(file_output_fig1)
detect_lines (search_sequence_lenght, search_sequence_gap)
