#
# Copyright (c) 2019 - 2020, Marcin Barylski
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
import numpy as np
from scipy.optimize import curve_fit
import scipy

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
max_num = 5

# Checkpoint value when partial results are drawn/displayed
# should be greater than zero
checkpoint_value = 1000

verbose = False

file_input_primes = '..\\primes\\t_prime_numbers.txt'
file_input_nonprimes = '..\\primes\\t_nonprime_numbers.txt'

#############################################################
# Settings - output directory and files
#############################################################

directory = "results/" + str(max_num)
if not os.path.exists(directory):
    os.makedirs(directory)
file_output_extension = ".png"

#############################################################
# Business logic
#############################################################

def find_unique_prime_in_sum (p, current_sum, list_of_primes_used):

    print ("d1", current_sum, list_of_primes_used)
    is_prime_lower_than_current_sum = True
    k = 1
    while (is_prime_lower_than_current_sum):
        q = p.get_ith_prime (k)
        print ("d2", q, k, is_prime_lower_than_current_sum)
        if (2 <= current_sum - q) and q not in list_of_primes_used:
            print ("d3", current_sum - q)
            new_list_of_primes_used = list_of_primes_used.append (q)
            find_unique_prime_in_sum (p, current_sum - q, new_list_of_primes_used)
        elif (2 <= current_sum - q):
            print ("d4", current_sum - q)
            k += 1
        else:
            print ("d4", q)
            list_of_primes_used.append (q)
            is_prime_lower_than_current_sum = False

    print (current_sum, list_of_primes_used)

    if current_sum == 0:
        return True
    else:
        return False

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

dt_start = datetime.now()
dt_current_previous = dt_start

for k in range (min_num, max_num, 1):

    q = p.get_ith_prime (k)
    print ("--- start for", k)
    p.find_unique_prime_in_sum (q)
    p.list_of_primes_used = []
    print ("--- end for", k)

dt_end = datetime.now()
dt_diff = dt_end - dt_start
print ("Total calculations lasted:", dt_diff)
