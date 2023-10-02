---
title: "Basic data structures"
date: "2021-11-12"
tags:
    - python, cs
execute:
    enabled: false
---

todo:
- Integrate notes from codebase.py

## Tuple

A tuple is a finite, ordered, immutable sequence of elements.

    type((1))   # => int
    type(())    # => tuple
    type((1,))  # => tuple

## Strings

Strings are a special type of array -- one composed of characters.

``` python
"abcd".strip("cd")
```

    'ab'

``` python
"Hello world".find("wo")
```

    6

### Unicode conversion

Convert character string into unicode code point

``` python
ord("1"), ord("2"), ord("A"), ord("B")
```

    (49, 50, 65, 66)

Convert unicode code point to character

``` python
chr(49), chr(50), chr(65), chr(66)
```

    ('1', '2', 'A', 'B')

Trick to convert integer to string representation

``` python
chr(ord("0") + 2)
```

    '2'

## Sequences

### Useful stuff

Ignore minus sign in string number (using fact that `False` is `0` and `True` is `1`.

``` python
a, b = "-123", "123"

a[a[0] == "-" :], b[b[0] == "-" :]
```

    ('123', '123')

### Slice from (and/or) to particular characters

``` python
a = "abc[def]"
a[a.find("[") :]
```

    '[def]'

this works because

``` python
a.find("[")
```

    3

## Sets

``` python
# A set is an unordered, finite collection of distinct, hashable elements.
```

``` python
a = set("hello")
b = set("world")
```

**Lookup**

Lookup has worst case time complexity O(n) and avearge time complexity O(1). Why?

``` python
"e" in a
```

    True

**Difference**

Basic set difference *a-b* has time complexity O(len(a)) (for every element in a move to new set, if not in b) and space complexity O(len(a) + len(b)), since a new set is being created.

``` python
a - b
```

    {'e', 'h'}

A variant is difference update, which has time complexity O(len(b)) (for every element in b remove from a if it exists) and space complexity O(1), as we don't create a new set but update set a in place.

``` python
a.difference_update(b)
a
```

    {'e', 'h'}

Basic operations

``` python
print(a)  # unique elements in a
print("k" in a)  # membership testing
a.add("z")
a.remove("l")  # remove element from set, KeyError if not a member
a.discard("m")  # remove element from set, do nothing if not a member
print(a)
print({"e", "h"} < a)  # {e, h} is a strict subset of a
print(a & b)  # intersection
print(a | b)  # union
print(a - b)  # difference
print(a ^ b)  # symmetric difference
```

## Named tuples

Basic use

``` python
from collections import namedtuple

# create Stock class
Stock = namedtuple("Stock", ["name", "shares", "price", "date", "time"])

# instantiate class
s = Stock("aapl", "100", "55", None, None)

# attribute access
s.name
```

    'aapl'

Replace values

``` python
s._replace(shares=200)
```

    Stock(name='aapl', shares=200, price='55', date=None, time=None)

Use replace to populate named tuples with optional or missing fields

``` python
stock_prototype = Stock("", 0, 0.0, None, None)


def dict_to_stock(s):
    return stock_prototype._replace(**s)


portfolio = [
    {"name": "IBM", "shares": 100, "price": 91.1},
    {"name": "AAPL", "shares": 50, "price": 543.22},
    {"name": "FB", "shares": 200, "price": 21.09},
]

stocks = [dict_to_stock(s) for s in portfolio]
stocks
```

    [Stock(name='IBM', shares=100, price=91.1, date=None, time=None),
     Stock(name='AAPL', shares=50, price=543.22, date=None, time=None),
     Stock(name='FB', shares=200, price=21.09, date=None, time=None)]

## Sources

-   [Python time complexities](https://wiki.python.org/moin/TimeComplexity)
