#
# Copyright (c) 2018-2020, Marcin Barylski
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

import math

#############################################################
# Class
#############################################################

class Calculations:

    def get_next_greater_power_of_two (self, n):
        return (2**(n - 1).bit_length())

    def get_next_greater_power_of_three (self, n):
        return (3**math.ceil(math.log(n, 3)))

    def get_number_of_dec_digits (self, n):
        return (int(math.log10(n)) + 1)

    def get_last_dec_digit (self, n):
        return (n % 10)

    def get_last_two_dec_digits (self, n):
        return (n % 100)

    def get_first_two_dec_digits (self, n):
        return (int(str(n)[:2]))

    def calculate_3a_2b (self, n):
        done = False
        a = int(n/3)
        b = 1
        while not done:
            remainder = n - 3*a
            b = int(remainder / 2)
            if b < 1:
                a -= 1
            if a < 1:
                break
            if a >= 1 and b >= 1:
                done = True
                break
        return (a, b)

    def calculate_2a_3b (self, n):
        done = False
        a = int(n/2)
        b = 1
        while not done:
            remainder = n - 2*a
            b = int(remainder / 3)
            if b < 1:
                a -= 1
            if a < 1:
                break
            if a >= 1 and b >= 1:
                done = True
                break
        return (a, b)

    def get_all_subnums (self, n, l, include_last):
        s = str(n)
        result_s = [s[i: j] for i in range(len(s)) 
            for j in range(i + 1, len(s) + 1)]
        result = []
        for v in result_s:
            if len(v) == l:
                result.append (int(v))
        if not include_last and len(result) > 0:
            del result[-1]
        return result

    def get_avg_from_dict (self, d):
        c = 0
        s = 0
        for k in d:
            s += d[k]
            c += 1
        return (s/c)

    def new_dict_from_avg (self, d):
        nd = {}
        try:
            avg = self.get_avg_from_dict (d)
        except:
            avg = 1
        for k in d:
            nd[k] = d[k] - avg
        return (nd)
        
