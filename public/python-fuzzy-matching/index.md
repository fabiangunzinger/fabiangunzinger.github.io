# Fuzzy matching in Python


## `difflib`

-   Docs [here](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.set_seq2)

``` python
import difflib
```

Most simple use case

``` python
m = difflib.SequenceMatcher(None, 'NEW YORK METS', 'NEW YORK MEATS')
m.ratio()
```

    0.9629629629629629

Create helper function so we don't need to specify `None` each time.

``` python
from functools import partial
matcher = partial(difflib.SequenceMatcher, None)

matcher('NEW YORK METS', 'NEW YORK MEATS').ratio()
```

    0.9629629629629629

Compare one sequence to multiple other sequences (`SequenceMatcher` caches second sequence)

``` python
m = difflib.SequenceMatcher()
m.set_seq2('abc')

for s in ['abc', 'ab', 'abcd', 'cde', 'def']:
    m.set_seq1(s)
    length = len(m.a) + len(m.b)
    print('{}, {:{}} -> {:.3f}'.format(m.a, m.b, 10-length, m.ratio()))
```

    abc, abc  -> 1.000
    ab, abc   -> 0.800
    abcd, abc -> 0.857
    cde, abc  -> 0.333
    def, abc  -> 0.000

## `fuzzywuzzy`

Based on [this](https://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/) tutorial.

### Finding perfect or imperfect substrings

One limitation of `SequenceMatcher` is that two sequences that clearly refer to the same thing might get a lower score than two sequences that refer to something different.

``` python
print(matcher("YANKEES", "NEW YORK YANKEES").ratio())
matcher("NEW YORK METS", "NEW YORK YANKEES").ratio()
```

    0.6086956521739131

    0.7586206896551724

`fuzzywuzzy` has a useful function for this based on what they call the "best-partial" heuristic, which returns the similarity score for the best substring of length `min(len(seq1)), len(seq2))`.

``` python
from fuzzywuzzy import fuzz

print(fuzz.partial_ratio("YANKEES", "NEW YORK YANKEES"))
print(fuzz.partial_ratio("NEW YORK METS", "NEW YORK YANKEES"))
```

    100
    69

For one of my projects, I want to filter out financial transactions for which the description is a perfect or near-perfect substring of another transaction. So this is exactly what I need.

``` python
a = ''
```

