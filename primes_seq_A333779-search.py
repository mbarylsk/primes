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
max_num = 1000
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
file_sufix = str(option_candidate) + "-" + str(option_delta)
file_output_fig1 = directory + "/f_A333779_whenprimefound_delta_opt" + file_sufix + file_output_extension
file_output_fig2 = directory + "/f_A333779_whenprimefound_steps_opt" + file_sufix + file_output_extension

#############################################################
# Business logic
#############################################################

list_nums = []
list_when_prime_found = []
list_when_prime_found_deltaplus = []
list_when_prime_found_deltaminus = []
list_when_prime_found_avg = []
list_when_prime_found_avg_deltaplus = []
list_when_prime_found_avg_deltaminus = []
list_when_prime_found_steps = []
list_when_prime_found_steps_avg = []
list_when_prime_found_steps_avg_deltaplus = []
list_when_prime_found_steps_avg_deltaminus = []
list_primes = []
avg_delta = 0
avg_deltaplus = 0
avg_deltaminus = 0
delta = 0
avg_steps = 0
exact_match = 0

def calculate_candidate (m, option):
    if option == 1:
        a = 9.81764596
        b = 1.09031708
        result = (int(a * (m ** b)) + m)
    elif option == 2:
        result = 10 * m
    elif option == 3:
        a = 9.1
        b = 1.1
        result = (int(a * (m ** b)) + m + 10)
    return result

def calculate_delta (c, d, pk, option):
    delta = 0
    if option == 1:
        delta = d + 1
    elif option == 2:
        if d == 0:
            delta = 1
        else:
            delta = (d + np.sign(d))*(-1)
    elif option == 3:
        ld = c.get_last_dec_digit(pk + d)
        if ld == 1:
            delta = d + 2 # 3-1=2
        elif ld == 3:
            delta = d + 4 # 7-3=4
        elif ld == 7:
            delta =  d + 2 # 9-7=2 
        elif ld == 9:
            delta = d + 2 # 11-9=2
        elif ld == 5:
            delta = d + 2 # 7-5=2
        elif ld == 4:
            delta = d + 3 # 7-4=3
        else:
            delta = d + 1 # all other cases: ld = 2, 6, 8, 0

    return delta

def update_metrics (dp, pk, delta, steps):
    global prime_greatest, list_when_prime_found, list_when_prime_found_avg, avg_delta, list_when_prime_found_steps, list_when_prime_found_steps_avg, avg_steps, exact_match, avg_deltaplus, avg_deltaminus

    list_primes.append (pk)
    
    if pk > prime_greatest:
        prime_greatest = pk
        
    list_when_prime_found.append (delta)
    if delta > 0:
        list_when_prime_found_deltaplus.append (delta)
    elif delta < 0:
        list_when_prime_found_deltaminus.append (delta)
    else:
        exact_match += 1
        
    avg_delta = dp.get_avg_value_from_list(list_when_prime_found)
    list_when_prime_found_avg.append (avg_delta)

    avg_deltaplus = dp.get_avg_value_from_list(list_when_prime_found_deltaplus)
    avg_deltaminus = dp.get_avg_value_from_list(list_when_prime_found_deltaminus)
    list_when_prime_found_avg_deltaplus.append (avg_deltaplus)
    list_when_prime_found_avg_deltaminus.append (avg_deltaminus)

    list_when_prime_found_steps.append (steps)

    avg_steps = dp.get_avg_value_from_list(list_when_prime_found_steps)
    list_when_prime_found_steps_avg.append (avg_steps)

#############################################################
# Presentation
#############################################################

def write_results_to_figures():

    fig = plt.figure(1)
    plt.clf()
    blue_patch = mpatches.Patch(color='blue', label='value')
    red_patch = mpatches.Patch(color='red', label='avg')
    green_patch = mpatches.Patch(color='green', label='avg +')
    magenta_patch = mpatches.Patch(color='magenta', label='avg -')
    plt.legend(handles=[blue_patch, red_patch, green_patch, magenta_patch], loc='upper left', prop={'size': 6})
    plt.plot(list_nums, list_when_prime_found, 'b.', ms=1)
    plt.plot(list_nums, list_when_prime_found_avg, 'r-', ms=1)
    plt.plot(list_nums, list_when_prime_found_avg_deltaplus, 'g-', ms=1)
    plt.plot(list_nums, list_when_prime_found_avg_deltaminus, 'm-', ms=1)
    plt.savefig(file_output_fig1)
    plt.close(fig)

    fig = plt.figure(2)
    plt.clf()
    blue_patch = mpatches.Patch(color='blue', label='value')
    red_patch = mpatches.Patch(color='red', label='avg')
    plt.legend(handles=[blue_patch, red_patch], loc='upper left', prop={'size': 6})
    plt.plot(list_nums, list_when_prime_found_steps, 'b.', ms=1)
    plt.plot(list_nums, list_when_prime_found_steps_avg, 'r-', ms=1)
    plt.savefig(file_output_fig2)
    plt.close(fig)

def print_stats ():
    global avg_delta, avg_deltaplus, avg_deltaminus, avg_steps, prime_greatest, exact_match
    print (" - delta avg value so far:", avg_delta)
    print (" - delta plus avg value so far:", avg_deltaplus)
    print (" - delta minus avg value so far:", avg_deltaminus)
    print (" - steps avg value so far:", avg_steps)
    print (" - greatest prime so far:", prime_greatest)
    print (" - primes with exact match:", exact_match)
    
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

    found = False
    delta = 0
    steps = 0
    pki = calculate_candidate (m, option_candidate)
    while not found:
        steps += 1
        pk = pki + delta
        if p.is_prime (pk):
            found = True
            update_metrics (dp, pk, delta, steps)
        else:
            delta = calculate_delta (c, delta, pk, option_delta)

    # checkpoint - partial results
    if m % checkpoint_value == 0 and (m - min_num) > 1:

        perc_completed = str(int(m * 100 / max_num))
        print ("Checkpoint", m, "of total", max_num, "(" + perc_completed + "% completed)")
        print_stats ()
   
        # save results collected so far
        if verbose_figures:
            write_results_to_figures ()

dt_end = datetime.now()

if verbose:
    print ("When prime was found?")
    print (list_when_prime_found)
    print ("Primes found")
    print (list_primes)

# final results
if verbose_figures:
    write_results_to_figures ()

dt_diff = dt_end - dt_start
print ("Total calculations lasted:", dt_diff)
print_stats ()
