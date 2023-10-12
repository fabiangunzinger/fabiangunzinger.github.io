---
title: "Tidy data in Pandas"
date: "2020-09-22"
tags:
    - python, datascience
execute:
    enabled: false
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


Based on excellent materials materials from Daniel Chen [here](https://github.com/chendaniely/pydatadc_2018-tidy) and talk [here](https://www.youtube.com/watch?v=iYie42M1ZyU)

``` python
from imports import *
%load_ext autoreload
%autoreload 2
```

## Creating tidy data

Definition by Hadley Wickham [here](http://vita.had.co.nz/papers/tidy-data.pdf):

1.  Each variable is a column
2.  Each observation is a row
3.  Each type of observational unit is a table.

## Columns are values

``` python
pew = pd.read_csv('https://raw.githubusercontent.com/chendaniely/pydatadc_2018-tidy/master/data/pew.csv')
pew.head()
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

|     | religion           | \<\$10k | \$10-20k | \$20-30k | \$30-40k | \$40-50k | \$50-75k | \$75-100k | \$100-150k | \>150k | Don\'t know/refused |
|-----|--------------------|---------|----------|----------|----------|----------|----------|-----------|------------|--------|---------------------|
| 0   | Agnostic           | 27      | 34       | 60       | 81       | 76       | 137      | 122       | 109        | 84     | 96                  |
| 1   | Atheist            | 12      | 27       | 37       | 52       | 35       | 70       | 73        | 59         | 74     | 76                  |
| 2   | Buddhist           | 27      | 21       | 30       | 34       | 33       | 58       | 62        | 39         | 53     | 54                  |
| 3   | Catholic           | 418     | 617      | 732      | 670      | 638      | 1116     | 949       | 792        | 633    | 1489                |
| 4   | Don't know/refused | 15      | 14       | 15       | 11       | 10       | 35       | 21        | 17         | 18     | 116                 |

</div>

``` python
# Create a single income column
pew.melt(
    id_vars='religion',
    var_name='income',
    value_name='count'
).head()
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

|     | religion           | income  | count |
|-----|--------------------|---------|-------|
| 0   | Agnostic           | \<\$10k | 27    |
| 1   | Atheist            | \<\$10k | 12    |
| 2   | Buddhist           | \<\$10k | 27    |
| 3   | Catholic           | \<\$10k | 418   |
| 4   | Don't know/refused | \<\$10k | 15    |

</div>

``` python
billboard = pd.read_csv('https://raw.githubusercontent.com/chendaniely/pydatadc_2018-tidy/master/data/billboard.csv')
billboard.columns
```

    Index(['year', 'artist', 'track', 'time', 'date.entered', 'wk1', 'wk2', 'wk3',
           'wk4', 'wk5', 'wk6', 'wk7', 'wk8', 'wk9', 'wk10', 'wk11', 'wk12',
           'wk13', 'wk14', 'wk15', 'wk16', 'wk17', 'wk18', 'wk19', 'wk20', 'wk21',
           'wk22', 'wk23', 'wk24', 'wk25', 'wk26', 'wk27', 'wk28', 'wk29', 'wk30',
           'wk31', 'wk32', 'wk33', 'wk34', 'wk35', 'wk36', 'wk37', 'wk38', 'wk39',
           'wk40', 'wk41', 'wk42', 'wk43', 'wk44', 'wk45', 'wk46', 'wk47', 'wk48',
           'wk49', 'wk50', 'wk51', 'wk52', 'wk53', 'wk54', 'wk55', 'wk56', 'wk57',
           'wk58', 'wk59', 'wk60', 'wk61', 'wk62', 'wk63', 'wk64', 'wk65', 'wk66',
           'wk67', 'wk68', 'wk69', 'wk70', 'wk71', 'wk72', 'wk73', 'wk74', 'wk75',
           'wk76'],
          dtype='object')

``` python
idvars = billboard.columns[~bb.columns.str.startswith('wk')]

tidy_billboard = billboard.melt(
    id_vars=idvars,
    var_name='week', 
    value_name='rating'
)
tidy_billboard.head()
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

|     | year | artist       | track                     | time | date.entered | week | rating |
|-----|------|--------------|---------------------------|------|--------------|------|--------|
| 0   | 2000 | 2 Pac        | Baby Don\'t Cry (Keep\... | 4:22 | 2000-02-26   | wk1  | 87.0   |
| 1   | 2000 | 2Ge+her      | The Hardest Part Of \...  | 3:15 | 2000-09-02   | wk1  | 91.0   |
| 2   | 2000 | 3 Doors Down | Kryptonite                | 3:53 | 2000-04-08   | wk1  | 81.0   |
| 3   | 2000 | 3 Doors Down | Loser                     | 4:24 | 2000-10-21   | wk1  | 76.0   |
| 4   | 2000 | 504 Boyz     | Wobble Wobble             | 3:35 | 2000-04-15   | wk1  | 57.0   |

</div>

## Multiple variables stored in one column

``` python
ebola = pd.read_csv('https://raw.githubusercontent.com/chendaniely/pydatadc_2018-tidy/master/data/country_timeseries.csv')
ebola.head()
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

|     | Date       | Day | Cases_Guinea | Cases_Liberia | Cases_SierraLeone | Cases_Nigeria | Cases_Senegal | Cases_UnitedStates | Cases_Spain | Cases_Mali | Deaths_Guinea | Deaths_Liberia | Deaths_SierraLeone | Deaths_Nigeria | Deaths_Senegal | Deaths_UnitedStates | Deaths_Spain | Deaths_Mali |
|-----|------------|-----|--------------|---------------|-------------------|---------------|---------------|--------------------|-------------|------------|---------------|----------------|--------------------|----------------|----------------|---------------------|--------------|-------------|
| 0   | 1/5/2015   | 289 | 2776.0       | NaN           | 10030.0           | NaN           | NaN           | NaN                | NaN         | NaN        | 1786.0        | NaN            | 2977.0             | NaN            | NaN            | NaN                 | NaN          | NaN         |
| 1   | 1/4/2015   | 288 | 2775.0       | NaN           | 9780.0            | NaN           | NaN           | NaN                | NaN         | NaN        | 1781.0        | NaN            | 2943.0             | NaN            | NaN            | NaN                 | NaN          | NaN         |
| 2   | 1/3/2015   | 287 | 2769.0       | 8166.0        | 9722.0            | NaN           | NaN           | NaN                | NaN         | NaN        | 1767.0        | 3496.0         | 2915.0             | NaN            | NaN            | NaN                 | NaN          | NaN         |
| 3   | 1/2/2015   | 286 | NaN          | 8157.0        | NaN               | NaN           | NaN           | NaN                | NaN         | NaN        | NaN           | 3496.0         | NaN                | NaN            | NaN            | NaN                 | NaN          | NaN         |
| 4   | 12/31/2014 | 284 | 2730.0       | 8115.0        | 9633.0            | NaN           | NaN           | NaN                | NaN         | NaN        | 1739.0        | 3471.0         | 2827.0             | NaN            | NaN            | NaN                 | NaN          | NaN         |

</div>

``` python
# Tidying ebola step by step
tidy_ebola = ebola.melt(id_vars=['Date', 'Day'], value_name='Cases')
tidy_ebola[['Statistic', 'Country']] = (tidy_ebola.variable
                                        .str.split('_', expand=True))
tidy_ebola.drop('variable', axis=1, inplace=True)
tidy_ebola.head()
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

|     | Date       | Day | Cases  | Statistic | Country |
|-----|------------|-----|--------|-----------|---------|
| 0   | 1/5/2015   | 289 | 2776.0 | Cases     | Guinea  |
| 1   | 1/4/2015   | 288 | 2775.0 | Cases     | Guinea  |
| 2   | 1/3/2015   | 287 | 2769.0 | Cases     | Guinea  |
| 3   | 1/2/2015   | 286 | NaN    | Cases     | Guinea  |
| 4   | 12/31/2014 | 284 | 2730.0 | Cases     | Guinea  |

</div>

``` python
# Using a pipeline
(ebola
 .melt(id_vars=['Date', 'Day'], value_name='Cases')
 .assign(Statistic = lambda df: df.variable.str.split('_', expand=True)[0])
 .assign(Country = lambda df: df.variable.str.split('_', expand=True)[1])
 .drop('variable', axis=1)
).head()
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

|     | Date       | Day | Cases  | Statistic | Country |
|-----|------------|-----|--------|-----------|---------|
| 0   | 1/5/2015   | 289 | 2776.0 | Cases     | Guinea  |
| 1   | 1/4/2015   | 288 | 2775.0 | Cases     | Guinea  |
| 2   | 1/3/2015   | 287 | 2769.0 | Cases     | Guinea  |
| 3   | 1/2/2015   | 286 | NaN    | Cases     | Guinea  |
| 4   | 12/31/2014 | 284 | 2730.0 | Cases     | Guinea  |

</div>

## Variables are stored in both rows and columns

``` python
weather = pd.read_csv('https://raw.githubusercontent.com/chendaniely/pydatadc_2018-tidy/master/data/weather.csv')
weather.head()
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

|     | id      | year | month | element | d1  | d2   | d3   | d4  | d5   | d6  | d7  | d8  | d9  | d10  | d11  | d12 | d13 | d14 | d15 | d16  | d17 | d18 | d19 | d20 | d21 | d22 | d23  | d24 | d25 | d26 | d27 | d28 | d29 | d30  | d31 |
|-----|---------|------|-------|---------|-----|------|------|-----|------|-----|-----|-----|-----|------|------|-----|-----|-----|-----|------|-----|-----|-----|-----|-----|-----|------|-----|-----|-----|-----|-----|-----|------|-----|
| 0   | MX17004 | 2010 | 1     | tmax    | NaN | NaN  | NaN  | NaN | NaN  | NaN | NaN | NaN | NaN | NaN  | NaN  | NaN | NaN | NaN | NaN | NaN  | NaN | NaN | NaN | NaN | NaN | NaN | NaN  | NaN | NaN | NaN | NaN | NaN | NaN | 27.8 | NaN |
| 1   | MX17004 | 2010 | 1     | tmin    | NaN | NaN  | NaN  | NaN | NaN  | NaN | NaN | NaN | NaN | NaN  | NaN  | NaN | NaN | NaN | NaN | NaN  | NaN | NaN | NaN | NaN | NaN | NaN | NaN  | NaN | NaN | NaN | NaN | NaN | NaN | 14.5 | NaN |
| 2   | MX17004 | 2010 | 2     | tmax    | NaN | 27.3 | 24.1 | NaN | NaN  | NaN | NaN | NaN | NaN | NaN  | 29.7 | NaN | NaN | NaN | NaN | NaN  | NaN | NaN | NaN | NaN | NaN | NaN | 29.9 | NaN | NaN | NaN | NaN | NaN | NaN | NaN  | NaN |
| 3   | MX17004 | 2010 | 2     | tmin    | NaN | 14.4 | 14.4 | NaN | NaN  | NaN | NaN | NaN | NaN | NaN  | 13.4 | NaN | NaN | NaN | NaN | NaN  | NaN | NaN | NaN | NaN | NaN | NaN | 10.7 | NaN | NaN | NaN | NaN | NaN | NaN | NaN  | NaN |
| 4   | MX17004 | 2010 | 3     | tmax    | NaN | NaN  | NaN  | NaN | 32.1 | NaN | NaN | NaN | NaN | 34.5 | NaN  | NaN | NaN | NaN | NaN | 31.1 | NaN | NaN | NaN | NaN | NaN | NaN | NaN  | NaN | NaN | NaN | NaN | NaN | NaN | NaN  | NaN |

</div>

``` python
(weather
 .melt(
     id_vars=['id', 'year', 'month', 'element'],
     var_name='day',
     value_name='temp'
 )
 .pivot_table(
     index=['id', 'year', 'month', 'day'],
     columns='element',
     values='temp'
 )
 .reset_index()
 .assign(day = lambda df: df.day.str.extract('(\d+)'))
).head()
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

| element | id      | year | month | day | tmax | tmin |
|---------|---------|------|-------|-----|------|------|
| 0       | MX17004 | 2010 | 1     | 30  | 27.8 | 14.5 |
| 1       | MX17004 | 2010 | 2     | 11  | 29.7 | 13.4 |
| 2       | MX17004 | 2010 | 2     | 2   | 27.3 | 14.4 |
| 3       | MX17004 | 2010 | 2     | 23  | 29.9 | 10.7 |
| 4       | MX17004 | 2010 | 2     | 3   | 24.1 | 14.4 |

</div>

## Multiple types of observational units are stored in a single table

``` python
tidy_billboard.head()
tidy_bb = tidy_billboard
tidy_bb.head()
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

|     | year | artist       | track                     | time | date.entered | week | rating |
|-----|------|--------------|---------------------------|------|--------------|------|--------|
| 0   | 2000 | 2 Pac        | Baby Don\'t Cry (Keep\... | 4:22 | 2000-02-26   | wk1  | 87.0   |
| 1   | 2000 | 2Ge+her      | The Hardest Part Of \...  | 3:15 | 2000-09-02   | wk1  | 91.0   |
| 2   | 2000 | 3 Doors Down | Kryptonite                | 3:53 | 2000-04-08   | wk1  | 81.0   |
| 3   | 2000 | 3 Doors Down | Loser                     | 4:24 | 2000-10-21   | wk1  | 76.0   |
| 4   | 2000 | 504 Boyz     | Wobble Wobble             | 3:35 | 2000-04-15   | wk1  | 57.0   |

</div>

``` python
bb_songs = (
    tidy_bb[['year', 'artist', 'track', 'time', 'date.entered']]
    .drop_duplicates()
    .assign(id = lambda df: range(len(df)))
)
bb_songs.head()
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

|     | year | artist       | track                     | time | date.entered | id  |
|-----|------|--------------|---------------------------|------|--------------|-----|
| 0   | 2000 | 2 Pac        | Baby Don\'t Cry (Keep\... | 4:22 | 2000-02-26   | 0   |
| 1   | 2000 | 2Ge+her      | The Hardest Part Of \...  | 3:15 | 2000-09-02   | 1   |
| 2   | 2000 | 3 Doors Down | Kryptonite                | 3:53 | 2000-04-08   | 2   |
| 3   | 2000 | 3 Doors Down | Loser                     | 4:24 | 2000-10-21   | 3   |
| 4   | 2000 | 504 Boyz     | Wobble Wobble             | 3:35 | 2000-04-15   | 4   |

</div>

``` python
bb_ratings = (
    tidy_bb
    .merge(bb_songs)
    .loc[:, ['week', 'rating', 'id']]
)
bb_ratings.head()
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

|     | week | rating | id  |
|-----|------|--------|-----|
| 0   | wk1  | 87.0   | 0   |
| 1   | wk2  | 82.0   | 0   |
| 2   | wk3  | 72.0   | 0   |
| 3   | wk4  | 77.0   | 0   |
| 4   | wk5  | 87.0   | 0   |

</div>
