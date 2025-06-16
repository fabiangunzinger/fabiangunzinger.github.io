# Pandas categories



<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous" data-relocate-top="true"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


## Basics

Values and order:

-   All values of a categorical valiable are either in `categories` or are `np.nan`.

-   Order is defined by the order of `categories`, not the lexical order of the values.

Memory structure:

-   Internally, the data structure consists of a `categories` array and an integer arrays of `codes`, which point to the values in the `categories` array.

-   The memory usage of a categorical variable is proportional to the number of categories plus the length of the data, while that for an object dtype is a constant times the length of the data. As the number of categories approaches the length of the data, memory usage approaches that of object type.

Use cases:

-   To save memory (if number of categories is small relative to the number of rows)

-   If logical order differs from lexical order (e.g. 'small', 'medium', 'large')

-   To signal to libraries that column should be treated as a category (e.g. for plotting)

## General best practices

Operating on categories:

-   Operate on category values directly rather than column elements (e.g. to rename categories use `df.catvar.cat.rename_rategories(*args, **kwargs)`).

-   If there is no `cat` method available, consider operating on categories directly with `df.catvar.cat.categories`.

Merging:

-   Pandas treats categorical variables with different categories as different data types

-   Category merge keys will only be categories in the merged dataframe if they are of the same data types (i.e. have the same categories), otherwise they will be converted back to objects

Grouping:

-   By default, we group on all categories, not just those present in the data.

-   More often than not, you'll want to use `df.groupby(catvar, observed=True)` to only use categories observed in the data.

## Operations I frequently use

``` python
import numpy as np
import pandas as pd
import seaborn as sns
```

``` python
df = sns.load_dataset("taxis")
df["pickup"] = pd.to_datetime(df.pickup)
df["dropoff"] = pd.to_datetime(df.dropoff)
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

|  | pickup | dropoff | passengers | distance | fare | tip | tolls | total | color | payment | pickup_zone | dropoff_zone | pickup_borough | dropoff_borough |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | 2019-03-23 20:21:09 | 2019-03-23 20:27:24 | 1 | 1.60 | 7.0 | 2.15 | 0.0 | 12.95 | yellow | credit card | Lenox Hill West | UN/Turtle Bay South | Manhattan | Manhattan |
| 1 | 2019-03-04 16:11:55 | 2019-03-04 16:19:00 | 1 | 0.79 | 5.0 | 0.00 | 0.0 | 9.30 | yellow | cash | Upper West Side South | Upper West Side South | Manhattan | Manhattan |

</div>

### Convert all string variables to categories

``` python
str_cols = df.select_dtypes("object")
df[str_cols.columns] = str_cols.astype("category")
```

### Convert labels of all categorical variables to lowercase

``` python
cat_cols = df.select_dtypes("category")
df[cat_cols.columns] = cat_cols.apply(lambda col: col.cat.rename_categories(str.lower))
```

### String and datetime accessors

-   When using the `str` and `dt` accessors on a variable of type `category`, pandas applies the operation on the `categories` rather than the entire array (which is nice) and then creates and returns a new string or date array (which is often not helpful for me).

``` python
df.payment.str.upper().head(3)
```

    0    CREDIT CARD
    1           CASH
    2    CREDIT CARD
    Name: payment, dtype: object

-   For operations that `cat` provides methods for (e.g. renaming as used above), the solution is to use those methods.

-   For others (e.g. regex searches) the solution is to operate on the categories directly myself.

## Object creation

Convert *sex* and *class* to the same categorical type, with categories being the union of all unique values of both columns.

``` python
cols = ["sex", "who"]
unique_values = np.unique(titanic[cols].to_numpy().ravel())
categories = pd.CategoricalDtype(categories=unique_values)
titanic[cols] = titanic[cols].astype(categories)
print(titanic.sex.cat.categories)
print(titanic.who.cat.categories)
```

    Index(['child', 'female', 'male', 'man', 'woman'], dtype='object')
    Index(['child', 'female', 'male', 'man', 'woman'], dtype='object')

``` python
# restore sex and who to object types
titanic[cols] = titanic[cols].astype("object")
```

## Custom order

``` python
df = pd.DataFrame({"quality": ["good", "excellent", "very good"]})
df.sort_values("quality")
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

|     | quality   |
|-----|-----------|
| 1   | excellent |
| 0   | good      |
| 2   | very good |

</div>

``` python
ordered_quality = pd.CategoricalDtype(["good", "very good", "excellent"], ordered=True)
df.quality = df.quality.astype(ordered_quality)
df.sort_values("quality")
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

|     | quality   |
|-----|-----------|
| 0   | good      |
| 2   | very good |
| 1   | excellent |

</div>

## Unique values

`Series.unique` returns values in order of appearance, and only returns values that are present in the data.

``` python
dfs = df.head(5)
```

``` python
assert not len(dfs.pickup_zone.unique()) == len(dfs.pickup_zone.cat.categories)
```

## References

-   [Docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/categorical.html#object-creation)

-   [Useful Medium article](https://towardsdatascience.com/staying-sane-while-adopting-pandas-categorical-datatypes-78dbd19dcd8a)

