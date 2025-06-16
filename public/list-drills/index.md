# List drills



Drills to practice working with lists in Python.

## Basics

Solve the below tasks and state their time and space complexities.

Define a list.

A list is a finite, ordered, and mutable sequence of elements.

Create a list `a` containing the letters *a*, *b*, and *c*.

``` python
a = list("abc")
```

Append *z*.

``` python
a.append("z")
```

Insert *x* at the second position.

``` python
a.insert(1, "x")
```

Append the characters *m*, *n*.

``` python
a.extend("mn")
```

Remove the first occurrence of *x* from the list.

``` python
a.remove("x")
```

Remove the second to last element from the list.

``` python
del a[-2]
```

Remove and return the last item.

``` python
a.pop()
```

Remove and return the second item.

``` python
a.pop(1)
```

Check whether *c* is in the list.

``` python
"c" in a
```

Return the index of *c*.

``` python
a.index("c")
```

Count occurrences of 'c'.

``` python
a.count("c")
```

Sort the list in place.

``` python
a.sort()
```

Insert 'z' in the first position.

``` python
a.insert(0, "z")
```

Replace the just inserted *z* with 'k'

``` python
a[0] = "k"
```

Create a sorted copy of the list.

``` python
sorted(a)
```

Reverse the order in place.

``` python
a.reverse()
```

Create a reversed iterator.

``` python
reversed(a)
```

Delete all elements from the list.

``` python
a.clear()
```

## Deep and shallow copies

``` python
a = [1, 2, [3]]
```

Create shallow copies `b`, `c`, `d`, and `e` of `a`, all in different ways.

``` python
import copy

b = list(a)
c = a[:]
d = a.copy()
e = copy.copy(a)
```

Check that the new lists are indeed shallow copies.

``` python
all(a is not copy and a[2] is copy[2] for copy in [b, c, d])
```

    True

Create a deep copy `e` of `a`.

``` python
e = copy.deepcopy(a)
```

Check that the new list is a deep copy.

``` python
e is not a and e[2] is not a[2]
```

## List comprehensions

``` python
colors = ["blue", "yellow"]
sizes = "SML"
```

Reproduce the output of the below using a list comprehension.

    results = []
    for color in colors:
        for size in sizes:
            results.append((color, size))
    results

``` python
results = [(color, size) for color in colors for size in sizes]
results
```

Create a copy of `results` sorted by size in ascending order.

``` python
sorted(results, key=lambda x: x[1], reverse=True)
```

## Summing elements

``` python
a = [1, 2, 3, 4, 5]
```

Sum `a` using the built-in method.

``` python
sum(a)
```

Sum the list using a recursive algorithm.

``` python
def rec_sum(items):
    if not items:
        return 0
    head, *tail = items
    return head + rec_sum(tail) if tail else head
```

    8

Sum the list using a for loop.

``` python
def for_sum(items):
    result = 0
    for item in items:
        result += item
    return result


for_sum(a)
```

Sum the list using a while loop without altering the input.

``` python
def while_sum(items):
    result = i = 0
    while i < len(items):
        result += items[i]
        i += 1
    return result


while_sum(a)
```

## Misc.

What is `c`?

``` python
a = 1
b = 2
c = [a, b]
a = 2
c
```

    [1, 2]

Find the indices of the min and max elements in the list below.

``` python
a = [1, 3, 4, 9, 9, 10, 2, 4, 2, 33]
```

``` python
a.index(min(a)), a.index(max(a))
```

### Removing duplicates

Write an algorithm to remove duplicates from a list while maintaining it's original order (from Python cookbook recipe 1.10).

``` python
def dedupe(items):
    seen = set()
    deduped = []
    for item in items:
        if item not in seen:
            deduped.append(item)
        seen.add(item)
    return deduped


dedupe([1, 1, 2, 3, 2])
```

Use a generator function to achieve the same.

``` python
def dedupe_gen(items):
    seen = set()
    for item in items:
        if item not in seen:
            seen.add(item)
            yield item


for item in dedupe_gen([1, 1, 2, 3, 2]):
    print(item)
```

Remove duplicates from the below sorted list by updating the original list

``` python
a = [1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7]
```

``` python
def dedupe_inplace(items):
    write_index = 1
    for i in range(2, len(items)):
        if items[i] != items[write_index - 1]:
            items[write_index] = items[i]
            write_index += 1
    return items[:write_index]


dedupe_inplace(a)
```

    [1, 2, 3, 4, 5, 6, 7]

## Implementing a stack

Implement a stack with `push()`, `pop()`, `peek()`, and `is_empty()` methods.

``` python
class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        self.data.pop()

    def peek(self):
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0
```

## Implementing a queue

Implement a queue with basic operations `enqueue()`, `dequeue()`, and `is_empty()`.

``` python
class Queue:
    def __init__(self):
        self.data = []

    def enqueue(self, item):
        self.data.append(item)

    def dequeue(self):
        return self.data.pop(0)

    def is_empty(self):
        return len(self.data) == 0
```

