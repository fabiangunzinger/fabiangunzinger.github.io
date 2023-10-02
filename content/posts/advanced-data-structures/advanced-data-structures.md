---
title: "Advanced data structures"
date: "2021-11-12"
tags:
    - python, cs
execute:
    enabled: false
---

## Queues

**Using built-in list**

Implement a single-ended queue with basic operations `enqueue()`, `dequeue()`, and `is_empty()`, as well as optional argument `maxlen`.

``` python
class Queue:
    """
    Dequeue takes O(n) time since all elements need to shift.
    """

    def __init__(self, maxlen=None):
        self.items = []
        self.maxlen = maxlen

    def enqueue(self, item):
        if maxlen and len(self.items) == maxlen:
            self.items = self.items[1:]
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0
```

**Using standard library implementation**

Import the standard library queue module. What does its name stand for?

``` python
# I tend to forget whether it is deque or heapq that is part of the
# collections module. Use 'deck from collections' as an mnemonic.
# Deque stands for 'double-ended-queue'.
from collections import deque
```

Instantiate the que with a max length of 3.

``` python
q = deque(maxlen=3)
```

Add *1*, and then, in one go, *2*, *3*, and *4*, and, finally, the list *\[5, 6, 7\]* to the queue.

``` python
q.append(1)
q.extend([2, 3, 4])
q.append([5, 6, 7])
```

Dequeue the first item. What will it be?

``` python
q.popleft()
```

    3

## Stacks

Using a list

``` python
stack = [1, 2, 3, 4, 5]
stack.pop()
stack
```

    [1, 2, 3, 4]

Using `deque`

``` python
from collections import deque

stack = deque([1, 2, 3, 4])
reversed_stack = []
while stack:
    reversed_stack.append(stack.pop())
reversed_stack
```

    [4, 3, 2, 1]

``` python
stack.append(1)
stack.append([9, 4, 2])
print(stack.popleft(), stack.pop())
```

    1 [9, 4, 2]

## Sources

-   [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
-   [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
-   [Learning Python](https://www.oreilly.com/library/view/learning-python-5th/9781449355722/)
-   [The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/)
-   [Effective Python](https://effectivepython.com)
