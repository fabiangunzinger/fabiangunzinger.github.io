---
title: Iterators and generators
date: '2022-01-22'
tags:
  - python
execute:
  enabled: false
---


## Iterators

-   A Python object is described as *iterable* (adjective) or as *an iterable* (noun) when it can be iterated over -- when we can process the elements it contains in turn.

-   An *iterator* is a value-producing object that returns the content of an iterable on demand one by one as we call `next()`.

-   We can create an iterator from an iterable using the built-in `iter()` function.

-   One (the?) main feature of iterators is that they are lazy: they produce the next item in the sequence only once it is required, which, for large sequences, can save a lot of memory and allow us to process data that doesn't fit into memory all at once.

Iterator example:

``` python
iterable = "hello world"
iterator = iter(iterable)
next(iterator), next(iterator)
```

    ('h', 'e')

## Generators

-   Generators are a tool to easily create iterators ([docs](https://docs.python.org/3/tutorial/classes.html#generators))

-   Similarly to `return`, the `yield` statement indicates that a value is returned to the caller, but unlike it, function execution is not terminated but merely suspended with the current state of the function saved, and function execution will pick up right after the `yield` statement on the next call to a generator method.

``` python
import inspect


def gen(x):
    yield x


a = gen(5)
print(inspect.getgeneratorstate(a))

next(a)
print(inspect.getgeneratorstate(a))

try:
    next(a)
except StopIteration:
    print(inspect.getgeneratorstate(a))
```

    GEN_CREATED
    GEN_SUSPENDED
    GEN_CLOSED

**Example: creating a generator from an iterator using generator comprehension**

``` python
a = [1, 2, 3]
reversed(a), (i for i in reversed(a))
```

    (<list_reverseiterator at 0x15f191b80>,
     <generator object <genexpr> at 0x15f5e1200>)

**Example: creating an infinite sequence**

``` python
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1


gen = infinite_sequence()
next(gen), next(gen)
```

    (0, 1)

**Example: generator expressions**

(They are well suited in cases where memory is an issue, but then can be slower than list expressions.)

``` python
import sys

nums_squared_lc = [i ** 2 for i in range(10000)]
print(sys.getsizeof(nums_squared_lc))

nums_squared_gc = (i ** 2 for i in range(10000))
sys.getsizeof(nums_squared_gc)
```

    85176

    112

**Example: reading a file line by line**

``` python
def csv_reader(filepath):
    for row in open(filepath, "r"):
        yield row


filepath = "/Users/fgu/example.csv"
csv_gen = csv_reader(filepath)  # or: csv_gen = (row for row in open(filepath))
row_count = 0
for row in csv_gen:
    row_count += 1

print(f"Row count: {row_count}")
```

    Row count: 2017

**Example: data processing pipeline**

``` python
filepath = "/Users/fgu/example.csv"

# exctract lines
lines = (line for line in open(filepath))

# turn lines into lists of items
list_line = (line.rstrip().split(",") for line in lines)

# extract column names
col_names = next(list_line)

# create dict with col name keys for each line
line_dicts = (dict(zip(col_names, data)) for data in list_line)

# extract needed data
sf_temps = (float(d["temperature"]) for d in line_dicts if d["city"] == "San Francisco")

# start iteration to calculate result
sf_min_temp = min(sf_temps)
print(f"SF min temperature was {sf_min_temp}")
```

    SF min temperature was 15.4496008956306

**Example: implementing a `for` loop**

``` python
items = ["a", "b", "c"]
it = iter(items)
while True:
    try:
        item = next(it)
    except StopIteration:
        break
    print(item)
```

    a
    b
    c

**Example: implementing `range()`**

(From the Python Cookbook recipee 4.3)

``` python
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment


rng = frange(1, 10, 2)
list(rng)
```

    [1, 3, 5, 7, 9]

**Example: creating an arithmetic progression sequence**

``` python
def aritprog(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index


a = aritprog(0, 5, 20)
for a in a:
    print(a)
```

    0
    5
    10
    15

## `yield from`

-   `yield from` allows for easily splitting up a generator into multiple generators.

``` python
def gen():
    for i in range(5):
        yield i
    for j in range(5, 10):
        yield j
```

We can split it into two

``` python
def gen1():
    for i in range(5):
        yield i


def gen2():
    for j in range(5, 10):
        yield j


def gen():
    for i in gen1():
        yield i
    for j in gen2():
        yield j


list(gen())
```

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

`yield from` allows us to simplify the above.

``` python
def gen():
    yield from gen1()
    yield from gen2()


list(gen())
```

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

**Merging two sorted collections**

``` python
def sorted_merge(left, right):
    """Returns two sorted collections as a single sorted collection."""
    def _merge():
        while left and right:
            yield (left if left[0] < right[0] else right).pop(0)
        yield from left
        yield from right

    return _merge()


list(sorted_merge([1, 3, 4, 99, 111], [2, 5, 7, 88]))
```

    [1, 2, 3, 4, 5, 7, 88, 99, 111]

## Sources

-   [Real Python, Python "for" loops](https://realpython.com/python-for-loop/)
-   [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
-   [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
-   [Simeon Visser, Using `yield from` in generators](http://simeonvisser.com/posts/python-3-using-yield-from-in-generators-part-1.html)
