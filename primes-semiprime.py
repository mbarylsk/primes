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
min_num = 3
max_num = 1000003

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
file_output_fig1 = directory + "/f_prime_semiprime_diff" + file_output_extension
file_output_fig2 = directory + "/f_prime_semiprime_perc" + file_output_extension
file_output_fig3 = directory + "/f_prime_semiprime_sum" + file_output_extension

#############################################################
# Results of calculations
#############################################################

list_nums = []
list_diff = []
list_sum = []
list_percentage = [[],[]]
count_all_nums = 0
count_delta_ok = 0
count_delta_below = 0
current_sum = 0

#############################################################
# Business logic
#############################################################

def calculate_metrics (i, p1, p2, p3, p4):
    global list_init_nums, list_delta, count_all_nums, count_delta_ok, count_delta_below, current_sum

    sp1 = p2*p3
    sp2 = p1*p4
    diff = sp1 - sp2

    current_sum += diff

    if diff > 0:
        count_delta_ok += 1
    else:
        count_delta_below += 1
        
    #print (p1, p2, p3, p4, sp1, sp2, diff)

    list_nums.append (i)
    list_diff.append (diff)
    list_sum.append (current_sum)
    list_percentage[0].append (100*count_delta_ok/count_all_nums)
    list_percentage[1].append (100*count_delta_below/count_all_nums)
    
#############################################################
# Presentation
#############################################################

def write_results_to_figures():

    fig = plt.figure(1)
    plt.clf()
    b_patch = mpatches.Patch(color='blue', label='diff sp1-sp2')
    list_of_handles = []
    list_of_handles.append(b_patch)
    plt.plot(list_nums, list_diff, 'b.', ms=1)
    plt.legend(handles=list_of_handles, loc='upper right', bbox_to_anchor=(0.4, 0.9), fontsize=6)
    fig.suptitle("Difference between semiprimes", fontsize=10)
    plt.savefig(file_output_fig1)
    plt.close(fig)

    fig = plt.figure(2)
    plt.clf()
    g_patch = mpatches.Patch(color='green', label='% met')
    r_patch = mpatches.Patch(color='red', label='% not met')
    list_of_handles = []
    list_of_handles.append(g_patch)
    list_of_handles.append(r_patch)
    plt.plot(list_nums, list_percentage[0], 'g.', ms=1)
    plt.plot(list_nums, list_percentage[1], 'r.', ms=1)
    plt.legend(handles=list_of_handles, loc='upper right', bbox_to_anchor=(0.4, 0.9), fontsize=6)
    fig.suptitle("Correctness of hypothesis", fontsize=10)
    plt.savefig(file_output_fig2)
    plt.close(fig)

    fig = plt.figure(3)
    plt.clf()
    b_patch = mpatches.Patch(color='blue', label='sum of diff sp1-sp2')
    list_of_handles = []
    list_of_handles.append(b_patch)
    plt.plot(list_nums, list_sum, 'b.', ms=1)
    plt.legend(handles=list_of_handles, loc='upper right', bbox_to_anchor=(0.4, 0.9), fontsize=6)
    fig.suptitle("Sum of differences between semiprimes", fontsize=10)
    plt.savefig(file_output_fig3)
    plt.close(fig)
    
#############################################################
# Main
#############################################################

print ("Initialize objects...")
p = primes.Primes(caching_primality_results)
print ("DONE")
print ("Loading helper sets...")
p.init_set(file_input_primes, True)
p.init_set(file_input_nonprimes, False)
print ("DONE")
print ("Sorting primes...")
p.sort_primes_set()
print ("DONE")

# new calculations
p1 = p.get_ith_prime (0)
p2 = p.get_ith_prime (1)
p3 = p.get_ith_prime (2)
for k in range (min_num, max_num):

    count_all_nums += 1
    p4 = p.get_ith_prime (k)

    calculate_metrics (k, p1, p2, p3, p4)
    
    p1 = p2
    p2 = p3
    p3 = p4
    p4 = 0

    # checkpoint - partial results
    if (k - min_num) % checkpoint_value == 0:

        perc_completed = str(int(k * 100 / max_num))
        print ("Checkpoint", k, "of total", max_num, "(" + perc_completed + "% completed)")
   
        # save results collected so far
        write_results_to_figures ()
    	
# final results

write_results_to_figures ()
