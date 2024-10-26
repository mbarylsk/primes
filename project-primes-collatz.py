#
# Copyright (c) 2021, Marcin Barylski
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
import matplotlib.patches as mpatches

#############################################################
# Settings - configuration
#############################################################

# Minimal and maximum number - range of iterations
min_num = 0
max_num = 100000

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
file_output_fig1 = directory + "/f_prime_collatz_lenght_of_seq_3xp1" + file_output_extension
file_output_fig2 = directory + "/f_prime_collatz_lenght_of_seq_3xp3" + file_output_extension

#############################################################
# Results of calculations
#############################################################

k = 0
numbers_in_all_sequences_3xplus1 = set()
numbers_in_all_sequences_3xplus3 = set()

sequence_loop1_3xplus1= [2, 7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4]
sequence_loop1_3xplus3= [3, 12, 6]

list_init_nums = []
list_number_of_terms_3xplus1 = []
list_number_of_terms_3xplus3 = []

#############################################################
# Business logic
#############################################################

def calculate_metics (p):
    i = 0
	
def calculate_terms_3xplus1 (p, n_start):
    global list_init_nums, list_number_of_terms_3xplus1, numbers_in_all_sequences_3xplus1, sequence_loop1_3xplus1

    completed = False
    n = n_start
    numbers_in_sequence = []

    while (not completed):
        numbers_in_sequence.append(n)
        numbers_in_all_sequences_3xplus1.add (n)
        if p.is_prime(n):
            n = 3*n+1
        else:
            l = p.factorize (n)
            l.sort()
            f = l[0]
            n = int(n/f)
        if n in numbers_in_sequence:
            completed = True
    
    print ("For n=", n_start, "we have:", numbers_in_sequence)
	
    list_number_of_terms_3xplus1.append(len(numbers_in_sequence))

    for s in sequence_loop1_3xplus1:
        if s not in numbers_in_sequence:
            print ("--> New loop detected!")

def calculate_terms_3xplus3 (p, n_start):
    global list_init_nums, list_number_of_terms_3xplus1, numbers_in_all_sequences_3xplus1, sequence_loop1_3xplus1

    completed = False
    n = n_start
    numbers_in_sequence = []

    while (not completed):
        numbers_in_sequence.append(n)
        numbers_in_all_sequences_3xplus3.add (n)
        if p.is_prime(n):
            n = 3*n+3
        else:
            l = p.factorize (n)
            l.sort()
            f = l[0]
            n = int(n/f)
        if n in numbers_in_sequence:
            completed = True
    
    print ("For n=", n_start, "we have:", numbers_in_sequence)
	
    list_number_of_terms_3xplus3.append(len(numbers_in_sequence))

    for s in sequence_loop1_3xplus3:
        if s not in numbers_in_sequence:
            print ("--> New loop detected!")
    
#############################################################
# Presentation
#############################################################

def write_results_to_figures():

    fig = plt.figure(1)
    plt.clf()
    b_patch = mpatches.Patch(color='blue', label='lenght of seq till loop (3x+1)')
    list_of_handles = []
    list_of_handles.append(b_patch)
    plt.plot(list_init_nums, list_number_of_terms_3xplus1, 'b.', ms=1)
    plt.legend(handles=list_of_handles, loc='upper right', bbox_to_anchor=(0.4, 0.9), fontsize=6)
    fig.suptitle("Lenght of sequences", fontsize=10)
    plt.savefig(file_output_fig1)
    plt.close(fig)

    fig = plt.figure(2)
    plt.clf()
    b_patch = mpatches.Patch(color='blue', label='lenght of seq till loop (3x+3)')
    list_of_handles = []
    list_of_handles.append(b_patch)
    plt.plot(list_init_nums, list_number_of_terms_3xplus3, 'b.', ms=1)
    plt.legend(handles=list_of_handles, loc='upper right', bbox_to_anchor=(0.4, 0.9), fontsize=6)
    fig.suptitle("Lenght of sequences", fontsize=10)
    plt.savefig(file_output_fig2)
    plt.close(fig)
    
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
for k in range (min_num, max_num):

    prime = p.get_ith_prime (k)
    list_init_nums.append (prime)

    calculate_terms_3xplus1 (p, prime)
    calculate_terms_3xplus3 (p, prime)
    	
# final results

print (numbers_in_all_sequences_3xplus1)
write_results_to_figures ()
