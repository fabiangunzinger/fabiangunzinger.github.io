# Fluent Pandas



<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous" data-relocate-top="true"></script>
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

## Filter

``` python
df = sns.load_dataset("diamonds", cache=False)
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

### Filter rows

Filter based on column value

``` python
cutoff = 5_000

a = df.loc[df.price > cutoff]
b = df.query("price > @cutoff")
c = df[df.price > cutoff]

all(a == b) == all(b == c)
```

    True

Filter based on index

``` python
df.iloc[5:10]
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
| 5   | 5.4          | 3.9         | 1.7          | 0.4         | setosa  |
| 6   | 4.6          | 3.4         | 1.4          | 0.3         | setosa  |
| 7   | 5.0          | 3.4         | 1.5          | 0.2         | setosa  |
| 8   | 4.4          | 2.9         | 1.4          | 0.2         | setosa  |
| 9   | 4.9          | 3.1         | 1.5          | 0.1         | setosa  |

</div>

More complex index filtering

``` python
df.filter(regex='^\d0$', axis=0).head()
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

|     | sepal_length | sepal_width | petal_length | petal_width | species    |
|-----|--------------|-------------|--------------|-------------|------------|
| 10  | 5.4          | 3.7         | 1.5          | 0.2         | setosa     |
| 20  | 5.4          | 3.4         | 1.7          | 0.2         | setosa     |
| 30  | 4.8          | 3.1         | 1.6          | 0.2         | setosa     |
| 40  | 5.0          | 3.5         | 1.3          | 0.3         | setosa     |
| 50  | 7.0          | 3.2         | 4.7          | 1.4         | versicolor |

</div>

### Filter columns

``` python
df = sns.load_dataset('iris', cache=False)
df.head(3)
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

``` python
df.filter(like='sepal', axis=1).head(3)
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
| 2   | 4.7          | 3.2         |

</div>

``` python
df.filter(regex="_length").head(2)
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

## Expanding dataset

Sometimes I want to duplicate each row in a dataset a certain number of times.

``` python
df.iloc[df.index.repeat(2)].reset_index(drop=True).head()
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
| 1   | 5.1          | 3.5         | 1.4          | 0.2         | setosa  |
| 2   | 4.9          | 3.0         | 1.4          | 0.2         | setosa  |
| 3   | 4.9          | 3.0         | 1.4          | 0.2         | setosa  |
| 4   | 4.7          | 3.2         | 1.3          | 0.2         | setosa  |

</div>

## Grouping and resampling

`groupby()` implements the splict-apply-combine paradigm, while `resample()` is a convenience method for frequency conversion and resampling of time series. When both are used on time series, the main difference is that `resample()` fills in missing dates while `groupby()` doesn't.

``` python
index = pd.date_range('2024', freq='2d', periods=3)
data = {'col': range(len(index))}
df = (pd.DataFrame(data=data, index=index)
      .loc[lambda df: df.index.repeat(2)])
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

|            | col |
|------------|-----|
| 2024-01-01 | 0   |
| 2024-01-01 | 0   |
| 2024-01-03 | 1   |
| 2024-01-03 | 1   |
| 2024-01-05 | 2   |
| 2024-01-05 | 2   |

</div>

``` python
df.resample("d").col.sum()
```

    2024-01-01    0
    2024-01-02    0
    2024-01-03    2
    2024-01-04    0
    2024-01-05    4
    Freq: D, Name: col, dtype: int64

``` python
df.groupby(level=0).col.sum()
```

    2024-01-01    0
    2024-01-03    2
    2024-01-05    4
    Name: col, dtype: int64

## Grouping -- count vs size

-   `count()` is a DataFrame, Series, and Grouper method that return the count of non-missing rows.
-   `size()` is a Grouper method that returns the count of rows per group (including rows with missing elements)
-   `size` is also a DataFrame property that returns the number of elements (including cells with missing values) and a Series property that returns the number of rows (including rows with missing values).

``` python
df = sns.load_dataset("titanic")
df.head(3)
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

|  | survived | pclass | sex | age | sibsp | parch | fare | embarked | class | who | adult_male | deck | embark_town | alive | alone |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | 0 | 3 | male | 22.0 | 1 | 0 | 7.2500 | S | Third | man | True | NaN | Southampton | no | False |
| 1 | 1 | 1 | female | 38.0 | 1 | 0 | 71.2833 | C | First | woman | False | C | Cherbourg | yes | False |
| 2 | 1 | 3 | female | 26.0 | 0 | 0 | 7.9250 | S | Third | woman | False | NaN | Southampton | yes | True |

</div>

``` python
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

|  | survived | pclass | age | sibsp | parch | fare | embarked | class | who | adult_male | deck | embark_town | alive | alone |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| sex |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| female | 314 | 314 | 261 | 314 | 314 | 314 | 312 | 314 | 314 | 314 | 97 | 312 | 314 | 314 |
| male | 577 | 577 | 453 | 577 | 577 | 577 | 577 | 577 | 577 | 577 | 106 | 577 | 577 | 577 |

</div>

``` python
df.groupby("sex").size()
```

    sex
    female    314
    male      577
    dtype: int64

``` python
df.size, df.sex.size
```

    (13365, 891)

## Aggregating -- different methods

``` python
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

|  | survived | pclass | sex | age | sibsp | parch | fare | embarked | class | who | adult_male | deck | embark_town | alive | alone |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | 0 | 3 | male | 22.0 | 1 | 0 | 7.2500 | S | Third | man | True | NaN | Southampton | no | False |
| 1 | 1 | 1 | female | 38.0 | 1 | 0 | 71.2833 | C | First | woman | False | C | Cherbourg | yes | False |
| 2 | 1 | 3 | female | 26.0 | 0 | 0 | 7.9250 | S | Third | woman | False | NaN | Southampton | yes | True |
| 3 | 1 | 1 | female | 35.0 | 1 | 0 | 53.1000 | S | First | woman | False | C | Southampton | yes | False |
| 4 | 0 | 3 | male | 35.0 | 0 | 0 | 8.0500 | S | Third | man | True | NaN | Southampton | no | True |

</div>

``` python
def range(x):
    return int(x.min()), int(x.max())

df.groupby(['class', 'sex']).agg(
    age_mean=('age', 'mean'),
    fare_range=('fare',range),
    survived_mean=('survived', 'mean')
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

|        |        | age_mean  | fare_range | survived_mean |
|--------|--------|-----------|------------|---------------|
| class  | sex    |           |            |               |
| First  | female | 34.611765 | (25, 512)  | 0.968085      |
|        | male   | 41.281386 | (0, 512)   | 0.368852      |
| Second | female | 28.722973 | (10, 65)   | 0.921053      |
|        | male   | 30.740707 | (0, 73)    | 0.157407      |
| Third  | female | 21.750000 | (6, 69)    | 0.500000      |
|        | male   | 26.507589 | (0, 69)    | 0.135447      |

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
df.head(3)
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

|  | survived | pclass | sex | age | sibsp | parch | fare | embarked | class | who | adult_male | deck | embark_town | alive | alone |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | 0 | 3 | male | 22.0 | 1 | 0 | 7.2500 | S | Third | man | True | NaN | Southampton | no | False |
| 1 | 1 | 1 | female | 38.0 | 1 | 0 | 71.2833 | C | First | woman | False | C | Cherbourg | yes | False |
| 2 | 1 | 3 | female | 26.0 | 0 | 0 | 7.9250 | S | Third | woman | False | NaN | Southampton | yes | True |

</div>

``` python
df.sex.apply(lambda x: len(x)).head(3)
```

    0    4
    1    6
    2    6
    Name: sex, dtype: int64

``` python
df.sex.map(lambda x: len(x)).head(3)
```

    0    4
    1    6
    2    6
    Name: sex, dtype: int64

``` python
df.applymap(lambda x: len(str(x))).head(3)
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

|  | survived | pclass | sex | age | sibsp | parch | fare | embarked | class | who | adult_male | deck | embark_town | alive | alone |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | 1 | 1 | 4 | 4 | 1 | 1 | 4 | 1 | 5 | 3 | 4 | 3 | 11 | 2 | 5 |
| 1 | 1 | 1 | 6 | 4 | 1 | 1 | 7 | 1 | 5 | 5 | 5 | 1 | 9 | 3 | 5 |
| 2 | 1 | 1 | 6 | 4 | 1 | 1 | 5 | 1 | 5 | 5 | 5 | 3 | 11 | 3 | 4 |

</div>

``` python
new_labs = {"male": "m", "female": "f"}
df.sex.apply(new_labs.get).head(3)
```

    0    m
    1    f
    2    f
    Name: sex, dtype: object

`get` turns a dictionary into a function that takes a key and returns its corresponding value if the key is in the dictionary and a default value otherwise.

## Create Meta type retention curves

``` python
np.random.choice([0, 1])
```

    1

``` python
n_users = 3
n_periods = 2

date = pd.period_range(start="Jan 2023", freq="D", periods=n_periods).to_list() * n_users
uid = np.arange(n_users).repeat(n_periods)
active = np.random.choice([0, 1], n_users * n_periods)

df = pd.DataFrame({
    "uid": uid,
    "date": date,
    "active": active
})
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

|     | uid | date       | active |
|-----|-----|------------|--------|
| 0   | 0   | 2023-01-01 | 1      |
| 1   | 0   | 2023-01-02 | 0      |
| 2   | 1   | 2023-01-01 | 1      |
| 3   | 1   | 2023-01-02 | 1      |
| 4   | 2   | 2023-01-01 | 1      |
| 5   | 2   | 2023-01-02 | 1      |

</div>

``` python
df.groupby('uid').rolling(window=2, min_periods=1).mean()
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

|     |     | active |
|-----|-----|--------|
| uid |     |        |
| 0   | 0   | 1.0    |
|     | 1   | 0.5    |
| 1   | 2   | 1.0    |
|     | 3   | 1.0    |
| 2   | 4   | 1.0    |
|     | 5   | 1.0    |

</div>

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

