#
# Copyright (c) 2022, Marcin Barylski
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
min_num = 1
max_num = 10000

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

file_output_fig1 = directory + "/f_pxpminp_params" + file_output_extension
file_output_fig2 = directory + "/f_pxpminp_params_knot35" + file_output_extension
file_output_fig3 = directory + "/f_pxpminp_params_jdotk1" + file_output_extension
file_output_fig4 = directory + "/f_pxpminp_params_k1dotj" + file_output_extension
file_output_fig5 = directory + "/f_pxpminp_params_jk1" + file_output_extension

file_output_results_pxpminp = directory + "/t_results_pxpminp.txt"

#############################################################
# Results of calculations
#############################################################

list_nums = []
list_k1 = []
list_k2 = []
list_j = []
found_sets = []
found_sets_knot35 = []
list_nums_primes = []
list_data_jdotk1 = []
list_data_k1dotj = []
list_data_j = []
list_data_k1 = []

#############################################################
# Business logic
#############################################################
    
#############################################################
# Presentation
#############################################################

def new_file (filename):
    f = open(filename, 'w')
    f.close()

def write_to_file (filename, data):
    f = open(filename, 'a+')
    f.writelines(data)
    f.close()

def write_results_to_figures ():

    fig = plt.figure(1)
    plt.clf()
    r_patch = mpatches.Patch(color='red', label='k1')
    g_patch = mpatches.Patch(color='blue', label='k2')
    b_patch = mpatches.Patch(color='green', label='j')
    list_of_handles = []
    list_of_handles.append(r_patch)
    list_of_handles.append(g_patch)
    list_of_handles.append(b_patch)
    plt.plot(list_nums, list_k1, 'r.', ms=1)
    plt.plot(list_nums, list_k2, 'b.', ms=1)
    plt.plot(list_nums, list_j, 'g.', ms=1)
    plt.legend(handles=list_of_handles, loc='upper right', bbox_to_anchor=(0.4, 0.8), fontsize=6)
    fig.suptitle("Prime = j*k1 +- k2", fontsize=10)
    plt.savefig(file_output_fig1)
    plt.close(fig)

    fig = plt.figure(2)
    plt.clf()
    r_patch = mpatches.Patch(color='red', label='# of partitions')
    list_of_handles = []
    list_of_handles.append(r_patch)
    plt.plot(list_nums, found_sets_knot35, 'r.', ms=1)
    plt.legend(handles=list_of_handles, loc='upper right', bbox_to_anchor=(0.4, 0.8), fontsize=6)
    fig.suptitle("Prime = j*k1 +- k2 when k1>3 - partitions", fontsize=10)
    plt.savefig(file_output_fig2)
    plt.close(fig)

    fig = plt.figure(3)
    plt.clf()
    plt.plot(list_nums_primes, list_data_jdotk1, 'r.', ms=1)
    fig.suptitle("j.k1 for primes", fontsize=10)
    plt.savefig(file_output_fig3)
    plt.close(fig)

    fig = plt.figure(4)
    plt.clf()
    plt.plot(list_nums_primes, list_data_jdotk1, 'r.', ms=1)
    fig.suptitle("k1.j for primes", fontsize=10)
    plt.savefig(file_output_fig4)
    plt.close(fig)

    fig = plt.figure(5)
    plt.clf()
    plt.plot(list_data_j, list_data_k1, 'r.', ms=1)
    fig.suptitle("j and k1", fontsize=10)
    plt.savefig(file_output_fig5)
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

new_file (file_output_results_pxpminp)

# new calculations
for k in range (min_num, max_num):

    found = False
    smallest_jk1 = 0
    my_j = 0
    my_k1 = 0
    my_k2 = 0
    
    prime = p.get_ith_prime (k)

    list_nums.append(prime)
    count_knot35 = 0

    for i in range (min_num, max_num):
        for j in range (min_num, max_num):
            k1 = p.get_ith_prime (i)
            k2 = p.get_ith_prime (i+1)
            

            if prime == j*k1 - k2:
                s = str(prime) + "=" + str(j) + "x" + str(k1) + "-" + str(k2) + "\n"
                write_to_file (file_output_results_pxpminp, s)

                if not found:
                    smallest_jk1 =  j*k1
                    my_j = j
                    my_k1 = k1
                    my_k2 = k2
                    found = True
                elif j*k1 < smallest_jk1:
                    smallest_jk1 =  j*k1
                    my_j = j
                    my_k1 = k1
                    my_k2 = k2

                found_sets.append ([j, k1, k2])
                if k1 > 3:
                    count_knot35+= 1

                list_nums_primes.append (prime)
                list_data_jdotk1.append ((j + k1/(10**c.get_number_of_dec_digits(k1)))*(-1))
                list_data_k1dotj.append ((k1 + j/(10**c.get_number_of_dec_digits(j)))*(-1))
                list_data_j.append (j)
                list_data_k1.append (k1)

            if prime == j*k1 + k2:
                s = str(prime) + "=" + str(j) + "x" + str(k1) + "+" + str(k2) + "\n"
                write_to_file (file_output_results_pxpminp, s)

                if not found:
                    smallest_jk1 =  j*k1
                    my_j = j
                    my_k1 = k1
                    my_k2 = k2
                    found = True
                elif j*k1 < smallest_jk1:
                    smallest_jk1 =  j*k1
                    my_j = j
                    my_k1 = k1
                    my_k2 = k2

                found_sets.append ([j, k1, k2])
                if k1 > 3:
                    count_knot35+= 1

                list_nums_primes.append (prime)
                list_data_jdotk1.append (j + k1/(10**c.get_number_of_dec_digits(k1)))
                list_data_k1dotj.append (k1 + j/(10**c.get_number_of_dec_digits(j)))
                list_data_j.append (j)
                list_data_k1.append (k1)

    found_sets_knot35.append (count_knot35)

    if not found:
        s = "--> no solution found for:" + str(prime) + " (checked until " + str(max_num) + ")" + "\n"
        write_to_file (file_output_results_pxpminp, s)
        list_k1.append (0)
        list_k2.append (0)
        list_j.append (0)
    else:
        list_k1.append (my_k1)
        list_k2.append (my_k2)
        list_j.append (my_j)

    write_results_to_figures ()
    	
# final results
write_results_to_figures ()
