# Python string formatting


## Formatted string literals (f-strings)

A basic f-string consists of a combination of literal characters and replacement characters, the latter of which are placed inside braces (full grammar [here](https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals), useful explanation of how they are parsed [here](https://mail.python.org/pipermail/python-dev/2016-November/146797.html)).

The general form for the replacement field is `"{" expression ["="] ["!" conversion] [":" format_spec] "}"`.

``` python
name = "world"
f"Hello {name}"
```

    'Hello world'

Add `=` to also print the name of the replacement expression (useful for debugging).

``` python
name = "world"
f"Hello {name=}"
```

    "Hello name='world'"

Add a `!` for conversion: `!s` calls `str()`, `!r` calls `repr()`, and `!a` calls `ascii()`.

``` python
name = "world"
f"Hello {name!r}"
```

    "Hello 'world'"

Add `:` to add a format specifier, using the format mini language.

``` python
import datetime

today = datetime.datetime.today()

f"It's {today:%H.%M} on {today:%d %B, %Y.}"
```

    "It's 06.45 on 01 December, 2021."

Expressions can be nested (it's a contrived example, we could just used `%p` to get *AM* and *PM*)

``` python
f"It's {today:%H.%M{'am' if today.hour < 12 else 'pm'}} on {today:%d %B, %Y.}"
```

    "It's 06.45am on 01 December, 2021."

``` python
value = 5.123
width = 5
precision = 2
f"{value:{width}.{precision}}"
```

    '  5.1'

Backslashes are not allowed in expressions. If I need backslash escapes, use a variable.

``` python
newline = ord("\n")
f"newline: {newline}"
```

    'newline: 10'

## Format specifier form

The general form of the format specifier is ([docs](https://docs.python.org/3/library/string.html#format-specification-mini-language)):

`[[fill]align][sign][#][0][width][grouping_option][.precision][type]`

where:

-   `fill`: any character
-   `align`: `<`, `>`, `^` (right, left, centered alignment), `=` (sign-aware zero padding, see below)
-   `sign`: `+` (show positive and negative sign), `-` (show negative sign only, default), `space` (show space for positive numbers and minus sign for negative ones)
-   `#`: user "alternate form" for conversion. Effect depends on type. Prevents removal of trailing zeroes in `g` and `G` conversion (see below)
-   `grouping_option`: `,`, `_`, `n` (comma, underscore, locale aware thousands separator)
-   `0`: Turns on sign-aware zero padding (equivalent to `0` fill character with `=` alignment, see below)
-   `.precision`: number of digits after decimal points for `f` or `F` formatted floats, before and after decimal point for `g` or `G` formatted floats, and number of characters used for non-numeric types.
-   `type`: see below.

## Types

The `type` determines how the data should be presented.

### String types

The only available type is `s` for string format, which is the default and can be omitted.

``` python
s = "Hello World."
f"{s}", f"{s:s}"
```

    ('Hello World.', 'Hello World.')

### Integer types

The default is `d` for *decimal integer*, which represents the integer in base 10. This is pretty much all I ever need. But the below also shows examples of how to prepresent an integer in bases two (`b` for *binary*), eight (`o` for *octal*), and sixteen (`x` for *hexadecimal*). There are also a few more options available.

``` python
n = 10
f"{n:d}", f"{n:b}", f"{n:o}", f"{n:x}"
```

    ('10', '1010', '12', 'a')

### Float (and integer) types

(Much of this also applies to [decimals](https://docs.python.org/3/library/decimal.html#module-decimal), which provide a solution to minor rounding issues that happen with floats. But I've never needed them and ignore them for now.)

`e` produces scientific notation with one digit before and `precision` digits after the decimal point for a total of `1 + precision` significant digits. `precision` defaults to 6. `E` is the same but uses an upper case *E* as a separator.

``` python
n = 01234.56789
precision = 0.3

f"{n:e}", f"{n:{precision}e}", f"{n:{precision}E}"
```

    ('1.234568e+03', '1.235e+03', '1.235E+03')

`f` produces fixed-point notation with `precision` number of digits after the decimal point. `precision` defaults to 6. `F` is the same but converts `nan` to `NAN` and `inf` to `INF`.

``` python
f"{n:f}", f"{n:{precision}f}"
```

    ('1234.567890', '1234.568')

`g` produces general format with `precision` number of significant digits and the number formatted either using fixed-point or scientific notation depending on its magnitude. `precision` defaults to 6. `G` has the same behaviour as `F` and converts large numbers to scientific notation. (In the last example, remember that the high precision doesn't add zero padding because it determines the number of [significant digits](https://en.wikipedia.org/wiki/Significant_figures).)

``` python
f"{n:g}", f"{n:.1g}", f"{n:.3g}", f"{n:.12g}"
```

    ('1234.57', '1e+03', '1.23e+03', '1234.56789')

The below might be unexpected (it was for me, anyways). It is a result of the fact that decimals can't be represented exactly in binary [floating point](https://en.wikipedia.org/wiki/Floating-point_arithmetic#Decimal-to-binary_conversion). The right-hand side expression represents another example of the same limitation. If such high precision is needed, the [`decimal`](https://docs.python.org/3/library/decimal.html) module should help.

``` python
f"{n:.25g}", 1.1 + 2.2
```

    ('1234.567890000000033978722', 3.3000000000000003)

`%` produces a percentage by multiplying the number by 100, adding a percent sign, and formatting the number using fixed-point format (e.g. the default is 6 "precision digits" after the decimal point).

``` python
f"{n:%}", f"{n:.2%}"
```

    ('123456.789000%', '123456.79%')

### Strings

`.precision` determines the number of characters used.

``` python
text = "Hello World!"
f"{text:.^30.5}"
```

    '............Hello.............'

### Digits

By convention, an empty format field produces the same result as calling `str()` on the value.

``` python
n = 01234.56789

f"{n:}", str(n)
```

    ('1234.56789', '1234.56789')

By default, the `width` equals the length of the data, so `fill` and `align` have no effect.

``` python
f"{n:@<}"
```

    '1234.56789'

We can use `=` alignment to add padding between the `sign` and the digit, and use a `0` before `width` as a shortcut to get sign-aware zero padding (i.e. the equivalent of a `0` fill with `=` alignment).

``` python
f"{n:=+15}", f"{n:0=+15}", f"{n:+015}"
```

    ('+    1234.56789', '+00001234.56789', '+00001234.56789')

Use `#` to keep trailing zeroes in `g` and `G` conversions.

``` python
f"{123.400:g}", f"{123.400:#g}"
```

    ('123.4', '123.400')

Thousands separators.

``` python
n = 1_000_000
f"{n:,}", f"{n:_}", f"{n:n}"
```

    ('1,000,000', '1_000_000', '1000000')

## Character sets

The `string` module (docs [here](https://docs.python.org/3/library/string.html#helper-functions)) provides a set of useful character sets as module constants.

``` python
import string
```

``` python
string.ascii_lowercase
```

    'abcdefghijklmnopqrstuvwxyz'

``` python
string.ascii_letters
```

    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

``` python
string.digits
```

    '0123456789'

``` python
string.punctuation
```

    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

## Dates

Quick reference for `strftime()` and `strptime()` codes I use often and keep forgetting. Full list [here](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes). (As a reminder: `strftime()` is an instance method that converts `datetime` objects to a string in a given **f**ormat, while `strptime()` is a class method that **p**arses a string and converts it to `datetime`.)

``` python
import datetime

today = datetime.datetime.today()
print(today)
```

    2021-12-01 06:36:20.652838

``` python
fmt = "%d %b %Y"
today.strftime(fmt), datetime.datetime.strptime("1 Dec 2021", fmt)
```

    ('01 Dec 2021', datetime.datetime(2021, 12, 1, 0, 0))

``` python
today.strftime("%y %Y")
```

    '21 2021'

``` python
today.strftime("%a %A")
```

    'Wed Wednesday'

``` python
today.strftime("%b %B")
```

    'Dec December'

``` python
print(today.strftime("%H:%M:%S"))  # 24-hour clock
print(today.strftime("%I:%M%p"))  # 12-hour clock
```

    06:36:20
    06:36AM

``` python
today.strftime("%c || %x || %X")  # Locale's appropriate formatting and literals
```

    'Wed Dec  1 06:36:20 2021 || 12/01/21 || 06:36:20'

## Applications

### `string` doc examples

Accessing argument's items

``` python
point = (2, 5)
"x = {0[0]}, y = {0[1]}".format(point)
```

    'x = 2, y = 5'

Using format mini-language

``` python
n = 10000
"{:.>20,.2f}".format(n)
```

    '...........10,000.00'

Formatting dates

``` python
import datetime

today = datetime.datetime.today()

print("Day: {date:%d}\nMonth: {date:%b}\nYear: {date:%Y}".format(date=today))
```

    Day: 07
    Month: Dec
    Year: 2021

### Create table from list of tuples

Based on example from page 29 in [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/). Code is available [here](https://github.com/fluentpython/example-code/blob/master/02-array-seq/metro_lat_long.py).

``` python
metro_areas = [
    ("Tokyo", "JP", 36.933, (35.689722, 139.691667)),
    ("Delhi NCR", "IN", 21.935, (28.613889, 77.208889)),
    ("Mexico City", "MX", 20.142, (19.433333, -99.133333)),
    ("New York-Newark", "US", 20.104, (40.808611, -74.020386)),
    ("Sao Paulo", "BR", 19.649, (-23.547778, -46.635833)),
]

hline, hhline = "-" * 39, "=" * 39
print(hhline)
print("{:15} | {:^9} | {:^9}".format(" ", "lat.", "long."))
print(hline)
fmt = "{:15} | {:>9.4f} | {:>9.4f}"
for name, cc, pop, (lat, long) in metro_areas:
    if long <= 0:
        print(fmt.format(name, lat, long))
print(hhline)
```

    =======================================
                    |   lat.    |   long.  
    ---------------------------------------
    Mexico City     |   19.4333 |  -99.1333
    New York-Newark |   40.8086 |  -74.0204
    Sao Paulo       |  -23.5478 |  -46.6358
    =======================================

## Main sources

-   [`string` docs](https://docs.python.org/3.4/library/string.html)
-   [Formatted string literals docs](https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals)
-   [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
-   [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)

