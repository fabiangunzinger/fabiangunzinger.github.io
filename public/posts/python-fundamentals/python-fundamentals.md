---
title: Python fundamentals
date: '2021-10-10'
tags:
  - python
execute:
  enabled: false
---


## Data model - everything is an object

``` python
# Everything is an object
isinstance(4, object)  # => True
isinstance([1, 2], object)  # => True

# Objects have identity
id(4)  # => 4501558496 (e.g.)

# Objects have type
type(4)  # => int
isinstance(type(4), object)  # => Types are also objects

# Objects have value
(41).__sizeof__()  # => 28 (bytes)

# Variables are references to objects
x = 4
y = x
x == y  # => True (both refer to object 4)

# Duck typing (if it walks, swims, and quacks like a duck...)
def compute(a, b, c):
    return (a + b) * c


compute(1, 2, 3)
compute([1], [2, 3], 4)
compute("lo", "la", 3)
```

## Lexical analysis

-   What is a Python program read by? A *parser*, which reads a sequence of tokens produced by a lexical analyser.

-   What is a legixal analyser? A program that performs lexical analysis.

-   What is lexical analysis, and what's the etymology of the term? Lexical analysis, also called lexing or tokenizing, is the process of converting a sequence of characters into a sequence of tokens ([src](https://en.wikipedia.org/wiki/Lexical_analysis)). The root of the term is the Greek *lexis*, meaning *word*.

-   What is a *token*? A string with an identified meaning, structured as a name-value tuple. Common token names (aking to parts of speech in linguistics) are *identifier*, *keyword*, *separator*, *operator*, *literal*, *comment*. For the expression `a = b + 2`, lexical analysis would yield the sequence of tokens `[(identifier, a), (operator, =), (identifier, b), (operator, +), (literal, 2)]` ([src](https://en.wikipedia.org/wiki/Lexical_analysis#Token)).

-   What's the difference between lexical and syntactic definitions? The former operates on the individual characters of the input source (during tokenizing), the latter on the stream of tokens created by lexial analysis (during parsing).

-   By default, Python reads text as Unicode code points. Hence, [encoding declarations](https://docs.python.org/3/reference/lexical_analysis.html#encoding-declarations) are only needed if some other encoding is required.

# References

-   [Python Language Reference](https://docs.python.org/3/reference/index.html)
