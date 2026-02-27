#
# Copyright (c) 2020, Marcin Barylski
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

#############################################################
# Settings - configuration
#############################################################

# Minimal and maximum number - range of iterations
min_num = 2
max_num = 1000000

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
file_output_fig1 = directory + "/f_two_digits_freq_primes" + file_output_extension
file_output_fig2 = directory + "/f_two_digits_freq_composites" + file_output_extension
file_output_fig3 = directory + "/f_three_digits_freq_primes" + file_output_extension
file_output_fig4 = directory + "/f_three_digits_freq_composites" + file_output_extension
file_output_fig5 = directory + "/f_two_digits_from_avg_freq_primes" + file_output_extension
file_output_fig6 = directory + "/f_three_digits_from_avg_freq_primes" + file_output_extension
file_output_fig7 = directory + "/f_two_digits_from_avg_freq_composites" + file_output_extension
file_output_fig8 = directory + "/f_three_digits_from_avg_freq_composites" + file_output_extension

#############################################################
# Results of calculations
#############################################################

dict_frequency2 = {}
dict_frequency2_comp = {}
dict_frequency2_diff_from_avg = {}
dict_frequency2_diff_from_avg_comp = {}

dict_frequency3 = {}
dict_frequency3_comp = {}
dict_frequency3_diff_from_avg = {}
dict_frequency3_diff_from_avg_comp = {}

k = 0

#############################################################
# Business logic
#############################################################

def calculate_metics (p, c, k, subnums2, subnums3):
    global dict_frequency2, dict_frequency2_comp, dict_frequency3, dict_frequency3_comp
    global dict_frequency2_diff_from_avg, dict_frequency3_diff_from_avg, dict_frequency2_diff_from_avg_comp, dict_frequency3_diff_from_avg_comp
    
    if p.is_prime (k):
        for subnum in subnums2:
            if subnum in dict_frequency2:
                dict_frequency2[subnum] += 1
            else:
                dict_frequency2[subnum] = 1
        for subnum in subnums3:
            if subnum in dict_frequency3:
                dict_frequency3[subnum] += 1
            else:
                dict_frequency3[subnum] = 1
    else:
        for subnum in subnums2:
            if subnum in dict_frequency2_comp:
                dict_frequency2_comp[subnum] += 1
            else:
                dict_frequency2_comp[subnum] = 1
        for subnum in subnums3:
            if subnum in dict_frequency3_comp:
                dict_frequency3_comp[subnum] += 1
            else:
                dict_frequency3_comp[subnum] = 1

    dict_frequency2_diff_from_avg = c.new_dict_from_avg(dict_frequency2)
    dict_frequency3_diff_from_avg = c.new_dict_from_avg(dict_frequency3)
    dict_frequency2_diff_from_avg_comp = c.new_dict_from_avg(dict_frequency2_comp)
    dict_frequency3_diff_from_avg_comp = c.new_dict_from_avg(dict_frequency3_comp)
    
#############################################################
# Presentation
#############################################################

def write_results_to_figures(g):

    g.graph_plot_bars_from_dict (dict_frequency2, file_output_fig1)
    g.graph_plot_bars_from_dict (dict_frequency2_comp, file_output_fig2)
    g.graph_plot_bars_from_dict (dict_frequency3, file_output_fig3)
    g.graph_plot_bars_from_dict (dict_frequency3_comp, file_output_fig4)
    g.graph_plot_bars_from_dict (dict_frequency2_diff_from_avg, file_output_fig5)
    g.graph_plot_bars_from_dict (dict_frequency3_diff_from_avg, file_output_fig6)
    g.graph_plot_bars_from_dict (dict_frequency2_diff_from_avg_comp, file_output_fig7)
    g.graph_plot_bars_from_dict (dict_frequency3_diff_from_avg_comp, file_output_fig8)
    
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

    subnums2 = c.get_all_subnums(k, 2, False)
    subnums3 = c.get_all_subnums(k, 3, False)

    calculate_metics (p, c, k, subnums2, subnums3)

# final results
write_results_to_figures (g)
