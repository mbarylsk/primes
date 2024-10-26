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
import calculations
import numpy as np

#############################################################
# Syntax
#############################################################

# ./script <min_num> <max_num> <option_candidate> <option_delta>

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
max_num = 10000
if len(sys.argv) > 2:
    max_num = int(sys.argv[2])

# Checkpoint value when partial results are drawn/displayed
# should be greater than zero
checkpoint_value =  int(max_num/1000)

# option for formula calculating first candidate
option_candidate = 3
if len(sys.argv) > 3:
    option_candidate = int(sys.argv[3])
option_delta = 3
if len(sys.argv) > 4:
    option_delta = int(sys.argv[4])

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
file_output_fig1 = directory + "/f_values_v1_v2" + file_output_extension
file_output_fig2 = directory + "/f_values_v1_v2_perc" + file_output_extension

#############################################################
# Business logic
#############################################################

list_nums = []
list_values = [[],[]]
total_v1_greater_than_v2 = 0
total_v1_non_greater_than_v1 = 0
total_v1_smaller_than_one = 0
list_perc = [[],[],[]]

#############################################################
# Presentation
#############################################################

def write_results_to_figures():

    fig = plt.figure(1)
    plt.clf()
    plt.plot(list_nums, list_values[0], 'b.', ms=1)
    plt.plot(list_nums, list_values[1], 'r.', ms=1)
    plt.savefig(file_output_fig1)
    plt.close(fig)

    fig = plt.figure(2)
    plt.clf()
    plt.plot(list_nums, list_perc[0], 'b-', ms=1)
    plt.plot(list_nums, list_perc[1], 'r-', ms=1)
    plt.plot(list_nums, list_perc[2], 'g-', ms=1)
    plt.savefig(file_output_fig2)
    plt.close(fig)

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

dt_start = datetime.now()
dt_current_previous = dt_start

prime_greatest = 0
avg = 0
for m in range (min_num, max_num, 1):

    list_nums.append (m)

    p1 = p.get_ith_prime (m)
    p2 = p.get_ith_prime (m+1)
    p3 = p.get_ith_prime (m+2)
    p4 = p.get_ith_prime (m+3)

    v1 = (p1+p4)/(p2+p3)
    v2 = (p1*p4)/(p2*p3)
    if v1 <= v2:
        #print ("v1 <= v2:", p1, p2, p3, p4, v1, v2)
        total_v1_non_greater_than_v1 += 1
    else:
        total_v1_greater_than_v2 += 1
    if v1 < 1:
        total_v1_smaller_than_one += 1
    list_values[0].append (v1)
    list_values[1].append (v2)
    list_perc[0].append (total_v1_greater_than_v2/m*100)
    list_perc[1].append (total_v1_non_greater_than_v1/m*100)
    list_perc[2].append (total_v1_smaller_than_one/m*100)

    if verbose_figures:
        write_results_to_figures ()
    
dt_end = datetime.now()

# final results
if verbose_figures:
    write_results_to_figures ()

dt_diff = dt_end - dt_start
print ("Total calculations lasted:", dt_diff)
#print_stats ()
