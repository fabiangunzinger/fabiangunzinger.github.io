---
title: Documenting Sample Selection
date: '2020-08-12'
tags:
  - 'python, datascience'
execute:
  enabled: false
---


<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous" data-relocate-top="true"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


``` python
import numpy as np
import pandas as pd
```

## Problem

I have a dataframe on which I perform a series of data selection steps. What I want is to automatically build a table for the appendix of my paper that tells me the number of users left in the data after each selection step.

Here's a mock dataset:

``` python
df = (pd.DataFrame({'user_id': [1, 2, 3, 4] * 2, 'data': np.random.rand(8)})
      .sort_values('user_id'))
df
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | user_id | data     |
|-----|---------|----------|
| 0   | 1       | 0.107515 |
| 4   | 1       | 0.306182 |
| 1   | 2       | 0.184724 |
| 5   | 2       | 0.217231 |
| 2   | 3       | 0.688004 |
| 6   | 3       | 0.284524 |
| 3   | 4       | 0.990159 |
| 7   | 4       | 0.466758 |

</div>

here some selection functions:

``` python
def first_five(df):
    return df[:5]

def n_largest(df, n=3):
    return df.loc[df.data.nlargest(n).index]

def select_sample(df):
    return (
        df
        .pipe(first_five)
        .pipe(n_largest)
    )

select_sample(df)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | user_id | data     |
|-----|---------|----------|
| 2   | 3       | 0.688004 |
| 4   | 1       | 0.306182 |
| 5   | 2       | 0.217231 |

</div>

## Solution

If we have a single dataframe on which to perform selection, as in the setting above, we can use a decorator and a dictionary.

As a first step, let's build a decorator that prints out the number of users after applying each function:

``` python
from functools import wraps

def user_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)
        num_users = df.user_id.nunique()
        print(f'{func.__name__}: {num_users}')
        return df
    return wrapper

@user_counter
def first_five(df):
    return df[:5]

@user_counter
def n_largest(df, n=3):
    return df.loc[df.data.nlargest(n).index]

def select_sample(df):
    return (
        df
        .pipe(first_five)
        .pipe(n_largest)
    )

select_sample(df)
```

    first_five: 3
    n_largest: 3

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | user_id | data     |
|-----|---------|----------|
| 2   | 3       | 0.688004 |
| 4   | 1       | 0.306182 |
| 5   | 2       | 0.217231 |

</div>

That's already nice. But I need those counts for the data appendix of my paper, so what I really want is to store the counts in a container that I can turn into a table. To do this, we can store the counts in a dictionary instead of printing them.

``` python
counts = dict()

def user_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)
        num_users = df.user_id.nunique()
        counts.update({func.__name__: num_users})
        return df
    return wrapper

@user_counter
def first_five(df):
    return df[:5]

@user_counter
def n_largest(df, n=3):
    return df.loc[df.data.nlargest(n).index]

def select_sample(df):
    return (
        df
        .pipe(first_five)
        .pipe(n_largest)
    )

display(select_sample(df))
counts
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | user_id | data     |
|-----|---------|----------|
| 2   | 3       | 0.688004 |
| 4   | 1       | 0.306182 |
| 5   | 2       | 0.217231 |

</div>

    {'first_five': 3, 'n_largest': 3}

Next, I want to add the number of users at the beginning and the end of the process (the count at the end is identical with the final step, but I think it's worth adding so readers can easily spot the final numbers).

``` python
counts = dict()

def user_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)
        num_users = df.user_id.nunique()
        counts.update({func.__name__: num_users})
        return df
    return wrapper

@user_counter
def first_five(df):
    return df[:5]

@user_counter
def n_largest(df, n=3):
    return df.loc[df.data.nlargest(n).index]

def add_user_count(df, step):
    num_users = df.user_id.nunique()
    counts.update({step: num_users})
    return df

def select_sample(df):
    return (
        df
        .pipe(add_user_count, 'start')
        .pipe(first_five)
        .pipe(n_largest)
        .pipe(add_user_count, 'end')
    )

display(select_sample(df))
counts
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | user_id | data     |
|-----|---------|----------|
| 2   | 3       | 0.688004 |
| 4   | 1       | 0.306182 |
| 5   | 2       | 0.217231 |

</div>

    {'start': 4, 'first_five': 3, 'n_largest': 3, 'end': 3}

We're nearly there. Let's turn this into a table that we can store to disk (as a Latex table, say) and automatically import in our paper.

``` python
table = pd.DataFrame(counts.items(), columns=['Processing step', 'Number of unique users'])
table 
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | Processing step | Number of unique users |
|-----|-----------------|------------------------|
| 0   | start           | 4                      |
| 1   | first_five      | 3                      |
| 2   | n_largest       | 3                      |
| 3   | end             | 3                      |

</div>

Finally, let's make sure readers of our paper (and we ourselves a few weeks from now) actually understand what's going on at each step.

``` python
description = {
    'start': 'Raw dataset',
    'first_five': 'Keep first five observations',
    'n_largest': 'Keep three largest datapoints',
    'end': 'Final dataset'
}

table['Processing step'] = table['Processing step'].map(description)
table
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | Processing step               | Number of unique users |
|-----|-------------------------------|------------------------|
| 0   | Raw dataset                   | 4                      |
| 1   | Keep first five observations  | 3                      |
| 2   | Keep three largest datapoints | 3                      |
| 3   | Final dataset                 | 3                      |

</div>

That's it. We can can now export this as a Latex table (or some other format) and automatically load it in our paper.

### Multiple datasets

Instead of having a single dataframe on which to perform selection, I actually have multiple pieces of a large dataframe (because the full dataframe doesn't fit into memory). What I want is to perform the data selection on each chunk separately but have the values in the counter object add up so that -- at the end -- the counts represent the counts for the full dataset. The solution here is to use `collection.Counter()` instead of a dictionary.

So, my setup is akin to the following:

``` python
large_df = pd.DataFrame({'user_id': list(range(12)), 'data': np.random.rand(12)})
large_df
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | user_id | data     |
|-----|---------|----------|
| 0   | 0       | 0.507218 |
| 1   | 1       | 0.933454 |
| 2   | 2       | 0.740951 |
| 3   | 3       | 0.654135 |
| 4   | 4       | 0.952187 |
| 5   | 5       | 0.807332 |
| 6   | 6       | 0.742915 |
| 7   | 7       | 0.344259 |
| 8   | 8       | 0.134813 |
| 9   | 9       | 0.952129 |
| 10  | 10      | 0.859282 |
| 11  | 11      | 0.376175 |

</div>

``` python
buckets = pd.cut(large_df.user_id, bins=2)
raw_pieces = [data for key, data in large_df.groupby(buckets)]
for piece in raw_pieces:
    display(piece)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | user_id | data     |
|-----|---------|----------|
| 0   | 0       | 0.507218 |
| 1   | 1       | 0.933454 |
| 2   | 2       | 0.740951 |
| 3   | 3       | 0.654135 |
| 4   | 4       | 0.952187 |
| 5   | 5       | 0.807332 |

</div>
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>

|     | user_id | data     |
|-----|---------|----------|
| 6   | 6       | 0.742915 |
| 7   | 7       | 0.344259 |
| 8   | 8       | 0.134813 |
| 9   | 9       | 0.952129 |
| 10  | 10      | 0.859282 |
| 11  | 11      | 0.376175 |

</div>

What happens if we use a `dict()` as our counts object as we did above.

``` python
counts = dict()

def user_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)
        num_users = df.user_id.nunique()
        counts.update({func.__name__: num_users})
        return df
    return wrapper

@user_counter
def first_five(df):
    return df[:5]

@user_counter
def n_largest(df, n=3):
    return df.loc[df.data.nlargest(n).index]

def add_user_count(df, step='start'):
    num_users = df.user_id.nunique()
    counts.update({step: num_users})
    return df

def select_sample(df):
    return (
        df
        .pipe(add_user_count)
        .pipe(first_five)
        .pipe(n_largest)
        .pipe(add_user_count, 'end')
    )

selected_pieces = []
for piece in raw_pieces:
    selected_pieces.append(select_sample(piece))
    print(counts)

df = pd.concat(selected_pieces)
```

    {'start': 6, 'first_five': 5, 'n_largest': 3, 'end': 3}
    {'start': 6, 'first_five': 5, 'n_largest': 3, 'end': 3}

The counts are replaced rather than added up, which is how updating works for a dictionary:

``` python
m = dict(a=1, b=2)
n = dict(b=3, c=4)

m.update(n)
m
```

    {'a': 1, 'b': 3, 'c': 4}

`collections.Counter()` ([docs](https://docs.python.org/3/library/collections.html#counter-objects)) solve this problem.

``` python
import collections

counts = collections.Counter()

def user_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)
        num_users = df.user_id.nunique()
        counts.update({func.__name__: num_users})
        return df
    return wrapper

@user_counter
def first_five(df):
    return df[:5]

@user_counter
def n_largest(df, n=3):
    return df.loc[df.data.nlargest(n).index]

def add_user_count(df, step='start'):
    num_users = df.user_id.nunique()
    counts.update({step: num_users})
    return df

def select_sample(df):
    return (
        df
        .pipe(add_user_count)
        .pipe(first_five)
        .pipe(n_largest)
        .pipe(add_user_count, 'end')
    )

selected_pieces = []
for piece in raw_pieces:
    selected_pieces.append(select_sample(piece))
    print(counts)

df = pd.concat(selected_pieces)
```

    Counter({'start': 6, 'first_five': 5, 'n_largest': 3, 'end': 3})
    Counter({'start': 12, 'first_five': 10, 'n_largest': 6, 'end': 6})

Now, updating adds up the values for each key, just as we want. We can add the same formatting as we did above and are done with our table.

## Background

### Other cool stuff `Counter()` can do

``` python
o = collections.Counter(a=1, b=2)
p = collections.Counter(b=3, c=-4)

o.update(p)
o
```

    Counter({'a': 1, 'b': 5, 'c': -4})

Counters can also do cool things like this:

``` python
list(o.elements())
```

    ['a', 'b', 'b', 'b', 'b', 'b']

``` python
o.most_common(2)
```

    [('b', 5), ('a', 1)]

``` python
o - p
```

    Counter({'a': 1, 'b': 2})

### Why is counts a global variable?

Because I want *all* decorated functions to write to the *same* counter object.

Often, decorators make use of closures instead, which have access to a nonlocal variable defined inside the outermost function. Let's look at what happens if we do this for our user counter.

``` python
def user_counter(func):
    counts = collections.Counter()
    @wraps(func)
    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)
        num_users = df.user_id.nunique()
        counts.update({func.__name__: num_users})
        print(counts)
        return df
    return wrapper

@user_counter
def first_five(df):
    return df[:5]

@user_counter
def largest(df):
    return df.loc[df.data.nlargest(3).index]

def select(df):
    return (
        df
        .pipe(first_five)
        .pipe(largest)
    )
result = select(df)
```

    Counter({'first_five': 5})
    Counter({'largest': 3})

Now, each decorated function gets its own counter object, which is not what we want here. For more on decorator state retention options, see chapter 39 in [Learning Python](https://www.oreilly.com/library/view/learning-python-5th/9781449355722/).

### What are closures and nonlocal variables?

(Disclaimer: Just about all of the text and code on closures is taken -- sometimes verbatim -- from chapter 7 in [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/). So the point here is not to produce new insight, but to absorb the material and write an easily accessible note to my future self.)

Closures are functions that have access to nonlocal arguments -- variabls that are neither local nor global, but are defined inside an outer function within which the closure was defined, and to which the closure has access.

Let's look at an example. A simple function that takes one number as an argument and returns the average of all numbers passed to it since it's definition. For this, we need a way to store all previously passed values. One way to do this is to define a class with a call method.

``` python
class Averager():
    
    def __init__(self):
        self.series = []
        
    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)
    
avg = Averager()

avg(10), avg(20), avg(30)
```

    (10.0, 15.0, 20.0)

Another way is to use a closure function and store the series of previously passed numbers as a free variable.

``` python
def make_averager():
    series = []    
    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)
    return averager
    
avg = make_averager()

avg(10), avg(20), avg(30)
```

    (10.0, 15.0, 20.0)

This gives the same result, but is arguably simpler than defining a class.

We can improve the above function by storing previous results so that we don't have to calculate the new average from scratch at every function call.

``` python
def make_fast_averager():
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return averager

avg = make_fast_averager()

avg(10), avg(11), avg(12)
```

    (10.0, 10.5, 11.0)

``` python
%%timeit
avg = make_averager()
[avg(n) for n in range(10_000)]
```

    233 ms ± 8.03 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

``` python
%%timeit
avg = make_fast_averager()
[avg(n) for n in range(10_000)]
```

    1.69 ms ± 53.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

This simple change gives us a massive speedup.

Notice the `nonlocal` statement inside the averager function. Why do we need this? Let's see what happens if we don't specify it:

``` python
def make_fast_averager():
    count = 0
    total = 0
    def averager(new_value):
        count += 1
        total += new_value
        return total / count
    return averager

avg = make_fast_averager()

avg(10), avg(11), avg(12)
```

<pre><span class="ansi-red-fg">---------------------------------------------------------------------------</span>
<span class="ansi-red-fg">UnboundLocalError</span>                         Traceback (most recent call last)
<span class="ansi-green-fg">/var/folders/xg/n9p73cf50s52twlnz7z778vr0000gn/T/ipykernel_10646/1095891491.py</span> in <span class="ansi-cyan-fg">&lt;module&gt;</span>
<span class="ansi-green-fg ansi-bold">     10</span> avg <span class="ansi-blue-fg">=</span> make_fast_averager<span class="ansi-blue-fg">(</span><span class="ansi-blue-fg">)</span>
<span class="ansi-green-fg ansi-bold">     11</span> 
<span class="ansi-green-fg">---&gt; 12</span><span class="ansi-red-fg"> </span>avg<span class="ansi-blue-fg">(</span><span class="ansi-cyan-fg">10</span><span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">,</span> avg<span class="ansi-blue-fg">(</span><span class="ansi-cyan-fg">11</span><span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">,</span> avg<span class="ansi-blue-fg">(</span><span class="ansi-cyan-fg">12</span><span class="ansi-blue-fg">)</span>

<span class="ansi-green-fg">/var/folders/xg/n9p73cf50s52twlnz7z778vr0000gn/T/ipykernel_10646/1095891491.py</span> in <span class="ansi-cyan-fg">averager</span><span class="ansi-blue-fg">(new_value)</span>
<span class="ansi-green-fg ansi-bold">      3</span>     total <span class="ansi-blue-fg">=</span> <span class="ansi-cyan-fg">0</span>
<span class="ansi-green-fg ansi-bold">      4</span>     <span class="ansi-green-fg">def</span> averager<span class="ansi-blue-fg">(</span>new_value<span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">:</span>
<span class="ansi-green-fg">----&gt; 5</span><span class="ansi-red-fg">         </span>count <span class="ansi-blue-fg">+=</span> <span class="ansi-cyan-fg">1</span>
<span class="ansi-green-fg ansi-bold">      6</span>         total <span class="ansi-blue-fg">+=</span> new_value
<span class="ansi-green-fg ansi-bold">      7</span>         <span class="ansi-green-fg">return</span> total <span class="ansi-blue-fg">/</span> count

<span class="ansi-red-fg">UnboundLocalError</span>: local variable 'count' referenced before assignment</pre>

How come our fast averager can't find count and total even though our slow averager could find series just fine?

The answer lies in Python's variable scope rules and the difference between assigning to unmutable objects and updating mutable ones.

1.  Whenever we assign to a variable inside a function, it is treated as a local variable.

2.  count += 1 is the same as count = count + 1, so we are assigning to count, which makes it a local variable (the same goes for total). We are assigning new values to count rather than updaing it because integers are immutable, so we can't update it.

3.  Lists are mutable, so series.append() doesn't create a new list, but merely appends to it, which doesn't count as an assignment, so that series is not treated as a local variable.

Hence, we need to explicitly tell Python that count and total are nonlocal variables.

## Main sources

-   [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
-   [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
-   [Learning Python](https://www.oreilly.com/library/view/learning-python-5th/9781449355722/)
