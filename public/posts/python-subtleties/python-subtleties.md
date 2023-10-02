---
title: "Python subtleties"
date: "2020-10-07"
tags:
    - python
execute:
    enabled: false
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


A collection of subtle (or not so subtle) mistakes I made and puzzles I've come across.

``` python
import pandas as pd
import numpy as np
```

## Changing a mutable element of an immutable sequence

The puzzle is from page 40 in [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/).

``` python
t = (1, 2, [3, 4])
t[2] += [5, 6]
```

    TypeError: 'tuple' object does not support item assignment

``` python
type(t).__name__
```

    'tuple'

``` python
t
```

    (1, 2, [3, 4, 5, 6])

What's going on here? As part of the assignment, Python does the following:

1.  Performs augmented addition on the value of `t[2]`, which works because that value is the list `[3, 4]`, which is mutable.

2.  Then it tries to assign the result from 1 to `t[2]`, which doesn't work, because `t` is immutable.

3.  But because the 2nd element in `t` is not the list itself but a reference to it, and because the list was changed in step 1, the value of `t[2]` has changed, too.

A great way to visualise the process is to see what happens under the hood using the amazing [Python Tutor](http://www.pythontutor.com).

## NANs are True

I have a dataframe with some data:

``` python
df = pd.DataFrame({'data': list('abcde')})
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

|     | data |
|-----|------|
| 0   | a    |
| 1   | b    |
| 2   | c    |
| 3   | d    |
| 4   | e    |

</div>

I can shift the data column:

``` python
df.data.shift()
```

    0    NaN
    1      a
    2      b
    3      c
    4      d
    Name: data, dtype: object

I want to add a check column that tells me where the shift is missing:

``` python
df['check'] = np.where(df.data.shift(), 'ok', 'missing')
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

|     | data | check |
|-----|------|-------|
| 0   | a    | ok    |
| 1   | b    | ok    |
| 2   | c    | ok    |
| 3   | d    | ok    |
| 4   | e    | ok    |

</div>

That's not what I wanted. The reason it happens is that **missing values that aren't `None` evaluate to `True`** (follows from the [docs](https://docs.python.org/2/library/stdtypes.html#truth-value-testing)). One way to see this:

``` python
[e for e in [np.nan, 'hello', True, None] if e]
```

    [nan, 'hello', True]

Hence, to get the check I wanted I should do this:

``` python
df['correct_check'] = np.where(df.data.shift().notna(), 'ok', 'missing')
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

|     | data | check | correct_check |
|-----|------|-------|---------------|
| 0   | a    | ok    | missing       |
| 1   | b    | ok    | ok            |
| 2   | c    | ok    | ok            |
| 3   | d    | ok    | ok            |
| 4   | e    | ok    | ok            |

</div>

## Truthy vs True

As follows clearly from the [docs](https://docs.python.org/2/library/stdtypes.html#truth-value-testing), `True` is one of many values that evaluate to `True`. This seems clear enough. Yet I just caught myself getting confused by the following:

I have a list of values that I want to filter for Truthy elements -- elements that evaluate to `True`:

``` python
mylist = [np.nan, 'hello', True, None]
[e for e in mylist if e]
```

    [nan, 'hello', True]

This works as intended. For a moment, however, I got confused by the following:

``` python
[e for e in mylist if e is True]
```

    [True]

I expected it to yield the same result as the above. But it doesn't becuase it only returns valus that actually are `True`, as in having the same object ID as the value `True` ([this](https://stackoverflow.com/a/20421344/13666841) Stack Overflow answer makes the point nicely). We can see this below:

``` python
[id(e) for e in mylist]
```

    [4599359344, 4859333552, 4556488160, 4556589160]

``` python
id(True)
```

    4556488160
