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
file_output_fig1 = directory + "/f_triangle_primes_delta" + file_output_extension
file_output_fig2 = directory + "/f_triangle_primes_delta_plus" + file_output_extension
file_output_fig3 = directory + "/f_triangle_primes_delta_minus" + file_output_extension
file_output_fig4 = directory + "/f_triangle_primes_delta_frequency" + file_output_extension

#############################################################
# Results of calculations
#############################################################
list_triangle_index = []
list_triangle_value = []
list_primes_to_triangle_delta_plus = []
list_primes_to_triangle_delta_minus = []
list_primes_to_triangle_plus = []
list_primes_to_triangle_minus = []
dict_delta_count = {}
list_delta_keys = []
list_delta_values = []

#############################################################
# Presentation
#############################################################

def update_delta_count (delta):
    global dict_delta_count 
    dict_delta_count[delta] = dict_delta_count.get(delta, 0) + 1

def prepare_data (c):
    global dict_delta_count, list_delta_keys, list_delta_values
    (list_delta_keys, list_delta_values) = c.trans_dict_int_to_lists (dict_delta_count)

def print_stats ():
    global dict_delta_count
    print ({k: v for k, v in sorted(dict_delta_count.items(), key=lambda item: item[1])})

def write_results_to_figures ():

    red_patch = mpatches.Patch(color='red', label='delta plus')
    blue_patch = mpatches.Patch(color='blue', label='delta_minus')
    
    fig = plt.figure(1)
    plt.clf()
    plt.plot(list_primes_to_triangle_plus, list_primes_to_triangle_delta_plus, 'r', ms=1)
    plt.plot(list_primes_to_triangle_minus, list_primes_to_triangle_delta_minus, 'b', ms=1)
    fig.suptitle("Delta positive and/or negative", fontsize=10)
    plt.legend(handles=[red_patch, blue_patch], loc='upper right', bbox_to_anchor=(1, 1), fontsize=6)
    plt.savefig(file_output_fig1)
    plt.close(fig)

    fig = plt.figure(2)
    plt.clf()
    plt.plot(list_primes_to_triangle_plus, list_primes_to_triangle_delta_plus, 'r', ms=1)
    fig.suptitle("Delta positive", fontsize=10)
    plt.savefig(file_output_fig2)
    plt.close(fig)

    fig = plt.figure(3)
    plt.clf()
    plt.plot(list_primes_to_triangle_minus, list_primes_to_triangle_delta_minus, 'b', ms=1)
    fig.suptitle("Delta negative", fontsize=10)
    plt.savefig(file_output_fig3)
    plt.close(fig)

    fig = plt.figure(4)
    plt.clf()
    plt.plot(list_delta_keys, list_delta_values, 'b', ms=1)
    fig.suptitle("Delta frequency", fontsize=10)
    plt.savefig(file_output_fig4)
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
triangle_number_index = 0
for k in range (min_num, max_num):

    triangle_number_index += 1
    list_triangle_index.append (triangle_number_index)

    # get proper triangle number
    triangle_number = c.get_triangular_number (triangle_number_index)
    list_triangle_value.append (triangle_number)

    # look for the closest prime
    prime_found = False
    list_of_primes = []
    delta = 0
    delta_plus_found = False
    delta_zero_found = False
    delta_minus_found = False
    while not prime_found:
        if p.is_prime(triangle_number - delta):
            prime_found = True
            list_of_primes.append (triangle_number - delta)
            if delta == 0:
                list_primes_to_triangle_delta_plus.append (delta)
                list_primes_to_triangle_plus.append (triangle_number)
                list_primes_to_triangle_delta_minus.append (delta)
                list_primes_to_triangle_minus.append (triangle_number)
                delta_zero_found = True
            else:
                list_primes_to_triangle_delta_minus.append (delta)
                list_primes_to_triangle_minus.append (triangle_number)
                delta_minus_found = True
        if p.is_prime(triangle_number + delta) and delta > 0:
            prime_found = True
            list_of_primes.append (triangle_number + delta)
            list_primes_to_triangle_delta_plus.append (delta)
            list_primes_to_triangle_plus.append (triangle_number)
            delta_plus_found = True
        if not prime_found:
            delta += 1
        else:
            update_delta_count (delta)

        if prime_found and delta > delta_threshold:
            print (triangle_number, delta, delta_plus_found, delta_zero_found, delta_minus_found)

prepare_data(c)
write_results_to_figures()

print_stats ()