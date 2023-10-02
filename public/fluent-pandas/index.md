# Fluent Pandas


<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


This post is part of my series of posts on [`pandas`](https://pandas.pydata.org).

[Fluent Pandas](http://localhost:8888/lab/tree/_notebooks/2021-03-12-fluent-pandas.ipynb) contains notes on how to effectively use pandas core features.

[Fast pandas](http://localhost:8888/lab/tree/_notebooks/0000-09-03-fast-pandas.ipynb) contains notes on how to effectively work with large datasets.

[Pandas cookbook](http://localhost:8888/lab/tree/_notebooks/2020-08-09-pandas-cookbook.ipynb) is a list of recipes for effectively solving common and not so common problems.

``` python
import numpy as np
import pandas as pd
import seaborn as sns
```

## Sort and filter

``` python
df = sns.load_dataset("diamonds")
print(df.shape)
df.head(2)
```

    (53940, 10)

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

|     | carat | cut     | color | clarity | depth | table | price | x    | y    | z    |
|-----|-------|---------|-------|---------|-------|-------|-------|------|------|------|
| 0   | 0.23  | Ideal   | E     | SI2     | 61.5  | 55.0  | 326   | 3.95 | 3.98 | 2.43 |
| 1   | 0.21  | Premium | E     | SI1     | 59.8  | 61.0  | 326   | 3.89 | 3.84 | 2.31 |

</div>

### Filter data

``` python
cutoff = 30_000
a = df.loc[df.amount > cutoff]
b = df.query("amount > @cutoff")
c = df[df.amount > cutoff]
all(a == b) == all(b == c)
```

    True

### Filter columns

``` python
df.filter(like="sepal", axis=1).head(2)
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

|     | sepal_length | sepal_width |
|-----|--------------|-------------|
| 0   | 5.1          | 3.5         |
| 1   | 4.9          | 3.0         |

</div>

``` python
df.filter(regex=".+_length").head(2)
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

|     | sepal_length | petal_length |
|-----|--------------|--------------|
| 0   | 5.1          | 1.4          |
| 1   | 4.9          | 1.4          |

</div>

## `groupb()` vs `resample()`

`groupby()` implements the splict-apply-combine paradigm, while `resample()` is a convenience method for frequency conversion and resampling of time series. When both are used on time series, the main difference is that `resample()` fills in missing dates while `groupby()` doesn't.

``` python
index = pd.date_range("2020", freq="2d", periods=3)
data = pd.DataFrame({"col": range(len(index))}, index=index)
data
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

|            | col |
|------------|-----|
| 2020-01-01 | 0   |
| 2020-01-03 | 1   |
| 2020-01-05 | 2   |

</div>

``` python
data.resample("d").col.sum()
```

    2020-01-01    0
    2020-01-02    0
    2020-01-03    1
    2020-01-04    0
    2020-01-05    2
    Freq: D, Name: col, dtype: int64

``` python
data.groupby(level=0).col.sum()
```

    2020-01-01    0
    2020-01-03    1
    2020-01-05    2
    Freq: 2D, Name: col, dtype: int64

## Aggregate

### `count()` vs `size()`

-   `count()` is a DataFrame, Series, and Grouper method that return the count of non-missing rows.
-   `size()` is a Grouper method that returns the count of rows per group (including rows with missing elements)
-   `size` is also a DataFrame property that returns the number of elements (including cells with missing values) and a Series property that returns the number of rows (including rows with missing values).

``` python
df = sns.load_dataset("titanic")
df.groupby("sex").count()
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

|        | survived | pclass | age | sibsp | parch | fare | embarked | class | who | adult_male | deck | embark_town | alive | alone |
|--------|----------|--------|-----|-------|-------|------|----------|-------|-----|------------|------|-------------|-------|-------|
| sex    |          |        |     |       |       |      |          |       |     |            |      |             |       |       |
| female | 314      | 314    | 261 | 314   | 314   | 314  | 312      | 314   | 314 | 314        | 97   | 312         | 314   | 314   |
| male   | 577      | 577    | 453 | 577   | 577   | 577  | 577      | 577   | 577 | 577        | 106  | 577         | 577   | 577   |

</div>

``` python
df.groupby("sex").size()
```

    sex
    female    314
    male      577
    dtype: int64

### Naming columns

``` python
def spread(s):
    return s.max() - s.min()


df.groupby("species").agg(
    mean_sepal_length=("sepal_length", "mean"),
    max_petal_width=("petal_width", "max"),
    spread_petal_width=("petal_width", spread),
)
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

|            | mean_sepal_length | max_petal_width | spread_petal_width |
|------------|-------------------|-----------------|--------------------|
| species    |                   |                 |                    |
| setosa     | 5.006             | 0.6             | 0.5                |
| versicolor | 5.936             | 1.8             | 0.8                |
| virginica  | 6.588             | 2.5             | 1.1                |

</div>

## MultiIndex

Working with indices, expecially column indices, and especially with hierarchical ones, is an area of Pandas I keep finding perplexing. The point of this notebook is to help my future self.

``` python
df = sns.load_dataset("iris")
df.head(2)
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

</div>

Create hierarchical column names

``` python
df = df.set_index("species")
tuples = [tuple(c) for c in df.columns.str.split("_")]
df.columns = pd.MultiIndex.from_tuples(tuples)
df.head(2)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>

|         | sepal  |       | petal  |       |
|---------|--------|-------|--------|-------|
|         | length | width | length | width |
| species |        |       |        |       |
| setosa  | 5.1    | 3.5   | 1.4    | 0.2   |
| setosa  | 4.9    | 3.0   | 1.4    | 0.2   |

</div>

Flatten column names

``` python
names = ["_".join(c) for c in df.columns]
df.columns = names
df.reset_index(inplace=True)
df.head(2)
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

|     | species | sepal_length | sepal_width | petal_length | petal_width |
|-----|---------|--------------|-------------|--------------|-------------|
| 0   | setosa  | 5.1          | 3.5         | 1.4          | 0.2         |
| 1   | setosa  | 4.9          | 3.0         | 1.4          | 0.2         |

</div>

Flattening using method (from [here](https://stackoverflow.com/a/49483208/13666841))

``` python
df.set_axis(df.columns.map("_".join), axis=1)
```

or, of course, with a list comprehension, like so:

``` python
df.set_axis(["_".join(c) for c in df.columns], axis=1)
```

## Mappings

### `apply` vs `map` vs `applymap`

-   `apply` applies a function along an axis of a dataframe or on series values
-   `map` applies a correspondance to each value in a series
-   `applymap` applies a function to each element in a dataframe

``` python
data = df.loc[:2, ["gender", "merchant"]]
gender = {"m": "male", "f": "female"}
data
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

|     | gender | merchant  |
|-----|--------|-----------|
| 0   | m      | aviva     |
| 1   | m      | tesco     |
| 2   | m      | mcdonalds |

</div>

``` python
data.apply(lambda x: x.map(gender))
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

|     | gender | merchant |
|-----|--------|----------|
| 0   | male   | NaN      |
| 1   | male   | NaN      |
| 2   | male   | NaN      |

</div>

``` python
data.gender.map(gender)
```

    0    male
    1    male
    2    male
    Name: gender, dtype: object

``` python
data.applymap(gender.get)
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

|     | gender | merchant |
|-----|--------|----------|
| 0   | male   | None     |
| 1   | male   | None     |
| 2   | male   | None     |

</div>

`get` turns a dictionary into a function that takes a key and returns its corresponding value if the key is in the dictionary and a default value otherwise.

## Sources

-   [Python for Data Analysis](https://www.oreilly.com/library/view/python-for-data/9781491957653/)
-   [Python Data Science Handbook](https://www.oreilly.com/library/view/python-data-science/9781491912126/) (PDSH)
-   [Pandas cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html)

<!-- - [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
- [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
- [Learning Python](https://www.oreilly.com/library/view/learning-python-5th/9781449355722/)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/)
- [Effective Python](https://effectivepython.com)
- [Python for Data Analysis](https://www.oreilly.com/library/view/python-for-data/9781491957653/)
- [Python Data Science Handbook](https://www.oreilly.com/library/view/python-data-science/9781491912126/) -->

