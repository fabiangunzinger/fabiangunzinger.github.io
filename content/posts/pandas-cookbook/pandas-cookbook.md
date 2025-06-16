---
title: Pandas cookbook
date: '2020-08-09'
tags:
  - python
execute:
  enabled: false
---


<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous" data-relocate-top="true"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


A collection of recipes for effectively solving common and not so common problems in Pandas.

<!-- This post is part of my series of posts on [`pandas`](https://pandas.pydata.org). -->
<!-- [Fluent Pandas](http://localhost:8888/lab/tree/_notebooks/2021-03-12-fluent-pandas.ipynb) contains notes on how to effectively use pandas core features.

[Fast pandas](http://localhost:8888/lab/tree/_notebooks/0000-09-03-fast-pandas.ipynb) contains notes on how to effectively work with large datasets.

[Pandas cookbook](http://localhost:8888/lab/tree/_notebooks/2020-08-09-pandas-cookbook.ipynb) is a list of recipes for effectively solving common and not so common problems. -->

``` python
import numpy as np
import pandas as pd
import seaborn as sns
```

## Splitting dataframes based on column values

You want to split the dataframe every time case equals B and store the resulting dataframes in a list.

``` python
df = pd.DataFrame(
    data={
        "case": ["A", "A", "A", "B", "A", "A", "B", "A", "A"],
        "data": np.random.randn(9),
    }
)
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

|     | case | data      |
|-----|------|-----------|
| 0   | A    | 0.064975  |
| 1   | A    | -0.486814 |
| 2   | A    | 0.411896  |
| 3   | B    | -1.397003 |
| 4   | A    | 1.148971  |
| 5   | A    | 0.817843  |
| 6   | B    | -0.993385 |
| 7   | A    | 1.143321  |
| 8   | A    | -0.134907 |

</div>

### Understanding the cookbook solution

From the [cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#id2):

``` python
dfs = list(
    zip(
        *df.groupby(
            (1 * (df["case"] == "B")).cumsum().rolling(window=3, min_periods=1).median()
        )
    )
)[-1]
dfs
```

    (  case      data
     0    A -0.900566
     1    A -1.127128
     2    A  0.342823
     3    B -0.854102,
       case      data
     4    A  1.058840
     5    A -0.307737
     6    B  0.013741,
       case      data
     7    A -1.768852
     8    A  0.550569)

This works. But because it's so heavily nested and uses methods like `rolling()` and `median()` not really designed for that purpose, the code is impossible to interpret at a glance.

Let's break this down into separate pieces.

First, the code creates a grouping variable that changes its value each time *case* equaled *B* on the previous row.

``` python
# Creating grouping variable

a = df.case == "B"
b = 1 * (df.case == "B")
c = 1 * (df.case == "B").cumsum()
d = 1 * (df.case == "B").cumsum().rolling(window=3, min_periods=1).median()

a, b, c, d
```

    (0    False
     1    False
     2    False
     3     True
     4    False
     5    False
     6     True
     7    False
     8    False
     Name: case, dtype: bool,
     0    0
     1    0
     2    0
     3    1
     4    0
     5    0
     6    1
     7    0
     8    0
     Name: case, dtype: int64,
     0    0
     1    0
     2    0
     3    1
     4    1
     5    1
     6    2
     7    2
     8    2
     Name: case, dtype: int64,
     0    0.0
     1    0.0
     2    0.0
     3    0.0
     4    1.0
     5    1.0
     6    1.0
     7    2.0
     8    2.0
     Name: case, dtype: float64)

Series *d* above is the argument passed to `groupby()` in the solution. This works, but is a very roundabout way to create such a series. I'll use a different approach below.

Next, the code uses `list()`, `zip()`, and argument expansion to pack the data for each group into a single list of dataframes. Let's look at these one by one.

First, `groupby()` stores the grouped data as *(label, df)* tuples.

``` python
groups = df.groupby("case")
for g in groups:
    print(type(g))
    print(g, end="\n\n")
```

    <class 'tuple'>
    ('A',   case      data
    0    A -0.900566
    1    A -1.127128
    2    A  0.342823
    4    A  1.058840
    5    A -0.307737
    7    A -1.768852
    8    A  0.550569)

    <class 'tuple'>
    ('B',   case      data
    3    B -0.854102
    6    B  0.013741)

Simplified, this is what we work with:

``` python
groups2 = [("g1", "data1"), ("g2", "data2")]
groups2
```

    [('g1', 'data1'), ('g2', 'data2')]

[Argument expansion](https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists) unpacks elements from a list as separate arguments that can be passed to a function. In our context here, it turns each *(label, df)* tuple into a separate object.

``` python
print(groups2)
print(*groups2)
```

    [('g1', 'data1'), ('g2', 'data2')]
    ('g1', 'data1') ('g2', 'data2')

`zip()` stitches together the ith elements of each iterable passed to it, effectively separating the "columns", and returns an iterator.

``` python
zip(*groups2)
```

    <zip at 0x16b1d3c80>

``` python
list(zip(*groups2))
```

    [('g1', 'g2'), ('data1', 'data2')]

Putting this all together, `zip()` is used to separate the group label from the data, and `list()` consumes the iterator created by zip and displays its content.

``` python
list(zip(*groups))
```

    [('A', 'B'),
     (  case      data
      0    A -0.900566
      1    A -1.127128
      2    A  0.342823
      4    A  1.058840
      5    A -0.307737
      7    A -1.768852
      8    A  0.550569,
        case      data
      3    B -0.854102
      6    B  0.013741)]

Because we only want the data, we select the last element from the list:

``` python
list(zip(*groups))[-1]
```

    (  case      data
     0    A  0.684978
     1    A  0.000269
     2    A -1.040497
     4    A  0.448596
     5    A  0.222168
     7    A -2.208787
     8    A -0.440758,
       case      data
     3    B  0.451358
     6    B  1.031011)

Now we're basically done. What remains is to use the `list(zip(*groups))` procedure on the more complicated grouping variable, to obtain the original result.

``` python
d = 1 * (df.case == "B").cumsum().rolling(window=3, min_periods=1).median()
groups = df.groupby(d)
list(zip(*groups))[-1]
```

    (  case      data
     0    A  0.684978
     1    A  0.000269
     2    A -1.040497
     3    B  0.451358,
       case      data
     4    A  0.448596
     5    A  0.222168
     6    B  1.031011,
       case      data
     7    A -2.208787
     8    A -0.440758)

### Simplifying the code

I think this can be made much more readable like so:

``` python
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

|     | case | data      |
|-----|------|-----------|
| 0   | A    | 0.064975  |
| 1   | A    | -0.486814 |
| 2   | A    | 0.411896  |
| 3   | B    | -1.397003 |
| 4   | A    | 1.148971  |
| 5   | A    | 0.817843  |
| 6   | B    | -0.993385 |
| 7   | A    | 1.143321  |
| 8   | A    | -0.134907 |

</div>

``` python
grouper = df.case.eq('B').cumsum().shift(fill_value=0)
frames = [df for g, df, in df.groupby(grouper)]
frames
```

    [  case      data
     0    A  0.064975
     1    A -0.486814
     2    A  0.411896
     3    B -1.397003,
       case      data
     4    A  1.148971
     5    A  0.817843
     6    B -0.993385,
       case      data
     7    A  1.143321
     8    A -0.134907]

Where the grouper works like so:

``` python
dd = df.set_index("case", drop=False)  # Use case as index for clarity
a = dd.case.eq("B")  # Boolean logic
b = a.cumsum()  # Create groups
c = b.shift(fill_value=0)  # Shift so B included in previous group and fills missings with 0
a, b, c
```

    (case
     A    False
     A    False
     A    False
     B     True
     A    False
     A    False
     B     True
     A    False
     A    False
     Name: case, dtype: bool,
     case
     A    0
     A    0
     A    0
     B    1
     A    1
     A    1
     B    2
     A    2
     A    2
     Name: case, dtype: int64,
     case
     A    0
     A    0
     A    0
     B    0
     A    1
     A    1
     B    1
     A    2
     A    2
     Name: case, dtype: int64)

## Creating new columns based on existing ones using mappings

The below is a straightforward adaptation from the [cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#new-columns):

``` python
df = pd.DataFrame({"AAA": [1, 2, 1, 3], "BBB": [1, 1, 4, 2], "CCC": [2, 1, 3, 1]})

source_cols = ["AAA", "BBB"]
new_cols = [str(c) + "_cat" for c in source_cols]
cats = {1: "One", 2: "Two", 3: "Three"}

dd = df.copy()
dd[new_cols] = df[source_cols].applymap(cats.get)
dd
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

|     | AAA | BBB | CCC | AAA_cat | BBB_cat |
|-----|-----|-----|-----|---------|---------|
| 0   | 1   | 1   | 2   | One     | One     |
| 1   | 2   | 1   | 1   | Two     | One     |
| 2   | 1   | 4   | 3   | One     | None    |
| 3   | 3   | 2   | 1   | Three   | Two     |

</div>

But it made me wonder why applymap required the use of the get method while we can map values of a series like so:

``` python
s = pd.Series([1, 2, 3, 1])
s.map(cats)
```

    0      One
    1      Two
    2    Three
    3      One
    dtype: object

or so

``` python
s.map(cats.get)
```

    0      One
    1      Two
    2    Three
    3      One
    dtype: object

The answer is simple: applymap requires a function as argument, while map takes functions or mappings.

One limitation of the cookbook solution above is that is doesn't seem to allow for default values (notice that 4 gets substituted with "None").

One way around this is the following:

``` python
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

|     | AAA | BBB | CCC |
|-----|-----|-----|-----|
| 0   | 1   | 1   | 2   |
| 1   | 2   | 1   | 1   |
| 2   | 1   | 4   | 3   |
| 3   | 3   | 2   | 1   |

</div>

``` python
dd[new_cols] = dd[source_cols].applymap(lambda x: cats.get(x, "Hello"))
dd
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

|     | AAA | BBB | CCC | AAA_cat | BBB_cat |
|-----|-----|-----|-----|---------|---------|
| 0   | 1   | 1   | 2   | One     | One     |
| 1   | 2   | 1   | 1   | Two     | One     |
| 2   | 1   | 4   | 3   | One     | Hello   |
| 3   | 3   | 2   | 1   | Three   | Two     |

</div>

## Creating dummy variables

A reminder to my future self, based on [this](https://www.youtube.com/watch?v=0s_1IsROgDc&list=PL5-da3qGB5ICCsgW1MxlZ0Hq8LL5U3u9y&index=24) great video from Data School.

``` python
df = pd.DataFrame(
    {
        "id": [1, 2, 3, 4, 5],
        "quality": ["good", "excellent", "very good", "excellent", "good"],
    }
)
df.head()
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

|     | id  | quality   |
|-----|-----|-----------|
| 0   | 1   | good      |
| 1   | 2   | excellent |
| 2   | 3   | very good |
| 3   | 4   | excellent |
| 4   | 5   | good      |

</div>

Pandas makes creating dummies easy:

``` python
pd.get_dummies(df.quality)
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

|     | excellent | good | very good |
|-----|-----------|------|-----------|
| 0   | 0         | 1    | 0         |
| 1   | 1         | 0    | 0         |
| 2   | 0         | 0    | 1         |
| 3   | 1         | 0    | 0         |
| 4   | 0         | 1    | 0         |

</div>

If you want to label the source of the data, you can use the prefix argument:

``` python
pd.get_dummies(df.quality, prefix="quality")
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

|     | quality_excellent | quality_good | quality_very good |
|-----|-------------------|--------------|-------------------|
| 0   | 0                 | 1            | 0                 |
| 1   | 1                 | 0            | 0                 |
| 2   | 0                 | 0            | 1                 |
| 3   | 1                 | 0            | 0                 |
| 4   | 0                 | 1            | 0                 |

</div>

Often when we work with dummies from a variable with $n$ distinct values, we create $n-1$ dummies and treat the remaining group as the reference group. Pandas provides a convenient way to do this:

``` python
pd.get_dummies(df.quality, prefix="quality", drop_first=True)
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

|     | quality_good | quality_very good |
|-----|--------------|-------------------|
| 0   | 1            | 0                 |
| 1   | 0            | 0                 |
| 2   | 0            | 1                 |
| 3   | 0            | 0                 |
| 4   | 1            | 0                 |

</div>

Usually, we'll want to use the dummies with the rest of the data, so it's conveninet to have them in the original dataframe. One way to do this is to use concat like so:

``` python
dummies = pd.get_dummies(df.quality, prefix="quality", drop_first=True)
df_with_dummies = pd.concat([df, dummies], axis=1)
df_with_dummies.head()
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

|     | id  | quality   | quality_good | quality_very good |
|-----|-----|-----------|--------------|-------------------|
| 0   | 1   | good      | 1            | 0                 |
| 1   | 2   | excellent | 0            | 0                 |
| 2   | 3   | very good | 0            | 1                 |
| 3   | 4   | excellent | 0            | 0                 |
| 4   | 5   | good      | 1            | 0                 |

</div>

This works. But Pandas provides a much easier way:

``` python
df_with_dummies1 = pd.get_dummies(df, columns=["quality"], drop_first=True)
df_with_dummies1
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

|     | id  | quality_good | quality_very good |
|-----|-----|--------------|-------------------|
| 0   | 1   | 1            | 0                 |
| 1   | 2   | 0            | 0                 |
| 2   | 3   | 0            | 1                 |
| 3   | 4   | 0            | 0                 |
| 4   | 5   | 1            | 0                 |

</div>

That's it. In one line we get a new dataframe that includes the dummies and excludes the original quality column.

## Pivot tables

``` python
df = sns.load_dataset("planets")
print(df.shape)
df.head(3)
```

    (1035, 6)

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

|     | method          | number | orbital_period | mass | distance | year |
|-----|-----------------|--------|----------------|------|----------|------|
| 0   | Radial Velocity | 1      | 269.300        | 7.10 | 77.40    | 2006 |
| 1   | Radial Velocity | 1      | 874.774        | 2.21 | 56.95    | 2008 |
| 2   | Radial Velocity | 1      | 763.000        | 2.60 | 19.84    | 2011 |

</div>

Create a table that shows the number of planets discovered by each method in each decade

``` python
# Using groupby

decade = (df.year.astype(str).str[:3] + '0s')
decade.name = 'decade'

df.groupby(['method', decade]).number.sum().unstack().fillna(0).astype(int)
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

| decade                        | 1980s | 1990s | 2000s | 2010s |
|-------------------------------|-------|-------|-------|-------|
| method                        |       |       |       |       |
| Astrometry                    | 0     | 0     | 0     | 2     |
| Eclipse Timing Variations     | 0     | 0     | 5     | 10    |
| Imaging                       | 0     | 0     | 29    | 21    |
| Microlensing                  | 0     | 0     | 12    | 15    |
| Orbital Brightness Modulation | 0     | 0     | 0     | 5     |
| Pulsar Timing                 | 0     | 9     | 1     | 1     |
| Pulsation Timing Variations   | 0     | 0     | 1     | 0     |
| Radial Velocity               | 1     | 52    | 475   | 424   |
| Transit                       | 0     | 0     | 64    | 712   |
| Transit Timing Variations     | 0     | 0     | 0     | 9     |

</div>

``` python
# Using pivot_table

df.pivot_table(index='method', columns=decade, values='number', aggfunc='sum', fill_value=0)
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

| decade                        | 1980s | 1990s | 2000s | 2010s |
|-------------------------------|-------|-------|-------|-------|
| method                        |       |       |       |       |
| Astrometry                    | 0     | 0     | 0     | 2     |
| Eclipse Timing Variations     | 0     | 0     | 5     | 10    |
| Imaging                       | 0     | 0     | 29    | 21    |
| Microlensing                  | 0     | 0     | 12    | 15    |
| Orbital Brightness Modulation | 0     | 0     | 0     | 5     |
| Pulsar Timing                 | 0     | 9     | 1     | 1     |
| Pulsation Timing Variations   | 0     | 0     | 1     | 0     |
| Radial Velocity               | 1     | 52    | 475   | 424   |
| Transit                       | 0     | 0     | 64    | 712   |
| Transit Timing Variations     | 0     | 0     | 0     | 9     |

</div>

## Counting number of equal adjacent values

In the below column, cumulatively count the number of adjacent equal values.

``` python
df = pd.DataFrame([1, 5, 7, 7, 1, 1, 1, 0], columns=["a"])
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

|     | a   |
|-----|-----|
| 0   | 1   |
| 1   | 5   |
| 2   | 7   |
| 3   | 7   |
| 4   | 1   |
| 5   | 1   |
| 6   | 1   |
| 7   | 0   |

</div>

Solution based on [this](https://stackoverflow.com/a/29143354/13666841) Stack Overflow answer:

``` python
df["count"] = df.groupby((df.a != df.a.shift()).cumsum()).cumcount().add(1)
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

|     | a   | count |
|-----|-----|-------|
| 0   | 1   | 1     |
| 1   | 5   | 1     |
| 2   | 7   | 1     |
| 3   | 7   | 2     |
| 4   | 1   | 1     |
| 5   | 1   | 2     |
| 6   | 1   | 3     |
| 7   | 0   | 1     |

</div>

## Reset `cumsum()` at each missing value

``` python
s = pd.Series([1.0, 3.0, 1.0, np.nan, 1.0, 1.0, 1.0, 1.0, np.nan, 1.0])
s
```

    0    1.0
    1    3.0
    2    1.0
    3    NaN
    4    1.0
    5    1.0
    6    1.0
    7    1.0
    8    NaN
    9    1.0
    dtype: float64

What I don't want:

``` python
s.cumsum()
```

    0     1.0
    1     4.0
    2     5.0
    3     NaN
    4     6.0
    5     7.0
    6     8.0
    7     9.0
    8     NaN
    9    10.0
    dtype: float64

Instead, I want to reset the counter to zero after each missing value. Solution from [this](https://stackoverflow.com/a/36436195/13666841) SO answer.

``` python
cumsum = s.cumsum().ffill()
reset = -cumsum[s.isna()].diff().fillna(cumsum)
result = s.where(s.notna(), reset).cumsum()
result
```

    0    1.0
    1    4.0
    2    5.0
    3    0.0
    4    1.0
    5    2.0
    6    3.0
    7    4.0
    8    0.0
    9    1.0
    dtype: float64

## Apply

### Using apply with groupby

From the [cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#grouping):

``` python
df = pd.DataFrame(
    {
        "animal": "cat dog cat fish dog cat cat".split(),
        "size": list("SSMMMLL"),
        "weight": [8, 10, 11, 1, 20, 12, 12],
        "adult": [False] * 5 + [True] * 2,
    }
)
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

|     | animal | size | weight | adult |
|-----|--------|------|--------|-------|
| 0   | cat    | S    | 8      | False |
| 1   | dog    | S    | 10     | False |
| 2   | cat    | M    | 11     | False |
| 3   | fish   | M    | 1      | False |
| 4   | dog    | M    | 20     | False |
| 5   | cat    | L    | 12     | True  |
| 6   | cat    | L    | 12     | True  |

</div>

For each type of animal, return the size of the heaviest one

``` python
df.groupby('animal').apply(lambda g: g.loc[g.weight.idxmax(), 'size'])
```

    animal
    cat     L
    dog     M
    fish    M
    dtype: object

### Expanding apply

Assume you want to calculate the cumulative return from a series of one-period returns in an expanding fashion -- in each period, you want the cumulative return up to that period.

``` python
s = pd.Series([i / 100.0 for i in range(1, 4)])
s
```

    0    0.01
    1    0.02
    2    0.03
    dtype: float64

The solution is given [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#grouping).

``` python
import functools


def cum_return(x, y):
    return x * (1 + y)


def red(x):
    res = functools.reduce(cum_return, x, 1)
    return res


s.expanding().apply(red, raw=True)
```

    0    1.010000
    1    1.030200
    2    1.061106
    dtype: float64

I found that somewhere between bewildering and magical. To see what's going on, it helps to add a few print statements:

``` python
import functools


def cum_return(x, y):
    print("x:", x)
    print("y:", y)
    return x * (1 + y)


def red(x):
    print("Series:", x)
    res = functools.reduce(cum_return, x, 1)
    print("Result:", res)
    print()
    return res


s.expanding().apply(red, raw=True)
```

    Series: [0.01]
    x: 1
    y: 0.01
    Result: 1.01

    Series: [0.01 0.02]
    x: 1
    y: 0.01
    x: 1.01
    y: 0.02
    Result: 1.0302

    Series: [0.01 0.02 0.03]
    x: 1
    y: 0.01
    x: 1.01
    y: 0.02
    x: 1.0302
    y: 0.03
    Result: 1.061106

    0    1.010000
    1    1.030200
    2    1.061106
    dtype: float64

This makes transparent how reduce works: it takes the starting value (1 here) as the initial x value and the first value of the series as y value, and then returns the result of cum_returns. Next, it uses that result as x, and the second element in the series as y, and calculates the new result of cum_returns. This is then repeated until it has run through the entire series.

What surprised me is to see that reduce always starts the calculation from the beginning, rather than re-using the last calculated result. This seems inefficient, but is probably necessary for some reason.

### Sort by sum of group values

``` python
df = pd.DataFrame(
    {
        "code": ["foo", "bar", "baz"] * 2,
        "data": [0.16, -0.21, 0.33, 0.45, -0.59, 0.62],
        "flag": [False, True] * 3,
    }
)

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

|     | code | data  | flag  |
|-----|------|-------|-------|
| 0   | foo  | 0.16  | False |
| 1   | bar  | -0.21 | True  |
| 2   | baz  | 0.33  | False |
| 3   | foo  | 0.45  | True  |
| 4   | bar  | -0.59 | False |
| 5   | baz  | 0.62  | True  |

</div>

``` python
g = df.groupby("code")
sort_order = g["data"].transform(sum).sort_values().index
df.loc[sort_order]
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

|     | code | data  | flag  |
|-----|------|-------|-------|
| 1   | bar  | -0.21 | True  |
| 4   | bar  | -0.59 | False |
| 0   | foo  | 0.16  | False |
| 3   | foo  | 0.45  | True  |
| 2   | baz  | 0.33  | False |
| 5   | baz  | 0.62  | True  |

</div>

### Get observation with largest data entry for each group

``` python
df.iloc[df.groupby('code').data.idxmax().values]
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

|     | code | data  | flag |
|-----|------|-------|------|
| 1   | bar  | -0.21 | True |
| 5   | baz  | 0.62  | True |
| 3   | foo  | 0.45  | True |

</div>

### Expanding group operations

Based on [this](https://stackoverflow.com/a/15489701/13666841) answer.

``` python
df = pd.DataFrame(
    {
        "code": ["foo", "bar", "baz"] * 4,
        "data": [0.16, -0.21, 0.33, 0.45, -0.59, 0.62] * 2,
        "flag": [False, True] * 6,
    }
)
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

|     | code | data  | flag  |
|-----|------|-------|-------|
| 0   | foo  | 0.16  | False |
| 1   | bar  | -0.21 | True  |
| 2   | baz  | 0.33  | False |
| 3   | foo  | 0.45  | True  |
| 4   | bar  | -0.59 | False |
| 5   | baz  | 0.62  | True  |
| 6   | foo  | 0.16  | False |
| 7   | bar  | -0.21 | True  |
| 8   | baz  | 0.33  | False |
| 9   | foo  | 0.45  | True  |
| 10  | bar  | -0.59 | False |
| 11  | baz  | 0.62  | True  |

</div>

``` python
g = df.groupby("code")

def helper(g):
    s = g.data.expanding()
    g["exp_mean"] = s.mean()
    g["exp_sum"] = s.sum()
    g["exp_count"] = s.count()
    return g


g.apply(helper).sort_values("code")
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

|     | code | data  | flag  | exp_mean  | exp_sum | exp_count |
|-----|------|-------|-------|-----------|---------|-----------|
| 1   | bar  | -0.21 | True  | -0.210000 | -0.21   | 1.0       |
| 4   | bar  | -0.59 | False | -0.400000 | -0.80   | 2.0       |
| 7   | bar  | -0.21 | True  | -0.336667 | -1.01   | 3.0       |
| 10  | bar  | -0.59 | False | -0.400000 | -1.60   | 4.0       |
| 2   | baz  | 0.33  | False | 0.330000  | 0.33    | 1.0       |
| 5   | baz  | 0.62  | True  | 0.475000  | 0.95    | 2.0       |
| 8   | baz  | 0.33  | False | 0.426667  | 1.28    | 3.0       |
| 11  | baz  | 0.62  | True  | 0.475000  | 1.90    | 4.0       |
| 0   | foo  | 0.16  | False | 0.160000  | 0.16    | 1.0       |
| 3   | foo  | 0.45  | True  | 0.305000  | 0.61    | 2.0       |
| 6   | foo  | 0.16  | False | 0.256667  | 0.77    | 3.0       |
| 9   | foo  | 0.45  | True  | 0.305000  | 1.22    | 4.0       |

</div>

### Get observation with largest data entry for each group

``` python
df = pd.DataFrame({"a": [4, 5, 6, 7], "b": [10, 20, 30, 40], "c": [100, 50, -30, -50]})
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

|     | a   | b   | c   |
|-----|-----|-----|-----|
| 0   | 4   | 10  | 100 |
| 1   | 5   | 20  | 50  |
| 2   | 6   | 30  | -30 |
| 3   | 7   | 40  | -50 |

</div>

``` python
myval = 34
df.loc[(df.c - myval).abs().argsort()]
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

|     | a   | b   | c   |
|-----|-----|-----|-----|
| 1   | 5   | 20  | 50  |
| 2   | 6   | 30  | -30 |
| 0   | 4   | 10  | 100 |
| 3   | 7   | 40  | -50 |

</div>

Reminder of what happens here:

``` python
a = (df.c - myval).abs()
b = a.argsort()
a, b
```

    (0    66
     1    16
     2    64
     3    84
     Name: c, dtype: int64,
     0    1
     1    2
     2    0
     3    3
     Name: c, dtype: int64)

`argsort` returns a series of indexes, so that `df[b]` returns an ordered dataframe. The first element in `b` thus refers to the index of the smallest element in `a`.

### Creating separate dataframe for each group

``` python
df = sns.load_dataset("iris")
pieces = dict(list(df.groupby("species")))
pieces["setosa"].head(3)
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

|     | sepal_length | sepal_width | petal_length | petal_width | species |
|-----|--------------|-------------|--------------|-------------|---------|
| 0   | 5.1          | 3.5         | 1.4          | 0.2         | setosa  |
| 1   | 4.9          | 3.0         | 1.4          | 0.2         | setosa  |
| 2   | 4.7          | 3.2         | 1.3          | 0.2         | setosa  |

</div>

## Aggregating

From [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#pivot)

``` python
df = pd.DataFrame(
    {
        "StudentID": ["x1", "x10", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"],
        "StudentGender": ["F", "M", "F", "M", "F", "M", "F", "M", "M", "M"],
        "ExamYear": [
            "2007",
            "2007",
            "2007",
            "2008",
            "2008",
            "2008",
            "2008",
            "2009",
            "2009",
            "2009",
        ],
        "Exam": [
            "algebra",
            "stats",
            "bio",
            "algebra",
            "algebra",
            "stats",
            "stats",
            "algebra",
            "bio",
            "bio",
        ],
        "Participated": [
            "no",
            "yes",
            "yes",
            "yes",
            "no",
            "yes",
            "yes",
            "yes",
            "yes",
            "yes",
        ],
        "Passed": ["no", "yes", "yes", "yes", "no", "yes", "yes", "yes", "no", "yes"],
    },
    columns=[
        "StudentID",
        "StudentGender",
        "ExamYear",
        "Exam",
        "Participated",
        "Passed",
    ],
)

df.columns = [str.lower(c) for c in df.columns]
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

|     | studentid | studentgender | examyear | exam    | participated | passed |
|-----|-----------|---------------|----------|---------|--------------|--------|
| 0   | x1        | F             | 2007     | algebra | no           | no     |
| 1   | x10       | M             | 2007     | stats   | yes          | yes    |
| 2   | x2        | F             | 2007     | bio     | yes          | yes    |
| 3   | x3        | M             | 2008     | algebra | yes          | yes    |
| 4   | x4        | F             | 2008     | algebra | no           | no     |
| 5   | x5        | M             | 2008     | stats   | yes          | yes    |
| 6   | x6        | F             | 2008     | stats   | yes          | yes    |
| 7   | x7        | M             | 2009     | algebra | yes          | yes    |
| 8   | x8        | M             | 2009     | bio     | yes          | no     |
| 9   | x9        | M             | 2009     | bio     | yes          | yes    |

</div>

``` python
numyes = lambda x: sum(x == 'yes')
df.groupby('examyear').agg({'participated': numyes, 'passed': numyes})
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

|          | participated | passed |
|----------|--------------|--------|
| examyear |              |        |
| 2007     | 2            | 2      |
| 2008     | 3            | 3      |
| 2009     | 3            | 2      |

</div>

## Count days since last occurrence of event

We want a count of the number of days passed since the last event happened.

``` python
df = pd.DataFrame(
    {
        "date": pd.date_range(start="1 Jan 2022", periods=8, freq="d"),
        "event": [np.nan, np.nan, 1, np.nan, np.nan, np.nan, 4, np.nan],
        "result": [np.nan, np.nan, 0, 1, 2, 3, 0, 1],
    }
)
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

|     | date       | event | result |
|-----|------------|-------|--------|
| 0   | 2022-01-01 | NaN   | NaN    |
| 1   | 2022-01-02 | NaN   | NaN    |
| 2   | 2022-01-03 | 1.0   | 0.0    |
| 3   | 2022-01-04 | NaN   | 1.0    |
| 4   | 2022-01-05 | NaN   | 2.0    |
| 5   | 2022-01-06 | NaN   | 3.0    |
| 6   | 2022-01-07 | 4.0   | 0.0    |
| 7   | 2022-01-08 | NaN   | 1.0    |

</div>

``` python
def add_days_since_event(df):
    ones = df.event.ffill().where(lambda s: s.isna(), 1)
    cumsum = ones.cumsum()
    reset = -cumsum[df.event.notna()].diff().fillna(cumsum).sub(1)
    df["result"] = ones.where(df.event.isna(), reset).cumsum()
    return df


add_days_since_event(df)
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

|     | date       | event | result |
|-----|------------|-------|--------|
| 0   | 2022-01-01 | NaN   | NaN    |
| 1   | 2022-01-02 | NaN   | NaN    |
| 2   | 2022-01-03 | 1.0   | 0.0    |
| 3   | 2022-01-04 | NaN   | 1.0    |
| 4   | 2022-01-05 | NaN   | 2.0    |
| 5   | 2022-01-06 | NaN   | 3.0    |
| 6   | 2022-01-07 | 4.0   | 0.0    |
| 7   | 2022-01-08 | NaN   | 1.0    |

</div>

## Sources

-   [Python for Data Analysis](https://www.oreilly.com/library/view/python-for-data/9781491957653/)
-   [Python Data Science Handbook](https://www.oreilly.com/library/view/python-data-science/9781491912126/)
-   [Pandas cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html)
-   [Data School - Data science best practice with Pandas](https://www.youtube.com/watch?v=dPwLlJkSHLo)
