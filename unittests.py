#
# Copyright (c) 2016 - 2018, Marcin Barylski
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

import unittest
import primes
import calculations

################################################################################
# Unit tests
################################################################################

class TestMethods(unittest.TestCase):
    def test_isprime(self):
        p = primes.Primes(False)
        self.assertTrue(p.is_prime(2))
        self.assertTrue(p.is_prime(3))
        self.assertTrue(p.is_prime(5))
        self.assertTrue(p.is_prime(7))
        self.assertTrue(p.is_prime(11))

    def test_isprime_cuda(self):
        p = primes.Primes(False)
        self.assertTrue(p.is_prime_cuda(2))
        self.assertTrue(p.is_prime_cuda(3))
        self.assertTrue(p.is_prime_cuda(5))
        self.assertTrue(p.is_prime_cuda(7))
        self.assertTrue(p.is_prime_cuda(11))

    def test_isnotprime(self):
        p = primes.Primes(False)
        self.assertFalse(p.is_prime(1))
        self.assertFalse(p.is_prime(4))
        self.assertFalse(p.is_prime(6))
        self.assertFalse(p.is_prime(8))
        self.assertFalse(p.is_prime(10))
        self.assertFalse(p.is_prime(3379995))

    def test_isnotprime_cuda(self):
        p = primes.Primes(False)
        self.assertFalse(p.is_prime_cuda(1))
        self.assertFalse(p.is_prime_cuda(4))
        self.assertFalse(p.is_prime_cuda(6))
        self.assertFalse(p.is_prime_cuda(8))
        self.assertFalse(p.is_prime_cuda(10))
        self.assertFalse(p.is_prime_cuda(3379995))

    def test_get_ith_prime(self):
        p = primes.Primes(False)
        p.add_to_primes_set(2)
        p.add_to_primes_set(3)
        p.add_to_primes_set(5)
        p.add_to_primes_set(7)
        p.sort_primes_set()
        self.assertEqual(p.get_ith_prime(0), 2)
        self.assertEqual(p.get_ith_prime(1), 3)
        self.assertEqual(p.get_ith_prime(2), 5)

    def test_get_ith_prime_ahead(self):
        p = primes.Primes(False)
        self.assertEqual(p.get_ith_prime(0), 2)
        self.assertEqual(p.get_ith_prime(1), 3)
        self.assertEqual(p.get_ith_prime(2), 5)
        self.assertEqual(p.get_ith_prime(3), 7)
        self.assertEqual(p.get_ith_prime(4), 11)
        self.assertEqual(p.get_ith_prime(5), 13)
        self.assertEqual(p.get_ith_prime(6), 17)
        self.assertEqual(p.get_ith_prime(7), 19)
        self.assertEqual(p.get_ith_prime(8), 23)
        self.assertEqual(p.get_ith_prime(99), 541)

    def test_get_ith_twinprime(self):
        p = primes.Primes(False)
        p.add_to_twinprimes_set(3)
        p.add_to_twinprimes_set(5)
        p.add_to_twinprimes_set(7)
        p.add_to_twinprimes_set(11)
        p.add_to_twinprimes_set(13)
        p.sort_twinprimes_set()
        self.assertEqual(p.get_ith_twinprime(0), 3)
        self.assertEqual(p.get_ith_twinprime(1), 5)
        self.assertEqual(p.get_ith_twinprime(2), 7)
        self.assertEqual(p.get_ith_twinprime(3), 11)
        self.assertEqual(p.get_ith_twinprime(4), 13)

    def test_get_ith_twinprime_ahead(self):
        p = primes.Primes(False)
        self.assertEqual(p.get_ith_twinprime(0), 3)
        self.assertEqual(p.get_ith_twinprime(1), 5)
        self.assertEqual(p.get_ith_twinprime(2), 7)
        self.assertEqual(p.get_ith_twinprime(3), 11)
        self.assertEqual(p.get_ith_twinprime(4), 13)
        self.assertEqual(p.get_ith_twinprime(5), 17)
        self.assertEqual(p.get_ith_twinprime(6), 19)
        self.assertEqual(p.get_ith_twinprime(7), 29)
        self.assertEqual(p.get_ith_twinprime(8), 31)

    def test_is_in_nonprime_set(self):
        p = primes.Primes(False)
        p.add_to_primes_set(2)
        p.add_to_primes_set(3)
        p.add_to_primes_set(5)
        p.add_to_primes_set(7)
        p.add_to_nonprimes_set(4)
        p.add_to_nonprimes_set(6)
        p.add_to_nonprimes_set(8)
        self.assertTrue(p.is_in_nonprimes_set(4))
        self.assertTrue(p.is_in_nonprimes_set(6))
        self.assertTrue(p.is_in_nonprimes_set(8))

    def test_is_in_nonprime_set_negative(self):
        p = primes.Primes(False)
        p.add_to_primes_set(2)
        p.add_to_primes_set(3)
        p.add_to_primes_set(5)
        p.add_to_primes_set(7)
        p.add_to_nonprimes_set(4)
        p.add_to_nonprimes_set(6)
        p.add_to_nonprimes_set(8)
        self.assertFalse(p.is_in_nonprimes_set(2))
        self.assertFalse(p.is_in_nonprimes_set(3))
        self.assertFalse(p.is_in_nonprimes_set(7))

    def test_is_lesser_twin_prime(self):
        p = primes.Primes(False)
        self.assertTrue(p.is_lesser_twin_prime(3))
        self.assertTrue(p.is_lesser_twin_prime(5))
        self.assertTrue(p.is_lesser_twin_prime(11))
        self.assertFalse(p.is_lesser_twin_prime(13))
        self.assertFalse(p.is_lesser_twin_prime(2))
        self.assertFalse(p.is_lesser_twin_prime(9))

    def test_is_greater_twin_prime(self):
        p = primes.Primes(False)
        self.assertTrue(p.is_greater_twin_prime(5))
        self.assertTrue(p.is_greater_twin_prime(7))
        self.assertTrue(p.is_greater_twin_prime(13))
        self.assertFalse(p.is_greater_twin_prime(11))
        self.assertFalse(p.is_greater_twin_prime(2))
        self.assertFalse(p.is_greater_twin_prime(9))

    def test_is_symmetric_prime(self):
        p = primes.Primes(False)
        self.assertEqual(p.is_symmetric_prime(3,0), (True, 3, 3))
        self.assertEqual(p.is_symmetric_prime(13,0), (True, 13, 13))
        self.assertEqual(p.is_symmetric_prime(5,2), (True, 3, 7))
        self.assertEqual(p.is_symmetric_prime(4,1), (True, 3, 5))
        self.assertEqual(p.is_symmetric_prime(10,1), (False, 0, 0))
        self.assertEqual(p.is_symmetric_prime(12,0), (False, 0, 0))

    def test_factorize(self):
        p = primes.Primes(False)
        self.assertEqual(p.factorize(3), [3])
        self.assertEqual(p.factorize(5), [5])
        self.assertEqual(p.factorize(6), [2,3])
        self.assertEqual(p.factorize(20), [2,2,5])

    def test_get_next_greater_power_of_two(self):
        c = calculations.Calculations()
        self.assertEqual(c.get_next_greater_power_of_two(2), 2)
        self.assertEqual(c.get_next_greater_power_of_two(3), 4)
        self.assertEqual(c.get_next_greater_power_of_two(4), 4)
        self.assertEqual(c.get_next_greater_power_of_two(5), 8)
        self.assertEqual(c.get_next_greater_power_of_two(6), 8)
        self.assertEqual(c.get_next_greater_power_of_two(7), 8)
        self.assertEqual(c.get_next_greater_power_of_two(250), 256)

    def test_get_next_greater_power_of_three(self):
        c = calculations.Calculations()
        self.assertEqual(c.get_next_greater_power_of_three(2), 3)
        self.assertEqual(c.get_next_greater_power_of_three(3), 3)
        self.assertEqual(c.get_next_greater_power_of_three(4), 9)
        self.assertEqual(c.get_next_greater_power_of_three(25), 27)

    def test_get_number_of_dec_digits(self):
        c = calculations.Calculations()
        self.assertEqual(c.get_number_of_dec_digits(2), 1)
        self.assertEqual(c.get_number_of_dec_digits(5), 1)
        self.assertEqual(c.get_number_of_dec_digits(234), 3)
        self.assertEqual(c.get_number_of_dec_digits(123456789), 9)

    def test_get_last_dec_digit(self):
        c = calculations.Calculations()
        self.assertEqual(c.get_last_dec_digit(2), 2)
        self.assertEqual(c.get_last_dec_digit(123), 3)
        self.assertEqual(c.get_last_dec_digit(982917), 7)

    def test_get_last_two_dec_digits(self):
        c = calculations.Calculations()
        self.assertEqual(c.get_last_two_dec_digits(2), 2)
        self.assertEqual(c.get_last_two_dec_digits(123), 23)
        self.assertEqual(c.get_last_two_dec_digits(982917), 17)

    def test_get_first_two_dec_digits(self):
        c = calculations.Calculations()
        self.assertEqual(c.get_first_two_dec_digits(2), 2)
        self.assertEqual(c.get_first_two_dec_digits(123), 12)
        self.assertEqual(c.get_first_two_dec_digits(982917), 98)
    
################################################################################
# Main - run unit tests
################################################################################

unittest.main()
