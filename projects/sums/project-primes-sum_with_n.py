#
# Copyright (c) 2023, Marcin Barylski
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
import numpy as np
import primes
import calculations
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#############################################################
# Settings - configuration
#############################################################

# Minimal and maximum number - range of iterations
min_num = 0
max_num = 200000

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

#############################################################
# Settings - output directory and files
#############################################################

directory = "results/" + str(max_num)
if not os.path.exists(directory):
    os.makedirs(directory)
file_output_extension = ".png"
file_output_fig1 = directory + "/f_sum_with_n" + file_output_extension

#############################################################
# Results of calculations
#############################################################

k = 0

list_values = [[],[],[]]
list_arguments = []

#############################################################
# Business logic
#############################################################

#############################################################
# Presentation
#############################################################

def print_graphs ():
    global list_values, list_arguments
    
    fig = plt.figure(1)
    plt.clf()
    b_patch = mpatches.Patch(color='blue', label='(2+pn)/n')
    r_patch = mpatches.Patch(color='red', label='(3+pn)/n')
    g_patch = mpatches.Patch(color='green', label='ln(2n)')
    list_of_handles = []
    list_of_handles.append(b_patch)
    list_of_handles.append(r_patch)
    list_of_handles.append(g_patch)
    plt.plot(list_arguments, list_values[0], 'b.', ms=1)
    plt.plot(list_arguments, list_values[1], 'r.', ms=1)
    plt.plot(list_arguments, list_values[2], 'g.', ms=1)
    plt.legend(handles=list_of_handles, loc='upper right', bbox_to_anchor=(0.4, 0.9), fontsize=6)
    fig.suptitle("Sum", fontsize=10)
    plt.savefig(file_output_fig1)
    plt.close(fig)
    
#############################################################
# Main
#############################################################

print ("Initialize objects...")
p = primes.Primes(caching_primality_results)
c = calculations.Calculations()
print ("DONE")
print ("Loading helper sets...")
p.init_set(file_input_primes, True)
p.init_set(file_input_nonprimes, False)
print ("DONE")
print ("Sorting primes...")
p.sort_primes_set()
print ("DONE")

# new calculations
i = 2
for k in range (min_num, max_num):

    prime_next = p.get_ith_prime (k+1)
    prime_next2 = p.get_ith_prime (k+2)
    csum2 = (2+prime_next)/i
    csum3 = (3+prime_next2)/i

    v = np.log(2*i)
    
    list_arguments.append (i)
    list_values[0].append (csum2)
    list_values[1].append (csum3)
    list_values[2].append (v)
    
    print (csum2, csum3, v)

    print_graphs ()

    i += 1
    	
# final results

print_graphs ()
