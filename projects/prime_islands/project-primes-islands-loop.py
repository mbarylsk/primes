#
# Copyright (c) 2022 - 2026, Marcin Barylski
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
import matplotlib.pyplot as plt
import numpy as np
# path to libraries
sys.path.insert(1, "..\\..")
import primes
import calculations
import graphs

#############################################################
# Settings - configuration
#############################################################

# Minimal and maximum number - range of iterations
min_num = 1
max_num = 100
min_neighbours = 2
min_step = 0
max_step = 100
step = 2

sys.setrecursionlimit(10000)

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

# Graphs
#   o True - writes the graphs (visual form) to the file, separate switch to show on screen
#   o False - be quiet
show_islands_screen = True

#############################################################
# Settings - output directory and files
#############################################################

directory = "results/" + str(max_num)
if not os.path.exists(directory):
    os.makedirs(directory)
file_output_extension = ".png"

#############################################################
# Results of calculations
#############################################################

k = 0
cols = 10000
rows = int(cols/2)
arr = np.zeros((rows, cols))
island_squares = []
list_of_islands = []
results_for_steps = {}

#############################################################
# Business logic
#############################################################

# recursive function for finding all squares of the island
# (squares of non-zero values close to each other)
def add_island_to_list (island_squares):
    global list_of_islands
    island_found = False
    for square in island_squares:
        for island in list_of_islands:
            if square in island:
                island_found = True

    if not island_found:
        list_of_islands.append (island_squares)

# recursive function for finding all squares of the island
# (squares of non-zero values close to each other)
def check_square (m, x, y):
    global island_squares
    if m[x][y] == 0:
        return
    (rows, cols) = m.shape
    p = (x,y)
    island_squares.append (p)
    p1 = (x-1, y)
    p2 = (x+1, y)
    p3 = (x, y-1)
    p4 = (x, y+1)
    if x-1 >= 0 and p1 not in island_squares:
        check_square (m, x-1, y)
    if x+1 < cols and p2 not in island_squares:
        check_square (m, x+1, y)
    if y-1 >= 0 and p3 not in island_squares:
        check_square (m, x, y-1)
    if y+1 < rows and p4 not in island_squares:
        check_square (m, x, y+1)

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

# new calculations
for l in range (min_step, max_step+1, step):
    print ("Starting iteration for step: C=", l)
    arr = np.zeros((rows, cols))
    
    list_of_islands = []
    max_size_of_island = 0

    # Method A
    #prime = p.get_ith_prime (0)
    #for k in range (min_num, max_num):

    #    prime = p.get_ith_prime (k)
    
    #    pairs = []
        # this will show results for primes of form pxq-step
    #    pairs = p.factorize_to_pairs (prime+l)
    
    #    for pair in pairs:
    #        (x, y) = pair
    #        if y < cols and x < rows:
    #            arr[x][y]=1

    # Method B
    for x in range (min_num, max_num):
        for y in range (min_num, x):
            if p.is_prime (x*y+l) and y < cols and x < rows and y >=0 and x >= 0:
                arr[y][x]=1

    # get results
    print ("--> Now looking for islands")
    # prepare variables first
    arr2 = np.zeros((rows, cols))
    arr2 = c.get_matrix_of_neighbours (arr)

    print (arr2)

    # find greatest island first
    for i in range (0, rows):
        for j in range (0, cols):

            if arr2[i][j] >= min_neighbours:
                title = "Dimensions:" + str(i) + ",", str(j)
                delta = 5
                subarr2 = c.get_submatrix (arr2, i-delta, i+delta, j-delta, j+delta)

                island_squares = []
                check_square (arr2, i, j)
                size_of_island = len(island_squares)
                if size_of_island > max_size_of_island:
                    max_size_of_island = size_of_island
                    print ("--> Current size of greatest island found:", max_size_of_island)
    print ("--> Size of greatest island found:", max_size_of_island)

    for i in range (0, rows):
        for j in range (0, cols):

            if arr2[i][j] >= min_neighbours:
                title = "Dimensions:" + str(i) + ",", str(j)
                delta = 5
                subarr2= c.get_submatrix (arr2, i-delta, i+delta, j-delta, j+delta)

                island_squares = []
                check_square (arr2, i, j)
                size_of_island = len(island_squares)
                if size_of_island == max_size_of_island:
                    #print ("Size of island at: ", i, j, "is", size_of_island)
                    add_island_to_list (island_squares)

                    if show_islands_screen:
                        plt.matshow(subarr2, origin='lower')
                        plt.title (title)
                        plt.show()

    print ("--> Islands found:", list_of_islands)
    print ("--> Number of such islands found:", len(list_of_islands))

    result = (max_size_of_island, len(list_of_islands))
    results_for_steps[l]= result

print ("Final results:")
print (results_for_steps)

f = open("results_prime_island_loop.txt",'w')
print(results_for_steps, file=f)