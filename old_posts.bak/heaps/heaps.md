---
title: Basics
---

Define a heap.

Heaps are binary trees for which every parent node has a value less than or equal to any of its children.

Load the standard library module that implements heaps. What kind of heaps are supported?

``` python
# heapq implements min heaps. Push *-item* to implement max heap.
import heapq
```

Turn the below list into a min-heap.

``` python
heap = [1, -4, 7, 50]
```

``` python
heapq.heapify(heap)
```

Add *-1* to the heap.

``` python
heapq.heappush(heap, -1)
```

Remove and return the smallest element from the heap.

``` python
heapq.heappop(heap)
```

    -4

Add *-20* to the heap, then remove and return the smalles element.

``` python
heapq.heappushpop(heap, -20)
```

    -20

Remove and return the smallest element and add *3* to the heap.

``` python
heapq.heapreplace(heap, 3)
```

    -1

Display the heap.

``` python
heap
```

    [1, 3, 7, 50]

Return the two largest elements on the heap.

``` python
heapq.nlargest(2, heap)
```

    [50, 7]

For the heap below, return the two elements with the smallest digits.

``` python
heap = [("a", 3), ("b", 2), ("c", 1)]
```

``` python
heapq.nsmallest(2, heap, key=lambda x: x[1])
```

    [('c', 1), ('b', 2)]

## Applications

**Accessing shares**

For the shares portfolio below, return the data for the three most expensive shares, sorted in descending order.

``` python
portfolio = [
    {"name": "IBM", "shares": 100, "price": 91.1},
    {"name": "AAPL", "shares": 50, "price": 543.22},
    {"name": "FB", "shares": 200, "price": 21.09},
    {"name": "HPQ", "shares": 35, "price": 31.75},
]
```

``` python
heapq.nlargest(3, portfolio, lambda x: x["price"])
```

    [{'name': 'AAPL', 'shares': 50, 'price': 543.22},
     {'name': 'IBM', 'shares': 100, 'price': 91.1},
     {'name': 'HPQ', 'shares': 35, 'price': 31.75}]

Do the same using `operator.itemgetter()`.

``` python
from operator import itemgetter

heapq.nlargest(3, portfolio, key=itemgetter("price"))
```

Use a faster method that doesn't rely on `heapq` to achieve the same result.

``` python
%timeit sorted(portfolio, key=lambda x: x['price'], reverse=True)[:3]
```

    588 ns ± 16.9 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

``` python
%timeit heapq.nlargest(3, portfolio, key=lambda x: x['price'])
```

    2.1 µs ± 6.86 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

Calculate the running median for the list below.

**Building a priority queue**

Use `heapq` to build a priority queue that supports `push()` and `pop()` operations (based on Python Cookbook recipe 1.5 and `heapq` [docs](https://docs.python.org/3/library/heapq.html)). Specifically, build a queue that takes in items of the form `(value, priority)`, returns items in order or priority with higher values signifying higher priority, and breaks priority ties by returning items in the order they were added. To test the list, push the items *(foo, 1)*, *(bar, 3)*, and *(baz, 3)*. The first pop should return *(bar, 3)*.

``` python
import heapq


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Item({!r})".format(self.name)


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
```

``` python
q = PriorityQueue()
q.push(Item("foo"), 1)
q.push(Item("bar"), 3)
q.push(Item("baz"), 3)
q.pop()
```

    Item('bar')

**Running median**

Write a program that calculates the running median and test it on the list below.

``` python
def running_median(sequence):
    min_heap, max_heap, result = [], [], []
    for x in sequence:
        heapq.heappush(max_heap, -heapq.heappushpop(min_heap, x))
        if len(max_heap) > len(min_heap):
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
        result.append(
            (min_heap[0] + -max_heap[0]) / 2
            if len(min_heap) == len(max_heap)
            else min_heap[0]
        )
    return result
```

``` python
a = [1, 30, 2, -7, 99, 10]

running_median(a)
```

    [1, 15.5, 2, 1.5, 2, 6.0]

## Sources

-   [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
-   [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
-   [Learning Python](https://www.oreilly.com/library/view/learning-python-5th/9781449355722/)
-   [The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/)
-   [Effective Python](https://effectivepython.com)
