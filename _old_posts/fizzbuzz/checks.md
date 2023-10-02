---
title: Checks for fizzbuzz functions
---

Approach:

-   Use list below as ground truth.
-   Solutions to the fizzbuzz problem are two types of functions: the first type return a list with all 100 values, the second type takes a number and return its fizbuzz value.
-   Create a test that compares lists of 100 values to the ground truth.
-   Can use this directly for first type of function, and after creating a list of 100 values using second type of function.

Ground truth:

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

Basic fizzbuzz functions for testing:

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
    
    
def broken_fizzbuzz(n):
    if n % 15 == 0:
        return "wrong answer"
    elif n % 5 == 0:
        return "buzz"
    elif n % 3 == 0:
        return "fizz"
    else:
        return str(n)
    
```

## Test functions with list output

Test function design:
- First check that length is correct to avoid unnecessary checking in case it isn't.
- Create list of errors so we can see errors in case there are any (instead of just learning that the list is incorrect, which is not as helpful!).
- Note elegant use of assert statements instead of if/else statements.

``` python
from typing import List

def check_output(output: List[str]) -> None:
    assert len(output) == 100, "Output should have length 100"
    
    # Collect all errors in a list
    # The i+1 reflects that output[0] is the output for 1,
    # output[1] the output for 2, and so on
    errors = [
        f"({i+1}) actual: {output[i]}, expected: {FIZZ_BUZZ[i]}"
        for i in range(100)
        if output[i] != FIZZ_BUZZ[i]
    ]
    
    assert len(errors) == 0, f"{errors}"
```

Test we expect to pass:

``` python
check_output([fizzbuzz(n) for n in range(1, 101)])
```

Test we expect to fail:

``` python
try:
    check_output([broken_fizzbuzz(n+1) for n in range(100)])
except AssertionError as e:
    print(e)
```

    ['(15) actual: wrong answer, expected: fizzbuzz', '(30) actual: wrong answer, expected: fizzbuzz', '(45) actual: wrong answer, expected: fizzbuzz', '(60) actual: wrong answer, expected: fizzbuzz', '(75) actual: wrong answer, expected: fizzbuzz', '(90) actual: wrong answer, expected: fizzbuzz']

## Test functions with single output

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
    
    
# Tests
assert check_function(fizzbuzz) is None
```
