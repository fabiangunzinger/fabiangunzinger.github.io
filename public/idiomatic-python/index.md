# Idiomatic Python



## EAFP \> LBYL

Just try to do what you expect to work and handle exceptions later if they occurr - "it's easier to ask for forgiveness than permission" (EAFP) rather than "look before you leap" (LBYL).

``` python
def dont(m, n):
    if n == 0:
        print("Can't divide by 0")
        return None
    return m / n


def do(m, n):
    try:
        return m / n
    except ZeroDivisionError:
        print("Can't divide by 0")
        return None
```

Other examples

``` python
try:
    dangerous_code()
except SomeError:
    handle_error()
except (OneError, OtherError):
    handle_multiple_errors()
```

``` python
try:
    os.remove("filename")
except FileNotFoundError:
    pass
```

## Long strings

Use a separate set of parenthesis for each line and wrap them all in a set of parenthesis.

``` python
my_very_big_string = (
    "For a long time I used to go to bed early. Sometimes, "
    "when I had put out my candle, my eyes would close so quickly "
    "that I had not even time to say “I’m going to sleep.”"
)
```

## Generator expression instead of if-else membership testing

``` python
cities = ["Berlin", "New York", "London"]
text = "Time Square is in New York"


def dont(cities, text):
    for city in cities:
        if city in text:
            return True


def do(cities, text):
    return any(city in text for city in cities)
```

## Negated logical operators

Use `if x not in y` instead of `if not x in y`, since they are semantically identical but the former makes it clear that `not in` is a single operator and reads like English. (Idion from [PEP8](https://www.python.org/dev/peps/pep-0008/#programming-recommendations), rationale from Alex [Martelli](https://stackoverflow.com/a/3481700))

## Using argparse

There are different ways to use argparse. I usually use

``` python
def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")


def main(path):
    pass
    # something using path
```

I use this as my default approach because it's appropriately simple for my normal use case and it makes testing `main()` easy. Alternatively, I sometimes use the below (based on [this](https://www.artima.com/weblogs/viewpost.jsp?thread=4829)
discussion)

``` python
def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_args(argv)
    # do stuff with args
```

## Use `ast.literal_eval()` instead of `eval()`

Why? Basically, because `eval` is very
[dangerous](https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html)
and would happile evaluate a string like `os.system(rm -rf /)`, while
`ast.literal_eval` will only evaluate Python
[literals](https://docs.python.org/3/library/ast.html#ast.literal_eval).

