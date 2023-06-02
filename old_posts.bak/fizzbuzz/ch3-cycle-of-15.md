---
title: Chapter 3 - The Cycle of 15
---

## Sentinel values and the sentinel object pattern

-   Mainly based on [The Sentinel Object Pattern](https://python-patterns.guide/python/sentinel-object/) by Brandon Rhodes.

-   A sentinel value is a placeholder that signifies the absence of data (e.g. object attribute, entire object, unsupplied argument in a function, etc.).

-   The challenge is how to choose that placeholder so that it is distinguishable from useful data.

-   The standard Python sentinel is the built-in `None` object.

-   **Example**: `index("pattern")` tries to return the first occurrence of "pattern" in string and returns a `ValueError` on failure. In contrast, `find()` tries to do the same but returns `-1` on failuere - `-1` is a sentinel value.

``` python
import checks
```

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

### `None` is useful data.

-   Example: The standard library's `functools.lru_cache` needs to distinguish between cases where a value was cached and was `None` and cases where no value has been cached yet. The below achieves this. (`cache_get` is an alias for `dict.get()`.)

``` python
sentinel = object()
result = cache_get(key, sentinel)
if result is not sentinel:
    ...
```

### `None` is a function argument.

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

## Printing result in groups of 15

Basic solution

``` python
def fizzbuzz(n: int) -> str:
    if n % 15 == 0:
        return "fizzbuzz"
    elif n % 5 == 0:
        return "buzz"
    elif n % 3 == 0:
        return "fizz"
    else:
        return str(n)
```

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

## `dict.get()` solution

``` python
DICT_OF_15 = {
    3: 'fizz', 6: 'fizz', 9: 'fizz', 12: 'fizz',
    5: 'buzz', 10: 'buzz',
    0: 'fizzbuzz',
}

def fizzbuzz_15(n: int) -> str:
    return DICT_OF_15.get(n % 15, str(n))


checks.check_function(fizzbuzz_15)
```

## Truthiness and logic

**Falsy or Truthy**

``` python
[] or [1]
```

    [1]

**Falsy and Truthy**

``` python
[] and [1]
```

    []

**Truthy or Falsy**

``` python
[1] or []
```

    [1]

**Truthy and Falsy**

``` python
[1] and []
```

    []

**Truthy and Truthy**

``` python
[1] and [2]
```

    [2]

**Truthy or Truthy**

``` python
[1] or [2]
```

    [1]

Way to remember the Truthy/Falsy or Falsy/Truthy above: if statement evaluates to what you'd expect.

``` python
if [] and [1]:
    print('Nevery printed')
```
