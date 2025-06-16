# Python tricks



## Switching 0 to 1 and 1 to 0

Using `not`.

``` python
flip = lambda x: int(not x)

a, b = 1, 0
flip(a), flip(b)
```

    (0, 1)

Using `xor`.

``` python
flip = lambda x: x ^ 1

a, b = 1, 0
flip(a), flip(b)
```

    (0, 1)

## Coercing input to type of something else

``` python
type("")(5)
```

    '5'

## If-else logic in append statement

``` python
small = [1, 2]
large = [11, 12]

for x in [3, 4, 13, 14]:
    (small if x < 10 else large).append(x)

small, large
```

    ([1, 2, 3, 4], [11, 12, 13, 14])

## Indexing with the unary invert operator

``` python
def is_palindromic(string):
    return all(string[i] == string[~i] for i in range(len(string) // 2))


is_palindromic("kayak"), is_palindromic("world")
```

    (True, False)

What's happening here? `~` is the bitwise unary invert operator, which, for an integer `x`, returns `-(x+1)` ([docs](https://docs.python.org/3/reference/expressions.html#unary-arithmetic-and-bitwise-operations), to understand what's going on, start [here](https://stackoverflow.com/a/7278791/13666841)).

``` python
~1, ~2, ~12, ~-12
```

    (-2, -3, -13, 11)

This allows us to step through an array from the outside in.

``` python
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in range(5):
    print(a[i], a[~i])
```

    1 10
    2 9
    3 8
    4 7
    5 6

## Using an iterator to eliminate leading zeroes in arrays

(From Elements of Programming Interviews in Python problem 5.3)

``` python
a = [0, 0, 0, 1, 0, 2, 3]
a[next(i for i, x in enumerate(a) if x != 0) :]
```

    [1, 0, 2, 3]

What's happening here? Just like for a list extension, Python creates an object containing all elements that meet the condition and then iterates through them.

``` python
[i for i in a if i > 0]
```

    [1, 2, 3]

``` python
iterator = (i for i in a if i > 0)
for item in iterator:
    print(item)
```

    1
    2
    3

Using `next` once thus returns the first item that meets the condition. In the original example we thus get the index of the first non-zero item, which is `3`.

``` python
next(i for i, x in enumerate(a) if x != 0)
```

    3

The rest of the syntax produces a common list slice of the form `a[3:]`, which gets us what we want. Really rather clever.

## Sources

-   [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
-   [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
-   [Elements of Programming Interviews in Python](https://elementsofprogramminginterviews.com)

