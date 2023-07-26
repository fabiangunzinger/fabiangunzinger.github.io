# Intro


``` python
---
title: "Python Decorators"
date: "2021-03-23"
tags:
    - python
execute:
    enabled: false
---
```

My notes on decorator functions (I don't use classes enough to worry about class decorators).

-   Decorators are functions designed to wrap other functions to enhance their capability at runtime.
-   They do this by replacing the wrapped function with the return value of the decorator.
-   They work as syntactic sugar for `decorated = decorator(decorated)`.
-   Decorators are run when the decorated function is defined, not when it is run (i.e. they run at *import time*, not *runtime*).

## Basic mechanics

``` python
def decorator(func):
    print("Running decorator")
    return func


@decorator
def greeter():
    return "Hello"


greeter()
```

    Running decorator

    'Hello'

The above is equivalent to:

``` python
greeter = decorator(greeter)
greeter()
```

    Running decorator

    'Hello'

A decorator simply replaces the value of the function it wraps with the decorator's return value, which can, in principle, be anything.

``` python
def decorator(func):
    return "Decorator return value"


@decorator
def f():
    return "Function return value"


f
```

    'Decorator return value'

## Registration decorators

The simplest kind of decorator performs some kind of action and returns the function itself.

``` python
registry = []


def register(func):
    registry.append(func.__name__)
    return func


@register
def greeter():
    print("Hello")


registry
```

    ['greeter']

Notes:

-   `greeter = register(greeter)` assigns `greeter` to itself, as that's what's returned by `register`.

## Decorators that return a different function

``` python
import time


def timer(func):
    def wrapper(*args):
        start = time.time()
        result = func(*args)
        elapsed = time.time() - start
        name = func.__name__
        arg_str = ", ".join(repr(arg) for arg in args)
        print(f"[{elapsed:.6f}s] {name}({arg_str}) -> {result}")
        return result

    return wrapper


@timer
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


factorial(3)
```

    [0.000000s] factorial(1) -> 1
    [0.000353s] factorial(2) -> 2
    [0.000719s] factorial(3) -> 6

    6

### Q&A:

-   What's `functools.wraps()` about? It ensures that function metainformation is correctly handeled. For instance, that `factorial.__name__` returns *'factorial'*. Without wraps, it would return *'wrapper'*.

-   How does this work? By running `factorial = timer(factorial)`, the decorator assigns `factorial` to `wrapper`. Thus, when we call `factorial` we really call `wrapper`, which returns the same result `factorial` would have, but also performs the extra functionality. We can check the name attribute of factorial to confirm this; the decorated `factorial` function points to `wrapper`, no longer to `factorial`. (In practice, we should decorate the wrapper function with `functools.wraps(func)` to ensure that function meta information is passed through, so that `factorial.__name__` would return *'factorial'*.)

``` python
factorial.__name__
```

    'wrapper'

-   How does `wrapper` have access to `func` without taking it as an argument? `func` is a variable of the local scope of the `timer` function, which makes `wrapper` a closure: a function with access to variables that are neither global nor defined in its function body (my notes on [closures](https://fabiangunzinger.github.io/blog/python/2020/10/05/python-functions.html#Closures)). The below confirms this.

``` python
factorial.__closure__[0].cell_contents
```

    <function __main__.factorial(n)>

-   Where does `wrapper` get the arguments from `factorial` from? The short answer is: the arguments are passed directly to it when we call the decorated `factorial` function. This follows directly from the answer to the first question above: once `factorial` is decorated, calling it actually calls `wrapper`.

-   Why don't we pass the function arguments as arguments to `timer` (i.e. why isn't it `timer(func, *args)`? Because all timer does is replace `factorial` with `wrapper`, which then gets called as `wrapper(*args)`. So, `timer` has no use for arguments.

## Decorators with state

``` python
def logger(func):
    calls = 0

    def wrapper(*args, **kwargs):
        nonlocal calls
        calls += 1
        print(f"Call #{calls} of {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@logger
def greeter():
    print("Hello")


@logger
def singer():
    print("lalala")


@logger
def congratulator():
    print("Congratulations!")


greeter()
greeter()
singer()
congratulator()
```

    Call #1 of greeter
    Hello
    Call #2 of greeter
    Hello
    Call #1 of singer
    lalala
    Call #1 of congratulator
    Congratulations!

## Decorator with arguments

Now I want the ability to deactivate the logger for certain functions. So I wrap the decorator in a decorator factory, like so:

``` python
def param_logger(active=True):
    def decorator(func):
        calls = 0

        def wrapper(*args, **kwargs):
            nonlocal calls
            if active:
                calls += 1
                print(f"Call #{calls} of {func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@param_logger()
def greeter():
    print("Hello")


@param_logger(active=True)
def singer():
    print("lalala")


@param_logger(active=False)
def congratulator():
    print("Congratulations!")


greeter()
greeter()
singer()
congratulator()
```

    Call #1 of greeter
    Hello
    Call #2 of greeter
    Hello
    Call #1 of singer
    lalala
    Congratulations!

===== work in progress =====

How does this work? I'm not completely confident, actually, but this is how I explain it to myself.

How I think this works (not sure about this):

1.  temp = param_logger(), returns `decorator` with access to nonlocal `active` argument.
2.  Because we add () to decorator, `decorator` is immediately called and returns wrapper, which is also assigned to `temp`, i.e. `temp = decorator(func) = wrapper(*args, **kwargs)`.

In our initial logger function above, both the argument to the outer function (*func*) and the variable defined inside the outer function (*calls*) are free variables of the closure function wrapper, meaning that wrapper has access to them even though they are not bound inside wrapper.

===== work in progress =====

If we remember that

``` python
@logger
def greeter():
    print("Hello")
```

is equivalent to

``` python
greeter = logger(greeter)
```

and if we know that we can use `__code__.co_freevars` to get the free variables of a function, then it follows that we can get a view of the free variables of the decorated greeter function like so:

``` python
logger(greeter).__code__.co_freevars
```

    ('calls', 'func')

This is as expected. Now, what are the free variables of param_logger?

``` python
param_logger().__code__.co_freevars
```

    ('active',)

This makes sense: *active* is the function argument and we do not define any additional variables inside the scope of param_logger, so given our result above, this is what we would expect.

But param_logger is a decorator factory and not a decorator, which means it produces a decorator at the time of decoration. So, what are the free variables of the decorator it produces?

Similar to above, remembering that

``` python
@param_logger
def greeter():
    print("Hello")
```

is equivalent to

``` python
greeter = param_logger()(greeter)
```

we can inspect the decorated greeter function's free variables like so:

``` python
param_logger()(greeter).__code__.co_freevars
```

    ('active', 'calls', 'func')

We can see that active is now an additional free variable that our wrapper function has access to, which provides us with the answer to our question: decorator factories work by producing decorators at decoration time and passing on the specified keyword to the decorated function.

## Decorator factory beautifying

A final point for those into aesthetics or coding consistency: we can tweak our decorator factory so that we can ommit the `()` if we pass no keyword arguments.

``` python
def logger(func=None, active=True):
    def decorator(func):
        calls = 0

        def wrapper(*args, **kwargs):
            nonlocal calls
            if active:
                calls += 1
                print(f"Call #{calls} of {func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator(func) if func else decorator


@logger
def greeter():
    print("Hello")


@logger()
def babler():
    print("bablebalbe")


@logger(active=True)
def singer():
    print("lalala")


@logger(active=False)
def congratulator():
    print("Congratulations!")


greeter()
greeter()
babler()
singer()
congratulator()
```

    Call #1 of greeter
    Hello
    Call #2 of greeter
    Hello
    Call #1 of babler
    bablebalbe
    Call #1 of singer
    lalala
    Congratulations!

To understand what happens here, remember that decorating *func* with a decorator is equivalent to

``` python
func = decorator(func)
```

While decorating it with a decorator factory is equivalent to

``` python
func = decorator()(func)
```

The control flow in the final return statement of the above decorator factory simply switches between these two cases: if logger gets a function argument, then that's akin to the first scenario, where the func argument is passed into decorator directly, and so the decorator factory returns *decorator(func)* to mimic this behaviour. If *func* is not passed, then we're in the standard decorator factory scenario above, and we simply return the decorator uncalled, just as any plain decorator factory would.

Recipe 9.6 in the [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/) discusses a neat solution to the above for a registration decorator using functools.partial(), which I haven't managed to adapt to a scenario with a decorator factory. Might give it another go later.

## Mistakes I often make

I often do the below:

``` python
from functools import wraps


def decorator(func):
    @wraps
    def wrapper(*args, **kwargs):
        print("Func is called:", func.__name__)
        return func(*args, **kwargs)

    return wrapper


@decorator
def greeter(name):
    return f"Hello {name}"


greeter("World")
```

    AttributeError: 'str' object has no attribute '__module__'

What's wrong, there? `@wraps` should be `@wraps(func)`.

``` python
from functools import wraps


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Func is called:", func.__name__)
        return func(*args, **kwargs)

    return wrapper


@decorator
def greeter(name):
    return f"Hello {name}"


greeter("World")
```

    Func is called: greeter

    'Hello World'

## Applications

Reverse function arguments

``` python
from functools import wraps


def reversed_arguments(f):
    @wraps(f)
    def wrapper(*args):
        return f(*args[::-1])

    return wrapper


def power(a, b):
    return a ** b


new_power = reversed_arguments(power)
new_power(2, 3)
```

Pass kwargs to decorator and make factory return function result

``` python
funcs = []


def factory(**kwargs):
    def adder(func):
        funcs.append(func(**kwargs))
        return func

    return adder


@factory(text="This is very cool!")
def shout(text="Hello"):
    print(text.upper())


for f in funcs:
    f
```

    THIS IS VERY COOL!

Create tuple and supply kwargs upon function call in make_data.py

``` python
from collections import namedtuple

FunctionWithKwargs = namedtuple("FunctionWithKwargs", ["func", "kwargs"])

funcs = []


def factory(func=None, **kwargs):
    def adder(func):
        funcs.append(FunctionWithKwargs(func, kwargs))
        return func

    return adder(func) if func else adder


@factory(text="Ha", mark="@")
def shout(text="Hello", mark="!"):
    print(text.upper() + mark)


for f in funcs:
    f.func(**f.kwargs)
```

    HA@

Can I just alter the parametrisation of func inside the factory based on the kwargs and then return the newly parametrised function without having to call it?

## Main sources

-   [Fluent Python](https://www.oreilly.com/library/view/fluent-python/9781491946237/)
-   [Python Cookbook](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
-   [Python Essential Reference](https://www.oreilly.com/library/view/python-essential-reference/9780768687040/)
-   [Learning Python](https://www.oreilly.com/library/view/learning-python-5th/9781449355722/)

