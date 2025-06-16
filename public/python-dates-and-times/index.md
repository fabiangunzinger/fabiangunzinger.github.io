# Dates and times in Python



## Overview of Python libraries

There are a number of different libraries to work with dates and times:

-   [`time`](https://docs.python.org/3/library/time.html#module-time) provides time-related functions.
-   [`datetime`](https://docs.python.org/3/library/datetime.html#) provides classes to work with dates and times
-   [`dateutil`](https://dateutil.readthedocs.io/en/stable/#) is a third-party library that provides powerful extension to `datetime`.
-   [`pandas`](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#) provides extensive functionality to work with timeseries and dates.

``` python
import numpy as np
import pandas as pd
```

## The basics of working with dates and times in `datetime`

-   I don't usually work with (timezone-) *aware* dates, so these notes focus on the *naive* `date`, `time`, `datetime`, and `timedelta` objects.

### `date` objects

``` python
from datetime import date

d = date.today()
d
```

    datetime.date(2023, 2, 12)

Useful class attributes and instance methods

``` python
d.year, d.month, d.day, d.isoweekday()
```

    (2023, 1, 22, 7)

``` python
d.replace(year=d.year + 1).strftime("%A %d %B %Y")
```

    'Monday 22 January 2024'

### `time` objects

``` python
from datetime import time

t = time.fromisoformat("11:23:33")
t.hour, t.minute, t.second, t.replace(minute=55).minute
```

    (11, 23, 33, 55)

### `datetime` objects

``` python
import time
from datetime import datetime

dt = datetime.fromtimestamp(time.time())
dt.day, dt.year, dt.replace(day=1).strftime("%d %B %Y")
```

    (22, 2023, '01 January 2023')

### `timedelta` objects

``` python
today = date.today()
xmas = date.fromisoformat("2023-12-25")
td = xmas - today
print(f"Only {td.days} days to Xmas!")
```

    Only 337 days to Xmas!

``` python
from datetime import timedelta

year = timedelta(days=365)
year_from_today = today + year
year_from_today.strftime("%d %b %Y")
```

    '22 Jan 2024'

### `strftime()` and `strptime()` behaviour

-   A quick reference for `strftime()` and `strptime()` codes that I use frequently and keep forgetting.

-   The full list is [here](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

-   As a reminder: `strftime()` is an instance method that converts `datetime` objects into a string of a given **f**ormat, while `strptime()` is a class method that **p**arses a string and converts it to `datetime`.

``` python
from datetime import datetime

now = datetime.strptime("11 Dec 2022 09:55", "%d %b %Y %H:%M")
now
```

    datetime.datetime(2022, 12, 11, 9, 55)

``` python
fmt = "%d %b %Y"
now.strftime(fmt)
```

    '11 Dec 2022'

``` python
now.strftime("%d %b %y"), now.strftime("%d %b %Y")
```

    ('11 Dec 22', '11 Dec 2022')

``` python
now.strftime("%d %b %Y"), now.strftime("%d %B %Y")
```

    ('11 Dec 2022', '11 December 2022')

``` python
now.strftime("%a"), now.strftime("%A")
```

    ('Sun', 'Sunday')

``` python
now.strftime("%H:%M:%S"), now.strftime("%I:%M%p")
```

    ('09:55:00', '09:55AM')

## Powerful parsing with `dateutil`

While `datetime` can only dates in [ISO format](https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat), `dateutil` is more flexibe, which is often useful.

``` python
from dateutil.parser import parse

d = parse("22 Dec 2022")
d.year, d.month, d.day
```

    (2022, 12, 22)

## Recipees for frequently used tasks

Stuff to remember:
- I mostly work in Pandas, so most of these recipees are Pandas-specific

-   `pd.Timestamp` is Pandas's equivalent of Python's `datetime.datetime`

### Parsing a human-readable date string

Using `datetime`

``` python
from datetime import datetime

date = "22 Jan 2022"

datetime.strptime(date, "%d %b %Y")
```

    datetime.datetime(2022, 1, 22, 0, 0)

Using `dateutil`

``` python
from dateutil.parser import parse

parse(date)
```

    datetime.datetime(2022, 1, 22, 0, 0)

Using `pandas`

``` python
pd.Timestamp(date)
```

    Timestamp('2022-01-22 00:00:00')

### Creating date and period ranges

Create quarterly date rand and change format to first day of quarter in day-month-year

``` python
pd.period_range("Jan 2023", "July 2024", freq="Q").asfreq("d", how="start")
```

    PeriodIndex(['2023-01-01', '2023-04-01', '2023-07-01', '2023-10-01',
                 '2024-01-01', '2024-04-01', '2024-07-01'],
                dtype='period[D]')

### Date offsets

Period differences create [Date offsets](https://pandas.pydata.org/docs/reference/offset_frequency.html).

``` python
dates = pd.period_range(start="2023", periods=10)
d = dates.max() - dates.min()
print(d)
print(type(d))
d.n
```

    <9 * Days>
    <class 'pandas._libs.tslibs.offsets.Day'>

    9

