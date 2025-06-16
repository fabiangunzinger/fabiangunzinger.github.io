# Regex in Python



<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js" integrity="sha512-c3Nl8+7g4LMSTdrm621y7kf9v3SDPnhxLNhcjFJbKECVnmZHTdo+IRO05sNLTH/D3vA6u1X32ehoLC7WFVdheg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous" data-relocate-top="true"></script>
<script type="application/javascript">define('jquery', [],function() {return window.jQuery;})</script>


## Raw strings

> Raw string notation keeps regular expressions sane. [`re` tutorial](https://docs.python.org/3/library/re.html#raw-string-notation)

### Raw strings in Python

Just like the regex engine, Python uses `\` to [escape](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals) characters in strings that otherwise have special meaning (e.g. `'` and `\` itself) and to create tokens with special meaning (e.g. `\n`).

``` python
print("Hello\nWorld")
```

    Hello
    World

Without escaping a single quotation mark, it takes on its special meaning as a delimiter of a string.

``` python
'It's raining'
```

<pre><span class="ansi-cyan-fg">  File </span><span class="ansi-green-fg">"/var/folders/xg/n9p73cf50s52twlnz7z778vr0000gn/T/ipykernel_1847/3769801028.py"</span><span class="ansi-cyan-fg">, line </span><span class="ansi-green-fg">1</span>
<span class="ansi-red-fg">    'It's raining'</span>
        ^
<span class="ansi-red-fg">SyntaxError</span><span class="ansi-red-fg">:</span> invalid syntax
</pre>

To give it its literal meaning as an apostrophe, we need to escape it.

``` python
'It's raining"
```

    "It's raining"

### Python and regex interaction

A string is processed by the Python interpreter before being passed on to the regex engine. Once consequence of this is that if in our regex pattern we want to treat as a literal a character that has special meaning in both Python and regex, we have to escape it twice.

For example: to search for a literal backslash in our regex pattern, we need to write `\\\\`. The Python interpreter reads this as `\\` and passes it to the regex engine, which then reads it as `\` as desired.

``` python
import re
```

``` python
s = "a \ b"
m = re.search("a \\\\ b", s)
print(m[0])
m[0]
```

    a \ b

    'a \\ b'

This is obviously cumbersome. A useful alternative is to use raw strings `r''`, which make the Python interpreter read special characters as literals, obviating the first set of escapes. Hence, it's a good idea to use raw strings in Python regex expressions.

``` python
m = re.search(r"a \\ b", s)
print(m.group())
```

    a \ b

### Escape sequences rabbit hole

First things first: an escape sequence is a a sequence of characters that does not represent itself when used within a string literal but is translated into another character or sequence of characters that might be difficult or impossible to represent (from [Wikipedia](https://en.wikipedia.org/wiki/Escape_sequences_in_C)).

When I tried a version of this

``` python
string = "foo 1a bar 2baz"
pattern = "\b\d[a-z]\b"

re.findall(pattern, string)
```

    []

it took me 10 minutes to figure out why `1a` didn't match. The short answer is: **thou shalt use raw strings!**

``` python
raw_pattern = r"\b\d[a-z]\b"

re.findall(raw_pattern, string)
```

    ['1a']

But why? Because Python [interpretes](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals) escape sequences in strings according to the rules of Standard C, where `\b` happens to stand for the backspace. Hence, the pattern without the *r* prefix means "a backspace immediately followed by a digit immediately followed by a lowercase letter immediately followed by another backspace", which is not present in the string.

To convince ourselves of this, we can add backspaces to the string and try again -- now the pattern matches.

``` python
string = "foo \N{backspace}1a\N{backspace} baz 2bar"

re.findall(pattern, string)
```

    ['\x081a\x08']

One point that was not immediately obvious to me was why `pattern` works without the backspace character -- why do the backspaces in `\d` and `\w` not need escaping?

``` python
pattern = "\d\w"
re.findall(pattern, string)
```

    ['1a', '2b']

The explanation is that `\` is interpreted literally if it is not part of an escape sequence, as in

``` python
print("a\k")
```

    a\k

and `\d` and `\w` aren't escape sequences in Python (or C). Hence, these two tokens are passed on unaltered to the regex engine, where they are interpreted according to regex syntax rules.

### Remove punctuation rabbit hole

I wanted to remove punctuation in a string like the below.

``` python
s = "Some .' test & with * punctuation \ characters."
```

Thinking I was clever, I thought of the useful [constants](https://docs.python.org/3/library/string.html#string-constants) provided by the `string` module, which provide easy access to character sequences like the set of punctuation characters.

``` python
import string

string.punctuation
```

    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

I did the below and was about to celebrate victory.

``` python
p = string.punctuation
try:
    re.sub(p, " ", s)
except Exception as e:
    print(e)
```

    multiple repeat at position 10

Oops! It's a clear case where I jupmpted to a conclusion a little bit too soon, and where spending a few more minutes thinking things through before starting to code would probably have helped me see the two flaws in my approach: I need to escape special characters, and, given that I want to search for characters individually, I need to wrap them in a character rather than passing them as a single string🤦‍♂️

``` python
p = f"[{re.escape(string.punctuation)}]"
r = re.sub(p, "", s)
r
```

    'Some  test  with  punctuation  characters'

To remove extra whitespace, I could use:

``` python
re.sub(" +", " ", r)
```

    'Some test with punctuation characters'

Alternatively, I could use a regex-native approach.

``` python
p = r"[\W_]"
re.sub(p, " ", s)
```

    'Some    test   with   punctuation   characters '

## re module

``` python
import re
```

Overview of search methods

``` python
pattern = "a"
string = "Jack is a boy"

methods = [
    ("re.match (start of string)", re.match(pattern, string)),
    ("re.search (anywhere in string)", re.search(pattern, string)),
    ("re.findall (all matches)", re.findall(pattern, string)),
    ("re.finditer (all matches as iterator)", re.finditer(pattern, string)),
]

for desc, result in methods:
    print("{:40} -> {}".format(desc, result))
```

    re.match (start of string)               -> None
    re.search (anywhere in string)           -> <re.Match object; span=(1, 2), match='a'>
    re.findall (all matches)                 -> ['a', 'a']
    re.finditer (all matches as iterator)    -> <callable_iterator object at 0x11236d2e0>

### re.findall()

Returns list of all matches if no capturing groups specified, and a list of capturing groups otherwise.

Example: find stand-alone numbers

``` python
data = """
 012
foo34 
     56
78bar
9
 a10b
"""
```

Without capturing groups entire match is returned

``` python
proper_digits = "\s+\d+\s+"
re.findall(proper_digits, data, flags=re.MULTILINE)
```

    ['\n 012\n', ' \n     56\n', '\n9\n ']

One capturing groups returns list of capturing groups

``` python
proper_digits = "(?m)\s+(\d+)\s+"
re.findall(proper_digits, data, flags=re.MULTILINE)
```

    ['012', '56', '9']

Multiple capturing groups return list of multi-tuple capturing groups

``` python
proper_digits = "\s+(\d)(\d+)?\s+"
re.findall(proper_digits, data, flags=re.MULTILINE)
```

    [('0', '12'), ('5', '6'), ('9', '')]

To return the full match if the pattern uses capturing groups, simply capture the entire match, too.

``` python
s = "Hot is hot. Cold is cold."
p = r"((?i)(\w+) is \2)"
[groups[0] for groups in regex.findall(p, s)]
```

    ['Hot is hot', 'Cold is cold']

Finding overlapping matches

``` python
pattern = r"(?=(\w+))"
re.findall(pattern, "abc")
```

    ['abc', 'bc', 'c']

### re.match()

Find pattern at the beginning of a string

``` python
line = '"688293"|"777"|"2011-07-20"|"1969"|"20K to 30K"'

pattern = r'"\d+"\|"(?P<user_id>\d+)"'

match = re.match(pattern, line)
print(match)
print(match.group("user_id"))
print(match["user_id"])  # alternative, simpler, syntax
```

    <re.Match object; span=(0, 14), match='"688293"|"777"'>
    777
    777

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


def large_house_number(address, threshold=2000):
    house_number = int(re.match("\d+", address)[0])
    return house_number > threshold


has_large_number = [large_house_number(x) for x in addresses]
list(compress(addresses, has_large_number))
```

    ['5412 N CLARK',
     '5148 N CLARK',
     '5800 E 58TH',
     '2122 N CLARK5645 N RAVENSWOOD',
     '4801 N BROADWAY']

### re.escape()

I want to match "(other)". To match the parentheses literally, I'd have to escape them. If I don't, the regex engine interpres them as a capturing group.

``` python
m = re.search("(other)", "some (other) word")
print(m)
m[0]
```

    <re.Match object; span=(6, 11), match='other'>

    'other'

I can escape manually.

``` python
re.search("\(other\)", "some (other) word")
```

    <re.Match object; span=(5, 12), match='(other)'>

But if I have many fields with metacharacters (e.g. variable values that contain parentheses) this is a massive pain. The solution is to just use `re.escape()`, which does all the work for me.

``` python
re.search(re.escape("(other)"), "some (other) word")
```

    <re.Match object; span=(5, 12), match='(other)'>

### re.split()

``` python
pattern = r"(?<=\w)(?=[A-Z])"
s = "ItIsAWonderfulWorld"
re.split(pattern, s)
```

    ['It', 'Is', 'A', 'Wonderful', 'World']

### re.sub()

Stip a string of whitespace and punctuation.

``` python
s = "String. With! Punctu@tion# and _whitespace"
re.sub(r"[\W_]", "", s)
```

    'StringWithPunctutionandwhitespace'

Using zero-width match to turn CamelCase into snake_case

``` python
s = "ThisIsABeautifulDay"
pattern = r"(?<=[a-zA-Z])(?=[A-Z])"
re.sub(pattern, "_", s).lower()
```

    'this_is_a_beautiful_day'

Use same approach with MULTILINE mode to comment out all lines.

``` python
s = """first
second
third"""

pattern = "(?m)^"
print(re.sub(pattern, "#", s))
```

    #first
    #second
    #third

### Matching end of line and end of string

`\Z` matches strict end of string but not cases where last character is a line-break

``` python
a = """no newline 
at end"""

b = """newline
at end
"""

print(re.search(r"d\Z", a))
print(re.search(r"d\Z", b))
```

    <re.Match object; span=(17, 18), match='d'>
    None

`\$` matches end of string flexibly (i.e. before or after final linebreak)

``` python
a = """no newline 
at end"""

b = """newline
at end
"""

print(re.findall(r"[ed]$", a))
print(re.findall(r"[ed]$", b))
```

    ['d']
    ['d']

`\$` with MULTILINE mode matches end of line

``` python
a = """no newline
at end"""

b = """newline
at end
"""

print(re.findall(r"(?m)[ed]$", a))
print(re.findall(r"(?m)[ed]$", b))
```

    ['e', 'd']
    ['e', 'd']

## regex module

-   [docs](https://bitbucket.org/mrabarnett/mrab-regex/src/hg/)

Todo:
- [Comparison](https://github.com/rexdwyer/Splitsville/blob/master/Splitsville.ipynb) between `re` and `regex`.

``` python
# would usually import as `import regex as re`, but because I
# want to compare to built-in re here, I'll import as regex.

# default version is VERSION0, which emulates re to use additional
# functionality, use VERSION1

import regex

regex.DEFAULT_VERSION = regex.VERSION1
```

### Keep out token

The keep out token `\K` drops everything matched thus far from the overall match to be returned.

``` python
pattern = r"\w+_\K\d+"
string = "abc_12"

regex.match(pattern, string)[0]
```

    '12'

### Inline flags

Flags placed inside the regex pattern take effect from that point onwards. As an example, this helps us find uppercase words that later appear in lowercase. To start, let's match all words that reappear later in the string.

``` python
string = "HELLO world hello world"
pattern = r"(?i)(\b\w+\b)(?=.*\1)"

re.findall(pattern, string)
```

    ['HELLO', 'world']

To only match uppercase words that later reappear in lowercase, we can do this ([explanation](https://www.rexegg.com/regex-tricks.html#upper_lower)):

``` python
pattern = r"(\b[A-Z]+\b)(?=.*(?=\b[a-z]+\b)(?i)\1)"
regex.findall(pattern, string)
```

    ['HELLO']

### Subroutines

Subroutines obviate the repetition of long capturing groups

``` python
s = "Tarzan loves Jane"
p = r"(Tarzan|Jane) loves (?1)"
m = regex.search(p, s)
m[0], m[1]
```

    ('Tarzan loves Jane', 'Tarzan')

#### Recursive patterns

Subroutines can call themselves to create a recursive pattern, which can be useful to match tokens where one letter is perfectly balanced by another.

``` python
s = "ab and aabb and aab and aaabbb and abb"
p = r"\b(a(?1)?b)\b"
regex.findall(p, s)
```

    ['ab', 'aabb', 'aaabbb']

Experimental

-   only standalone expressions

``` python
s = "aaaabbbb aabb aab ab"
p = r"a(?R)?b"
regex.findall(p, s)
```

    ['aaaabbbb', 'aabb', 'ab', 'ab']

``` python
s = "a a a a b b b b aabb aab ab"
p = r"\b ?a(?R)? b\b"
regex.findall(p, s)
```

    ['a a a a b b b b']

#### Pre-defined subroutines

We can predefine subroutines to produce nicely modular patterns that can easily be reused through our regex. (The `\` in the pattern is needed because in free-spacing mode, whitespace that we want to match rather than ignore needs to be escaped.)

``` python
defs = """
    (?(DEFINE)
        (?<quant>\d+)
        (?<item>\w+)
    )
    """

pattern = rf"{defs} (?&quant)\ (?&item)"
string = "There were 5 elephants walking towards the water hole."

regex.search(pattern, string, flags=regex.VERBOSE)
```

    <regex.Match object; span=(11, 22), match='5 elephants'>

A useful application of this is to create [real-word boundaries](https://www.rexegg.com/regex-boundaries.html#real-word-boundary) (rwb) that match between letters and other characters (rather than between word and non-word characters).

``` python
defs = """
    (?(DEFINE)
        (?<rwb>
            (?i)                   # case insensitive
            (?<![a-z])(?=[a-z])    # beginning of word
            |(?<=[a-z])(?![a-z])   # end of word
        )
    )
    """

pattern = rf"{defs} (?&rwb)\w+(?&rwb)"
string = """
cats23,
 +dogs55,
%bat*"""

regex.findall(pattern, string, flags=regex.VERBOSE)
```

    ['cats', 'dogs', 'bat']

Using default word boundaries in the above string would also return digits and underscores, since they are word characters.

``` python
regex.findall(r"\b\w+\b", string)
```

    ['cats23', 'dogs55', 'bat']

### Named groups

Supports named groups with a cleaner syntax: `(?<name>...)` instead of the somewhat verbose `(?P<name>...)` to define named groups

``` python
s = "Zwätschgi was born on 23 Dec 1986"
p = r"\b(?<day>\d{2}) (?<month>\w{3}) (?<year>\d{4})\b"
regex.search(p, s).groupdict()
```

    {'day': '23', 'month': 'Dec', 'year': '1986'}

and `\g<name>` instead of `(?P=name)` for backreference.

``` python
s = "2012-12-12"
p = "\d\d(?<yy>\d\d)-\g<yy>-\g<yy>"
regex.match(p, s)
```

    <regex.Match object; span=(0, 10), match='2012-12-12'>

### Unicode categories

`regex` provides support for unicode [categories](https://www.regular-expressions.info/unicode.html), which can be super handy.

``` python
## search for any punctuation character

s = ". and _"
pattern = r"\p{P}"
regex.findall(pattern, s)
```

    ['.', '_']

### Variable-width lookbehinds

One useful feature of `regex` is that it allows for variable-width lookbehinds. Like most regex engines, the `re` doesn't and tells you so if you try.

For example, if we want to match uppercase words preceeded by a prefix compused of digits and an underscore, such as *BANANA* in *123_BANANA*, the below doesn't work:

``` python
string = "123456_ORANGE abc12_APPLE"
pattern = r"(?<=\b\d+_)[A-Z]+\b"

try:
    re.findall(pattern, string)
except Exception as e:
    print(e)
```

    look-behind requires fixed-width pattern

In contrast, `regex` succeeds.

``` python
regex.findall(pattern, string)
```

    ['ORANGE']

Another application is if we wanted (for whatever reason) to match all words beginning with *a* at the beginning of a line from lines three onwards.

``` python
string = """abba
abacus
alibaba ada
beta adagio
aladin abracadabra
"""

pattern = "(?<=\n.*\n)a\w+"

regex.findall(pattern, string)
```

    ['alibaba', 'aladin']

### Character class set operations

Intersection

``` python
# inside [] are optional but can make pattern easier to read
pattern = r"[[\W]&&[\S]]"
subject = "a.b*5_c 8!"
regex.findall(pattern, subject)
```

    ['.', '*', '!']

Union

``` python
pattern = r"[ab||\d]"
subject = "a.b*5_c 8!"
regex.findall(pattern, subject)
```

    ['a', 'b', '5', '8']

Subtraction

``` python
pattern = r"[[a-z]--[b]]"
subject = "a.b*5_c 8!"
regex.findall(pattern, subject)
```

    ['a', 'c']

``` python
pattern = "[\w--[_\d]]"
subject = "a b 3 k _ f 4"
regex.findall(pattern, subject)
```

    ['a', 'b', 'k', 'f']

## Pandas

``` python
import pandas as pd
```

### Insert text in position

Insert an underscore between words

``` python
df = pd.DataFrame({"a": ["HelloWorld", "HappyDay", "SunnyHill"]})

pattern = r"(?<=[a-z])(?=[A-Z])"
df["a"] = df.a.str.replace(pattern, "_", regex=True)
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

|     | a           |
|-----|-------------|
| 0   | Hello_World |
| 1   | Happy_Day   |
| 2   | Sunny_Hill  |

</div>

``` python
def colname_cleaner(df):
    """Convert column names to stripped lowercase with underscores."""
    df.columns = df.columns.str.lower().str.strip()
    return df


def str_cleaner(df):
    """Convert string values to stripped lowercase."""
    str_cols = df.select_dtypes("object")
    for col in str_cols:
        df[col] = df[col].str.lower().str.strip()
    return df


movies = data.movies().pipe(colname_cleaner).pipe(str_cleaner)
movies.head(2)
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

|  | title | us gross | worldwide gross | us dvd sales | production budget | release date | mpaa rating | running time min | distributor | source | major genre | creative type | director | rotten tomatoes rating | imdb rating | imdb votes |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | the land girls | 146083.0 | 146083.0 | NaN | 8000000.0 | jun 12 1998 | r | NaN | gramercy | None | None | None | None | NaN | 6.1 | 1071.0 |
| 1 | first love, last rites | 10876.0 | 10876.0 | NaN | 300000.0 | aug 07 1998 | r | NaN | strand | None | drama | None | None | NaN | 6.9 | 207.0 |

</div>

### Finding a single pattern in text

``` python
pattern = "hello"
text = "hello world it is a beautiful day."

match = re.search(pattern, text)
match.start(), match.end(), match.group()
```

    (0, 5, 'hello')

In Pandas

``` python
movies.title.str.extract("(love)")
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

|      | 0    |
|------|------|
| 0    | NaN  |
| 1    | love |
| 2    | NaN  |
| 3    | NaN  |
| 4    | NaN  |
| \... | \... |
| 3196 | NaN  |
| 3197 | NaN  |
| 3198 | NaN  |
| 3199 | NaN  |
| 3200 | NaN  |

<p>3201 rows × 1 columns</p>
</div>

-   `contains()`: Test if pattern or regex is contained within a string of a Series or Index.
-   `match()`: Determine if each string starts with a match of a regular expression.
-   `fullmatch()`:
-   `extract()`: Extract capture groups in the regex pat as columns in a DataFrame.
-   `extractall()`: Returns all matches (not just the first match).
-   `find()`:
-   `findall()`:
-   `replace()`:

``` python
movies.title.replace("girls", "hello")
```

    0                   the land girls
    1           first love, last rites
    2       i married a strange person
    3             let's talk about sex
    4                             slam
                       ...            
    3196    zack and miri make a porno
    3197                        zodiac
    3198                          zoom
    3199           the legend of zorro
    3200             the mask of zorro
    Name: title, Length: 3201, dtype: object

Let's drop all movies by distributors with "Pictures" and "Universal" in their title.

``` python
# inverted masking

names = ["Universal", "Pictures"]
pattern = "|".join(names)
mask = movies.distributor.str.contains(pattern, na=True)
result = movies[~mask]
result.head(2)
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

|  | title | us_gross | worldwide_gross | us_dvd_sales | production_budget | release_date | mpaa_rating | running_time_min | distributor | source | major_genre | creative_type | director | rotten_tomatoes_rating | imdb_rating | imdb_votes |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 0 | The Land Girls | 146083.0 | 146083.0 | NaN | 8000000.0 | Jun 12 1998 | R | NaN | Gramercy | None | None | None | None | NaN | 6.1 | 1071.0 |
| 1 | First Love, Last Rites | 10876.0 | 10876.0 | NaN | 300000.0 | Aug 07 1998 | R | NaN | Strand | None | Drama | None | None | NaN | 6.9 | 207.0 |

</div>

``` python
# negated regex

names = ["Universal", "Pictures"]
pattern = "\|".join(names)
neg_pattern = f"[^{pattern}]"
neg_pattern
mask = movies.distributor.str.contains(neg_pattern, na=False)
result2 = movies[mask]
```

``` python
neg_pattern
```

    '[^Universal\\|Pictures]'

``` python
def drop_card_repayments(df):
    """Drop card repayment transactions from current accounts."""
    tags = ["credit card repayment", "credit card payment", "credit card"]
    pattern = "|".join(tags)
    mask = df.auto_tag.str.contains(pattern) & df.account_type.eq("current")
    return df[~mask]
```

## Sources

-   [Python string documentation](https://docs.python.org/3/library/string.html#string-formatting)
-   [Pyformat](https://pyformat.info)
-   [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
-   [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
-   [Learning Python](https://www.oreilly.com/library/view/learning-python-5th/9781449355722/)
-   [Python for Data Analysis](https://www.oreilly.com/library/view/python-for-data/9781491957653/)
-   [Python Data Science Handbook](https://www.oreilly.com/library/view/python-data-science/9781491912126/)

