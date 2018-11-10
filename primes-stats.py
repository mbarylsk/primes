#
# Copyright (c) 2018, Marcin Barylski
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
import primes
import calculations

#############################################################
# Settings - configuration
#############################################################

# Minimal and maximum number - range of iterations
min_num = 2
max_num = 1000000

# Checkpoint value when partial results are drawn/displayed
# should be greater than zero
checkpoint_value = 10000

# dimension of color map, must be positive
base = 16

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

continue_previous_calculations = False

#############################################################
# Settings - output directory and files
#############################################################

directory = "results/" + str(max_num)
if not os.path.exists(directory):
    os.makedirs(directory)
file_output_extension = ".png"
file_output_fig1 = directory + "/f_lastdigit_closeto2n_all" + file_output_extension
file_output_fig2 = directory + "/f_lastdigit_closeto2n_primes" + file_output_extension
file_output_fig3 = directory + "/f_lastdigit_closeto2n_complex" + file_output_extension
file_output_fig4 = directory + "/f_noofdigits_closeto2n_all" + file_output_extension
file_output_fig5 = directory + "/f_noofdigits_closeto2n_primes" + file_output_extension
file_output_fig6 = directory + "/f_noofdigits_closeto2n_complex" + file_output_extension
file_output_fig7 = directory + "/f_closeto2n_closeto3n_all" + file_output_extension
file_output_fig8 = directory + "/f_closeto2n_closeto3n_primes" + file_output_extension
file_output_fig9 = directory + "/f_closeto2n_closeto3n_complex" + file_output_extension
file_output_fig10 = directory + "/f_lasttwodigits_closeto2n_all" + file_output_extension
file_output_fig11 = directory + "/f_colormap_lasttwodigits_closeto2n_primes" + file_output_extension
file_output_fig12 = directory + "/f_colormap_lasttwodigits_closeto2n_complex" + file_output_extension
file_output_fig13 = directory + "/f_colormap_lasttwodigits_closeto2n_all" + file_output_extension
file_output_fig14 = directory + "/f_colormap_closeto2n_closeto3n_primes" + file_output_extension
file_output_fig15 = directory + "/f_colormap_closeto2n_closeto3n_complex" + file_output_extension
file_output_fig16 = directory + "/f_colormap_closeto2n_closeto3n_all" + file_output_extension
file_output_fig17 = directory + "/f_colormap_firsttwodigits_closeto2n_primes" + file_output_extension
file_output_fig18 = directory + "/f_colormap_firsttwodigits_closeto2n_complex" + file_output_extension
file_output_fig19 = directory + "/f_colormap_firsttwodigits_closeto2n_all" + file_output_extension
file_output_fig20 = directory + "/f_firsttwodigits_closeto2n_all" + file_output_extension
file_output_fig21 = directory + "/f_colormap_lasttwodigits_firsttwodigits_primes" + file_output_extension
file_output_fig22 = directory + "/f_colormap_lasttwodigits_firsttwodigits_complex" + file_output_extension
file_output_fig23 = directory + "/f_colormap_lasttwodigits_firsttwodigits_all" + file_output_extension
file_output_fig24 = directory + "/f_colormap_primes" + file_output_extension
file_output_fig25 = directory + "/f_colormap_complex" + file_output_extension
file_output_fig26 = directory + "/f_lessertwinprimes_ratio" + file_output_extension

#############################################################
# Results of calculations
#############################################################

list_checkpoints = []
list_primes_digits = [[],[],[],[]]
list_primes_perc_of_next_milestone = [[],[]]
list_lesser_twin_primes_ratio = [[],[],[]]
list_complex_digits = [[],[],[],[]]
list_complex_perc_of_next_milestone = [[],[]]
array_primes_last_two_digits_2n = np.zeros((101, 101))
array_primes_last_two_digits_2n_perc = np.zeros((101, 101))
array_primes_last_two_digits_first_two_digits = np.zeros((101, 101))
array_primes_last_two_digits_first_two_digits_perc = np.zeros((101, 101))
array_primes_first_two_digits_2n = np.zeros((101, 101))
array_primes_first_two_digits_2n_perc = np.zeros((101, 101))
array_primes_2n_3n = np.zeros((101, 101))
array_primes_2n_3n_perc = np.zeros((101, 101))
array_complex_2n_3n = np.zeros((101, 101))
array_complex_2n_3n_perc = np.zeros((101, 101))
array_all_2n_3n = np.zeros((101, 101))
array_all_2n_3n_perc = np.zeros((101, 101))
array_complex_last_two_digits_2n = np.zeros((101, 101))
array_complex_last_two_digits_2n_perc = np.zeros((101, 101))
array_complex_last_two_digits_first_two_digits = np.zeros((101, 101))
array_complex_last_two_digits_first_two_digits_perc = np.zeros((101, 101))
array_complex_first_two_digits_2n = np.zeros((101, 101))
array_complex_first_two_digits_2n_perc = np.zeros((101, 101))
array_all_last_two_digits_2n = np.zeros((101, 101))
array_all_last_two_digits_2n_perc = np.zeros((101, 101))
array_all_last_two_digits_first_two_digits = np.zeros((101, 101))
array_all_last_two_digits_first_two_digits_perc = np.zeros((101, 101))
array_all_first_two_digits_2n = np.zeros((101, 101))
array_all_first_two_digits_2n_perc = np.zeros((101, 101))
array_primes = np.zeros((base+1, base+1))
array_complex = np.zeros((base+1, base+1))
num_of_primes = 0
num_of_lesser_twin_primes = 0
num_of_complex = 0
num_of_all = 0

k_current = 0
k = 0

#############################################################
# Presentation
#############################################################

def write_results_to_figures():
    global base
    area_primes = 100
    area_complex = 10
    xmin_perc = 0
    xmax_perc = 100
    xmax_perc_small = base
    ymin_perc = 0
    ymax_perc = 100
    ymax_perc_small = base

    red_patch = mpatches.Patch(color='red', label='primes')
    blue_patch = mpatches.Patch(color='blue', label='complex')
    
    fig = plt.figure(1)
    plt.clf()
    plt.scatter(list_primes_digits[1], list_primes_perc_of_next_milestone[0], s=area_primes, c='red', label='prime', alpha=0.2, edgecolors='none')
    plt.scatter(list_complex_digits[1], list_complex_perc_of_next_milestone[0], s=area_complex, c='blue', label='complex', alpha=0.2, edgecolors='none')
    fig.suptitle("last digit x perc to next 2^n", fontsize=10)
    plt.legend(handles=[red_patch, blue_patch], loc='upper right', bbox_to_anchor=(1, 1), fontsize=6)
    plt.savefig(file_output_fig1)
    plt.close(fig)

    fig = plt.figure(2)
    plt.clf()
    plt.scatter(list_primes_digits[1], list_primes_perc_of_next_milestone[0], s=area_primes, c='red', label='prime', alpha=0.2, edgecolors='none')
    fig.suptitle("last digit x perc to next 2^n - primes only", fontsize=10)
    plt.savefig(file_output_fig2)
    plt.close(fig)

    fig = plt.figure(3)
    plt.clf()
    plt.scatter(list_complex_digits[1], list_complex_perc_of_next_milestone[0], s=area_complex, c='blue', label='complex', alpha=0.2, edgecolors='none')
    fig.suptitle("last digit x perc to next 2^n - complex only", fontsize=10)
    plt.savefig(file_output_fig3)
    plt.close(fig)

    fig = plt.figure(4)
    plt.clf()
    plt.scatter(list_primes_digits[0], list_primes_perc_of_next_milestone[0], s=area_primes, c='red', label='prime', alpha=0.2, edgecolors='none')
    plt.scatter(list_complex_digits[0], list_complex_perc_of_next_milestone[0], s=area_complex, c='blue', label='complex', alpha=0.2, edgecolors='none')
    fig.suptitle("no of digits x perc to next 2^n", fontsize=10)
    plt.legend(handles=[red_patch, blue_patch], loc='upper right', bbox_to_anchor=(1, 1), fontsize=6)
    plt.savefig(file_output_fig4)
    plt.close(fig)

    fig = plt.figure(5)
    plt.clf()
    plt.scatter(list_primes_digits[0], list_primes_perc_of_next_milestone[0], s=area_primes, c='red', label='prime', alpha=0.2, edgecolors='none')
    fig.suptitle("no of digits x perc to next 2^n - primes only", fontsize=10)
    plt.savefig(file_output_fig5)
    plt.close(fig)

    fig = plt.figure(6)
    plt.clf()
    plt.scatter(list_complex_digits[0], list_complex_perc_of_next_milestone[0], s=area_complex, c='blue', label='complex', alpha=0.2, edgecolors='none')
    fig.suptitle("no of digits x perc to next 2^n - complex only", fontsize=10)
    plt.savefig(file_output_fig6)
    plt.close(fig)

    fig = plt.figure(7)
    plt.clf()
    plt.scatter(list_primes_perc_of_next_milestone[0], list_primes_perc_of_next_milestone[1], s=area_primes, c='red', label='primes', alpha=0.2, edgecolors='none')
    plt.scatter(list_complex_perc_of_next_milestone[0], list_complex_perc_of_next_milestone[1], s=area_complex, c='blue', label='complex', alpha=0.2, edgecolors='none')
    fig.suptitle("perc to next 2^n x perc to next 3^n", fontsize=10)
    plt.legend(handles=[red_patch, blue_patch], loc='upper right', bbox_to_anchor=(1, 1), fontsize=6)
    plt.savefig(file_output_fig7)
    plt.close(fig)

    fig = plt.figure(8)
    plt.clf()
    plt.scatter(list_primes_perc_of_next_milestone[0], list_primes_perc_of_next_milestone[1], s=area_primes, c='red', label='primes', alpha=0.2, edgecolors='none')
    fig.suptitle("perc to next 2^n x perc to next 3^n - primes only", fontsize=10)
    plt.savefig(file_output_fig8)
    plt.close(fig)

    fig = plt.figure(9)
    plt.clf()
    plt.scatter(list_complex_perc_of_next_milestone[0], list_complex_perc_of_next_milestone[1], s=area_complex, c='blue', label='complex', alpha=0.2, edgecolors='none')
    fig.suptitle("perc to next 2^n x perc to next 3^n - complex only", fontsize=10)
    plt.savefig(file_output_fig9)
    plt.close(fig)

    fig = plt.figure(10)
    plt.clf()
    plt.scatter(list_primes_digits [2], list_primes_perc_of_next_milestone[0], s=area_primes, c='red', label='prime', alpha=0.2, edgecolors='none')
    plt.scatter(list_complex_digits [2], list_complex_perc_of_next_milestone[0], s=area_complex, c='blue', label='complex', alpha=0.2, edgecolors='none')
    fig.suptitle("last two digits x perc to next 2^n", fontsize=10)
    plt.legend(handles=[red_patch, blue_patch], loc='upper right', bbox_to_anchor=(1, 1), fontsize=6)
    plt.savefig(file_output_fig10)
    plt.close(fig)

    fig = plt.figure(11)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_primes_last_two_digits_2n_perc)
    fig.suptitle("color map - primes - last two digits x perc to next 2^n", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig11)
    plt.close(fig)

    fig = plt.figure(12)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_complex_last_two_digits_2n_perc)
    fig.suptitle("color map - complex - last two digits x perc to next 2^n", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig12)
    plt.close(fig)

    fig = plt.figure(13)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_all_last_two_digits_2n_perc)
    fig.suptitle("color map - all - last two digits x perc to next 2^n", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig13)
    plt.close(fig)

    fig = plt.figure(14)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_primes_2n_3n_perc)
    fig.suptitle("color map - primes - perc to next 2^n x perc to next 3^n", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig14)
    plt.close(fig)

    fig = plt.figure(15)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_complex_2n_3n_perc)
    fig.suptitle("color map - complex - perc to next 2^n x perc to next 3^n", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig15)
    plt.close(fig)

    fig = plt.figure(16)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_all_2n_3n_perc)
    fig.suptitle("color map - all - perc to next 2^n x perc to next 3^n", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig16)
    plt.close(fig)

    fig = plt.figure(17)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_primes_first_two_digits_2n_perc)
    fig.suptitle("color map - primes - first two digits x perc to next 2^n", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig17)
    plt.close(fig)

    fig = plt.figure(18)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_complex_first_two_digits_2n_perc)
    fig.suptitle("color map - complex - first two digits x perc to next 2^n", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig18)
    plt.close(fig)

    fig = plt.figure(19)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_all_first_two_digits_2n_perc)
    fig.suptitle("color map - all - first two digits x perc to next 2^n", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig19)
    plt.close(fig)

    fig = plt.figure(20)
    plt.clf()
    plt.scatter(list_primes_digits [3], list_primes_perc_of_next_milestone[0], s=area_primes, c='red', label='prime', alpha=0.2, edgecolors='none')
    plt.scatter(list_complex_digits [3], list_complex_perc_of_next_milestone[0], s=area_complex, c='blue', label='complex', alpha=0.2, edgecolors='none')
    fig.suptitle("first two digits x perc to next 2^n", fontsize=10)
    plt.legend(handles=[red_patch, blue_patch], loc='upper right', bbox_to_anchor=(1, 1), fontsize=6)
    plt.savefig(file_output_fig20)
    plt.close(fig)

    fig = plt.figure(21)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_primes_last_two_digits_first_two_digits_perc)
    fig.suptitle("color map - primes - last two digits x first two digits", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig21)
    plt.close(fig)

    fig = plt.figure(22)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_complex_last_two_digits_first_two_digits_perc)
    fig.suptitle("color map - complex - last two digits x first two digits", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig22)
    plt.close(fig)

    fig = plt.figure(23)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc])
    axes.set_ylim([ymin_perc,ymax_perc])
    plt.pcolor(array_all_last_two_digits_first_two_digits_perc)
    fig.suptitle("color map - all - last two digits x first two digits", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig23)
    plt.close(fig)

    fig = plt.figure(24)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc_small])
    axes.set_ylim([ymin_perc,ymax_perc_small])
    plt.pcolor(array_primes)
    fig.suptitle("color map - primes - x, y", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig24)
    plt.close(fig)

    fig = plt.figure(25)
    plt.clf()
    axes = plt.gca()
    axes.set_xlim([xmin_perc,xmax_perc_small])
    axes.set_ylim([ymin_perc,ymax_perc_small])
    plt.pcolor(array_complex)
    fig.suptitle("color map - complex - x, y", fontsize=10)
    plt.colorbar()
    plt.savefig(file_output_fig25)
    plt.close(fig)

    fig = plt.figure(26)
    plt.clf()
    r_patch = mpatches.Patch(color='red', label='lesser/primes')
    g_patch = mpatches.Patch(color='green', label='lesser/complex')
    b_patch = mpatches.Patch(color='blue', label='lesser/all')
    list_of_handles = []
    list_of_handles.append(r_patch)
    list_of_handles.append(g_patch)
    list_of_handles.append(b_patch)
    plt.plot(list_checkpoints, list_lesser_twin_primes_ratio[0], 'r.', ms=2)
    plt.plot(list_checkpoints, list_lesser_twin_primes_ratio[1], 'b.', ms=2)
    plt.plot(list_checkpoints, list_lesser_twin_primes_ratio[2], 'g.', ms=2)
    plt.legend(handles=list_of_handles, loc='upper right', bbox_to_anchor=(0.4, 0.8))
    fig.suptitle("Lesser of twin primes vs. other numbers", fontsize=10)
    plt.savefig(file_output_fig26)
    plt.close(fig)

def update_color_maps (perc_2n, perc_3n, two_first_digits, two_last_digits, x, y, is_prime):
    global array_primes_last_two_digits_2n, array_primes_last_two_digits_2n_perc, num_of_primes
    global array_primes_first_two_digits_2n, array_primes_first_two_digits_2n_perc
    global array_complex_last_two_digits_2n, array_complex_last_two_digits_2n_perc, num_of_complex
    global array_complex_first_two_digits, array_complex_first_two_digits_2n_perc
    global array_all_last_two_digits_2n, array_all_last_two_digits_2n_perc, num_of_all
    global array_all_first_two_digits_2n, array_all_first_two_digits_2n_perc
    global array_primes_2n_3n, array_primes_2n_3n_perc, array_complex_2n_3n, array_complex_2n_3n_perc, array_all_2n_3n, array_all_2n_3n_perc
    global array_primes, array_complex

    if is_prime:
        array_primes_last_two_digits_2n[perc_2n][two_last_digits] += 1
        array_primes_first_two_digits_2n[perc_2n][two_first_digits] += 1
        array_primes_last_two_digits_first_two_digits[two_first_digits][two_last_digits] += 1
        array_primes_2n_3n [perc_2n][perc_3n] += 1
        array_primes [x][y] += 1
        
        for i in range (0, 100):
            for j in range (0, 100):
                array_primes_last_two_digits_2n_perc[i][j] = array_primes_last_two_digits_2n[i][j]/num_of_primes
                array_primes_last_two_digits_first_two_digits_perc[i][j] = array_primes_last_two_digits_first_two_digits[i][j]/num_of_primes
                array_primes_first_two_digits_2n_perc[i][j] = array_primes_first_two_digits_2n[i][j]/num_of_primes
                array_primes_2n_3n_perc[i][j] = array_primes_2n_3n[i][j]/num_of_primes

        for i in range (0, base):
            for j in range (0, base):
                array_primes [i][j] += array_primes [i][j]/num_of_primes

    else:
        array_complex_last_two_digits_2n[perc_2n][two_last_digits] += 1
        array_complex_last_two_digits_first_two_digits[two_first_digits][two_last_digits] += 1
        array_complex_first_two_digits_2n[perc_2n][two_first_digits] += 1
        array_complex_2n_3n [perc_2n][perc_3n] += 1
        array_complex [x][y] += 1
        
        for i in range (0, 100):
            for j in range (0, 100):
                array_complex_last_two_digits_2n_perc[i][j] = array_complex_last_two_digits_2n[i][j]/num_of_complex
                array_complex_last_two_digits_first_two_digits_perc[i][j] = array_complex_last_two_digits_first_two_digits[i][j]/num_of_complex
                array_complex_first_two_digits_2n_perc[i][j] = array_complex_first_two_digits_2n[i][j]/num_of_complex
                array_complex_2n_3n_perc[i][j] = array_complex_2n_3n[i][j]/num_of_complex

        for i in range (0, base):
            for j in range (0, base):
                array_complex [i][j] += array_complex [i][j]/num_of_complex

    array_all_last_two_digits_2n[perc_2n][two_last_digits] += 1
    array_all_last_two_digits_first_two_digits[two_first_digits][two_last_digits] += 1
    array_all_first_two_digits_2n[perc_2n][two_first_digits] += 1
    array_all_2n_3n [perc_2n][perc_3n] += 1

    for i in range (0, 100):
        for j in range (0, 100):
            array_all_last_two_digits_2n_perc[i][j] = array_all_last_two_digits_2n[i][j]/num_of_all
            array_all_first_two_digits_2n_perc[i][j] = array_all_first_two_digits_2n[i][j]/num_of_all
            array_all_last_two_digits_first_two_digits_perc[i][j] = array_all_first_two_digits_2n[i][j]/num_of_all
            array_all_2n_3n_perc[i][j] = array_all_2n_3n[i][j]/num_of_all
            
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
if continue_previous_calculations:
    print ("Restoring previous results...")
    restore_previous_results (file_output_pickle)
    if k_current > 0:
        min_num = k_current
        k = k_current
        print ("Resuming calculations at", min_num)
    print ("DONE")

# new calculations
for k in range (min_num, max_num):

    is_prime = False
    if p.is_prime (k):
        is_prime = True

    digits = c.get_number_of_dec_digits (k)
    last_digit = c.get_last_dec_digit (k)
    two_last_digits = c.get_last_two_dec_digits (k)
    two_first_digits = c.get_first_two_dec_digits (k)
    next_2n = c.get_next_greater_power_of_two (k)
    next_3n = c.get_next_greater_power_of_three (k)
    
    perc_2n = int((k - next_2n/2)/(next_2n - next_2n/2)*100)
    perc_3n = int((k - next_3n/3)/(next_3n - next_3n/3)*100)

    x = int (k / base) % base
    y = k % base

    num_of_all += 1
    if is_prime:
        list_primes_digits[0].append (digits)
        list_primes_digits[1].append (last_digit)
        list_primes_digits[2].append (two_last_digits)
        list_primes_digits[3].append (two_first_digits)
        list_primes_perc_of_next_milestone[0].append (perc_2n)
        list_primes_perc_of_next_milestone[1].append (perc_3n)
        if p.is_lesser_twin_prime (k):
            num_of_lesser_twin_primes += 1
        num_of_primes += 1
    else:
        list_complex_digits[0].append (digits)
        list_complex_digits[1].append (last_digit)
        list_complex_digits[2].append (two_last_digits)
        list_complex_digits[3].append (two_first_digits)
        list_complex_perc_of_next_milestone[0].append (perc_2n)
        list_complex_perc_of_next_milestone[1].append (perc_3n)
        num_of_complex += 1

    list_checkpoints.append(k)
    if num_of_primes > 0:
        ratio1 = num_of_lesser_twin_primes/num_of_primes
    else:
        ratio1 = 0
    if num_of_complex > 0:
        ratio2 = num_of_lesser_twin_primes/num_of_complex
    else:
        ratio2 = 0
    if num_of_all > 0: 
        ratio3 = num_of_lesser_twin_primes/num_of_all
    else:
        ratio3 = 0
    list_lesser_twin_primes_ratio[0].append(ratio1)
    list_lesser_twin_primes_ratio[1].append(ratio2)
    list_lesser_twin_primes_ratio[2].append(ratio3)
        
    update_color_maps (perc_2n, perc_3n, two_first_digits, two_last_digits, x, y, is_prime)

    # checkpoint - partial results
    if (k - min_num) % checkpoint_value == 0:

        perc_completed = str(int(k * 100 / max_num))
        print ("Checkpoint", k, "of total", max_num, "(" + perc_completed + "% completed)")
   
        # save results collected so far
        write_results_to_figures ()
        k_current = k

# final results
perc_completed = str(int(k * 100 / max_num))
write_results_to_figures ()
k_current = max_num

