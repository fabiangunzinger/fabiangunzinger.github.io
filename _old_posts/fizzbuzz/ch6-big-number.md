---
title: Chapter 6 - A big number
---

``` python
from typing import List
```

## Decimal, binary, and hexadecimal

### Decimal system

``` python
def decimal_digits(n: int) -> List[int]:
    digits: List[int] = []
    
    # If n is zero, it has no more digits
    while n > 0:
        # The rightmost digit is n%10
        digits.append(n % 10)
        # Remove rightmost digit and repeat
        n = n // 10
    
    digits.reverse()
    return digits

assert decimal_digits(0) == []
assert decimal_digits(345) == [3, 4, 5]
```

``` python
def from_decimal_digits(digits: List[int]) -> int:
    n = 0
    for digit in digits:
        n *= 10
        n += digit
    return n

assert from_decimal_digits([]) == 0
assert from_decimal_digits([0]) == 0
assert from_decimal_digits([3, 4, 5]) == 345
```

### Binary system

-   In the decimal system there are 10 numbers, 0-9, and for any given number, the rightmost digit represents the number of 1s, the next one the number of 10s (1 x 10), the next one the number of 100s (1 \* 10 \* 10), and so on.

-   In the binary system there are 2 numbers, 0 and 1, and for any given number, the rightmost digit presents the number of 1s, the next one the number of 2s (1 x 2), the next one the number of 4s (1 x 2 x 2), and so on.

-   Hence, the binary number 100101 equals 32 + 4 + 1 = 37 in binary.

Representing binary literals in Python.

``` python
assert 0b100101 == 37
assert int('100101', base=2) == 37
```

Getting binary representation of decimals.

``` python
assert bin(37) == '0b100101'
```

### Hexadecimal

-   In the hexadecimal system, the rightmost number is the number of 1s, the next on the number of 16s (1 x 16), the next one the number of 256s (1 x 16 x 16), and so on.

-   Hence, the hexadecimal number f83 equals 15*(16^2) + 8*(16) + 3\*(1) = 3971.

``` python
assert 0xf83 == 3971
assert int('f83', base=16) == 3971
assert hex(3971) == '0xf83'
```

## Dataclasses

Instead of this:

``` python
class Node:
    def __init__(self, value=0, parent=None, left=None, right=None):
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right
        
Node(1, 'myparent').parent
```

    'myparent'

I can just do this (attributes need to be typed)

``` python
from dataclasses import dataclass

@dataclass
class Node:
    value: int = None
    parent: str = None
    left: str = None
    right: str = None
    
Node(1, 'myparent').parent
```

    'myparent'

``` python
from typing import NamedTuple

class LeafNode(NamedTuple):
    count: int
    cla55: int
    
```

    5
