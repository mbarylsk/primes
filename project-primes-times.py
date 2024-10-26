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
min_num = 2
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
file_output_fig1 = directory + "/f_times_both_primes" + file_output_extension
file_output_fig2 = directory + "/f_times_one_prime" + file_output_extension
file_output_fig3 = directory + "/f_times_no_primes" + file_output_extension

#############################################################
# Results of calculations
#############################################################

k = 0

dict_both_primes = {}
dict_one_prime = {}
dict_no_primes = {}

#############################################################
# Business logic
#############################################################

#############################################################
# Presentation
#############################################################

def print_graphs ():
    global list_values, list_arguments

    width = 1.0
    
    fig = plt.figure(1)
    plt.bar(dict_both_primes.keys(), dict_both_primes.values(), width, color='g')
    fig.suptitle("Sum", fontsize=10)
    plt.savefig(file_output_fig1)
    plt.close(fig)

    fig = plt.figure(2)
    plt.bar(dict_one_prime.keys(), dict_one_prime.values(), width, color='g')
    fig.suptitle("Sum", fontsize=10)
    plt.savefig(file_output_fig2)
    plt.close(fig)

    fig = plt.figure(3)
    plt.bar(dict_no_primes.keys(), dict_no_primes.values(), width, color='g')
    fig.suptitle("Sum", fontsize=10)
    plt.savefig(file_output_fig3)
    plt.close(fig)

def update_stats (n1, n2, is_n1_prime, is_n2_prime, i):
    if is_n1_prime and is_n2_prime:
        if i not in dict_both_primes:
            dict_both_primes [i] = 0
        dict_both_primes [i] += 1
    elif is_n1_prime or is_n2_prime:
        if i not in dict_one_prime:
            dict_one_prime [i] = 0
        dict_one_prime [i] += 1
    else:
        if i not in dict_no_primes:
            dict_no_primes [i] = 0
        dict_no_primes [i] += 1
                  
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
for n1 in range (min_num, max_num):
    print (n1)
    print_graphs ()
    for n2 in range (min_num, max_num):

        i = 1
        found = False
        while not found:
            if p.is_prime (n1*n2-i):
                found = True
                break
            else:
                i += 1

        #print (n1, n2, i, n1*n2-i)

        update_stats (n1, n2, p.is_prime (n1), p.is_prime (n2), i)
        
    	
# final results

print_graphs ()
