---
title: Notes on fizzbuzz by Joel Grus
---

Book repo is [here](https://github.com/joelgrus/fizzbuzz).

``` python
import math

from hypothesis import given
import hypothesis.strategies as st
```

## My solution

``` python
def fizzbuzz(n):
    if n % 15 == 0:
        return "fizzbuzz"
    elif n % 5 == 0:
        return "buzz"
    elif n % 3 == 0:
        return "fizz"
    else:
        return str(n)
```

## Chapter 1 - 100 print statements

### Reusability and changeability

Writing output to file

``` python
with open("fizzbuzz.txt", "w") as f:
    for n in range(1, 101):
        f.write(f"{fizzbuzz(n)}\n")
```

Omit vowels

``` python
import re

for n in range(1, 16):
    print(re.sub("[aeiouAEIOU]", "", fizzbuzz(n)))
```

    1
    2
    fzz
    4
    bzz
    fzz
    7
    8
    fzz
    bzz
    11
    fzz
    13
    14
    fzzbzz

``` python
### Testability
```

``` python
Approach:

- Use list below as ground truth.
- Solutions to the fizzbuzz problem are two types of functions: the first type return a list with all 100 values, the second type takes a number and return its fizbuzz value.
- Create a test that compares lists of 100 values to the ground truth.
- Can use this directly for first type of function, and after creating a list of 100 values using second type of function.
```

``` python
Ground truth.
```

``` python
FIZZ_BUZZ = [
    '1', '2', 'fizz', '4', 'buzz', 'fizz', '7', '8', 'fizz',
    'buzz', '11', 'fizz', '13', '14', 'fizzbuzz', '16', '17',
    'fizz', '19', 'buzz', 'fizz', '22', '23', 'fizz', 'buzz',
    '26', 'fizz', '28', '29', 'fizzbuzz', '31', '32', 'fizz',
    '34', 'buzz', 'fizz', '37', '38', 'fizz', 'buzz', '41',
    'fizz', '43', '44', 'fizzbuzz', '46', '47', 'fizz', '49',
    'buzz', 'fizz', '52', '53', 'fizz', 'buzz', '56', 'fizz',
    '58', '59', 'fizzbuzz', '61', '62', 'fizz', '64', 'buzz',
    'fizz', '67', '68', 'fizz', 'buzz', '71', 'fizz', '73',
    '74', 'fizzbuzz', '76', '77', 'fizz', '79', 'buzz',
    'fizz', '82', '83', 'fizz', 'buzz', '86', 'fizz', '88',
    '89', 'fizzbuzz', '91', '92', 'fizz', '94', 'buzz',
    'fizz', '97', '98', 'fizz', 'buzz'
]
```

``` python
Test function design:
- First check that length is correct to avoid unnecessary checking in case it isn't.
- Create list of errors so we can see errors in case there are any (instead of just learning that the list is incorrect, which is not as helpful!).
- Note elegant use of assert statements instead of if/else statements.
```

``` python
from typing import List

def check_output(output: List[str]) -> None:
    assert len(output) == 100, "Output should have length 100"
    
    # Collect all errors in a list
    # The i+1 reflects that output[0] is the output for 1,
    # output[1] the output for 2, and so on
    errors = [
        f"({i+1}) predicted: {output[i]}, actual: {FIZZ_BUZZ[i]}"
        for i in range(100)
        if output[i] != FIZZ_BUZZ[i]
    ]
    
    assert len(errors) == 0, f"{errors}"
```

``` python
Test we expect to pass:
```

``` python
check_output([fizzbuzz(n) for n in range(1, 101)])
```

``` python
Test we expect to fail:
```

``` python
try:
    check_output([fizzbuzz(n) if n % 45 !=0 else 'ho' for n in range(1, 101)])
except AssertionError as e:
    print(e)
```

    ['(45) predicted: ho, actual: fizzbuzz', '(90) predicted: ho, actual: fizzbuzz']

``` python
from typing import Callable

def check_function(fizz_buzz: Callable[[int], str]) -> None:
    """
    Type casting says that fizz_buzz needs to be a 
    function that takes a single argument (which is an `int`)
    and returns a `str`.
    """
    output = [fizz_buzz(n+1) for n in range(100)]
    check_output(output)
```

Test we expect to pass:

``` python
check_function(fizzbuzz)
```

More testing - anagram checker

``` python
def anagrams(s1: str, s2: str) -> bool:
    return sorted(s1) == sorted(s2)

assert anagrams('abc', 'cba')
assert anagrams('lead', 'deal')
assert not anagrams('then', 'than')
assert not anagrams('meet', 'meat')
```

More testing - generate print statements

``` python
def make_print_statement(fizz_buzz: str) -> str:
    return f"print('{fizz_buzz}')"

assert make_print_statement('10') == "print('10')"
assert make_print_statement('fizz') == "print('fizz')"
assert make_print_statement('buzz') == "print('buzz')"
assert make_print_statement('fizzbuzz') == "print('fizzbuzz')"

for fizz_buzz in FIZZ_BUZZ[:5]:
    print(make_print_statement(fizz_buzz))
```

    print('1')
    print('2')
    print('fizz')
    print('4')
    print('buzz')

## Chapter 2 - if / elif / elif / else

This section discusses different solutions that solve the problem without using the modulus operator.

### The canonical solution

(And the way I have solved it.)

### Repeated subtraction

Avoid using modulus to check divisibility by using repeated subtraction.

``` python
def is_divisible_subtract(n: int, d: int) -> bool:
    assert d > 0 and n >= 0
    
    # Subtract d from n until result is smaller than d.
    while n >= d:
        n -= d
    
    # If we reached zero, n was divisible by d.
    return n == 0
```

Manual testing

``` python
divisible_pairs = [
    (0, 3), (3, 3), (6, 3), (9, 3),
    (0, 5), (5, 5), (10, 5), (100, 5),
    (40, 20), (300, 15), (1000, 50)
]

not_divisible_pairs = [
    (1, 3), (4, 3), (5, 3), (8, 3),
    (1, 5), (6, 5), (13, 5), (101, 5),
    (41, 20), (303, 15), (999, 50)
]

for n, d in divisible_pairs:
    assert is_divisible_subtract(n, d)
    
for n, d in not_divisible_pairs:
    assert not is_divisible_subtract(n, d)
```

Using hypothesis

``` python
@given(n=st.integers(min_value=0), d=st.integers(min_value=1))
def test_is_divisible_subtract(n: int, d: int):
    print(f"n: {n}, d: {d}")
    assert is_divisible_subtract(n, d) == (n % d == 0)
    
test_is_divisible_subtract()
```

    n: 0, d: 1
    n: 0, d: 1
    n: 27592, d: 18
    n: 0, d: 1
    n: 0, d: 1
    n: 71, d: 11580
    n: 0, d: 1
    n: 1645513541, d: 21453
    n: 0, d: 1
    n: 22756, d: 1864585566
    n: 0, d: 1
    n: 12728, d: 12779
    n: 12728, d: 12779
    n: 12728, d: 12729
    n: 12728, d: 12729
    n: 19422, d: 7866
    n: 7865, d: 7866
    n: 4808, d: 14590
    n: 14589, d: 14590
    n: 14589, d: 14590
    n: 352797536645655735, d: 5299700580723550389
    n: 352797536645655735, d: 352797536645655736
    n: 85015918816107155538282260884268790375, d: 10764

This gets stuck when testing for a very large n, since that would take a very long time to compute.

### Largest power

To avoid getting stuck, subtract instead the largest power of d that is smaller or equal to n (a power of d is a number of the form d \*\* k, with k being a positive [integer](https://en.wikipedia.org/wiki/Exponentiation)).

``` python
def largest_power(d: int, n: int) -> int:
    """
    Returns largest power of d (d ** k) that is smaller or equal to n.
    """
    assert 1 < d <= n, "This only works for 1 < d <= n"
    
    power = d
    
    while power * d <= n:
        power *= d
    
    return power
    

assert largest_power(3, 8) == 3
assert largest_power(3, 9) == 9
assert largest_power(5, 24) == 5
assert largest_power(5, 25) == 25
```

Using logs instead.

``` python
def largest_power(d: int, n: int) -> int:
    """
    Returns largest power of d (d ** k) that is smaller or equal to n.
    
    Uses:
    d ** k <= n < d ** (k + 1)
    k log(d) <= log(n) < (k + 1) log(d)
    k <= log(n) / log(d) < k + 1
    """
    assert 1 < d <= n, "This only works for 1 < d <= n"
    
    # int() rounds down to next integer value
    k = int(math.log(n) / math.log(d))
    return d ** k
```

Testing as usual.

``` python
@given(n=st.integers(min_value=1), d=st.integers(min_value=2))
def test_largest_power(d: int, n: int):
    if d <= n:
        dk = largest_power(d, n)
        assert dk <= n < dk * d
        
test_largest_power()
```

Using this in divisible subtract.

``` python
def divisible_subtract_fast(n: int, d: int) -> bool:
    # All numbers are divisible by 1
    if d == 1:
        return True

    while n >= d:
        # Subtract largest power of d that's smaller or equal to n
        n -= largest_power(d, n)

    # If n is divisible by d, then n is now zero
    return n == 0
```

Test again.

``` python
@given(n=st.integers(min_value=0), d=st.integers(min_value=1))
def test_divisible_subtract_fast(n: int, d:int):
    assert divisible_subtract_fast(n, d) == (n % d == 0)
       
test_divisible_subtract_fast()
```

### Well-known tricks

-   A number is divisible by 5 if and only if its last digit is 0 or 5.
-   A number is divisible by 3 if and only if the sum of its digits is divisible by 3.
-   We can use this to solve fizzbuzz without divisions.

Divisible by 5

``` python
def last_digit(n: int) -> int:
    """Returns last digit of n."""
    return int(str(n)[-1])


assert last_digit(1) == 1
assert last_digit(11) == 1
assert last_digit(111) == 1
assert last_digit(12) == 2
assert last_digit(123) == 3
```

``` python
def is_divisible_by_5(n: int) -> bool:
    # A number is divisible by 5 iff its last digit is 0 or 5
    return last_digit(n) in [0, 5]


@given(n=st.integers())
def test_is_divisible_by_5(n:int):
    assert is_divisible_by_5(n) == (n % 5 == 0)
    
test_is_divisible_by_5()
```

Divisible by 3

``` python
def sum_of_digits(n: int) -> int:
    """Returns sum of digits of n."""
    return sum(int(d) for d in str(n))

assert sum_of_digits(1) == 1
assert sum_of_digits(12) == 3
assert sum_of_digits(123) == 6
assert sum_of_digits(123456) == 21
```

``` python
def is_divisible_by_3_wrong(n: int) -> bool:
    return is_divisible_by_3_wrong(sum_of_digits(n))

try:
    is_divisible_by_3_wrong(21)
except RecursionError as e:
    print(e)
```

    maximum recursion depth exceeded while calling a Python object

Above leads to an infinite recursion because we are missing a base case.

To identify the base case, notice that:

1.  For any number with more than 3 digits, its sum has fewer than 3 digits (hence, large numbers start to "shrink" as we sum their digits).
2.  For any number with 2 digits, its sum is at most 18.
3.  For any number of 18 or less, its sum is at most 9.

Hence, repeatedly summing digits starting from any positive number eventually leads to a number smaller than 10.

``` python
def is_divisible_by_3(n: int) -> bool:
    """My version."""
    if n < 10:
        return n in [0, 3, 6, 9]
    return is_divisible_by_3(sum_of_digits(n))


def is_divisible_by_3(n: int) -> bool:
    """More elegant Grus version."""
    while n > 10:
        n = sum_of_digits(n)
    
    # Now n is a single digit number, and we can
    # check directly whether it's divisible by 3.
    return n in [0, 3, 6, 9]


@given(n=st.integers())
def test_is_divisible_by_3(n: int):
    assert is_divisible_by_3(n) == (n % 3 == 0)
```

Modulus-free fizzbuzz solution.

``` python
def fizzbuzz_modulus_free(n: int) -> str:
    """My version."""
    if is_divisible_by_5(n) and is_divisible_by_3(n):
        return "fizzbuzz"
    elif is_divisible_by_5(n):
        return "buzz"
    elif is_divisible_by_3(n):
        return "fizz"
    else:
        return str(n)

def fizzbuzz_modulus_free(n: int) -> str:
    """Grus version."""
    by5 = is_divisible_by_5(n)
    by3 = is_divisible_by_3(n)
    
    if by5 and by3:
        return "fizzbuzz"
    elif by5:
        return "buzz"
    elif by3:
        return "fizz"
    else:
        return str(n)
    

# Testing
check_function(fizzbuzz_modulus_free)
```

### Eliminating elif

Using dictionary lookup.

``` python
def fizzbuzz_dict(n: int) -> str:
    by5 = is_divisible_by_5(n)
    by3 = is_divisible_by_3(n)
    
    return {
        (True, True): "fizzbuzz",
        (True, False): "buzz",
        (False, True): "fizz",
        (False, False): str(n)
    }[by5, by3]

# Testing
check_function(fizzbuzz_dict)
```

Using list lookup.

``` python
def fizzbuzz_list_lookup(n: int) -> str:
    idx = [n % 15, n % 5, n % 3, 0].index(0)
    return ["fizzbuzz", "buzz", "fizz", str(n)][idx]


# Testing
check_function(fizzbuzz_list_lookup)
```

### Sentinel values and the sentinel object pattern

-   Mainly based on [The Sentinel Object Pattern](https://python-patterns.guide/python/sentinel-object/) by Brandon Rhodes.

-   A sentinel value is a placeholder that signifies the absence of data (e.g. object attribute, entire object, unsupplied argument in a function, etc.).

-   The challenge is how to choose that placeholder so that it is distinguishable from useful data.

-   The standard Python sentinel is the built-in `None` object.

-   **Example**: `index("pattern")` tries to return the first occurrence of "pattern" in string and returns a `ValueError` on failure. In contrast, `find()` tries to do the same but returns `-1` on failuere - `-1` is a sentinel value.

``` python
try:
    'ab'.index('c')
except ValueError as e:
    print(e)
```

    substring not found

``` python
'ab'.find('c')
```

    -1

-   There are two cases where this is not possible, in which case we use the can sentinel object pattern, which involves creating a featureless [object](https://docs.python.org/3/library/functions.html#object) that is the dedicated sentinel value.

#### `None` is useful data.

-   Example: The standard library's `functools.lru_cache` needs to distinguish between cases where a value was cached and was `None` and cases where no value has been cached yet. The below achieves this. (`cache_get` is an alias for `dict.get()`.)

``` python
sentinel = object()
result = cache_get(key, sentinel)
if result is not sentinel:
    ...
```

#### `None` is a function argument.

-   Sometimes, a function call needs to differentiate between no value supplied for given argument or `None` supplied for said argument.
-   Example: in below greeting function, we want to distinguish case were no titel is supplied and where caller passes in `None` for the title.

``` python
sentinel = object()

def greet(name: str, title = sentinel) -> str:
    if title is sentinel:
        # No title supplied
        return f"Hello {name}"
    elif title is None:
        # Caller explicitly provided None
        return f"Hello {name} with no title"
    else:
        return f"Hello {title} {name}"


assert greet('Joel') == "Hello Joel"
assert greet("Joel", None) == "Hello Joel with no title"
assert greet("Joel", "Mr.") == "Hello Mr. Joel"
```

### Printing result in groups of 15

``` python
# Remap to shorter outputs
remap = {'fizz': 'f', 'buzz': 'b', 'fizzbuzz': 'fb'}
output = [remap.get(fizzbuzz(n), '-') for n in range(1, 101)]

for start in range(0, 100, 15):
    group = output[start:start+15]
    print(' '.join(group))
```

    - - f - b f - - f b - f - - fb
    - - f - b f - - f b - f - - fb
    - - f - b f - - f b - f - - fb
    - - f - b f - - f b - f - - fb
    - - f - b f - - f b - f - - fb
    - - f - b f - - f b - f - - fb
    - - f - b f - - f b

### `dict.get()` solution

``` python
DICT_OF_15 = {
    3: 'fizz', 6: 'fizz', 9: 'fizz', 12: 'fizz',
    5: 'buzz', 10: 'buzz',
    0: 'fizzbuzz',
}

def fizzbuzz_15(n: int) -> str:
    return DICT_OF_15.get(n % 15, str(n))


check_function(fizzbuzz_15)
```
