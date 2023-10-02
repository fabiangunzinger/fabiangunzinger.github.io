---
title: Chapter 4 - Euclid's solution
---

``` python
import checks
```

## Finding primes

-   A prime number is any positive number larger than 1 that cannot be written as a product of two smaller numbers.

-   Here I want to compare the performance of three different functions to compare prime numbers.

### v1 - basic prime finder

``` python
def is_prime1(n: int) -> bool:
    """
    n is prime if it's larger than 2 and not
    divisible by any smaller number other than 1.
    """ 
    return n >= 2 and all(n % d != 0 for d in range(2, n))


assert all(is_prime1(n) for n in [2, 3, 5, 7, 11, 13, 17, 19, 23])
assert all(not is_prime1(n) for n in [4, 6, 8, 9, 10])
```

A helper function to find primes up to `n` with a given prime finder function.

``` python
from typing import List

def primes_up_to1(n: int) -> List[int]:
    return [i for i in range(2, n + 1) if is_prime1(i)]

assert primes_up_to1(20) == [2, 3, 5, 7, 11, 13, 17, 19]
assert primes_up_to1(100)[-3:] == [83, 89, 97]
```

Let's check how this scales.

``` python
import time
from typing import Callable

def prime_timings(func: Callable[[int], list[int]], power_max: int = 6):
    left_cell_width = power_max + 3
    print(f"{'n':>{left_cell_width}}  {'time':>12}")
    for power in range(2, power_max):
        n = 10 ** power
        start = time.perf_counter()
        func(n)
        end = time.perf_counter()
        time_in_ms = (end - start) * 1000        
        print(f"{n:>{left_cell_width},}: {time_in_ms:>10.3f}ms")
    
prime_timings(primes_up_to1)
```

            n          time
          100:      0.130ms
        1,000:      7.308ms
       10,000:    477.183ms
      100,000:  34922.543ms

### v2 - check up to sqrt(n) only

Improved finder checking only up to sqrt(n)

-   This uses the fact that if a and b \> sqrt(n), then a x b \> n.

-   This implies that for a \> sqrt(n), all solutions will be mirror images of earlier solutions.

-   For example: if n = 36, all solutions for a \> 6 will have already been checked but with a and b reversed - 36/2=18 will come up as 36/18=2, and similar for a = 3 and a = 4

-   Python creates ranges with integer boundaries. So, to implement this, we check all values up to `int(sqrt(n)) + 1`, which rounds the sqrt value down to the nearest integer and adds 1. Why do we need to add 1?

    -   It is *not* because we cound the sqrt result down to the next integer. This makes no difference. Because given that we want to check whether there are solutions where n can be written as the product of two integers, there are only two possible cases of interest here: either sqrt(n) is an integer, in which case the rounding has no effect, or it is a non-integer digit, in which case we care about its integer part only. Hence, rounding away the decimal part of non-integer square roots is no loss.

    -   It *is* to ensure that `range(2, ...)` generates the correct sequence of potential primes to check. For values of sqrt(n) \< 4, range is an empty list (because `range(2, 2)` and `range(2, 3)` are both empty). For sqrt(n) \>= 4, things work as intended. (Note, however, that we still don't properly implement our logic, since `range(2, sqrt(16))` returns `[2, 3]`, and the only reason multiples of 4 are eliminated from the returned list is because they are also multiples of 2, and similar for all higher values.

    -   Actually, the even simpler way to think about it is that it's nothing else than ensuring that if we want to create a range from a to b, both inclusive, we need to call `range(a, b + 1)`.

``` python
import math

def int_sqrt(n: int) -> int:
    return int(math.sqrt(n))

def is_prime2(n: int) -> bool:
    return n >= 2 and all(n % d != 0 for d in range(2, int_sqrt(n) + 1))


assert all(is_prime2(n) for n in [2, 3, 5, 7, 11, 13, 17, 19, 23])
assert all(not is_prime2(n) for n in [4, 6, 8, 9, 10])
```

``` python
def primes_up_to2(n: int) -> List[int]:
    return [i for i in range(2, n + 1) if is_prime2(i)]

assert primes_up_to2(20) == [2, 3, 5, 7, 11, 13, 17, 19]
assert primes_up_to2(100)[-3:] == [83, 89, 97]
```

``` python
prime_timings(primes_up_to2)
```

            n          time
          100:      0.095ms
        1,000:      1.342ms
       10,000:     15.906ms
      100,000:    250.009ms

-   This is already much faster than the above. It's the difference in complexity of `n*n` vs `n * sqrt(n)`.
-   But it still doesn't scale very well -- try finding all primes up to 1,000,000,000...!

### v3 - sieve

-   Each number that isn't prime is necessarily divisible by a number that is prime.

``` python
def primes_up_to3(n: int) -> List[int]: 
    candidates = range(2, n + 1)
    primes = []
    
    while candidates:
        # The smallest remaining element must be prime, since it
        # wasn't divisible by any prime smaller than itself.
        p = candidates[0]
        primes.append(p)
        
        # Remove all multiples of p as not-prime
        candidates = [c for c in candidates if c % p > 0]
        
    return primes


# Testing
assert primes_up_to3(10) == [2, 3, 5, 7]
assert primes_up_to3(100)[-3:] == [83, 89, 97]


# Timing
prime_timings(primes_up_to3)
```

            n          time
          100:      0.066ms
        1,000:      1.012ms
       10,000:     52.278ms
      100,000:   2546.478ms

-   This is slower than v2 - what's going on?
-   Profiling shows that we spend most time inside the list comprehension.
-   Let's eliminate unnecessary work there.

``` python
import cProfile
cProfile.run('primes_up_to3(100_000)')
```

             19188 function calls in 3.264 seconds

       Ordered by: standard name

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.095    0.095    3.264    3.264 3434994521.py:1(primes_up_to3)
         9592    3.167    0.000    3.167    0.000 3434994521.py:12(<listcomp>)
            1    0.000    0.000    3.264    3.264 <string>:1(<module>)
            1    0.000    0.000    3.264    3.264 {built-in method builtins.exec}
         9592    0.001    0.000    0.001    0.000 {method 'append' of 'list' objects}
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

``` python
def primes_up_to4(n: int) -> List[int]:
    # Make indices correspond to numeric value of item
    candidates = [False, False] + [True] * (n - 1)
    
    for p in range(2, int_sqrt(n) + 1):
        # If we haven't eliminated p as prime yet
        if candidates[p]:
            for m in range(p * p, n + 1, p):
                candidates[m] = False
                
    # Return indices we haven't eliminated
    return [n for n, prime in enumerate(candidates) if prime]


# Testing
assert primes_up_to4(10) == [2, 3, 5, 7]
assert primes_up_to4(100)[-3:] == [83, 89, 97]

# Timing
prime_timings(primes_up_to4)
```

            n          time
          100:      0.031ms
        1,000:      0.117ms
       10,000:      1.075ms
      100,000:     13.205ms

-   This is *much* faster!

### Finding prime factors

-   Every number can be written uniquely as the product of prime numbers. This is called "prime factorisation".
-   Using the sieve, finding the prime factors is straightforward. The only thing to remember that each prime factor might divide the number more than once.

``` python
def factorise(n: int) -> List[int]:
    primes = primes_up_to4(n)
    factors = []
    for p in primes:      
        # A prime might divide n more than once
        while n % p == 0:
            factors.append(p)
            n /= p
        # If we reach 1, there are no more prime factors.
        if n == 1:
            break
        
    return factors

assert factorise(19) == [19]
assert factorise(33) == [3, 11]
assert factorise(150) == [2, 3, 5, 5]
```

## GCD and LCM

``` python
import functools
import operator

def gcd_factorise(n: int, m: int) -> int:
    factors_n = factorise(n)
    factors_m = factorise(m)
    gcd = 1
    
    while factors_n and factors_m:
        # Largest factors are equal, multiply gcd by that factor
        if factors_n[-1] == factors_m[-1]:
            gcd *= factors_n.pop()
            factors_m.pop()
        # Largest factor of n is not a factor of m
        elif factors_n[-1] > factors_m[-1]:
            factors_n.pop()
        # Largest factor of m is not a factor of n
        else:
            factors_m.pop()
    
    return gcd
        
    

assert gcd_factorise(3, 12) == 3
assert gcd_factorise(11, 21) == 1
assert gcd_factorise(555, 225) == 15
```

``` python
def lcm_factorise(n: int, m: int) -> int:
    factors_n = factorise(n)
    factors_m = factorise(m)
    lcm = 1
    
    while factors_n or factors_m:
        if not factors_n:
            lcm *= factors_m.pop()
        elif not factors_m:
            lcm *= factors_n.pop()
        elif factors_n[-1] == factors_m[-1]:
            lcm *= factors_n.pop()
            factors_m.pop()
        elif factors_n[-1] < factors_m[-1]:
            lcm *= factors_m.pop()
        else:
            lcm *= factors_n.pop()
    
    return lcm


assert lcm_factorise(1, 5) == 5
assert lcm_factorise(2, 7) == 14
assert lcm_factorise(7, 9) == 63
```

-   The factors of 15 are \[3, 5\].
-   `gcd(n, m)` returns the product of the common factors of n and m.
-   Hence, `gcd(n, 15)` is 1 if neither 3 nor 15 are factors of n, 3 if 3 but not 5 is a factor of n, 5 if 5 but not 3 is a factor of n, and 15 if both are factors of n.
-   m is divisible by n iff n is a factor of m.
-   This leads to the solution below.

``` python
def fizz_buzz(n):
    choices = {1: str(n), 3: 'fizz', 5: 'buzz', 15: 'fizzbuzz'}
    return choices[math.gcd(n, 15)]
```

-   What if we didn't have access to `math.gcd` and needed a fast way to calculate the gcd?
-   This is where Euclid comes in.

## Euclids solution

Euclid's gcd algorithm is mighty clever. It relies on the following:

-   For n \>= m, where n = cm + r, we have: gcd(n, m) = gcd(m, n%m). To convince yourself intuitively, think of n and m being composed of LEGO bricks, and notice that as we form the reminder, we take a number of complete bricks (cm) away from another number of complete bricks (n), so that what is left over is necessarily a full number of bricks (hence, the remainder shares that divisor of n and m). Notice also that we didn't specify anything about the "width" of the bricks, so that this is true for all possible brick. Mathematically, using n = cm + r, it can be shown that and number that divides n and m also divides r, and that any number that divides m and r also divides n, so that {divisors of n and m} = {divisors of m and r}, which implies that the largest element of the two sets, the gcd, is also equal.

-   The above statement is recursively true: gcd(n, m) = gcd(m, n%m) = gcd(n%m, m%(n%m)) = ...

-   In the above recursive applicatioin of the statement, n and m keep getting smaller, since, necessarily, n%m \< m (if that weren't true, we can increase c).

-   The process comes to a stop once n%m = 0, in which case m divides n without a reminder, is -- of course -- the largest divisor of itself, and is thus the gcd.

-   The above happens either once m = 1 or earlier.

``` python
def gcd(n: int, m: int) -> int:
    """Euclid's algorithm."""
    # Ensure that n >= m
    n, m = max(n, m), min(n, m)
    
    # Recursively apply gcm(n, m) = gcm(m, n % m) until n % m == 0
    while n % m > 0:
        n, m = m, n % m
        
    # If n % m is 0, m is the gcd
    return m


assert gcd(4, 2) == 2
assert gcd(25, 5) == 5
assert gcd(75, 45) == 15
```

We can use that for our fizzbuzz solution above.

``` python
def fizz_buzz(n: int) -> str:
    choices = {1: str(n), 3: 'fizz', 5: 'buzz', 15: 'fizzbuzz'}
    return choices[gcd(n, 15)]


# Tests
checks.check_function(fizz_buzz)
```
