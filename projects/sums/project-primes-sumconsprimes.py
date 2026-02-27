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
max_num = 50000

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

list_max_factors = []
list_primes = []
list_max_factors2 = []
list_primes2 = []
list_max_factors3 = []
list_primes3 = []
list_max_factors4 = []
list_primes4 = []
list_max_factors5 = []
list_primes5 = []
list_max_factors6 = []
list_primes6 = []
list_max_factors7 = []
list_primes7 = []
list_max_factors8 = []
list_primes8 = []
list_max_factors9 = []
list_primes9 = []
list_max_factors10 = []
list_primes10 = []
list_max_factors11 = []
list_primes11 = []

#############################################################
# Business logic
#############################################################

	
def calculate_next_term1 (p, prime, prime_next):
    global list_max_factors, list_primes

    factors = p.factorize (prime + prime_next)
    max_factor = max (factors)

    if max_factor not in list_max_factors:
        list_max_factors.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes.append (new_list)
    else:
        max_factor_index = list_max_factors.index (max_factor)
        current_list = list_primes[max_factor_index]
        current_list.append (prime)
        del list_primes[max_factor_index]
        list_primes.insert (max_factor_index, current_list)


def calculate_next_term2 (p, prime):
    global list_max_factors2, list_primes2

    factors = p.factorize (prime*2+1)
    max_factor = max (factors)

    if max_factor not in list_max_factors2:
        list_max_factors2.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes2.append (new_list)
    else:
        max_factor_index = list_max_factors2.index (max_factor)
        current_list = list_primes2[max_factor_index]
        current_list.append (prime)
        del list_primes2[max_factor_index]
        list_primes2.insert (max_factor_index, current_list)

def calculate_next_term3 (p, prime, prime_next):
    global list_max_factors3, list_primes3

    factors = p.factorize (prime*prime_next+1)
    max_factor = max (factors)

    if max_factor not in list_max_factors3:
        list_max_factors3.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes3.append (new_list)
    else:
        max_factor_index = list_max_factors3.index (max_factor)
        current_list = list_primes3[max_factor_index]
        current_list.append (prime)
        del list_primes3[max_factor_index]
        list_primes3.insert (max_factor_index, current_list)

def calculate_next_term4 (p, prime):
    global list_max_factors4, list_primes4

    factors = p.factorize (prime*2+3)
    max_factor = max (factors)

    if max_factor not in list_max_factors4:
        list_max_factors4.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes4.append (new_list)
    else:
        max_factor_index = list_max_factors4.index (max_factor)
        current_list = list_primes4[max_factor_index]
        current_list.append (prime)
        del list_primes4[max_factor_index]
        list_primes4.insert (max_factor_index, current_list)

def calculate_next_term5 (p, prime):
    global list_max_factors5, list_primes5

    factors = p.factorize (prime*2+5)
    max_factor = max (factors)

    if max_factor not in list_max_factors5:
        list_max_factors5.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes5.append (new_list)
    else:
        max_factor_index = list_max_factors5.index (max_factor)
        current_list = list_primes5[max_factor_index]
        current_list.append (prime)
        del list_primes5[max_factor_index]
        list_primes5.insert (max_factor_index, current_list)

def calculate_next_term6 (p, prime):
    global list_max_factors6, list_primes6

    factors = p.factorize (prime*3+1)
    max_factor = max (factors)

    if max_factor not in list_max_factors6:
        list_max_factors6.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes6.append (new_list)
    else:
        max_factor_index = list_max_factors6.index (max_factor)
        current_list = list_primes6[max_factor_index]
        current_list.append (prime)
        del list_primes6[max_factor_index]
        list_primes6.insert (max_factor_index, current_list)

def calculate_next_term7 (p, prime):
    global list_max_factors7, list_primes7

    factors = p.factorize (prime*3+2)
    max_factor = max (factors)

    if max_factor not in list_max_factors7:
        list_max_factors7.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes7.append (new_list)
    else:
        max_factor_index = list_max_factors7.index (max_factor)
        current_list = list_primes7[max_factor_index]
        current_list.append (prime)
        del list_primes7[max_factor_index]
        list_primes7.insert (max_factor_index, current_list)

def calculate_next_term8 (p, prime):
    global list_max_factors8, list_primes8

    factors = p.factorize (prime*prime+1)
    max_factor = max (factors)

    if max_factor not in list_max_factors8:
        list_max_factors8.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes8.append (new_list)
    else:
        max_factor_index = list_max_factors8.index (max_factor)
        current_list = list_primes8[max_factor_index]
        current_list.append (prime)
        del list_primes8[max_factor_index]
        list_primes8.insert (max_factor_index, current_list)

def calculate_next_term9 (p, prime1, prime2, prime3):
    global list_max_factors9, list_primes9

    factors = p.factorize (prime1 + prime2 + prime3)
    max_factor = max (factors)

    if max_factor not in list_max_factors9:
        list_max_factors9.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes9.append (new_list)
    else:
        max_factor_index = list_max_factors9.index (max_factor)
        current_list = list_primes9[max_factor_index]
        current_list.append (prime)
        del list_primes9[max_factor_index]
        list_primes9.insert (max_factor_index, current_list)

def calculate_next_term10 (p, prime):
    global list_max_factors10, list_primes10

    factors = p.factorize (prime + 1)
    max_factor = max (factors)

    if max_factor not in list_max_factors10:
        list_max_factors10.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes10.append (new_list)
    else:
        max_factor_index = list_max_factors10.index (max_factor)
        current_list = list_primes10[max_factor_index]
        current_list.append (prime)
        del list_primes10[max_factor_index]
        list_primes10.insert (max_factor_index, current_list)

def calculate_next_term11 (p, prime):
    global list_max_factors11, list_primes11

    factors = p.factorize (prime + 2)
    max_factor = max (factors)

    if max_factor not in list_max_factors11:
        list_max_factors11.append (max_factor)
        new_list = []
        new_list.append (prime)
        list_primes11.append (new_list)
    else:
        max_factor_index = list_max_factors11.index (max_factor)
        current_list = list_primes11[max_factor_index]
        current_list.append (prime)
        del list_primes11[max_factor_index]
        list_primes11.insert (max_factor_index, current_list)

#############################################################
# Presentation
#############################################################

def print_graphs_stats (g, show, show_screen, filename_output):

    print("=================")
    print("Graph filename:", filename_output)
    print("Graph cycles:", list(nx.simple_cycles(g)))
    print("Graph size:", g.size())
    print("Graph density:", nx.density(g))

    if max_num > 50:
        options = {
        "font_size": 2,
        "node_size": 5,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 1,
        "width": 1,
        }
    else:
        options = {
        "font_size": 8,
        "node_size": 200,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 1,
        "width": 1,
        }

    if show:
        nx.draw_networkx(g, **options)
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.savefig(filename_output)
        if show_screen:
            plt.show()
        plt.close()

def print_graphs (show, show_screen):
    global list_max_factors, list_primes, list_max_factors2, list_primes2
    global list_max_factors3, list_primes3, list_max_factors4, list_primes4
    global list_max_factors5, list_primes5, list_max_factors6, list_primes6
    global list_max_factors7, list_primes7, list_max_factors8, list_primes8
    global list_max_factors9, list_primes9, list_max_factors10, list_primes10
    global list_max_factors11, list_primes11
    
    G1 = nx.DiGraph()
    index = 0
    for pr_list in list_primes:
        for pr1 in pr_list:
            pr2 = list_max_factors[index]
            G1.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G1, show, show_screen, filename_figure1)

    G2 = nx.DiGraph()
    index = 0
    for pr_list in list_primes2:
        for pr1 in pr_list:
            pr2 = list_max_factors2[index]
            G2.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G2, show, show_screen, filename_figure2)

    G3 = nx.DiGraph()
    index = 0
    for pr_list in list_primes3:
        for pr1 in pr_list:
            pr2 = list_max_factors3[index]
            G3.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G3, show, show_screen, filename_figure3)

    G4 = nx.DiGraph()
    index = 0
    for pr_list in list_primes4:
        for pr1 in pr_list:
            pr2 = list_max_factors4[index]
            G4.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G4, show, show_screen, filename_figure4)

    G5 = nx.DiGraph()
    index = 0
    for pr_list in list_primes5:
        for pr1 in pr_list:
            pr2 = list_max_factors5[index]
            G5.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G5, show, show_screen, filename_figure5)

    G6 = nx.DiGraph()
    index = 0
    for pr_list in list_primes6:
        for pr1 in pr_list:
            pr2 = list_max_factors6[index]
            G6.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G6, show, show_screen, filename_figure6)

    G7 = nx.DiGraph()
    index = 0
    for pr_list in list_primes7:
        for pr1 in pr_list:
            pr2 = list_max_factors7[index]
            G7.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G7, show, show_screen, filename_figure7)

    G8 = nx.DiGraph()
    index = 0
    for pr_list in list_primes8:
        for pr1 in pr_list:
            pr2 = list_max_factors8[index]
            G8.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G8, show, show_screen, filename_figure8)

    G9 = nx.DiGraph()
    index = 0
    for pr_list in list_primes9:
        for pr1 in pr_list:
            pr2 = list_max_factors9[index]
            G9.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G9, show, show_screen, filename_figure9)

    G10 = nx.DiGraph()
    index = 0
    for pr_list in list_primes10:
        for pr1 in pr_list:
            pr2 = list_max_factors10[index]
            G10.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G10, show, show_screen, filename_figure10)

    G11 = nx.DiGraph()
    index = 0
    for pr_list in list_primes11:
        for pr1 in pr_list:
            pr2 = list_max_factors11[index]
            G11.add_edge(pr1, pr2)
        index += 1

    print_graphs_stats (G11, show, show_screen, filename_figure11)
    
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
prime = p.get_ith_prime (0)
for k in range (min_num, max_num):

    prime_next = p.get_ith_prime (k+1)
    prime_next_next = p.get_ith_prime (k+2)
    
    calculate_next_term1 (p, prime, prime_next)
    calculate_next_term2 (p, prime)
    calculate_next_term3 (p, prime, prime_next)
    calculate_next_term4 (p, prime)
    calculate_next_term5 (p, prime)
    calculate_next_term6 (p, prime)
    calculate_next_term7 (p, prime)
    calculate_next_term8 (p, prime)
    calculate_next_term9 (p, prime, prime_next, prime_next_next)
    calculate_next_term10 (p, prime)
    calculate_next_term11 (p, prime)

    prime = prime_next
    	
# final results

print_graphs (show_graphs, show_graphs_screen)
