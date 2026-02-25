#
# Copyright (c) 2025 - 2026, Marcin Barylski
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

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import os
import sys
import random
# path to libraries
sys.path.insert(1, "..\\..")
import primes
import calculations

#############################################################
# Settings - configuration
#############################################################

# Minimal and maximum number - range of iterations
min_num = 0
max_num = 100

# Checkpoint value when partial results are drawn/displayed
# should be greater than zero
checkpoint_value = 100000

# threshold to be vocal about big enough delta
delta_threshold = 185

# Caching previous primality results
#   o True  - auxilary sets of primes and composite numbers will grow
#             it will speed up further primality tests but more RAM will
#             be occupied
#   o False - do not cache new primality test results
caching_primality_results = False

# Helper files
#   o file_input_primes - contains prime numbers
#   o file_input_nonprimes - contains composite numbers
file_input_primes = '..\\..\\t_prime_numbers.txt'
file_input_nonprimes = '..\\..\\t_nonprime_numbers.txt'

#############################################################
# Settings - output directory and files
#############################################################

directory = "results/" + str(max_num)
if not os.path.exists(directory):
    os.makedirs(directory)
file_output_extension = ".png"
file_output_fig1 = directory + "/f_triangle_delta_to_various_numbers" + file_output_extension
file_output_fig2 = directory + "/f_triangle_delta_frequency_to_various_numbers" + file_output_extension

#############################################################
# Results of calculations
#############################################################
list_delta_prime_to_triangle = []
list_delta_prime_to_random = []
list_delta_prime_to_n6m1 = []
list_id = []

dict_delta_t_count = {}
dict_delta_r_count = {}
dict_delta_n6m1_count = {}

list_delta_t_keys = []
list_delta_t_values = []
list_delta_r_keys = []
list_delta_r_values = []
list_delta_n6m1_keys = []
list_delta_n6m1_values = []

#############################################################
# Presentation
#############################################################

def update_delta_count (d, delta):
    d[delta] = d.get(delta, 0) + 1

def prepare_data (c):
    global dict_delta_t_count, list_delta_t_keys, list_delta_t_values, dict_delta_r_count, list_delta_r_keys, list_delta_r_values, dict_delta_n6m1_count, list_delta_n6m1_keys, list_delta_n6m1_values
    (list_delta_t_keys, list_delta_t_values) = c.trans_dict_int_to_lists (dict_delta_t_count)
    (list_delta_r_keys, list_delta_r_values) = c.trans_dict_int_to_lists (dict_delta_r_count)
    (list_delta_n6m1_keys, list_delta_n6m1_values) = c.trans_dict_int_to_lists (dict_delta_n6m1_count)

def write_results_to_figures ():
    global list_id, list_delta_prime_to_triangle, list_delta_prime_to_random, list_delta_prime_to_n6m3

    red_patch = mpatches.Patch(color='red', label='triangular')
    blue_patch = mpatches.Patch(color='blue', label='random')
    green_patch = mpatches.Patch(color='green', label='6n-1')
    
    fig = plt.figure(1)
    plt.clf()
    plt.plot(list_id, list_delta_prime_to_triangle, 'r', ms=1)
    plt.plot(list_id, list_delta_prime_to_random, 'b', ms=1)
    plt.plot(list_id, list_delta_prime_to_n6m1, 'g', ms=1)
    fig.suptitle("Delta prime to various numbers", fontsize=10)
    plt.legend(handles=[red_patch, blue_patch, green_patch], loc='upper right', bbox_to_anchor=(1, 1), fontsize=6)
    plt.savefig(file_output_fig1)
    plt.close(fig)

    fig = plt.figure(2)
    plt.clf()
    plt.plot(list_delta_n6m1_keys, list_delta_n6m1_values, 'g', ms=1)
    plt.plot(list_delta_t_keys, list_delta_t_values, 'r', ms=1)
    plt.plot(list_delta_r_keys, list_delta_r_values, 'b', ms=1)
    fig.suptitle("Delta frequency", fontsize=10)
    plt.legend(handles=[red_patch, blue_patch, green_patch], loc='upper right', bbox_to_anchor=(1, 1), fontsize=6)
    plt.savefig(file_output_fig2)
    plt.close(fig)

def create_results (c):
    global list_delta_prime_to_triangle, list_delta_prime_to_random, list_delta_prime_to_n6m1
    avg_t = c.get_avg_from_list(list_delta_prime_to_triangle) 
    avg_n = c.get_avg_from_list(list_delta_prime_to_random)
    avg_n6m1 = c.get_avg_from_list(list_delta_prime_to_n6m1)

    prepare_data (c)
    write_results_to_figures ()

    print ("Average prime to triangular:", avg_t)
    print ("Average prime to random:", avg_n)
    print ("Average prime to 6n-1:", avg_n6m1)

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
id = 0
for k in range (min_num, max_num):

    t = c.get_triangle_number (k)
    n = random.randint(min_num, max_num)
    n6m1 = id*6-1

    delta_t = p.get_abs_delta_to_closest_prime (t)
    delta_n = p.get_abs_delta_to_closest_prime (n)
    delta_n6m1 = p.get_abs_delta_to_closest_prime (n6m1)
  
    list_delta_prime_to_triangle.append (delta_t)
    list_delta_prime_to_random.append (delta_n)
    list_delta_prime_to_n6m1.append (delta_n6m1)
    update_delta_count (dict_delta_t_count, delta_t)
    update_delta_count (dict_delta_r_count, delta_n)
    update_delta_count (dict_delta_n6m1_count, delta_n6m1)
    list_id.append (id)
    id += 1

    if id % checkpoint_value == 0:
        print ("--> Checkpoint at: ", id)
        create_results (c)

    if delta_t > delta_threshold:
        print (t, delta_t)

create_results (c)