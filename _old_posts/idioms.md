---
title: "Python idioms"
subtitle: "A collection of best-practices"
tags: [python]

date: 2022-02-28
featured: false
draft: true

reading_time: false
profile: false
commentable: true
summary: " "

---

## Negated logical operators

- Use `if x not in y` instead of `if not x in y`, since they are semantically
  identical but the former makes it clear that `not in` is a single operator
  and reads like English. (Idion from
  [PEP8](https://www.python.org/dev/peps/pep-0008/#programming-recommendations),
  rationale from Alex [Martelli](https://stackoverflow.com/a/3481700))

## Docstrings

My docstring style.

```{python}
def function_name(*args, **kwargs):
    """A one-line summary in descriptive style terminated by a period.

    A one line space, followed by optional additional description of what
    the function does and what its rationale is.

    Args:
    - arg1: Concise description of first argument including its type
      and default value.
    - arg2: Same thing for all other arguments...
      
    Returns:
      Description of type of object is being returned and what it contains.
    """
```

## Nomenclature

In *Clean Code*, Robert Martin recommends choosing a single word per abstract
concept and sticking with it rather than using different words to mean the same
thing (what's the difference betweewn get, fetch, and retrieve?). Below a list
of words I frequently use.

Concept                                 | Term
Load data into working memory           | get


## Using argparse

There are different ways to use argparse. I usually use the following:

```{python}
import argparse
import sys

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('path')


def main(path):
    # something using path


if __name__ == '__main__':
    args = parse_args(sys.argv)
    main(args.path)
```

I use this as my default approach because it's appropriately
simple for my normal use case and it makes testing `main()` easy.

Alternatively, I sometimes use

```{python}
def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_args(argv)
    # do stuff with args
```

Based on [this](https://www.artima.com/weblogs/viewpost.jsp?thread=4829)
discussion.


## Use `ast.literal_eval()` instead of `eval()`

Why? Basically, because `eval` is very
[dangerous](https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html)
and would happile evaluate a string like `os.system(rm -rf /)`, while
`ast.literal_eval` will only evaluate Python
[literals](https://docs.python.org/3/library/ast.html#ast.literal_eval).
