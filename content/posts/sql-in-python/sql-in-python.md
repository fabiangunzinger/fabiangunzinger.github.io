---
title: SQL in Python
date: '2020-09-12'
tags:
  - tools
execute:
  enabled: false
---


<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous" data-relocate-top="true"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


## SQLite

Based on [docs](https://docs.python.org/3/library/sqlite3.html).

``` python
import os
import sys

src_path = os.path.abspath(os.path.join(".."))
sys.path.append(src_path)
import sqlite3

import pandas as pd
from src import config
```

``` python
# parameters

SAMPLE = "777"
```

``` python
df = pd.read_parquet(os.path.join(config.TEMPDIR, f"data_{SAMPLE}.parquet"))
print(df.shape)
df.head(2)
```

    (562996, 22)

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

|  | user_id | transaction_date | amount | transaction_description | merchant_name | auto_tag | tag | manual_tag | postcode | credit_debit | \... | account_created | user_registration_date | year_of_birth | account_id | merchant_business_line | latest_balance | transaction_id | account_last_refreshed | account_type | gender |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | 60777 | 2014-11-27 | 100.0 | xxxxxx xxxx5014 internet transfer | no merchant | transfers | broadband | no tag | n16 0 | debit | \... | 2015-02-12 | 2014-05-23 | 1988.0 | 378967 | personal | 0.0 | 58866450 | 2017-04-04 07:33:00 | savings | m |
| 1 | 60777 | 2014-11-27 | -250.0 | \<mdbremoved\> | no merchant | savings (general) | savings (general) | no tag | n16 0 | credit | \... | 2015-02-12 | 2014-05-23 | 1988.0 | 378968 | no merchant business line | 3000.0 | 58866344 | 2017-04-04 07:33:00 | savings | m |

<p>2 rows × 22 columns</p>
</div>

``` python
pd.read_sql("select * from pragma_table_info('outcomes')", conn).name.values
```

    array(['user_id'], dtype=object)

### Connect to database

``` python
db_path = os.path.join(config.DATADIR, f"{SAMPLE}.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()
```

``` python
def create_user_list(sample):
    """Create list of users of sample."""
    file_name = f'data_{sample}.parquet'
    file_path = os.path.join(config.TEMPDIR, file_name)
    df = pd.read_parquet(file_path)
    return df.user_id.unique()drop_duplicates().sort_values()

samples = ['XX7', 'X77', '777']
for sample in ['777']:
    create_user_list(sample).to_csv('/Users/fgu/tmp/test.csv', index=False)
```

``` python
path = os.path.join(config.DATADIR, "users_777.csv")
pd.read_csv(path)
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

|      | Unnamed: 0 | user_id |
|------|------------|---------|
| 0    | 0          | 777     |
| 1    | 0          | 1777    |
| 2    | 7116       | 7777    |
| 3    | 0          | 8777    |
| 4    | 1228       | 10777   |
| \... | \...       | \...    |
| 179  | 129064     | 578777  |
| 180  | 133470     | 579777  |
| 181  | 135176     | 582777  |
| 182  | 136885     | 586777  |
| 183  | 139404     | 587777  |

<p>184 rows × 2 columns</p>
</div>

### Create tables

Create tables with user_ids

``` python
ids = pd.Series({"user_id": df.user_id.unique()})

tables = ["targets", "predictions", "outcomes"]
for table in tables:
    ids.to_sql(table, conn, index=False)
    conn.execute(f"create index idx_{table}_user_id on {table}(user_id)")
```

``` python
pd.Series({"user_id": df.user_id.unique()})
```

    user_id    [60777, 64777, 777, 7777, 71777, 76777, 50777,...
    dtype: object

``` python
pd.read_sql("select * from sqlite_master", conn)
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

|  | type | name | tbl_name | rootpage | sql |
|----|----|----|----|----|----|
| 0 | table | targets | targets | 2 | CREATE TABLE \"targets\" (\n\"user_id\" INTEGER\n) |
| 1 | index | idx_targets_user_id | targets | 3 | CREATE INDEX idx_targets_user_id on targets(us\... |
| 2 | table | predictions | predictions | 4 | CREATE TABLE \"predictions\" (\n\"user_id\" INTEGE\... |
| 3 | index | idx_predictions_user_id | predictions | 5 | CREATE INDEX idx_predictions_user_id on predic\... |
| 4 | table | outcomes | outcomes | 6 | CREATE TABLE \"outcomes\" (\n\"user_id\" INTEGER\n) |
| 5 | index | idx_outcomes_user_id | outcomes | 7 | CREATE INDEX idx_outcomes_user_id on outcomes(\... |

</div>

``` python
pd.read_sql("select * from targets", conn)
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

|      | user_id |
|------|---------|
| 0    | 777     |
| 1    | 1777    |
| 2    | 7777    |
| 3    | 8777    |
| 4    | 10777   |
| \... | \...    |
| 179  | 578777  |
| 180  | 579777  |
| 181  | 582777  |
| 182  | 586777  |
| 183  | 587777  |

<p>184 rows × 1 columns</p>
</div>

### Add tables

``` python
def db_tables():
    res = conn.execute("select name from sqlite_master where type = 'table'")
    return [r[0] for r in res.fetchall()]


db_tables()
```

    ['targets', 'predictions', 'outcomes', 'tmp']

``` python
def db_tables():
    query = "select name from sqlite_master where type = 'table'"
    return pd.read_sql(query, conn).name.values


db_tables()
```

    array(['targets', 'predictions', 'outcomes', 'tmp'], dtype=object)

``` python
def add_table(table, table_name):
    """Add table to database."""
    if table_name not in db_tables():
        table.to_sql(table_name, conn, index=False)
```

### Add columns

``` python
conn.execute("select name from sqlite_master").fetchall()
```

    [('targets',), ('predictions',), ('outcomes',), ('tmp',)]

``` python
def tab_cols(table, conn):
    query = "select name from pragma_table_info(?)"
    return pd.read_sql(query, conn, params=(table,)).name.values


tab_cols("outcomes", conn)
```

    array(['user_id', 'spendmax', 'spendmin', 'spendmean'], dtype=object)

``` python
def tab_cols(table):
    """List table columns."""
    res = c.execute("select name from pragma_table_info(?)", (table,))
    return [n[0] for n in res.fetchall()]


tab_cols("outcomes")
```

    ['user_id', 'spendmax', 'spendmin', 'spendmean']

``` python
def add_column(df, table):
    """Add column to table.

    Input:
        pd.DataFrame with columns ['user_id', 'col_name'].
    """
    col_name = df.columns[1]
    if col_name not in tab_cols(table):
        df.to_sql("tmp", conn, index=False)
        conn.executescript(
            f"""
            alter table {table} add column {col_name};

            update {table}
            set {col_name} = (
                select {col_name} from tmp
                where {table}.user_id = tmp.user_id);

            drop table tmp;
            """
        )
```

``` python
def add_table(table):
    """Add table to database."""
```

``` python
def spendmax(df):
    return (
        df.groupby("user_id")
        .apply(lambda u: u[u.amount > 0].amount.max())
        .rename("spendmax")
        .reset_index()
    )


def spendmin(df):
    return (
        df.groupby("user_id")
        .apply(lambda u: u[u.amount > 0].amount.min())
        .rename("spendmin")
        .reset_index()
    )


def spendmean(df):
    return (
        df.groupby("user_id")
        .apply(lambda u: u[u.amount > 0].amount.mean())
        .rename("spendmean")
        .reset_index()
    )
```

``` python
outcomes = [spendmax, spendmin, spendmean]

for outcome in outcomes:
    add_column(outcome(df), "outcomes")
    display(pd.read_sql("select * from outcomes", conn))
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

|      | user_id | spendmax     | spendmin | spendmean  |
|------|---------|--------------|----------|------------|
| 0    | 60777   | 47885.449219 | 0.02     | 92.656956  |
| 1    | 64777   | 10000.000000 | 0.01     | 51.317209  |
| 2    | 777     | 4898.879883  | 0.01     | 54.275365  |
| 3    | 7777    | 22300.000000 | 0.07     | 111.685793 |
| 4    | 71777   | 4000.000000  | 0.01     | 146.197356 |
| \... | \...    | \...         | \...     | \...       |
| 179  | 299777  | 20265.000000 | 0.10     | 79.127393  |
| 180  | 8777    | 14998.000000 | 0.01     | 378.858950 |
| 181  | 80777   | 17633.800781 | 0.03     | 130.221119 |
| 182  | 83777   | 35000.000000 | 0.01     | 86.623218  |
| 183  | 86777   | 8000.000000  | 0.04     | 93.136604  |

<p>184 rows × 4 columns</p>
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

|      | user_id | spendmax     | spendmin | spendmean  |
|------|---------|--------------|----------|------------|
| 0    | 60777   | 47885.449219 | 0.02     | 92.656956  |
| 1    | 64777   | 10000.000000 | 0.01     | 51.317209  |
| 2    | 777     | 4898.879883  | 0.01     | 54.275365  |
| 3    | 7777    | 22300.000000 | 0.07     | 111.685793 |
| 4    | 71777   | 4000.000000  | 0.01     | 146.197356 |
| \... | \...    | \...         | \...     | \...       |
| 179  | 299777  | 20265.000000 | 0.10     | 79.127393  |
| 180  | 8777    | 14998.000000 | 0.01     | 378.858950 |
| 181  | 80777   | 17633.800781 | 0.03     | 130.221119 |
| 182  | 83777   | 35000.000000 | 0.01     | 86.623218  |
| 183  | 86777   | 8000.000000  | 0.04     | 93.136604  |

<p>184 rows × 4 columns</p>
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

|      | user_id | spendmax     | spendmin | spendmean  |
|------|---------|--------------|----------|------------|
| 0    | 60777   | 47885.449219 | 0.02     | 92.656956  |
| 1    | 64777   | 10000.000000 | 0.01     | 51.317209  |
| 2    | 777     | 4898.879883  | 0.01     | 54.275365  |
| 3    | 7777    | 22300.000000 | 0.07     | 111.685793 |
| 4    | 71777   | 4000.000000  | 0.01     | 146.197356 |
| \... | \...    | \...         | \...     | \...       |
| 179  | 299777  | 20265.000000 | 0.10     | 79.127393  |
| 180  | 8777    | 14998.000000 | 0.01     | 378.858950 |
| 181  | 80777   | 17633.800781 | 0.03     | 130.221119 |
| 182  | 83777   | 35000.000000 | 0.01     | 86.623218  |
| 183  | 86777   | 8000.000000  | 0.04     | 93.136604  |

<p>184 rows × 4 columns</p>
</div>

### Connection info

[PRAGMA](https://www.sqlite.org/pragma.html) is your friend for this and many other pieces of metadata.

List databases attached to the current connection

``` python
pd.read_sql_query("select * from pragma_database_list", conn)
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

|     | seq | name | file                                               |
|-----|-----|------|----------------------------------------------------|
| 0   | 0   | main | /Users/fgu/Library/Mobile Documents/com~apple~\... |

</div>

### Database info

List tables attached to a database

``` python
pd.read_sql_query(
    """
    select
        *
    from
        sqlite_master
    where
        type = 'table' and
        name not like 'sqlite_%'
    """,
    conn,
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

|     | type  | name     | tbl_name | rootpage | sql                                     |
|-----|-------|----------|----------|----------|-----------------------------------------|
| 0   | table | targets  | targets  | 2        | CREATE TABLE targets(\n user_id int\... |
| 1   | table | predict  | predict  | 3        | CREATE TABLE predict(\n user_id int\... |
| 2   | table | outcomes | outcomes | 4        | CREATE TABLE outcomes(\n user_id in\... |

</div>

List indices attached to database

``` python
pd.read_sql_query(
    """
select
    *
from
    sqlite_master
where
    type = 'index'
""",
    conn,
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

|     | type | name | tbl_name | rootpage | sql |
|-----|------|------|----------|----------|-----|

</div>

### Table info

List columns attached to a table

``` python
table = ("targets",)
pd.read_sql_query("select * from pragma_table_info(?)", conn, params=table)
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

|     | cid | name    | type    | notnull | dflt_value | pk  |
|-----|-----|---------|---------|---------|------------|-----|
| 0   | 0   | user_id | integer | 0       | None       | 1   |

</div>

Get structure of a table

``` python
print(c.execute("select sql from sqlite_master where name = ?", table).fetchall()[0][0])
```

    CREATE TABLE targets(
                user_id integer primary key
            )

Indices associated with a table

``` python
c.execute("pragma index_list('targets')").fetchall()
```

    []

## Misc usefuls stuff

Move content of one table to another table

``` python
c.execute("""insert into new_table select * from old_table""")
```

Vacuum database regularly after altering tables or columns to free up overhead and reduce disk space.

``` python
c.execute("vacuum;")
```

    <sqlite3.Cursor at 0x11c74a650>

### Enable foreign key constraints

``` python
c.execute("select * from pragma_foreign_keys").fetchall()
```

    [(0,)]

``` python
c.execute("pragma foreign_keys=on")
c.execute("select * from pragma_foreign_keys").fetchall()
```

    [(1,)]

``` python
c.execute("pragma foreign_keys=off")
c.execute("select * from pragma_foreign_keys").fetchall()
```

    [(0,)]

### Use `namedtuple()`

``` python
from collections import namedtuple

TableInfo = namedtuple("TableInfo", "cid, name, type, notnull, dflt_value, pk")


def tab_cols(table):
    """List table columns."""
    raw_cols = c.execute("select * from pragma_table_info(?)", (table,)).fetchall()
    named_cols = map(TableInfo._make, raw_cols)
    return [(c.name, c.type, c.pk) for c in named_cols]


tab_cols("outcomes")
```

    [('user_id', 'integer', 1)]

The above deliberately overuses `namedtuple` for practice.

### Use namedtuple

This is useful, and we can guess that the second element in each tuple is the column name. But it would be nice to know what the remaining information is, and then to be able to refer to different pieces of information by their name.

To find out what each piece of information is, we can either check out the [PRAGMA docs](https://sqlite.org/pragma.html#pragma_table_info) or, what I find even more useful, can use Pandas like so: (ideally, there would be a way to retrieve column names directly from the query, but I haven't been able to find any way to do so.)

``` python
import pandas as pd

tabinf = pd.read_sql_query("select * from pragma_table_info('stocks')", conn)
tabinf
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

|     | cid | name     | type | notnull | dflt_value | pk  |
|-----|-----|----------|------|---------|------------|-----|
| 0   | 0   | name     | text | 0       | None       | 0   |
| 1   | 1   | quantity | real | 0       | None       | 0   |
| 2   | 2   | price    | real | 0       | None       | 0   |

</div>

To label the pieces in the `table_cols` function, we can store the column names and create a `namedtuple()` ([docs](https://docs.python.org/3/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields)).

``` python
from collections import namedtuple

TableInfo = namedtuple("TableInfo", "cid, name, type, notnull, dflt_value, pk")
```

Mapping each tuple in the list that `table_info()` returns to our named tuple, we get the following:

``` python
for a in map(TableInfo._make, table_cols(table)):
    print(a)
```

    TableInfo(cid=0, name='name', type='text', notnull=0, dflt_value=None, pk=0)
    TableInfo(cid=1, name='quantity', type='real', notnull=0, dflt_value=None, pk=0)
    TableInfo(cid=2, name='price', type='real', notnull=0, dflt_value=None, pk=0)

Or, what we really want:

``` python
for a in map(TableInfo._make, table_cols(table)):
    print(a.name)
```

    name
    quantity
    price

We can now update our `table_cols` function.

### Adding a table with a row of data

``` python
# Create cursor
c = conn.cursor()

# Create table
c.execute(
    """CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)"""
)

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) changes
conn.commit()

# Close connection
conn.close()
```

To check that the database now contains our stocks table, list all its tables.

``` python
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("select name from sqlite_master where type = 'table'").fetchall()
```

    [('stocks',)]

### Retrieving data

``` python
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT * FROM stocks").fetchall()
```

    [('2006-01-05', 'BUY', 'RHAT', 100.0, 35.14)]

When adding Python variables to the query, never use string substitution directly like so:

``` python
symbol = "RHAT"
c.execute(f"select * from stocks where symbol = '{symbol}'").fetchall()
```

    [('2006-01-05', 'BUY', 'RHAT', 100.0, 35.14)]

While this works, it's vulnerable to [injection attacks](https://xkcd.com/327/). Use parameter substition instead. Either using question marks like so

``` python
symbol = ("RHAT",)
c.execute("select * from stocks where symbol = ?", symbol).fetchall()
```

    [('2006-01-05', 'BUY', 'RHAT', 100.0, 35.14)]

or using named placedholders like so

``` python
c.execute("select * from stocks where symbol = :symbol", {"symbol": "RHAT"}).fetchall()
```

    [('2006-01-05', 'BUY', 'RHAT', 100.0, 35.14)]

### Why do I need `fetchall()` after `cursor.execute()`?

Because the `curse.execute()` returns an iterater object containing all query results.

### Using namedtuples

``` python
EmployeeRecord = namedtuple("EmployeeRecord", "name, age, title, department, paygrade")

import csv

for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", "rb"))):
    print emp.name, emp.title

import sqlite3

conn = sqlite3.connect("/companydata")
cursor = conn.cursor()
cursor.execute("SELECT name, age, title, department, paygrade FROM employees")
for emp in map(EmployeeRecord._make, cursor.fetchall()):
    print emp.name, emp.title
```

## Using Pandas

Pandas is a very handy way to interact with databased in Python, as it makes dumping and retrieving dataframes very easy.

``` python
import pandas as pd

pd.read_sql_query("SELECT * FROM stocks", conn)
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

|     | date       | trans | symbol | qty   | price | newcol |
|-----|------------|-------|--------|-------|-------|--------|
| 0   | 2006-01-05 | BUY   | RHAT   | 100.0 | 35.14 | None   |

</div>

## SQLAlchemy

Summary of [this](https://www.youtube.com/watch?time_continue=1481&v=woKYyhLCcnU&feature=emb_logo) video.

## SQL best practices

-   Avoid \* in queries to have full control of returned columns (e.g. in case where table changes).

## Sources

-   [SQLite docs](https://www.sqlite.org/docs.html)
-   [sqite3 docs](https://docs.python.org/3/library/sqlite3.html)
-   [sqlite tutorial](https://www.sqlitetutorial.net)

## === Old notes to integrate ===

    # Selecting rows from a table

    SELECT col FROM table;
    SELECT col1, col2 FROM table;
    SELECT * FROM table LIMIT 10;
    SELECT DISTINCT col_values FROM table;


    # Counting

    SELECT COUNT(*) FROM table;             # Count rows of table
    SELECT COUNT(col) FROM table;           # Count non-missing values in col
    SELECT COUNT(DISTINCT col) FROM table;  # Count distinct values in col


    # Filtering

    SELECT * FROM table WHERE col1 > 2010:  # Get rows for which col1 > 2010
    SELECT COUNT(*) FROM table WHERE x < y  # Count number of rows for which x < y
    SELECT * FROM table WHERE x > Y AND y < z
    SELECT * FROM table WHERE x > Y OR y < z
    SELECT * FROM table WHERE x BETWEEN a AND b     # between a and b inclusive
    SELECT * FROM table WHERE x IN (a, b, c)

    SELECT title FROM films
    WHERE (release_year = 1994 OR release_year = 1995)
    AND (certification = 'PG' OR certification = 'R');


    # Filter based on results from aggregate function

    SELECT release_year
    FROM films
    GROUP BY release_year
    HAVING COUNT(title) > 10;


    # Missing values

    SELECT COUNT(*)
    FROM people
    WHERE birthdate IS NULL;

    SELECT name
    FROM people
    WHERE birthdate IS NOT NULL;


    # Wildcards

    SELECT name
    FROM companies
    WHERE name LIKE 'Data%';        # % matches zero, one, or many characters

    SELECT name
    FROM companies
    WHERE name LIKE 'DataC_mp';     # _ matches exactly one character

    SELECT name
    FROM people
    WHERE name NOT LIKE 'A%';


    # Aggregate functions

    SELECT AVG(budget)      # Also MAX, MIN, SUM,
    FROM films;


    # Aliasing

    SELECT MAX(budget) AS max_budget,
           MAX(duration) AS max_duration
    FROM films;


    # Arithmetic

    SELECT COUNT(deathdate) * 100.0 / COUNT(*) AS percentage_dead
    FROM people


    # Order by

    SELECT title
    FROM films
    ORDER BY release_year;

    SELECT title
    FROM films
    ORDER BY release_year DESC;


    # Group by

    SELECT sex, count(*)
    FROM employees
    GROUP BY sex;

    SELECT release_year, MAX(budget)
    FROM films
    GROUP BY release_year;


    # Building a database
    #######################


    # Create tables

    CREATE TABLE professors (
     firstname text,
     lastname text
    );


    # Alter tables

    ALTER TABLE table_name
    ADD COLUMN column_name data_type;

    ALTER TABLE table_name
    DROP COLUMN column_name;

    ALTER TABLE table_name
    RENAME COLUMN old_name TO new_name;

    DROP TABLE table_name


    # Insert values

    INSERT INTO transactions (transaction_date, amount, fee)
    VALUES ('2018-09-24', 5454, '30');

    SELECT transaction_date, amount + CAST(fee AS integer) AS net_amount
    FROM transactions;

    # Migrating data

    INSERT INTO target_table
    SELECT DISTINCT column_names
    FROM source_table;


    # Integrity constraints
    # 1. Attribute constraints (data types)
    # 2. Key constraints (primary keys)
    # 3. Referential integrity constraints (enforced through foreign keys)


    # Attribute constraints

    ALTER TABLE professors
    ALTER COLUMN firstname
    TYPE varchar(16)
    USING SUBSTRING(firstname FROM 1 FOR 16)

    ALTER TABLE professors
    ALTER COLUMN firstname
    SET NOT NULL;

    ALTER TABLE universities
    ADD CONSTRAINT university_shortname_unq UNIQUE(university_shortname);


    # Key constraints

    # Superkey: each combination of attributes that identifies rows uniquely
    # Candidate key: a superkey from which no column can be removed
    # Primary key: one candidate key chosen to act as primary key
    # Surrogate key: artificially created key (eg due to unsuitable candidate keys)
    # Foreign keys: points to the primary key of another table


    ALTER TABLE organizations
    RENAME COLUMN organization TO id;
    ALTER TABLE organizations
    ADD CONSTRAINT organization_pk PRIMARY KEY (id);

    ALTER TABLE affiliations
    DROP CONSTRAINT affiliations_organizations_id_fkey;

    ALTER TABLE professors
    ADD COLUMN ID serial

    UPDATE table_name
    SET new_var = CONCAT(v1, v2);

    -- Add a professor_id column that references id in professors table
    ALTER TABLE affiliations
    ADD COLUMN professor_id integer REFERENCES professors (id);
    -- Rename the organization column to organization_id
    ALTER TABLE affiliations
    RENAME organization TO organization_id;
    -- Add a foreign key on organization_id
    ALTER TABLE affiliations
    ADD CONSTRAINT affiliations_organization_fkey FOREIGN KEY (organization_id) REFERENCES organizations (id);

    -- Update professor_id to professors.id where firstname, lastname correspond to rows in professors
    UPDATE affiliations
    SET professor_id = professors.id
    FROM professors
    WHERE affiliations.firstname = professors.firstname AND affiliations.lastname = professors.lastname;


    # Referential integrity

    CREATE TABLE a (
        id integer PRIMARY KEY,
        col_a, varchar(64),
        ...,
        b_id integer REFERENCES b (id) VIOLATION SETTING)
    # Where violation setting is one of the following:
    # ON DELETE NO ACTION:  Deleting id in b that's referenced in a throws error
    # ON DELETE CASCADE:    Deleting id in b deletes references in all tables
    # RESTRICT:             Similar to no action
    # SET NULL              Set referencing column to null
    # SET DEFAULT           Set referencing column to default


    # Joins

    SELECT table_a.column1, table_a.column2, table_b.column1, table_b.column2, ...
    FROM table_a
    JOIN table_b
    ON table_a_foreign_key = table_b_primary_key
    WHERE condition;
