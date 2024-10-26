#
# Copyright (c) 2022-2024, Marcin Barylski
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
import networkx as nx

#############################################################
# Settings - configuration
#############################################################

# Minimal and maximum number - range of iterations
min_num = 0
max_num = 500

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

# Graphs
#   o True - writes the graphs (visual form) to the file, separate switch to show on screen
#   o False - be quiet
show_graphs = True
show_graphs_screen = False

#############################################################
# Settings - output directory and files
#############################################################

directory = "results/" + str(max_num)
if not os.path.exists(directory):
    os.makedirs(directory)
file_output_extension = ".png"
filename_figure1 = directory + "/fig1" + file_output_extension
filename_figure2 = directory + "/fig2" + file_output_extension
filename_figure3 = directory + "/fig3" + file_output_extension
filename_figure4 = directory + "/fig4" + file_output_extension
filename_figure5 = directory + "/fig5" + file_output_extension
filename_figure6 = directory + "/fig6" + file_output_extension
filename_figure7 = directory + "/fig7" + file_output_extension
filename_figure8 = directory + "/fig8" + file_output_extension
filename_figure9 = directory + "/fig9" + file_output_extension
filename_figure10 = directory + "/fig10" + file_output_extension
filename_figure11 = directory + "/fig11" + file_output_extension

#############################################################
# Results of calculations
#############################################################

k = 0

#############################################################
# Business logic
#############################################################

#############################################################
# Presentation
#############################################################

    
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

res = []

# new calculations
prime = p.get_ith_prime (0)
for k in range (min_num, max_num):

    prime_next = p.get_ith_prime (k+1)
    prime_next_next = p.get_ith_prime (k+2)
    
    k1 = 2*(prime_next+prime_next_next)+1
    k2 = 2*(prime_next+prime_next_next)-1

    if not p.is_prime(k1) and not p.is_prime(k2):
        print (prime_next,prime_next_next,k1, k2)
        res.append(prime_next)

        
    #else:
    #    if p.is_prime(k1):
    #        print ("Prime k1", prime_next, prime_next_next, k1)
    #    if p.is_prime(k2):
    #        print ("Prime k2", prime_next, prime_next_next, k2)
    	
# final results
print (res)
