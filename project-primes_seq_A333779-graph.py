#
# Copyright (c) 2019 - 2020, Marcin Barylski
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

import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
sys.path.insert(0, '..\\primes\\')
import primes
sys.path.insert(0, '..\\goldbach-partition\\')
import dataprocessing
import numpy as np
from scipy.optimize import curve_fit
import scipy
from scipy import optimize

#############################################################
# Settings - configuration
#############################################################

#############################################################
# Settings - output directory and files
#############################################################


#############################################################
# Business logic
#############################################################

def func(x, a, b, c):
    return (a * (x ** b) + c)

def func2(x, a, b):
    return (a * (x ** b))

def func3(x, a, b):
    return ((a / x) + b)

x = np.arange(40000)

##fig = plt.figure(1)
##plt.clf()
##plt.plot(x, func(x, 7.41655618, 1.12453747, -58.31764747 ), 'r-', label="terms: 1000")
##plt.plot(x, func(x, 8.59135892, 1.10523239, -260.5197196 ), 'b-', label="terms: 5000")
##plt.plot(x, func(x, 9.03416325, 1.09946314, -434.81544801 ), 'g-', label="terms: 10000")
##plt.plot(x, func(x, 9.67494142, 1.09211763, -884.89244159 ), 'y-', label="terms: 20000")
##plt.plot(x, func(x, 9.97948888e+00, 1.08898433e+00, -1.23465676e+03 ), 'm-', label="terms: 30000")
##plt.plot(x, func(x, 1.02739033e+01, 1.08614446e+00, -1.69756790e+03 ), 'k-', label="terms: 40000")
##plt.legend (loc='upper left', fontsize=6)
##plt.savefig("curve_fit.png")
##plt.show()
##plt.close()

##x_data = (1000, 5000, 10000, 20000, 30000, 40000)
##y_data = (7.41655618, 8.59135892, 9.03416325, 9.67494142, 9.97948888e+00, 1.02739033e+01)
##
##params, params_covariance = optimize.curve_fit(func2, x_data, y_data, p0=[2, 2])
##print(params)

##plt.figure(figsize=(6, 4))
##plt.scatter(x_data, y_data)
##popt, pcov = curve_fit(func2, x_data, y_data)
##plt.plot(x, func2(x, *popt), 'r-')
##print (*popt)

x_data = (1000,  2000,  3000,  4000,  5000,  6000,  7000,  8000,  9000,  10000,
          11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
          21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000,
          31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000)
y_data = (6.96830767, 7.39676569, 7.71116401, 7.88797205, 8.12277722, 8.21458396, 8.37057093, 8.47069868, 8.56506153, 8.62159545,
          8.76414298, 8.77573025, 8.90075275, 8.85437654, 9.02766378, 9.05616331, 9.08023322, 9.16007285, 9.14854003, 9.22652845,
          9.22652053, 9.26771994, 9.29016354, 9.40337378, 9.39419517, 9.44486097, 9.52108153, 9.51475708, 9.493371,   9.54898231,
          9.62915882, 9.62918219, 9.61484865, 9.65065324, 9.70772857, 9.76505854, 9.77202974, 9.77154319, 9.78572873, 9.81764596) 

#params, params_covariance = optimize.curve_fit(func2, x_data, y_data, p0=[2, 2])
#print(params)

plt.figure(figsize=(6, 10))
plt.scatter(x_data, y_data)
popt, pcov = curve_fit(func3, x_data, y_data)
#plt.plot(x, func3(3, *popt), 'r-')
print (*popt)

plt.show()
plt.close()
