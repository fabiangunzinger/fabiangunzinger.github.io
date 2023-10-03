---
title: "Python dicts"
date: "2022-02-28"
tags:
    - python
execute:
    enabled: false
---

Drills to practice working with Python dictionaries.

## Built-in dict

Create a dictionary, `d`, from the two lists below using the `dict()` constructor.

``` python
keys = ["a", "b", "c"]
values = range(3)
```

``` python
d = dict(zip(keys, values))
```

Recreate the same dictionary using dictionary comprehension and check that the result is identical to `d`.

``` python
dd = {key: value for key, value in zip(keys, values)}
dd == d
```

What does the below return and why?

``` python
{key: value for key in keys for value in values}
```

It returns *2* as the value for every key because for each key it iterates through all the values and returns the last one.

Return a list of all dictionary keys.

``` python
list(d)
```

Return the number of items in `d`.

``` python
len(d)
```

Return the value for key *b* in two different ways.

``` python
d["b"]
```

``` python
d.get("b")
```

Replace the above value with *5*.

``` python
d["b"] = 5
```

Remove the entry *c*.

``` python
del d["c"]
```

Check that *c* is no longer present.

``` python
"c" not in d
```

Create a shallow copy, `dd`, of `d`.

``` python
dd = d.copy()
```

Try to return the value for the non-existend key *x* and intead return *default*.

``` python
d.get("x", "default")
```

Return a view of all key-value pairs.

``` python
d.items()
```

Return a view of all keys.

``` python
d.keys()
```

Return a view of all values.

``` python
d.values()
```

Remove key *a* and return its value, ensuring that if *a* isn't in `d`, *default* is returned.

``` python
d.pop("a", "default")
```

Add keys *m* and *n* with values *10* and *11* to the dict.

``` python
d["m"] = 10
d["n"] = 11
```

Remove the last added key-value pair from the dict and return it.

``` python
d.popitem()
```

Return a reversed iterator over the keys and use it to print the values in reverse order.

``` python
for i in reversed(d):
    print(d[i])
```

Add key *z* to the dictionary initialising it with a default value of 0.

``` python
d.setdefault("z", 0)
```

Print the dictionary.

``` python
d
```

Check equality of `d.values()` with itself. What do you get and why?

It's `False`, like all comparisons of view objects.

Delete all elements from the dictionary.

``` python
d.clear()
d
```

Create dictionaries `m` and `n` with keys from the string below, and with all values initialised as *1* and *2*, repectively.

``` python
keys_m = "abcd"
keys_n = "cdef"
```

``` python
m = dict.fromkeys(keys_m, 1)
n = dict.fromkeys(keys_n, 2)
```

Create a new dict, `o`, with the combined keys of `m` and `n`, with the keys of the former taking precedent in the case of duplicate keys.

``` python
o = n | m
```

Update the values in `n` with those of `m` in place.

``` python
n.update(m)
```

Now update `m` with `n` using a different method.

``` python
m |= n
```

## Counter

Create a dictionary `d` that stores the number of occurrences for each item in `items`.

``` python
items = "aabbcdeaabdd"
```

``` python
from collections import Counter

d = Counter(items)
```

Use `d` to produce a sorted version of `items`.

``` python
list(d.elements())
```

Find the two most common element in `d` and their counts.

``` python
d.most_common(2)
```

Find the three least common elements in `d` (in ascending order of frequency) and their counts.

``` python
d.most_common()[:-4:-1]
```

Add the counts of `more_items` to `d`. How does the method to be used compare to when called on a regular dictionary?

``` python
more_items = "aabcxxyzz"
```

``` python
d.update(more_items)
```

Based on the below two counters, create a new counter containing the minimum of all counts (with zero counts deleted from the dict).

``` python
a = Counter("aab")
b = Counter("bbc")
```

``` python
a & b
```

Now create one that contains the maximum of all counts.

``` python
a | b
```

Drop all items with negative counts from counter `a` below and explain what's going on.

``` python
a = Counter({"a": 3, "b": -4})
a
```

    Counter({'a': 3, 'b': -4})

``` python
+a
```

There are two things going on here: First, mathematical operations on counters drop items with negative counts (counters are built for counting positive things), and, second, unary operations `+a` or `-a` are shorthand for adding to or subtracting from an empty counter.

## Ordered dict

Since Python 3.7, `dict` has been [declared](https://mail.python.org/pipermail/python-dev/2017-December/151283.html) to maintain the order of keys as they are encountered. Hence, the use of `OrderedDict` is more limited (see [here](https://realpython.com/python-ordereddict/) for a good discussion on when you might still use it), and `Counter` [inherits](https://docs.python.org/3/library/collections.html#collections.Counter) the new behaviour as it is a `dict` subclass 💥.

## Topics

### Setting default values

Create a dict `d` from the below items, concatenating the list values for duplicate keys.

``` python
items = [("a", [1, 2]), ("b", [3, 4]), ("a", [3, 4]), ("c", [5])]
```

First, what happens if we call `dict(items)`?

The first set of values for *a* get overwritten by the second set of values.

Now, create `d` using the built-in `dict`.

``` python
d = {}
for key, value in items:
    d.setdefault(key, []).extend(value)
d
```

Do the same but in a different way.

``` python
d = {}
for key, value in items:
    if key not in d:
        d[key] = []
    d[key].extend(value)
d
```

Now do the same using the `collections` module.

``` python
from collections import defaultdict

d = defaultdict(list)
for key, data in items:
    d[key].extend(data)
d
```

Now, using any additional module you like, create `d` again but this time with values `([items], occurrences)`, where the first element is the value items as before, and the second element is a count for the number of times the key occurres in `items` (e.g. for key *a* we want `([1, 2, 3, 4], 2)`.)

``` python
d = collections.defaultdict(lambda: [[], 0])
for key, value in items:
    d[key][0].extend(value)
    d[key][1] += 1
d
```

Create a `greeting` function that takes a user ID as input and returns *Hi name* if the user ID has an entry in `name_for_userid` and *Hi there* otherwise.

``` python
name_for_userid = {
    382: "Alice",
    590: "Bob",
    951: "Dilbert",
}
```

``` python
def greeting(user_id):
    return "Hi {}".format(name_for_userid.get(user_id, "there"))
```

### Setting default values in nested dictionaries

From [Khuyen Tran](https://mathdatasimplified.com/2021/10/14/double-dict-get-get-values-in-a-nested-dictionary-with-missing-keys/?utm_source=mailpoet&utm_medium=email&utm_campaign=weekend-read-3-data-science-tips-you-might-have-missed_207)

Get a list of the *taste* attribute for each fruit in list below, substituting *unknown* for fruits with no taste information.

``` python
fruits = [
    {
        'name': 'apple',
        'attr': {'colour': 'red', 'taste': 'sweet'},
    },
    {
        'name': 'orange',
        'attr': {'colour': 'orange'},
    },
    {
        'name': 'banana',
    },
]
```

Complete the task without using any dictionary methods.

``` python
[fruit['attr']['taste']
 if 'attr' in fruit and 'taste' in fruit['attr']
 else 'unknown'
 for fruit in fruits]
```

Complete the task more elegantly than above.

``` python
[fruit.get('attr', {}).get('taste', 'unknown')
 for fruit in fruits]
```

### Calculating with dics

Based on recipe 1.8 in the Python Cookbook

``` python
prices = {"ACME": 45.23, "AAPL": 612.78, "IBM": 205.55, "HPQ": 37.20, "FB": 10.75}
```

Return the name of the stock with the highest price.

``` python
max(prices, key=lambda x: prices[x])
```

Return the key-value pair for the stock with the lowest price.

``` python
min(prices.items(), key=lambda x: x[1])
```

Return the items in decreasing order of price.

``` python
sorted(prices.items(), key=lambda x: x[1], reverse=True)
```

### Mapping dict values to list items

Create a list containing the dict values of the elements in `a` in two different ways.

``` python
d = {1: 'a', 2: 'b', 3: 'c'}
a = [1, 2, 3, 1, 2]
```

``` python
list(map(d.get, a))
```

``` python
[d.get(item) for item in a]
```

Now do the same for the new list `a`, and use *99* as the value for items that aren't in `d`. Use again two different ways.

``` python
a = [1, 2, 3, 1, 100]
```

``` python
list(map(lambda x: d.get(x, 99), a))
```

``` python
[d.get(item, 99) for item in a]
```
