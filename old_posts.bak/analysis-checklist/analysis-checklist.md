---
title: General
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


A list of checklists to ensure consistency and quality across key data science
tasks.

``` python
import pandas as pd
import seaborn as sns

sns.set_style("whitegrid")
```

-   Use samples of different sized for code development if useful, but don't
    switch back and forth between samples for analysis (might get hung up on
    explaining small sample artifacts).

-   Do not rename variables in a dataset unless there is a very good reason for it (doing so makes it harder to communicate with stakeholders and other researchers using the same data). I used to do this because I preferred short and logical names, which you often don't get in a dataset. Renaming makes more and more sense the longer you will be working with a dataset, and the fewer other people work with it and are generally involved in the project.

-   Do not drop (non-redundant) variables in the cleaning state (you might use those columns even if you don't think you will).

## Questions to ask when starting to work with dataset

-   What is the unit of analysis? (e.g. rider? rider-hour? rider-zone-hour?)

## Data

### Storage

### Import

``` python
df = pd.read_csv("competitor_prices.csv", parse_dates=['Date'])
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

|     | Date       | Product_id | Competitor_id | Competitor_Price |
|-----|------------|------------|---------------|------------------|
| 0   | 2013-11-25 | 4.0        | C             | 74.95            |
| 1   | 2013-11-25 | 4.0        | D             | 74.95            |
| 2   | 2013-11-25 | 4.0        | E             | 75.00            |

</div>

### Inspection

``` python
# Check available variables and whether types are reasonable

df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 15395 entries, 0 to 15394
    Data columns (total 4 columns):
     #   Column            Non-Null Count  Dtype         
    ---  ------            --------------  -----         
     0   Date              15132 non-null  datetime64[ns]
     1   Product_id        15132 non-null  float64       
     2   Competitor_id     15132 non-null  object        
     3   Competitor_Price  15132 non-null  float64       
    dtypes: datetime64[ns](1), float64(2), object(1)
    memory usage: 481.2+ KB

``` python
# Look at raw samples to get feel for coding, missingness, anomalies, etc.
df.sample(n=10)
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

|       | Date       | Product_id | Competitor_id | Competitor_Price |
|-------|------------|------------|---------------|------------------|
| 841   | 2013-12-16 | 33.0       | D             | 64.40            |
| 2722  | 2014-02-18 | 126.0      | E             | 124.95           |
| 894   | 2013-08-12 | 51.0       | D             | 80.85            |
| 8594  | 2013-09-12 | 302.0      | C             | 119.95           |
| 14068 | 2013-12-15 | 405.0      | D             | 38.75            |
| 12120 | 2013-12-12 | 368.0      | D             | 30.00            |
| 12596 | 2014-02-18 | 380.0      | D             | 59.15            |
| 15380 | NaT        | NaN        | NaN           | NaN              |
| 5293  | 2014-02-13 | 192.0      | D             | 68.15            |
| 10872 | 2014-12-03 | 331.0      | D             | 39.50            |

</div>

``` python
# Check distribution of numeric variables
df.describe(datetime_is_numeric=True)
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

|       | Date                          | Product_id   | Competitor_Price |
|-------|-------------------------------|--------------|------------------|
| count | 15132                         | 15132.000000 | 15132.000000     |
| mean  | 2014-01-01 18:46:32.069785856 | 248.535223   | 85.339813        |
| min   | 2013-01-12 00:00:00           | 4.000000     | 2.300000         |
| 25%   | 2013-11-28 00:00:00           | 143.000000   | 49.950000        |
| 50%   | 2013-12-25 00:00:00           | 251.000000   | 75.000000        |
| 75%   | 2014-02-18 00:00:00           | 355.000000   | 108.000000       |
| max   | 2014-12-03 00:00:00           | 421.000000   | 500.000000       |
| std   | NaN                           | 115.916096   | 48.460998        |

</div>

``` python
# Check distribution of category columns

def cat_counts(df):
    cats = df.select_dtypes('object')
    for cat in cats:
        print(df[cat].value_counts(), end='\n--\n')
        
cat_counts(df)
```

    D    8092
    C    2475
    F    2248
    E    1478
    A     651
    G     124
    B      64
    Name: Competitor_id, dtype: int64
    --

### Exploration and integrity checks

#### Visual inspection

#### Missing values

todo: best practices of use of: https://github.com/ResidentMario/missingno

#### Duplicates

``` python
def dups(df):
    d = df.duplicated().sum()
    print(f"{d} of {len(df)} rows ({d/len(df):.1%}) are duplicates.")


dups(df)
```

    500 of 15395 rows (3.2%) are duplicates.

#### Columns types

Ensure that columns are of desired type

#### Value format

Ensure that values conform to required formats (e.g. use regex to validate postcodes and ids)

### Tidying

### Transform

-   Subsetting data
-   Creating new variables

### Variable transformation

-   For discussion on when and when not to use log(x + c), see mullahy2022why

## Analysis

### Regression model specification

-   Does it make sense to take logs of currency amounts or large integers
    (especially if there are few cases with zero, in which case using *log(x +
    1)* is usually fine to avoid missing values from zeroes)?

-   Does it make sense to standardise some variables to interpret changes in std
    or even standardise all variables (to get Beta coefficients) to easily gage
    relative importance of variables?

-   Have I included variables that I shouldn't have given the ceteris-paribus
    interpretation of the coefficients (e.g. include alcohol consumption when
    estimating effect of alcohol tax on traffic fatalities, which will mostly run
    through lower alcohol consumption).

-   Are there variables that are correlated with *y* but not the included *x*s
    that I haven't included yet? (If so, I should, as it increases precision of
    the estimates without causing multicollinearity issues.)

## Communication
