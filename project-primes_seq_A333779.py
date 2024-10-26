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
max_num = 40000

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
file_output_fig1 = directory + "/f_A333779_terms" + file_output_extension

#############################################################
# Business logic
#############################################################

list_nums = []
list_marked_primes = []
list_left_primes = []
list_A333779_terms = []

def update_metrics (dp, k, a):
    global list_marked_primes, list_A333779_terms, list_A333779_terms_avg

    if k == 0:
        list_marked_primes.append (a)
    else:
        list_marked_primes.append (a-k)
        list_marked_primes.append (a+k)
    
    list_A333779_terms.append (a)

def func_abc(x, a, b, c):
    return a * (x ** b) + c

def func_ab(x, a, b):
    return a * (x ** b)

#############################################################
# Presentation
#############################################################

def write_results_to_figures(use_curve_fit):

    red_patch = mpatches.Patch(color='red', label='fitted curve')
    blue_patch = mpatches.Patch(color='blue', label='term')
    
    fig = plt.figure(1)
    plt.clf()
    plt.plot(list_nums, list_A333779_terms, 'b-', ms=1)

    if use_curve_fit:
        x = np.asarray(list_nums, dtype=np.uint64)
        y = np.asarray(list_A333779_terms, dtype=np.uint64)
        popt, pcov = curve_fit(func_ab, x, y)
        plt.plot(x, func_ab(x, *popt), 'r-')
        print (popt)
    
    plt.savefig(file_output_fig1)
    plt.close(fig)
    
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

    list_nums.append (k)
    found = False
    a = 2
    while not found:
        if a - k > 1 and p.is_prime(a-k) and p.is_prime (a+k) and (a-k) not in list_marked_primes and (a+k) not in list_marked_primes:

            update_metrics (dp, k, a)
            found = True
          
        a += 1

    # checkpoint - partial results
    if k % checkpoint_value == 0 and (k - min_num) > 1:

        perc_completed = str(int(k * 100 / max_num))
        print ("Checkpoint", k, "of total", max_num, "(" + perc_completed + "% completed)")
   
        # save results collected so far
        write_results_to_figures (True)
      
max_marked_prime = max(list_marked_primes)
all_checked = False
i = 1
while not all_checked:
    q = p.get_ith_prime (i)
    if max_marked_prime >= q:
        if q not in list_marked_primes:
            list_left_primes.append (q)
    else:
        all_checked = True
    i += 1

list_marked_primes.sort()

dt_end = datetime.now()

if verbose:
    print ("Terms of A333779")
    print (list_A333779_terms)
    print ("Primes marked")
    print (list_marked_primes)
    print ("Primes left")
    print (list_left_primes)

# final results
write_results_to_figures (True)

dt_diff = dt_end - dt_start
print ("Total calculations lasted:", dt_diff)
