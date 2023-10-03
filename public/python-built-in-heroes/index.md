# Python built-in heroes


<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


## Operator

([docs](https://docs.python.org/3/library/operator.html))

### `itemgetter()`

Basic use:

``` python
from operator import itemgetter

print(itemgetter(1, 3, 5)("Watermelon"))
print(itemgetter(slice(5, None))("Watermelon"))
print(itemgetter("name")(dict(name="Paul", age=44)))
```

    ('a', 'e', 'm')
    melon
    Paul

Application (from docs):

``` python
inventory = [("apple", 3), ("banana", 2), ("pear", 5), ("orange", 1)]

getcount = itemgetter(1)

# get second item from list
print(getcount(inventory))

# get second item from each element in list
list(map(getcount, inventory))
```

    ('banana', 2)

    [3, 2, 5, 1]

Application: sorting list of dictionaries (from Python Cookbook recipe 1.13)

``` python
data = [
    {"fname": "Brian", "lname": "Jones", "uid": 1003},
    {"fname": "David", "lname": "Beazley", "uid": 1002},
    {"fname": "John", "lname": "Cleese", "uid": 1001},
    {"fname": "Big", "lname": "Jones", "uid": 1004},
]

# get second row from data
print(itemgetter(2)(data))

# get ids from all rows
print(list(map(itemgetter("uid"), data)))

# sort data by fname and lname
sorted(data, key=itemgetter("fname", "lname"))
```

    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}
    [1003, 1002, 1001, 1004]

    [{'fname': 'Big', 'lname': 'Jones', 'uid': 1004},
     {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
     {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
     {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}]

`lambda` alternative to the above:

``` python
sorted(data, key=lambda r: (r["fname"], r["lname"]))
```

    [{'fname': 'Big', 'lname': 'Jones', 'uid': 1004},
     {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
     {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
     {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}]

Beazley notes that itemgetter is often a bit faster. I also find `itemgetter` easier to read. But I usually use `lambda` as it's built it.

### `attrgetter()`

Basic use:

``` python
from operator import attrgetter

def greeter():
    print("Hello")


func_name = attrgetter("__name__")
func_name(greeter)
```

    'greeter'

Application: sort objects without native support (from Python Cookbook recipe 1.14)

``` python
class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def __repr__(self):
        return f'User({self.name!r}, {self.id!r})'
    

users = [User('Trev', 1), User('Rodika', 33), User('Gab', 2), User('Claire', 9)]
sorted(users, key=attrgetter('name', 'id'))

```

    [User('Claire', 9), User('Gab', 2), User('Rodika', 33), User('Trev', 1)]

## Itertools

``` python
import itertools
```

### Infinite iterators

-   `count()` creates evenly spaced value
-   `cycle()` repeates elements of an iterable
-   `repeat()` repeats an object

Application: create custom tuple patterns

``` python
count = itertools.count(1, 2)
cycle = itertools.cycle("abc")
repeat = itertools.repeat("ho")
a = [1, 2, 3, 4, 5]

list(zip(a, count, cycle, repeat))
```

    [(1, 1, 'a', 'ho'),
     (2, 3, 'b', 'ho'),
     (3, 5, 'c', 'ho'),
     (4, 7, 'a', 'ho'),
     (5, 9, 'b', 'ho')]

Application: create sequence of functions with custom arguments

``` python
count = itertools.count(1, 2)
repeat = itertools.repeat("ho")


def repeater(word, count):
    print(word * count)


for _ in range(3):
    next(map(repeater, count, repeat))
```

    ho
    hohoho
    hohohohoho

### `islice()`

-   Automatically stops if sequence is exhausted instead of throwing an error.

``` python
import itertools

s = [1, 2, 3, 4, 5]

for x in itertools.islice(s, 10):
    print(x)
```

    1
    2
    3
    4
    5

### `groupby()`

**Sorting addresses** (Python Cookbook recipe 1.15)

``` python
rows = [
    {"address": "5412 N CLARK", "date": "07/01/2012"},
    {"address": "5148 N CLARK", "date": "07/04/2012"},
    {"address": "5800 E 58TH", "date": "07/02/2012"},
    {"address": "2122 N CLARK", "date": "07/03/2012"},
    {"address": "5645 N RAVENSWOOD", "date": "07/02/2012"},
    {"address": "1060 W ADDISON", "date": "07/02/2012"},
    {"address": "4801 N BROADWAY", "date": "07/01/2012"},
    {"address": "1039 W GRANVILLE", "date": "07/04/2012"},
]
```

Iterate over the entries grouped by *date* (use `groupby`)

``` python
from itertools import groupby
from operator import itemgetter

rows.sort(key=itemgetter("date"))
for date, items in groupby(rows, lambda x: x["date"]):
    print(date)
    for i in items:
        print(i)
```

    07/01/2012
    {'address': '5412 N CLARK', 'date': '07/01/2012'}
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'}
    07/02/2012
    {'address': '5800 E 58TH', 'date': '07/02/2012'}
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}
    {'address': '1060 W ADDISON', 'date': '07/02/2012'}
    07/03/2012
    {'address': '2122 N CLARK', 'date': '07/03/2012'}
    07/04/2012
    {'address': '5148 N CLARK', 'date': '07/04/2012'}
    {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}

Repeat the above but without using `groupby`.

``` python
import collections

sorted_rows = collections.defaultdict(list)
for row in rows:
    sorted_rows[row["date"]].append(row)

for date, items in sorted_rows.items():
    print(date)
    for item in items:
        print(item)
```

    07/01/2012
    {'address': '5412 N CLARK', 'date': '07/01/2012'}
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'}
    07/02/2012
    {'address': '5800 E 58TH', 'date': '07/02/2012'}
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}
    {'address': '1060 W ADDISON', 'date': '07/02/2012'}
    07/03/2012
    {'address': '2122 N CLARK', 'date': '07/03/2012'}
    07/04/2012
    {'address': '5148 N CLARK', 'date': '07/04/2012'}
    {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}

**Creating look-and-say sequence** (EPI 6.7)

Return the nth entry of the look-and-say sequence

``` python
def look_and_say(n):
    s = "1"
    for _ in range(1, n):
        s = "".join(key + str(len(list(group))) for key, group in groupby(s))
    return s


look_and_say(3)
```

    '12'

### `compress()`

``` python
from itertools import compress

addresses = [
    "5412 N CLARK",
    "5148 N CLARK",
    "5800 E 58TH",
    "2122 N CLARK" "5645 N RAVENSWOOD",
    "1060 W ADDISON",
    "4801 N BROADWAY",
    "1039 W GRANVILLE",
]

counts = [0, 3, 10, 4, 1, 7, 6, 1]

# keep all popular addresses (with > 5 counts)
popular = [x > 5 for x in counts]
list(compress(addresses, popular))
```

    ['5800 E 58TH', '4801 N BROADWAY', '1039 W GRANVILLE']

### `starmap()`

Using `starmap()` to calculate a running average:

``` python
from itertools import accumulate, starmap

numbers = range(0, 21, 5)
list(starmap(lambda a, b: b / a, enumerate(accumulate(numbers), start=1)))
```

    [0.0, 2.5, 5.0, 7.5, 10.0]

How this works:

``` python
list(numbers)
```

    [0, 5, 10, 15, 20]

``` python
list(accumulate(numbers))
```

    [0, 5, 15, 30, 50]

``` python
list(enumerate(accumulate(numbers), start=1))
```

    [(1, 0), (2, 5), (3, 15), (4, 30), (5, 50)]

``` python
import operator

name = "Emily"
list(starmap(operator.mul, enumerate(name, 1)))
```

    ['E', 'mm', 'iii', 'llll', 'yyyyy']

### `dropwhile()`

From [docs](https://docs.python.org/3/library/itertools.html#itertools.dropwhile)

``` python
def dropwhile(predicate, iterable):
    iterable = iter(iterable)
    for x in iterable:
        if not predicate(x):
            yield x
            break
    for x in iterable:
        yield x


predicate = lambda x: x < 5
iterable = [1, 2, 3, 6, 7, 3]
list(dropwhile(predicate, iterable))
```

    [6, 7, 3]

What happens here?

1.  `iter()` is used so that the iterable becomes an iterator (which gets emptied as it's being iterated over).

2.  The first for loop moves until the first element fails the condition in `predicate`, at which point that element is yielded and the program breakes out of that for loop, advancing to the next.

3.  Because of step 1, `iterable` now only contains all elements after the element that caused the previous for loop to break, and all of these are yielded.

``` python
def sensemaker(predicate, iterable):
    iterable = iter(iterable)
    for x in iterable:
        if not predicate(x):
            print("First loop")
            print(x)
            break
    print("Second loop")
    for x in iterable:
        print(x)


sensemaker(predicate, iterable)
```

    First loop
    6
    Second loop
    7
    3

``` python
def sensemaker(predicate, iterable):
    #     iterable = iter(iterable)
    for x in iterable:
        if not predicate(x):
            print("First loop")
            print(x)
            break
    print("Second loop")
    for x in iterable:
        print(x)


sensemaker(predicate, iterable)
```

    First loop
    6
    Second loop
    1
    2
    3
    6
    7
    3

If we don't turn the iterable into an iterator, it doesn't get exhausted and the second loop simply loops over all its objects.

### More itertools

From [more itertools](https://more-itertools.readthedocs.io/en/stable/index.html)

``` python
import more_itertools

more_itertools.take(4, more_itertools.pairwise(itertools.count()))
```

    [(0, 1), (1, 2), (2, 3), (3, 4)]

## Functools

### `partial`

``` python
print(operator.mul(2, 3))
tripple = partial(mul, 3)
tripple(2)
```

    6

    6

### `reduce()`

``` python
from functools import reduce
```

Basic use:

``` python
reduce(operator.mul, [1, 2, 3, 4])
```

    24

Application:

``` python
import pandas as pd

df = pd.DataFrame(
    {"AAA": [4, 5, 6, 7], "BBB": [10, 20, 30, 40], "CCC": [100, 50, -30, -50]}
)
```

What I usually do

``` python
crit1 = df.AAA > 5
crit2 = df.BBB > 30
crits = crit1 & crit2

df[crits]
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
| 3   | 7   | 40  | -50 |

</div>

Alternative using `functools.reduce()`

``` python
import functools

crit1 = df.AAA > 5
crit2 = df.BBB > 30
crits = [crit1, crit2]

mask = functools.reduce(lambda x, y: x & y, crits)
df[mask]
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
| 3   | 7   | 40  | -50 |

</div>

## Misc.

### Iterable unpacking

When looping over a list of records (maybe of unequal length), we can access each records elements directly using star expressions. (From Python Cookbook recipe 1.2.)

``` python
records = [("foo", 1, 2), ("bar", "hello")]
```

``` python
# conventional loop

for record in records:
    print(record)
```

    ('foo', 1, 2)
    ('bar', 'hello')

``` python
# accessign items

for a, *b in records:
    print(a)
    print(b)
```

    foo
    [1, 2]
    bar
    ['hello']

``` python
# example use

def do_foo(x, y):
    print(f"foo: args are {x} and {y}.")


def do_bar(x):
    print(f"bar: arg is {x}.")


for tag, *args in records:
    if tag == "foo":
        do_foo(*args)
    elif tag == "bar":
        do_bar(*args)
```

    foo: args are 1 and 2.
    bar: arg is hello.

### `iter()`

Basic use

``` python
a = iter([1, 2, 3])
next(a), next(a), next(a)
```

    (1, 2, 3)

Creating a `callable_iterator`: roll a die until a 6 is rolled

``` python
import random


def roll():
    return random.randint(1, 6)


roll_iter = iter(roll, 6)
roll_iter
```

    <callable_iterator at 0x112c75850>

``` python
for r in roll_iter:
    print(r)
```

    1
    2
    4
    2

``` python
list(iter(roll, 4))
```

    [3, 1, 2, 5, 3, 5, 3]

To read file until an empty line:

``` python
with open("filepath") as f:
    for line in iter(f.readline, ""):
        process_line(line)
```

### `filter()`

``` python
a = [0, 1, 0, 2, 3]
non_zero = list(filter(lambda x: x != 0, a))
non_zero
```

    [1, 2, 3]

``` python
a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
[a[i] for i in range(3)]
```

    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

``` python
def unique(array):
    return len(array) == len(set(array))


cols = [[a[row][col] for row in range(3)] for col in range(3)]
all(unique(a) for a in cols)
```

    True

### String

``` python
import string
```

``` python
string.ascii_letters
```

    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

``` python
string.punctuation
```

    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

## Sources

-   David Beazley [talk](https://www.youtube.com/watch?v=lyDLAutA88s) (the inspiration for the title)
-   [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
-   [Pandas cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#cookbook)
-   Elements of programming interviews in Python (EPI)

